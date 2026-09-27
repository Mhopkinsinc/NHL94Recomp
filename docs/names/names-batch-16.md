# Name review: names-batch-16.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$009020` -> `ai_PrintSummaryRowAbove`  (confidence 0.5, 13 insns)

**Evidence.** twin of ai_PrintSummaryRowAt: prints ScoreSum entry (d0 high word) * 6 at the row VertLineScrolling/8 - 3 (mod 32), i.e. the entry scrolling in at the top of the summary list; caller sub_8FB8

**Callers.** ai_ScrollSummaryList
**Callees.** ai_PrintScoringSummaryRow, printz
**RAM.** VertLineScrolling, printy

```
009020  move.l	d0,-(sp)
009022  swap	d0
009024  moveq	#6,d3
009026  mulu.w	d0,d3
009028  jsr	sub_11B92
00902E  dc.w	6
009030  dc.b	$BE
009031  dc.b	0
009032  dc.b	0
009033  dc.b	0
009034  move.w	($FFFFD5AE).w,d0
009038  lsr.w	#3,d0
00903A  subq.w	#3,d0
00903C  and.w	#$1F,d0
009040  move.w	d0,($FFFFB02A).w
009044  bsr.w	sub_907C
009048  move.l	(sp)+,d0
00904A  rts
```

## `$009428` -> `ai_ShowPlayoffStats`  (confidence 0.6, 13 insns)

**Evidence.** PeriodOver: unpacks the playoff stats (ai_UnpackPlayoffStats), selects the team record whose id $28 matches the user's playoff team byte $CEF4[potreeteam] (home, else away) and shows the stats screen with d7 = 1 ('Playoff  Stats'); caller PeriodOver

**Callers.** PeriodOver
**Callees.** ai_PrintStatsScreen, ai_UnpackPlayoffStats
**RAM.** potreeteam

```
009428  movem.l	a2,-(sp)
00942C  jsr	sub_1833A
009432  move.w	#$CEF4,a0
009436  move.w	($FFFFCEEE).w,d0
00943A  move.b	(a0,d0.w),d0
00943E  move.w	#$C6CE,a2
009442  cmp.w	$28(a2),d0
009446  beq.w	loc_944E
00944A  add.w	#$364,a2
00944E  moveq	#1,d7
009450  bsr.w	loc_945C
009454  movem.l	(sp)+,a2
009458  rts
```

## `$00F590` -> `ai_CpuLineChangeAtFaceoff`  (confidence 0.6, 13 insns)

**Evidence.** puckfaceoff: with line changes enabled (OptLine = 0) and team d0 not controlled by a human (cont1team/cont2team, bypassed by $C2FC bit 4), picks the fresher line with CompLine, applies it with SetPersonel, refreshes the HUD (PrintScores1) and sets $C304 = $2710; caller puckfaceoff

**Callers.** puckfaceoff
**Callees.** CompLine, PrintScores1, SetPersonel
**RAM.** OptLine, cont1team, cont2team

```
00F590  tst.w	($FFFFD058).w
00F594  bne.w	locret_15464
00F598  btst	#4,($FFFFC2FC).w
00F59E  bne.w	loc_F5B2
00F5A2  cmp.w	($FFFFC328).w,d0
00F5A6  beq.w	locret_15464
00F5AA  cmp.w	($FFFFC32A).w,d0
00F5AE  beq.w	locret_15464
00F5B2  bsr.w	sub_F790
00F5B6  bsr.w	sub_15788
00F5BA  bsr.w	loc_12C04
00F5BE  move.w	#$2710,($FFFFC304).w
00F5C4  rts
```

## `$01351C` -> `ai_PlayFinishedSeriesHighlights`  (confidence 0.6, 13 insns)

**Evidence.** Intermission: for every series record from the current one down (sub_1828A gives the count) that is not finished (bit 2 of +$E) and has its pending flag bit 1 set, clears the flag and plays it as a highlight with ai_PlayHighlightFromGame; caller Intermission

**Callers.** Intermission
**Callees.** GetShifter, ai_PlayHighlightFromGame

```
01351C  bsr.w	sub_1828A
013520  moveq	#$10,d3
013522  mulu.w	d1,d3
013524  move.w	#$CE66,a0
013528  add.w	d3,a0
01352A  btst	#2,$E(a0)
013530  bne.w	loc_13542
013534  bclr	#1,$E(a0)
01353A  beq.w	loc_13542
01353E  bsr.w	sub_1354C
013542  suba.w	#$10,a0
013546  dbf	d1,loc_1352A
01354A  rts
```

## `$0FCF86` -> `ai_ChangeRatingsPosition`  (confidence 0.7, 13 insns)

