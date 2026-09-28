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

---

## `$C2EC` sflags: status flags

IDA documents every bit of this one; the code agrees. `PauseMode` saves and
restores the whole word; `ai_PlayHighlightFromGame` clears the low byte.

| bit | IDA | meaning | set | cleared | tested by |
|---|---|---|---|---|---|
| 0 | paused | **game paused / a menu is up** | `demoread` `$7CD4` (pause request), `Intermission` `$1314C` (menu) | `PauseMode` `$7DA8` on exit, `puckpenshot` `$EFD8`, `puckfaceoff2` `$F90E` ("no pause"), `setupice` `$16A3A`, `ai_InitRinkScreen` `$16BB4` | `GameLoop`, `ClrHor`, `SetHor`, `ai_TickerAreaSetup`, `ai_GameVBlankRoutine` (no clock while paused), `checkfo` |
| 1 | controller pause | **which controller paused**: 0 = controller 1, 1 = controller 2 | `demoread` and `waitxsr` set or clear it from the pad that pressed Start (`$7CC0`..`$7CF0`, `$111F8`..`$1124E`) | `PeriodOver` `$172D4` | `ai_GetControllingTeam`, `ai_PrintPauseMenuItem`, `getpzjoy`, `ai_ToggleGoalieControl`, `ai_BuildUserNameString` |
| 2 | sfspdir | **pass-direction mode**: B is held, the D-pad aims the pass | `setpassmode` `$BC38` | `passmode` `$BC68` when the pass is released, `puckstick`/`puckgoalie` when the puck changes hands, `SetLCmode` `$B91C` | `ai_ClampChaseDelta` `$B744` (goalie input) |
| 3 | sfssdir | **shot-direction mode**: C is held, the D-pad aims the shot | `SetShotMode` `$C1E4` | `doshot` `$C31A` when the shot leaves, `holdcheck` `$13F2C` (checked while winding up), `puckstick`, `puckgoalie`, `SetLCmode` | `doinput`, `ai_ClampChaseDelta`, `assgoaliecpu` `$D97C`/`$D9AE` (the goalie reads the wind-up), `assshoot` |
| 4 | replay wrapped | **the replay ring has wrapped** (older frames overwritten) | `updatereplay` `$A90A` when `recbpr` reaches `$AF54` and restarts at `$FF0000` | `ClockLength` `$78D6` (reset replay), `ai_LoadPlayoffPassword`, `ai_SavePlayoffPassword` | `ai_StepReplayBack` `$A500` (may step past `$FF0000` only if wrapped) |
| 5 | manual scroll | **replay camera under manual control** | `ai_InstantReplay` `$A104`, `$A1DA` (D-pad moves the camera) | `ai_InstantReplay` `$A016`, `$A2D0`, `$A3B2` | `ai_ReinitRinkAndReplay` `$A5BA`, `SetRCords` `$A832` |
| 6 | sfslock | **camera locked to `$BF8E`/`$BF90`** (xc1/yc1) instead of following the puck | `freezewindow` `$AFC2`, `puckfaceoff` `$F540` (horizontal mode), `setInjuryType` `$144D2` (lock on the injured player), `CheckBump` `$14BA8` (fight), `wallcollb2` `$14C2C`, `ai_TileAnimationStep` `$FE4FC` (script end centres on `$160`) | `puckpenshot` `$F064`, `puckfaceoff2` `$F9BE` (then scrolls to the faceoff spot) | `checkwindow` `$AFD2` |
| 7 | sfhor | **screen in horizontal (menu/board) mode** rather than the rink | `SetHor` `$12B98` | `ClrHor` `$12B44` | 34 readers: everything that draws or moves on the rink checks it first (`updateplayers`, `updateanim`, `doinput`, `puckshadow`, `showref`, `showcrowd`, `showclock`, `SprSort`, `updatescroll`, `UpdateCrowdMeter`, ...) |

---

## `$C2EE` sflags2

IDA documents every bit. `ai_PlayHighlightFromGame` writes `4` to the low
byte (record disabled); `ai_StartPowerPlaySong` saves and restores the word.

