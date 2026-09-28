# Game flag words

The game keeps its mode and event state in a run of flag words at
`$C2EA`..`$C2FE` (IDA: `gmode`, `sflags`, `sflags2`, `sflags3`,
`BA_PS_flags`, ...). Each bit is documented here from every instruction that
sets, clears or tests it, with the routine it lives in. Addresses are WRAM
(`$C2F2` = `$FFC2F2`). A routine name in `ai_` form is an unreviewed
proposal from the naming pass (`docs/names/`).

Method for each word: list every `bset`/`bclr`/`btst` on it in the listing,
group by bit, and read the code around every set and clear. The tables
below cite those sites so the reading can be checked.

---

## `$C2F2` BA_PS_flags: breakaway / penalty-shot / shootout attempt

The word describes one **one-on-one attempt**: a penalty shot awarded during
a game, or one shooter's turn in a shootout. It is cleared as a whole by
`ai_ClearGameState` at game setup (`$FD76C`). The *shootout mode* itself
(the whole post-game session) is a different flag, `$C2FA` bit 0; this word
tracks each attempt inside it, and also the in-game penalty shots that
`OptPen` allows.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | unused: no instruction sets it | never | `doinput` `$B4FC` every frame | nobody |
| 1 | the controlled goalie is pinned against the crease boundary this frame | `doinput` `$B644`/`$B65E` when x leaves -`$24`..`$24` with velocity outward, `$B69E` when y leaves -`$E7`..`$E7` with velocity outward; the velocity is zeroed at the same time | `doinput` `$B62A` at the start of the goalie branch each frame (only when `$34(a3)` = 0, the goalie slot) | `doinput` `$B6A8`: when set the rest of the goalie's input handling is skipped |
| 2 | **an attempt is live**: the shooter and goalie are alone and the one-on-one rules apply | `assshoot` `$EDB0`, after the attempt clock `$D454` is loaded with `$19` and `loc_F712` placed the players; if `ai_PickBestAvailableSkater` finds nobody the bit is cleared again at `$EDD0` and a normal faceoff (assignment `$1B`) is used instead | `ai_EndShootoutAttempt` `$F3A4` (from `checkgoal`); `puckfaceoff2` `$F898` (any faceoff); `assshoot` `$ED0E` on the attempt-concluded path, where the team's +`$360` counter is incremented first | about thirty readers: player input (`doinput`, `changeplayer`, `chgplayer`, `restorep1`, `check4bench`), pass and shot entry (`setpassmode`, `passmode`, `SetShotMode` "check for PS or SO", `shotdiradj`), all skater and goalie AI (`asspuckc`, `assnearest`, `assgoaliecpu`, `assgoaliectrl`, `assgoaliebreakwait`, `chkpuckc`, `checkob`), rules (`ChkOffsides`, `checkgoal`, `checkpuckcoll`, `chkprogress`), presentation (`ai_ShowGoalBanner`, `ai_PlaceOffscreenIndicator`), `pucknorm` (routes to `ai_GoalieFreezePuck` when set) |
| 3 | **a penalty shot has been awarded** for a foul on a breakaway and is pending | `getBAplayerInfo` `$12180`, only when `OptPen` (`$D056`) is on; the routine then records the shooter (`BA_Sktr_SCnum`), the goalie (`BA_Goalie_SCnum`) and the checker's roster indexes | `getBAplayerInfo` `$121B4` when the fouled team has no goalie; `PenShotChk` `$12160` when the check is not a foul; `checkgoal` `$149C2` once the goal is scored; `ai_EndShootoutAttempt` `$F3AA` | `PenShotChk` `$12128` (a second foul while one is pending is ignored); `getBAplayerInfo` tail `$123C6`: assignment `$1E` (penalty-shot sequence) when set, else `$1B` (faceoff) |
| 4 | **the attempt is over**, a stoppage is due | goalie AI when its hold timer `temp5` runs out during an attempt (`assgoaliectrl` `$D4D8`, `assgoaliecpu` `$D6CA`, both guarded by bit 2); `ai_GoalieFreezePuck` `$F342` when the goalie has covered the puck, `$F350` when the attempt clock `$D454` reaches 0 | `assshoot` `$ED14`, `ai_EndShootoutAttempt` `$F3B6` | `ai_GoalieFreezePuck` `$F356`: nothing happens until it is set |
| 5 | **the shooter has committed**: a shot or pass was started during the attempt | `setpassmode` `$BC22` and `SetShotMode` `$C1C8`, both only while bit 2 is set (they also clear `$C2FA` bit 2) | `assshoot` `$ED1A`, `ai_EndShootoutAttempt` `$F3B0`, `puckfaceoff2` `$F89E` | `assnearest` `$E972` (with bit 2: the AI stops chasing once the shot is away); `ai_GoalieFreezePuck` `$F308`: the freeze path is only taken after the shooter committed |
| 6 | end-of-attempt already handled (once-only latch) | `ai_GoalieFreezePuck` `$F36C`, right before it posts event `$A` through `sub_11F62` and freezes the camera (`freezewindow`) | `assshoot` `$ED20`, `ai_EndShootoutAttempt` `$F3BC`, `getBAplayerInfo` `$123BC` | `ai_GoalieFreezePuck` `$F362`: returns if already set |
| 7 | the **PENALTY SHOT!** announcement is pending | `puckpenshot` `$F274`, together with `$C2EE` bit 2 and the `$190`-frame timer `$C31A` | `chkprogress` `$1206C` right after showing it | `chkprogress` `$1200C`: with bit 2 set, calls `ai_ShowGoalBanner` (which prints "PENALTY SHOT!" in this state) |

**Life of a penalty shot** (bits in order): a check on a breakaway →
`PenShotChk`/`getBAplayerInfo` set bit 3 and pick the players → `puckpenshot`
sets bit 7 (banner) and `assshoot` sets bit 2 (attempt live) → the shooter
skates in; `setpassmode`/`SetShotMode` set bit 5 on release → the goalie
covers, the shot goes in, or the `$D454` clock expires → bit 4 → `ai_GoalieFreezePuck`
sets bit 6 once and posts the stoppage → `checkgoal`/`ai_EndShootoutAttempt`
clear bits 2..6 and, in a shootout, `ai_AdvanceShootoutRound` moves to the
next shooter.

**Your reading was right** for bit 2 as far as shootouts go: it goes up when
an attempt starts and down when it ends. Two refinements: it is per
*attempt*, not per shootout (`$C2FA` bit 0 is the session flag), and it is
just as much the in-game penalty-shot flag, which is what the IDA name
`BA_PS_flags` (breakaway / penalty shot) records.

Related words seen on the same paths, not yet worked through bit by bit:

- `$C2FA`: bit 0 shootout mode (IDA "set when shootout?"), bit 1 set by
  `assshoot` when an attempt is armed, bit 2 cleared when the shooter enters
  pass/shot mode, bit 3 shootout decided (`ai_AdvanceShootoutRound`), bit 4
  breakaway (IDA).
- `$C2EA` gmode: bit 0 clock stopped, bit 2 penalty called (IDA).
- `$D454`: the attempt clock, loaded with `$19` by `assshoot` and counted
  down in `ai_GameVBlankRoutine`; `$C31A`: the announcement timer.
- Team record +`$360`: counter incremented when an attempt concludes
  (`assshoot` `$ED08`), most likely penalty shots / shootout attempts.