**Evidence.** matchups screen: moves the per-position comparison $D598 by d0 with wrap-around in 0..6, restarts the hold timer $D5A8 = $10E, then reselects the players, redraws the pictures and reprints the ratings (ai_SelectRatingsPlayers, ai_DrawRatingsPictures, ai_PrintTeamRatingsScreen); caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** ai_DrawRatingsPictures, ai_PrintTeamRatingsScreen, ai_SelectRatingsPlayers, loc_FCFA6

```
0FCF86  move.w	#$10E,($FFFFD5A8).w
0FCF8C  add.w	($FFFFD598).w,d0
0FCF90  bmi.w	loc_FCFA2
0FCF94  cmpnw	 7,d0
0FCF98  blt.w	loc_FCFA6
0FCF9C  clr.w	d0
0FCF9E  bra.w	loc_FCFA6
0FCFA2  move.w	#6,d0
0FCFA6  move.w	d0,($FFFFD598).w
0FCFAA  bsr.w	sub_FD46C
0FCFAE  bsr.w	sub_FD084
0FCFB2  bsr.w	loc_FD1FE
0FCFB6  rts
```

## `$0FF318` -> `ai_TitleWaitFrame`  (confidence 0.5, 13 insns)

**Evidence.** newTitleScreen: waits for the next V-blank (vcount change), decrements the title timer $B8B2 by 2 (floor 0), reads the pad with sub_112BC and, when Start (bit 7) is pressed, discards its caller's return address so control leaves the title loop; caller newTitleScreen

**Callers.** newTitleScreen
**Callees.** orjoy
**RAM.** vcount

```
0FF318  movem.l	d0-a6,-(sp)
0FF31C  move.w	($FFFFB03E).w,d0
0FF320  cmp.w	($FFFFB03E).w,d0
0FF324  beq.s	loc_FF320
0FF326  subq.w	#2,($FFFFB8B2).w
0FF32A  bpl.w	loc_FF332
0FF32E  clr.w	($FFFFB8B2).w
0FF332  jsr	sub_112BC
0FF338  btst	#7,d1
0FF33C  movem.l	(sp)+,d0-a6
0FF340  beq.w	locret_FF346
0FF344  addq.w	#4,sp
0FF346  rts
```

## `$00B5D8` -> `ai_ClampChaseDelta`  (confidence 0.4, 12 insns)

**Evidence.** doinput helper: clears d0 when the player a3 is the puck carrier (puckc equals $52(a3)), clamps the offset d1 to -$103..$103 and subtracts d3; byte-identical to ai_ClampChaseDeltaGoalie at $DB3E; caller doinput

**Callers.** doinput
**Callees.** none
**RAM.** puckc

```
00B5D8  move.w	($FFFFB7AA).w,d2
00B5DC  cmp.w	$52(a3),d2
00B5E0  bne.w	loc_B5E6
00B5E4  clr.w	d0
00B5E6  cmpnw	 $103,d1
00B5EA  blt.w	loc_B5F2
00B5EE  move.w	#$103,d1
00B5F2  cmpnw	 $FEFD,d1
00B5F6  bgt.w	loc_B5FE
00B5FA  move.w	#$FEFD,d1
00B5FE  sub.w	d3,d1
00B600  rts
```

## `$00DB3E` -> `ai_ClampChaseDeltaGoalie`  (confidence 0.4, 12 insns)

**Evidence.** assgoaliecpu helper, byte-identical to ai_ClampChaseDelta ($B5D8): clears d0 when the goalie a3 has the puck, clamps d1 to -$103..$103 and subtracts d3; caller assgoaliecpu

**Callers.** assgoaliecpu
**Callees.** none
**RAM.** puckc

```
00DB3E  move.w	($FFFFB7AA).w,d2
00DB42  cmp.w	$52(a3),d2
00DB46  bne.w	loc_DB4C
00DB4A  clr.w	d0
00DB4C  cmpnw	 $103,d1
00DB50  blt.w	loc_DB58
00DB54  move.w	#$103,d1
00DB58  cmpnw	 $FEFD,d1
00DB5C  bgt.w	loc_DB64
00DB60  move.w	#$FEFD,d1
00DB64  sub.w	d3,d1
00DB66  rts
```

## `$013068` -> `ai_SelectSpecialTeamsLine`  (confidence 0.6, 12 insns)

**Evidence.** sub_13056 helper: refills the energy (ai_ResetLineEnergy), sets team a3's line $16 to 0, and with automatic lines (OptLine = 0) picks line 3 when a3 has more skaters than a2 (power play) or line 5 when fewer (penalty kill); caller sub_13056

**Callers.** ai_SelectSpecialTeamsLinesBoth
**Callees.** ai_ResetLineEnergy
**RAM.** OptLine

```
013068  bsr.w	sub_130BE
01306C  clr.w	$16(a3)
013070  tst.w	($FFFFD058).w
013074  bne.w	locret_15464
013078  move.w	$24(a3),d0
01307C  sub.w	$24(a2),d0
013080  beq.w	locret_15464
013084  move.w	#3,$16(a3)
01308A  tst.w	d0
01308C  bpl.w	locret_15464
013090  move.w	#5,$16(a3)
013096  rts
```