| bit | IDA | meaning | set | cleared | tested by |
|---|---|---|---|---|---|
| 0 | sf2faceoff | **faceoff in progress** | `puckfaceoff2` `$F934` | `Endfaceoff` `$FE20` (the puck is dropped) | `updateplayers`, `doinput`, `assfaceoff`, `assfaceoffpl` |
| 1 | sf2refref | **referee sprite needs a refresh** | `PushRef` `$12746`/`$12768` | `puckpenshot` `$EFF0`, `puckfaceoff2` `$F92E` | no `btst`; read through the whole-word paths |
| 2 | record disabled | **instant-replay recording is off** | `ClockLength` `$78D0` ("dont record"), `puckfaceoff2` `$F93A` ("dont record yet"), `assscore` `$CCAA` (after the goal celebration timer `$DED0`), `puckpenshot` `$F27A`, `ai_EndShootoutAttempt` `$F392`, `chkprogress` `$120B6`, `ai_ShowGoalBanner` `$188A8` (during an attempt), `ai_ShootoutWinnersCelebrate` `$FD61C` | `Endfaceoff` `$FE3A`, `chkprogress` `$1202A` | `updatereplay` `$A8D4`, `ai_ReinitRinkAndReplay` `$A5D6` |
| 3 | replay in progress | **instant replay is being shown** | `ai_InstantReplay` `$9FDE` | `ai_InstantReplay` `$A3CC` on exit | `ai_PrintClockLabel`, `ai_PlaceOffscreenIndicator`, `ai_EmitAnimationSprites` (suppressed during replay) |
| 4 | sf2shot | **a shot was taken** and has not yet been resolved | `doshot` `$C340` (by the puck carrier, not a whiff) | `a2touchpuck` `$101A4` (somebody touched it), `ChkShotStat` `$12F44` (counted as a shot on goal), `wallcoll` `$14CAC` (hit the boards) | `puckstick` `$1522A` |
| 5 | sf2pwrplay | **power play in progress** | `updatepwrplay` `$12ACC` (counts `tmpwrplays` at +4 of the team record on the rising edge), `ai_StartPowerPlaySong` `$FF83A` | `updatepwrplay` `$12B32` (the penalty expired; the HUD panel is redrawn), `ai_ClearPowerPlaySongLatch` | `chkpk`, `assnearest`, `ai_DrawHudPanel`, `ChkShotStat`, `checkgoal` (power-play goal), `setplayer`, `updatePPTeamTime` |
| 6 | sf2pwrtm | **which team has the power play**: 0 home, 1 away | `updatepwrplay` `$12AAC`, `ai_StartPowerPlaySong` `$FF81A` | the same routines when the other side is up | `chkpk2`, `updatepwrplay`, `ChkShotStat`, `checkgoal`, `updatePPTeamTime`, `ai_StartPowerPlaySong` |
| 7 | sf2offsig | **the linesman's offside signal is showing** | `checkob` `$E69C` | `checkob` `$E68A` | `asspuckc` `$E0C2`, `chk4shot` `$E408` (the carrier dumps it instead of carrying in) |

---

## `$C2F0` sflags3

`ai_PlayHighlightFromGame` clears the low byte.

| bit | IDA | meaning | set | cleared | tested by |
|---|---|---|---|---|---|
| 0 | lower line change | **the line-change box was drawn in the lower half** of the screen (row `$F` or below) | `ai_PrintLineChangeMenu` `$B93C` | `lcfound2` `$BB4E`, `puckpenshot` `$EFDE`, `puckfaceoff2` `$F914` ("no line changes") | `PrintScores1` `$12C6A`, `UpdateCrowdMeter` `$F6ED2` |
| 1 | replay play mode | **replay is playing** (as opposed to paused / frame stepping) | toggled by `ai_InstantReplay` `$A274` on the play/pause button | `ai_InstantReplay` `$A03E`, `$A2AA`, `$A300`, `$A344` | `ai_InstantReplay` `$A306` |
| 2 | alt. tree | **alternate playoff tree**: the bracket was rebuilt after a game and the password re-encoded | `ai_AdvancePlayoffSeries` `$18484` | never (only the whole byte) | `ai_AdvancePlayoffsAfterGame` `$1814A` (decodes `$D176` again) |
| 3 | start pressed | **Start pressed to skip** the intermission highlights | `Intermission` `$13196`, `ai_PlayHighlightFromGame` `$137E0` | `Intermission` `$131A0` | `ai_PlayHighlightFromGame` `$13550`, `$13568` |
| 4 | end of faceoff | **faceoff just ended, nobody has touched the puck yet** | `Endfaceoff` `$FE50` | `puckstick` `$152B2` on the first touch, which then credits the faceoff win (team record +`$E`) | that `bclr` |
| 5 | | **replay camera locked on a player** (a player was found near the puck to follow) | `ai_InstantReplay` `$A1A0` | `ai_InstantReplay` `$A01C`, `$A128`, `$A2CA` | `ai_InstantReplay` `$A0C8`, `$A1B0`, `SetRCords` `$A83E` |
| 6 | penalty timer up | **one second of penalty time elapsed this frame** | `updatepentime` `$128D0` (every 24 jiffies) | `updatepentime` `$128B2` the next frame | `updateplayers` `$ABC2` |
| 7 | period 1 or 2 | **not the last period yet** | `ClockLength` `$7932` when `gsp` < 2 | `puckfaceoff` `$F4BC` at the first faceoff with at least 60 s left, which gates a once-per-period event | that `bclr` |

