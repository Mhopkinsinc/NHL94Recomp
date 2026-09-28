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

Related: `$D454` is the attempt clock, loaded with `$19` by `assshoot` and
counted down in `ai_GameVBlankRoutine` while `$C2FA` bit 1 is set; `$C31A`
is the announcement timer; team record +`$360` is incremented when an
attempt concludes (`assshoot` `$ED08`), most likely penalty shots /
shootout attempts.

---

## `$C2FA`: shootout session, breakaway, attempt clock

No IDA name. Cleared as a whole by `ai_ClearGameState` (`$FD778`). Where
`$C2F2` describes one attempt, this word holds the longer-lived shootout
state and a few shot-related events.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **shootout mode** for the whole session | `GameSetUp_2` `$F8490`, when the play mode `OptPlayMode` (`$D048`) is 4 (Shootout): the mode is reset to 0, the bit set and `ai_InitShootout` run | only `ai_ClearGameState` | about 35 readers, from `StartGame` and `ClockLength` (no periods) through the shot, goalie and puck AI (`doshot` "check if shootout", `assgoaliebreakwait`, `asspuckc`), `puckfaceoff`, `checkgoal` (no short-handed stats), `PrintScores1`, `showclock`, `Intermission`, `PeriodOver`, `ai_ShowGoalBanner` (jumps to the shootout banner) and `ai_PrintShootoutWinner` |
| 1 | **attempt clock in use**: the one-on-one is armed and `$D454` counts instead of the game clock | `assshoot` `$ED90`, right after the game clock is stopped (`$C2EA` bit 0) and before bit 2 of `$C2F2` | `puckfaceoff` `$F46C` | `ai_GameVBlankRoutine` `$15DD8`: with the bit set the routine decrements the attempt clock `$D454` (fraction `$D456`) rather than `gameclock`; `PrintScores1` `$12C4E` prints the label from `word_191F8` entry 4 instead of the period label; `updatepwrplay` and `ai_StartPowerPlaySong` return early; `ai_PrintClockLabel`; `ai_WaypointScriptActive` requires it |
| 2 | **shooter skating in**: the penalty-shot taker has the puck and the attempt clock runs even though the game clock is stopped | `puckpenshot` `$F2A8`, when the shooter is given assignment `$18` (`pucknorm`) | `setpassmode` `$BC1C` and `SetShotMode` `$C1C2` (the shot or pass is released), `ai_EndShootoutAttempt` `$F39E` | `ai_GameVBlankRoutine` `$15DC4`: bypasses the clock-stopped test so the attempt clock keeps counting |
| 3 | **shootout decided** | `ai_AdvanceShootoutRound` `$FC53A`, once five rounds are done and the scores differ | `ai_InitShootout` `$FC496` | `ai_StartShootoutAttempt` `$FC4C0` (jumps to the end sequence), `SetPA`/`setPA2` `$12664`/`$126D4` (post-attempt presentation) |
| 4 | **shot taken on a breakaway** (the shot in flight) | `doshot` `$C306` when the shooter has the breakaway bit (object `$64` bit 1) | `doshot` `$C2F6` at the start of every shot, `updateplayers` `$AA6C` when the breakaway ends, `checkgoal` `$14898` after the goal is credited | `checkgoal` `$1489E` (breakaway goal statistics, team record +`$35A`) |
| 5 | **puck loose after the attempt shot** | `ai_GoalieFreezePuck` `$F324`, once the shooter has committed (`$C2F2` bit 5) and `puckc` is negative (nobody has the puck) | `setpassmode` `$BC2C`, `SetShotMode` `$C1D2` | `ai_GoalieFreezePuck` `$F312`: skips re-detection once set |
| 6 | unused: no instruction references it | | | |
| 7 | **a banner is on screen** (GOAL! / PENALTY SHOT!) | `ai_ShowGoalBanner` `$187B8`, first instruction | `assshoot` `$ECD2` when an attempt is (re)started, `chkprogress` `$12030` when the message is retired | `doinput` `$B140` (input is treated differently while the banner shows), `ai_GameVBlankRoutine` `$15E3E` (the attempt clock is frozen while it is up) |

---

## `$C2EA` gmode: game-mode byte

IDA named this word `gmode` and most of its bits (`gmclock`, `gmdir`,
`gmpen`, `gmpendel`, `gmoffs`). Only the low byte is used: `StartGame`
clears it (`$776A`) and `ai_PlayHighlightFromGame` writes `$10` to it
(`$13612`).