## `$017542` -> `ai_PlayoffScreenInput`  (confidence 0.7, 12 insns)

**Evidence.** PlayoffScreen: reads both pads (sub_11340 | sub_11358); Start leaves via loc_175D4, Right sets the bracket scroll velocity PlayerScrollCtr to -2, Left to +2, then falls into ai_ScrollPlayoffBracket; caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** ReadJoy1, ReadJoy2
**RAM.** PlayerScrollCtr

```
017542  bsr.w	sub_11340
017546  move.w	d3,-(sp)
017548  bsr.w	sub_11358
01754C  or.w	(sp)+,d3
01754E  btst	#7,d3
017552  bne.w	loc_175D4
017556  btst	#3,d3
01755A  beq.w	loc_17564
01755E  move.w	#$FFFE,($FFFFD5B0).w
017564  btst	#2,d3
017568  beq.w	sub_17572
01756C  move.w	#2,($FFFFD5B0).w
```

## `$0175FC` -> `ai_PrintSeriesScore`  (confidence 0.8, 12 insns)

**Evidence.** builds 'W-L' in $BFA4 from the series record a2's win counts +4 and +6 (single digits, '-' between) and prints it; caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** print

```
0175FC  move.w	#$BFA4,a1
017600  move.w	#6,(a1)+
017604  move.w	4(a2),d0
017608  add.w	#$30,d0
01760C  move.b	d0,(a1)+
01760E  move.b	#$2D,(a1)+
017612  move.w	6(a2),d0
017616  add.w	#$30,d0
01761A  move.b	d0,(a1)+
01761C  clr.b	(a1)+
01761E  move.w	#$BFA4,a1
017622  bra.w	sub_11BA4
```

## `$0FAF8C` -> `ai_SelectRecordsPlayer`  (confidence 0.5, 12 insns)

**Evidence.** records screen: takes entry $D4F4 - 1 of the starters/bench list for the selected side ($D4FA home, $D514 away by $D4F6, built by ai_SplitRosterByLineup) and stores the player index in $D52E; caller loc_FAEBC

**Callers.** ai_DrawRecordsPlayerPhoto
**Callees.** none

```
0FAF8C  movem.l	d1/a0,-(sp)
0FAF90  move.l	#$FFFFD4FA,a0
0FAF96  tst.w	($FFFFD4F6).w
0FAF9A  beq.w	loc_FAFA4
0FAF9E  move.l	#$FFFFD514,a0
0FAFA4  move.w	($FFFFD4F4).w,d1
0FAFA8  subq.w	#1,d1
0FAFAA  move.b	(a0,d1.w),d0
0FAFAE  ext.w	d0
0FAFB0  move.w	d0,($FFFFD52E).w
0FAFB4  movem.l	(sp)+,d1/a0
0FAFB8  rts
```

## `$0FB750` -> `ai_CharToEntryIndex`  (confidence 0.8, 12 insns)

**Evidence.** returns d0 = the index of character d0 in the name-entry alphabet 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.12 -' (30 when absent); caller sub_FB722 (name entry)

**Callers.** ai_SnapEntryCharToAlphabet
**Callees.** none

```
0FB750  movem.l	d1-d3/a0-a6,-(sp)
0FB754  move.l	#aAbcdefghijklmnopqrstu,a0
0FB75A  move.b	d0,d1
0FB75C  clr.w	d0
0FB75E  move.w	#$1E,d3
0FB762  cmp.b	(a0,d0.w),d1
0FB766  beq.w	loc_FB774
0FB76A  addq.w	#1,d0
0FB76C  dbf	d3,loc_FB762
0FB770  move.w	#$1E,d0
0FB774  movem.l	(sp)+,d1-d3/a0-a6
0FB778  rts
```

## `$0FECF8` -> `ai_NopShortHandedCheck`  (confidence 0.5, 12 insns)

**Evidence.** puckfaceoff: works out which team has fewer skaters ($24 of the home/away records) and compares its id $28 with $13, but the bne targets the very next instruction, so the routine has no effect beyond restoring registers; looks like a disabled team-specific check left in the shipped ROM; caller puckfaceoff

**Callers.** puckfaceoff
**Callees.** none

```
0FECF8  movem.l	d0-d2/a0-a2,-(sp)
0FECFC  move.l	#$FFFFC6CE,a0
0FED02  move.l	#$FFFFCA32,a1
0FED08  move.w	$24(a0),d0
0FED0C  sub.w	$24(a1),d0
0FED10  beq.w	loc_FED24
0FED14  bpl.w	loc_FED1A
0FED18  exg	a0,a1
0FED1A  cmp.w	#$13,$28(a0)
0FED20  bne.w	*+4
0FED24  movem.l	(sp)+,d0-d2/a0-a2
0FED28  rts
```