---

## `$C2F4`: goalie AI, replay angle, goal banner

No IDA name; only bits 4 and 7 are annotated. Cleared as a whole by
`ai_ClearGameState`.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **a goal was scored on this play** | `checkgoal` `$14828` | `puckfaceoff2` `$F8A4` | `assgoaliecpu` `$D52C`/`$D652`, `goalieacc` `$109A2`, `ChkShotStat` `$12F4E` (the shot counts as a goal) |
| 1 | **CPU goalie lunging**: the puck came inside x = +-`$14` of the goalie | `assgoaliecpu` `$D5A0` | `puckfaceoff2` `$F8AA` | `assgoaliecpu` `$D540` |
| 2 | **goalie deflection pending** (the puck was flipped off the goalie) | `puckgoalie` `$1558C` | `wallcoll` `$14D7A` (plays sound 5 if it was set), `checkpuckcoll` `$150C2`, `puckgoalie` `$154EE` (IDA: "not used anywhere, might have been a debug flag") | the `bclr` results |
| 3 | **CPU goalie in the pad-stack animation** (frame `$2C8`, sound `$1C`) | `assgoaliecpu` `$D568` | `assgoaliecpu` `$D5A6` when it lunges instead | `assgoaliecpu` `$D54A` |
| 4 | **reverse-angle replay** | toggled by `ai_ReinitRinkAndReplay` `$A536` (`bchg`) | `ai_InstantReplay` `$9FE4` on entry and `$A3BC` on exit | 13 readers: `SetRCords` (negated camera), `RevReplayAdj`, `updatescroll`, `showcrowd`, `setupice`, `ai_LoadRinkGraphics`, `ai_DrawRinkAuxBitmap`, `ai_EmitAnimationSprites` |
| 5 | **goal banner text pending** (scorer and assists not yet printed) | `checkgoal` `$147F4` | `ai_ShowGoalBanner` `$189B0`, `$18A08` | `checkgoal` `$14880` |
| 6 | **replay reinit requested** (the angle toggle button was pressed) | `ai_InstantReplay` `$A378` | `ai_ReinitRinkAndReplay` `$A528` (consumed) | that `bclr` |
| 7 | **reverse-angle frame adjustment in progress** | `RevReplayAdj` `$A686` | `SetRCords` `$A880` after the camera was negated | `ai_CenterCameraOnObject` `$A61C`, `$A62E` (negates the object coordinates) |

---

## `$C2F6`: breakaway, shot setup, replay control