| bit | IDA name | meaning | set | cleared | tested by |
|---|---|---|---|---|---|
| 0 | gmclock | **clock stopped** (1 = play is stopped, whistle) | `ResetClock` `$7846`, `clockcont` `$7C22` ("stop clock", when the period clock runs out), `Stop4Pen` `$124A6` (penalty), `assshoot` `$ED8A` (attempt armed), `ai_EndShootoutAttempt` `$F398` | `Endfaceoff` `$FE40` (the puck is dropped) | roughly 30 readers: every AI assignment routine (`assdefo`, `assdefd`, `asswingd`, `asswingo`, `asscenterd`, `asscentero`, `assnearest`, `asspassrec`, `assgoaliectrl`, `assgoaliecpu`, `assgoalietopuck`, `assonetimer`) returns or idles while it is set; `pucknorm` ("check for play stoppage"), `AddPenalty` (no penalty without a whistle), `updatepentime`, `ChkShotStat`, `checkint`, `CCStart`, `FallDown`, `CheckBump`, `wallcollb2`, `checkgoal`, `ai_GameVBlankRoutine` (the game clock only counts while clear) |
| 1 | gmdir | **direction of play**: 0 = the home team shoots up | `bchg` in `PeriodOver` `$1723A` every period change (teams switch ends) | same `bchg` | `setupice` `$16B02` and `ai_InitRinkScreen` `$16BE2` (flip every player's facing bit), `puckfaceoff2` `$FBD8`/`$FC84`, `ChkOffsides` `$10028`/`$10072`, `chkatop`, `checkgoal` `$14870`, `setlccords`; `ai_PlayHighlightFromGame` sets it (`$13622`) when restoring a recorded game |
| 2 | gmpen | **penalty called** | `Stop4Pen` `$12562` | `getBAplayerInfo` tail `$123B2` (a breakaway foul becomes a penalty shot instead) | `chkprogress` `$12074` ("check if penalty called"), `checkfornewpen` `$1242C` |
| 3 | gmpendel | **delayed penalty** pending (the offending team has not touched the puck yet) | `checkfornewpen` `$12494` | `chkprogress` `$1208E` ("clear del pen bit") | `assshoot` `$ED2C`, `puckfaceoff` `$F49A`, `ChkGoalies` `$F6E8` (the goalie may be pulled for the extra attacker) |
| 4 | (highlight) | **highlight playback**: the game is replaying a recorded highlight, not being played | `ai_PlayHighlightFromGame` (`move.b #$10`) | `StartGame` (`clr.b`) | `updatereplay` "check if highlight", `doshot` "always perfect" shots, `ChkShotStat`, `checkint`, `CCStart`, `holdcheck`, `FallDown`, `puckstick`, `puckgoalie`, `a2offsides`, `ChooseSong` (no songs), `ai_TriggerPeriodSong` |
| 5 | gmoffs | **offside rule active** | `StartGame` `$7778` when `OptPen` (`$D056`) is exactly 1 ("On"; 2 is "On, no offsides") | `StartGame` `clr.b` | `ChkOffsides` `$FFEA`, `a2offsides` `$100E6`, `AddPenalty` `$11F50`, `chk4pass`, `EvadePC` ("check if offsides is on"), `checkob` |
| 6 | **?** | **period ended, waiting for the stoppage to finish** | `clockcont` `$7C28`, immediately after stopping the clock when the period time expires (IDA: "set bit 6 gmode (?)") | not cleared explicitly; `StartGame` clears the byte | `puckfaceoff` `$F47A`: at the next faceoff, if set, control goes to the period-over path (`loc_17236`, which advances `gsp` and flips gmdir) |
| 7 | | **stars of the game shown** (once-only latch) | `ai_StarsOfTheGameScreen` `$18514` (`bset`, returns if already set) | `StartGame` `clr.b` | itself |

**How they fit together on a whistle:** something stops play, and whichever
routine blew the whistle sets `gmclock` (bit 0): a penalty, the period
ending, or an attempt starting. The AI idles and the clock freezes. At the
next faceoff `puckfaceoff` decides what comes next from bits 2, 3 and 6
(penalty, delayed penalty, period over), and `Endfaceoff` clears bit 0 when
the puck is dropped.