No IDA name; bits 2 and 4 annotated. Note that bit 2 is reused by the
setup-screen cursor code for an unrelated purpose.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **replay: stop requested** (Start pressed during playback) **?** | `ai_InstantReplay` `$A34A` | `ai_InstantReplay` `$9FD0` on entry, `$A37E` | `ai_InstantReplay` `$A0AA`, `$A26A`, `$A282`, `$A2B0`, `$A32C` |
| 1 | **pause menu: skip the redraw** after the handler ran | `ai_InstantReplay` `$A3A2` (returning to the pause menu) | `ai_PauseMenuInput` `$7ED8` (consumed) | that `bclr` |
| 2 | **breakaway detected this frame** | `breakaway` `$DDC4` | `asspuckc` `$DF18`, `assnearest` `$E6F4` (consumed; the object's breakaway bit `$64` bit 1 is cleared with it). Also reused by `ai_MoveSetupCursor` as "the setup menu scrolled" (`$F76D6`, `$F76F6`, `$F7738`, tested `$F7768`) | the `bclr` results |
| 3 | **pass requested by the auto-pass path** (line change or CPU shot logic decided to pass; goes through `dopass` at `loc_BC64`) | `ai_ClampChaseDelta` `$B7AC`/`$B7D2`/`$B7F2` (doinput continuation), `chk4shot` `$E2D4` | `passmode` `$BC7E` (IDA: "Not in NHL Hockey Source") | `SetLCmode` `$B912`, `lineinput` `$BA88`, `passmode` `$BC48` |
| 4 | **in-close top-shelf shot**: shooting from within `$D8` of the goal with the goalie out or stacked | `prepshot` `$C2E8` | `prepshot` `$C274` at the start of the wind-up, `doshot` `$C51E` (consumed: raises `puckvz`) | that `bclr` |
| 5 | **the breakaway foul is a five-minute major** | `getBAplayerInfo` `$12294` | `getBAplayerInfo` `$12278` | `getBAplayerInfo` `$12348` |
| 6 | unused: never set | | | `doinput` `$B2A2`, `ai_ClampChaseDelta` `$B82E`, `getGoalieSCnum` `$B89E`, `chgplayer` `$FF9A8` (IDA: "never set anywhere") |
| 7 | **crowd roar** (excitement above the quadratic threshold) | `UpdateCrowdMeter` `$F6F1C` | `UpdateCrowdMeter` `$F6F38`, `PrintScores1` `$12C12` (consumed: starts the `$78`-frame HUD timer `$C304`) | `UpdateCrowdMeter` `$F6EDC` |

---

## `$C2F8`: printer and puck-handling switches

No IDA name; bits 4 and 5 annotated. Cleared as a whole by `ai_ClearGameState`.
Bits 0, 3, 6 and 7 are parameters passed to helpers through the flag word
rather than game state.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **dobitmap: apply the attribute in `printa`** to the map it draws | bracketed around `dobitmap` calls in `puckfaceoff2` `$FBA6`, `ai_MoveSetupCursor` `$F77E4`, `ai_DrawSetupPhotoFrame` `$F87BE`, `ai_PrintRecordsScreen` `$FA56A`, `newTitleScreen` `$FF15A` | right after each call | `dobitmap` `$11710` |
| 1 | **one-timer shot pending** | `onetimershot` `$F6D1A`, `assshoot` `$ED26` | `updateplayers` `$AA4E` once somebody carries the puck, `puckfaceoff` `$F466` | `checkpuckcoll` `$14FEC` |
| 2 | **pass target from the deep-zone table** | `ai_ComputePassTarget` `$F6810` | `ai_ComputePassTarget` `$F67E8`, `$F682A` | `passmode` `$BC94` |
| 3 | **print: use the setup-screen attribute** for the text | bracketed around `print`/`print2` calls in `ai_RefreshSetupOptions` `$F7908`, `ai_PrintSetupMenuLabels` `$F8074`, `ai_ShowNextSetupPhoto` (six sites) | right after each call | `print2` `$11A5A`/`$11AB4`, `print` `$11C24`/`$11C3C` |
| 4 | **wall collision registered** (handshake) | `$14B22` around the `sub_14C70` call in the collision code | `$14B2C` after it, `wallcoll` `$14D06` (consumed: sets the object's wall-collision bit `$64` bit 4) | the `bclr` result |
| 5 | **the puck carrier is in the slot** (x within +-`$47`) | `setSlotBit` `$F8BE8` | `setSlotBit` `$F8BA0` each call | `assnearest` (four sites), `check4check` `$EB5E`, `puckstick` `$1511E`/`$15176` |
| 6 | **SRAM write** (selects `WriteSRAM` in the record helpers) | `ai_WriteRecordField`, `ai_WriteTeamRecord`, `ai_WriteUserRecord`, `ai_WriteUserNames`, `ai_SkipOwnUserEntry` `$FBCDA` | the read entries (`ai_ReadRecordField`, `ReadTeamRecord`, `ai_ReadUserRecord`, `ai_ReadUserNames`), `ai_SkipOwnUserEntry` `$FBCD0` | the shared bodies, `ai_RankUsersByRecordByte` |
| 7 | **trim trailing spaces** in `ai_BuildUserNameString` | `ai_AppendRecordUserName`, `ai_AppendRecordHolderText`, `ai_PrintGoalRecordLine`, `ai_BuildCrowdRecordText` | `ai_PrintRankedUserName` `$FC174` | `ai_BuildUserNameString` `$FA04E` |

---

## `$C2FC`: overtime, injury, crowd record, options

No IDA name; bits 5 and 6 annotated.

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **tile animation requested** (`$D6BE` holds the id) | `ai_RequestTileAnimation` `$FE53C` | `ai_StopTileAnimation` `$FE54E` | `puckfaceoff2` `$FB3C` |
| 1 | **overtime** (period 3 reached with the game tied) | `ClockLength` `$7870` when `gsp` is 3 | `GameSetUp` `$F73BC` | `ai_PrintRatingsPlayerName` `$FDA24`, `ai_PrintPeriodStatColumns` `$FDBDC` (the OT column) |
| 2 | unused: only cleared (`puckfaceoff` `$F438`) | | | nobody |
| 3 | **waypoint script reached its end marker** | `ai_NextWaypoint` `$FE848` | `ai_StartWaypointScript` `$FE76E` | `ai_WaypointScriptActive` `$FE91A` |
| 4 | **line changes forced automatic**: the line-change option was 2 | `GameSetUp_2` `$F8474` (`OptLine` 2 is reset to 0 and this bit set instead) | only `ai_ClearGameState` | `SetLCmode`, `burst`, `ai_CpuLineChangeCheck`, `puckfaceoff`, `ai_CpuLineChangeAtFaceoff`, `playeracc`, `makepde` |
| 5 | **game injury**: a player was injured for the rest of the game (status -4) | `setInjuryType` `$1453A` | `setInjuryType` `$1450C`, `$14524` (period injury, status -3) | `FallDown` `$14454`, `ai_ScorePlayerForStars` `$18732` |
| 6 | **crowd meter record broken** (current meter at or above the arena record) | `updateplayers` `$AA34` | `updateplayers` `$AA22` each frame before the test, `puckfaceoff` `$F432` | 16 readers, all AI: every skater and goalie assignment routine and `playeracc` give a speed boost while it is set |
| 7 | **hide the position letters on the player labels** (during an attempt) | `assshoot` `$ECC0` | `puckfaceoff` `$F420` | `ai_BuildPlayerLabelSprites` `$1672A` |

---

## `$C2FE`: goal and song latches

No IDA name; bit 1 annotated as "Crowd Meter Broken (bugged)".

| bit | meaning | set | cleared | tested by |
|---|---|---|---|---|
| 0 | **shootout goal scored** on this attempt | `checkgoal` `$1480E` after bumping the side's round score (`$D574`/`$D576`) | `puckfaceoff` `$F40E` | nobody by `btst`; read by the faceoff flow |
| 1 | **crowd-meter-broken mirror**, always set: `set_bit1_C2FE` (`$FEF66`) branches unconditionally to the `bset` at `$FEF74`, so the `bclr` at `$FEF6A` is unreachable and the bit is set on the first `updateplayers` frame and never cleared | `set_bit1_C2FE` from `updateplayers` `$AA3A` | unreachable | `assnearest` `$EA18`, `playeracc` `$10C02`/`$10C86`, `Bcheck` `$13FF6`, `checkpuckcoll` `$14F86` (IDA: "always is") |
| 3 | **shot already counted for this goal** (handshake between the shot and goal statistics) | `ChkShotStat` `$12F62` | `ChkShotStat` `$12F58`, `checkgoal` `$1482E` | the `bclr` results |
| 4 | **faceoff song started** | `puckfaceoff` `$F4EC` after `ChooseSong` | `puckfaceoff` `$F3E4`, `puckfaceoff2` `$FCB6`/`$FCC0` (stops the song via `sub_11156`) | the `bclr` results |
| 5 | unused: only cleared (`assonetimer` `$F6958`) | | | nobody |
| 6 | **power-play song started** | `ai_StartPowerPlaySong` `$FF85E` | `puckfaceoff2` `$FCAC`, `ChooseSong` `$FE56C` | `puckfaceoff` `$F4D0` |
| 7 | **one-timer in flight** (a one-timer shot or touch is being resolved) | `a2touchpuck` `$10170` (touch by a one-timer shooter), `puckstick` `$15214`, `onetimershot` `$F6CF4` | `updateplayers` `$AA48` once somebody carries the puck, `puckfaceoff2` `$FA3E`, `ai_ResetLinesForFaceoff` `$1380E`, `assonetimer` `$F6A9E`, `checkgoal` `$148E8` (consumed: counts a one-timer goal, team record +`$35E`) | the `bclr` results |

The team-record offsets these paths touch that were not in
`docs/STRUCTURES.md`: +4 power plays (`tmpwrplays`), +`$35E` one-timer
goals, +`$360` penalty-shot / shootout attempts.
