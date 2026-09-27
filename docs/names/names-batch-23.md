# Name review: names-batch-23.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0081F2` -> `ai_PrintSeriesMatchup`  (confidence 0.6, 24 insns)

**Evidence.** playoff results list: for series d3 (skipped when it is the current series $CEE6 or its +$E flags 1/2 mark it pending/finished) prints the away team and its wins (+2, +$C) and the home team and its wins (+0, +$A) with ai_PrintTeamNameAndNumber, then the game/round label from word_191E4 (entry 8(a0) - 1) at column $1C

**Callers.** none found
**Callees.** ai_PrintNextString, ai_PrintTeamNameAndNumber
**RAM.** gamenum, printx, printy

```
0081F2  cmp.w	($FFFFCEE6).w,d3
0081F6  beq.w	locret_A9D4
0081FA  moveq	#$10,d0
0081FC  mulu.w	d3,d0
0081FE  move.w	#$CE66,a0
008202  add.w	d0,a0
008204  btst	#1,$E(a0)
00820A  bne.w	locret_A9D4
00820E  btst	#2,$E(a0)
008214  bne.w	locret_A9D4
008218  move.w	2(a0),d0
00821C  move.w	$C(a0),d1
008220  bsr.w	sub_8250
008224  addq.w	#1,($FFFFB02A).w
008228  move.w	(a0),d0
00822A  move.w	$A(a0),d1
00822E  bsr.w	sub_8250
008232  move.w	8(a0),d0
008236  subq.w	#1,d0
008238  move.l	#word_191E4,a1
00823E  move.w	#$1C,($FFFFB028).w
008244  jsr	sub_13508
00824A  addq.w	#2,($FFFFB02A).w
00824E  rts
```

## `$00F64E` -> `ai_TickLineChangeTimer`  (confidence 0.5, 24 insns)

**Evidence.** per-controller line-change box: a3 + d0 = timer word, +4 = player index (object $B04A + index*$80, team by $62 bit 6); when the player is not in line-change mode ($63 bit 3) sets the timer to -1 and shows the menu (ai_PrintLineChangeMenu); otherwise counts it down by d7 and on expiry auto-completes the change (sub_BB06 with d2 = 0) and reprints the menu

**Callers.** none found
**Callees.** ai_PrintLineChangeMenu, lcfound

```
00F64E  tst.w	(a3,d0.w)
00F652  bmi.w	locret_15464
00F656  move.w	4(a3,d0.w),d1
00F65A  asl.w	#7,d1
00F65C  move.w	#$B04A,a0
00F660  move.w	#$C6CE,a2
00F664  btst	#6,$62(a0,d1.w)
00F66A  beq.w	loc_F672
00F66E  add.w	#$364,a2
00F672  btst	#3,$63(a0,d1.w)
00F678  bne.w	loc_F684
00F67C  st	(a3,d0.w)
00F680  bra.w	sub_B92E
00F684  sub.w	d7,(a3,d0.w)
00F688  bpl.w	locret_15464
00F68C  move.l	a3,-(sp)
00F68E  lea	(a0,d1.w),a3
00F692  btst	#3,$63(a3)
00F698  beq.w	loc_F6A6
00F69C  clr.w	d2
00F69E  bsr.w	sub_BB06
00F6A2  bsr.w	sub_B92E
00F6A6  move.l	(sp)+,a3
00F6A8  rts
```

## `$0FC986` -> `ai_PrintShootoutScreen`  (confidence 0.6, 24 insns)

**Evidence.** shootout screen frame: erases the body (ai_EraseStatsBody), draws the background bitmap off_54E24 at tile base 1, a 26x6 box at column 7 row 1 and the 'Shootout' title; reached from the shootout mode dispatcher

**Callers.** none found
**Callees.** Framer, ai_DrawTeamBannerTiles, ai_EraseStatsBody, ai_PrintBigInline, dobitmap, printz
**Strings.** Shootout

```
0FC986  bsr.w	sub_FCA04
0FC98A  movem.l	d0-d5/a0-a2,-(sp)
0FC98E  jsr	sub_11B92
0FC994  dc.w	6
0FC996  dc.b	$FD
0FC997  dc.b	0
0FC998  dc.b	0
0FC999  dc.b	0
0FC99A  move.l	#off_54E24,a1
0FC9A0  add.l	4(a1),a1
0FC9A4  move.w	#$30A,a2
0FC9A8  clr.w	d0
0FC9AA  clr.w	d1
0FC9AC  move.w	(a1),d2
0FC9AE  move.w	2(a1),d3
0FC9B2  moveq	#1,d4
0FC9B4  moveq	#0,d5
0FC9B6  jsr	sub_1169A
0FC9BC  movem.l	(sp)+,d0-d5/a0-a2
0FC9C0  jsr	sub_11B92
0FC9C6  dc.w	6
0FC9C8  dc.b	$BE
0FC9C9  dc.b	7
0FC9CA  dc.b	1
0FC9CB  dc.b	0
0FC9CC  moveq	#$1A,d0
0FC9CE  moveq	#6,d1
0FC9D0  jsr	sub_119B8
0FC9D6  jsr	sub_11DE2
0FC9DC  dc.w	$14
0FC9DE  dc.b	$BE
0FC9DF  dc.b	$A
0FC9E0  dc.b	4
0FC9E1  aShootout_0:	dc.b	'  Shootout  '
0FC9ED  dc.b	$BE
0FC9EE  dc.b	$F
0FC9EF  dc.b	1
0FC9F0  clr.w	d0
0FC9F2  cmp.w	#$C6CE,a2
0FC9F6  beq.w	loc_FC9FE
0FC9FA  move.w	#$2C,d0
0FC9FE  jmp	sub_8078
```

## `$0086F8` -> `ai_PrintEditLinesScreen`  (confidence 0.6, 19 insns)

**Evidence.** edit-lines screen frame, byte-for-byte the shape of ai_PrintShootoutScreen: erases the body (ai_EraseEditLinesBody), draws the background bitmap off_54E24 at tile base 1 and the 26x6 title box at column 7 row 1

**Callers.** none found
**Callees.** Framer, ai_EraseEditLinesBody, ai_PrintBigInline, dobitmap, printz

```
0086F8  bsr.w	sub_8774
0086FC  movem.l	d0-d5/a0-a2,-(sp)
008700  jsr	sub_11B92
008706  dc.w	6
008708  dc.b	$FD
008709  dc.b	0
00870A  dc.b	0
00870B  dc.b	0
00870C  move.l	#off_54E24,a1
008712  add.l	4(a1),a1
008716  move.w	#$30A,a2
00871A  clr.w	d0
00871C  clr.w	d1
00871E  move.w	(a1),d2
008720  move.w	2(a1),d3
008724  moveq	#1,d4
008726  moveq	#0,d5
008728  jsr	sub_1169A
00872E  movem.l	(sp)+,d0-d5/a0-a2
008732  jsr	sub_11B92
008738  dc.w	6
00873A  dc.b	$BE
00873B  dc.b	7
00873C  dc.b	1
00873D  dc.b	0
00873E  moveq	#$1A,d0
008740  moveq	#6,d1
008742  jsr	sub_119B8
008748  jsr	sub_11DE2
00874E  dc.w	$14
008750  dc.b	$BE
008751  dc.b	$A
008752  dc.b	4
008753  dc.b	$4C
008754  dc.b	$69
008755  dc.b	$6E
008756  dc.b	$65
008757  dc.b	$20
008758  dc.b	$20
008759  dc.b	$45
00875A  dc.b	$64
00875B  dc.b	$69
00875C  dc.b	$74
00875D  dc.b	$6F
00875E  dc.b	$72
00875F  dc.b	$BE
008760  dc.b	$E
008761  dc.b	1
008762  dc.b	$42
008763  dc.b	$40
008764  dc.b	$B4
008765  dc.b	$FC
008766  dc.b	$C6
008767  dc.b	$CE
008768  dc.b	$67
008769  dc.b	0
00876A  dc.b	$F9
00876B  dc.b	$E
00876C  dc.b	$30
00876D  dc.b	$3C
...
```

## `$009A84` -> `ai_PrintCrowdMeterLevels`  (confidence 0.7, 23 insns)

**Evidence.** crowd meter page: prints 'Current Level' (CwdExciteLvl), 'Average Level' (SumCwdExciteLvl / NumCwdExciteLvl), 'Peak Level' (MaxCwdExciteLvl) and 'Arena Record' with ai_PrintCrowdMeterValue for each, then falls into ai_PrintLeagueCrowdRecord

**Callers.** none found
**Callees.** ReadTeamRecord, ai_PrintCrowdMeterValue, printz2
**Strings.** Current Level | Average Level | Peak Level | Arena Record
**RAM.** CwdExciteLvl, HomeTeam, MaxCwdExciteLvl, NumCwdExciteLvl, SumCwdExciteLvl, ValidSRAM

```
009A84  bsr.w	sub_11A36
009A88  dc.w	$16
009A8A  dc.b	$F8
009A8B  dc.b	4
009A8C  dc.b	2
009A8D  dc.b	4
009A8E  dc.b	$C
009A8F  aCurrentLevel:	dc.b	'Current Level'
009A9C  dc.b	$FD
009A9D  dc.b	$1C
009A9E  move.w	($FFFFB8A2).w,d0
009AA2  bsr.w	sub_9BB4
009AA6  bsr.w	sub_11A36
009AAA  dc.w	$16
009AAC  dc.b	$FD
009AAD  dc.b	4
009AAE  dc.b	$FA
009AAF  dc.b	2
009AB0  aAverageLevel:	dc.b	'Average Level'
009ABD  dc.b	$FD
009ABE  dc.b	$1C
009ABF  dc.b	0
009AC0  move.l	($FFFFB8A8).w,d0
009AC4  divu.w	($FFFFB8A6).w,d0
009AC8  bsr.w	sub_9BB4
009ACC  bsr.w	sub_11A36
009AD0  dc.w	$12
009AD2  dc.b	$FD
009AD3  dc.b	4
009AD4  dc.b	$FA
009AD5  dc.b	2
009AD6  aPeakLevel:	dc.b	'Peak Level'
009AE0  dc.b	$FD
009AE1  dc.b	$1C
009AE2  move.w	($FFFFB8A4).w,d0
009AE6  bsr.w	sub_9BB4
009AEA  movem.l	d0-a6,-(sp)
009AEE  tst.w	($FFFFD458).w
009AF2  bmi.w	loc_9BAE
009AF6  move.w	($FFFFC330).w,d1
009AFA  ext.l	d1
009AFC  move.l	#$FFFFCF36,a0
009B02  jsr	sub_F9BE2
009B08  move.b	8(a0),d0
009B0C  bne.w	loc_9B14
009B10  move.b	#$50,d0
009B14  and.w	#$FF,d0
009B18  move.w	d0,-(sp)
009B1A  bsr.w	sub_11A36
```

## `$009B4A` -> `ai_PrintLeagueCrowdRecord`  (confidence 0.7, 18 insns)

**Evidence.** crowd meter page tail: finds the loudest team (ai_FindLoudestCrowdTeam), reads its record byte 8 (default $50) and prints 'League Record' with the value as a 3-digit number followed by 'dB'

**Callers.** none found
**Callees.** DeterStrLength?, ReadTeamRecord, ai_FindLoudestCrowdTeam, print, printz, printz2
**Strings.** League Record | dB

```
009B4A  dc.w	6
009B4C  dc.b	$20
009B4D  dc.b	$64
009B4E  dc.b	$42
009B4F  dc.b	0
009B50  jsr	sub_FEC5E
009B56  move.w	d0,d1
009B58  ext.l	d1
009B5A  move.l	#$FFFFCF36,a0
009B60  jsr	sub_F9BE2
009B66  move.b	8(a0),d0
009B6A  bne.w	loc_9B72
009B6E  move.w	#$50,d0
009B72  and.w	#$FF,d0
009B76  move.w	d0,-(sp)
009B78  bsr.w	sub_11A36
009B7C  dc.w	$16
009B7E  dc.b	$FD
009B7F  dc.b	4
009B80  dc.b	$FA
009B81  dc.b	2
009B82  aLeagueRecord:	dc.b	'League Record'
009B8F  dc.b	$FD
009B90  dc.b	$1C
009B91  dc.b	0
009B92  move.w	(sp)+,d0
009B94  move.w	#3,d1
009B98  jsr	sub_11D3A
009B9E  jsr	sub_11BA4
009BA4  bsr.w	sub_11B92
009BA8  dc.w	6
009BAA  aDb:		dc.b	' dB',0
009BAE  movem.l	(sp)+,d0-a6
009BB2  rts
```

## `$0FCAB8` -> `ai_PrintShootoutShooterBox`  (confidence 0.5, 19 insns)

**Evidence.** shootout screen: draws a 24x3 box at column 8 row 7 and prints, at column $15, the shooter selected by $D5B8 from the home ($D57A) or away ($D588) shooter list of ai_LoadShootoutShooters (a2 chooses the side)

**Callers.** none found
**Callees.** Framer, getname, print2, printz2
**RAM.** printx

```
0FCAB8  jsr	sub_11A36
0FCABE  dc.w	$A
0FCAC0  dc.b	$F8
0FCAC1  dc.b	4
0FCAC2  dc.b	2
0FCAC3  dc.b	8
0FCAC4  dc.b	7
0FCAC5  dc.b	$F9
0FCAC6  dc.b	1
0FCAC7  dc.b	0
0FCAC8  moveq	#$18,d0
0FCACA  moveq	#3,d1
0FCACC  jsr	sub_119B8
0FCAD2  jsr	sub_11A36
0FCAD8  dc.w	8
0FCADA  dc.b	$FD
0FCADB  dc.b	$15
0FCADC  dc.b	$FC
0FCADD  dc.b	8
0FCADE  dc.b	$FE
0FCADF  dc.b	6
0FCAE0  move.l	#$FFFFD57A,a1
0FCAE6  cmp.l	#$FFFFC6CE,a2
0FCAEC  beq.w	loc_FCAF6
0FCAF0  move.l	#$FFFFD588,a1
0FCAF6  move.w	($FFFFD5B8).w,d0
0FCAFA  asl.w	#1,d0
0FCAFC  move.w	(a1,d0.w),d0
0FCB00  jsr	sub_18A90
0FCB06  move.w	(a1),d0
0FCB08  lsr.w	#1,d0
0FCB0A  sub.w	d0,($FFFFB028).w
0FCB0E  jsr	sub_11A48
0FCB14  clr.w	($FFFFB030).w
0FCB18  rts
```

## `$0FEAFA` -> `ai_PrintGoalsInParens`  (confidence 0.7, 19 insns)

**Evidence.** prints ' (' + player d0's goal total (team column +$B4, 1..3 digits) + ')' then moves to the next row at column $E; used by the ticker/scoring text

**Callers.** none found
**Callees.** DeterStrLength?, print, printz
**RAM.** printx, printy

```
0FEAFA  movem.l	d0/a2,-(sp)
0FEAFE  jsr	sub_11B92
0FEB04  dc.w	4
0FEB06  dc.b	' ('
0FEB08  add.w	#$B4,a2
0FEB0C  move.b	(a2,d0.w),d0
0FEB10  ext.w	d0
0FEB12  move.w	#1,d1
0FEB16  cmpnw	 9,d0
0FEB1A  ble.w	loc_FEB2E
0FEB1E  move.w	#2,d1
0FEB22  cmpnw	 $63,d0
0FEB26  ble.w	loc_FEB2E
0FEB2A  move.w	#3,d1
0FEB2E  jsr	sub_11D3A
0FEB34  jsr	sub_11BA4
0FEB3A  jsr	sub_11B92
0FEB40  dc.w	4
0FEB42  dc.b	')',0
0FEB44  addq.w	#1,($FFFFB02A).w
0FEB48  move.w	#$E,($FFFFB028).w
0FEB4E  movem.l	(sp)+,d0/a2
0FEB52  rts
```

## `$0FB822` -> `ai_PrintUserNameList`  (confidence 0.7, 18 insns)

**Evidence.** user selection screen: prints the seven stored user names (entries 1..7 of $D45A via ai_CopyUserNameDashed and ai_PrintNameEntryField) one per row from column 5 row 8, preserving $D4E8/$D4EA

**Callers.** none found
**Callees.** ai_CopyUserNameDashed, ai_PrintNameEntryField, printz
**RAM.** printx, printy

```
0FB822  movem.l	d0-a6,-(sp)
0FB826  move.w	($FFFFD4E8).w,-(sp)
0FB82A  move.w	($FFFFD4EA).w,-(sp)
0FB82E  jsr	sub_11B92
0FB834  dc.w	6
0FB836  dc.b	$BF
0FB837  dc.b	5
0FB838  dc.b	8
0FB839  dc.b	0
0FB83A  move.w	#6,d7
0FB83E  move.w	#1,($FFFFD4EA).w
0FB844  move.l	#$FFFFBF20,a1
0FB84A  bsr.w	sub_FB992
0FB84E  move.w	($FFFFB028).w,-(sp)
0FB852  bsr.w	sub_FB91A
0FB856  move.w	(sp)+,($FFFFB028).w
0FB85A  addq.w	#1,($FFFFB02A).w
0FB85E  addq.w	#1,($FFFFD4EA).w
0FB862  dbf	d7,loc_FB84A
0FB866  move.w	(sp)+,($FFFFD4EA).w
0FB86A  move.w	(sp)+,($FFFFD4E8).w
0FB86E  movem.l	(sp)+,d0-a6
0FB872  rts
```

## `$0FC4C0` -> `ai_StartShootoutAttempt`  (confidence 0.6, 18 insns)

**Evidence.** shootout attempt start: when the shootout is already decided ($C2FA bit 3) jumps to loc_172E4; otherwise starts a skating script (ai_StartWaypointScript), sets BA_Team = the shooting side $D594, the goalie slot BA_Goalie_SCnum = $B (home) or 5 (away), takes the shooter index from the side's list ($D57A/$D588) at $D586 into $D40A and clears $B7AC bit 2

**Callers.** none found
**Callees.** ai_StartWaypointScript, loc_172E4
**RAM.** BA_Goalie_SCnum, BA_Skater_Offset, BA_Team

```
0FC4C0  btst	#3,($FFFFC2FA).w
0FC4C6  beq.w	loc_FC4D0
0FC4CA  jmp	loc_172E4
0FC4D0  movem.l	d0-a6,-(sp)
0FC4D4  bsr.w	sub_FE756
0FC4D8  move.w	($FFFFD594).w,($FFFFD404).w
0FC4DE  move.w	#$B,($FFFFD408).w
0FC4E4  move.l	#$FFFFD57A,a0
0FC4EA  tst.w	($FFFFD594).w
0FC4EE  beq.w	loc_FC4FE
0FC4F2  move.w	#5,($FFFFD408).w
0FC4F8  move.l	#$FFFFD588,a0
0FC4FE  move.w	($FFFFD586).w,d0
0FC502  add.w	d0,d0
0FC504  move.w	(a0,d0.w),($FFFFD40A).w
0FC50A  bclr	#2,($FFFFB7AC).w
0FC510  movem.l	(sp)+,d0-a6
0FC514  rts
```

## `$0FEF8C` -> `ai_PuckApproachingPlayer`  (confidence 0.5, 18 insns)

**Evidence.** returns (in the condition codes) whether the puck is within $1E of player a3 in x and y and moving toward him: the sign of (puckx - x) is compared with puckvx and, when both agree, (pucky - y) with puckvy; used by the pass-reception checks

**Callers.** none found
**Callees.** none
**RAM.** puckvx, puckvy, puckx, pucky

```
0FEF8C  movem.w	d0-d1,-(sp)
0FEF90  move.w	($FFFFB74A).w,d0
0FEF94  sub.w	(a3),d0
0FEF96  cmpnw	 $1E,d0
0FEF9A  bgt.w	loc_FEFC6
0FEF9E  move.w	($FFFFB772).w,d1
0FEFA2  eor.w	d1,d0
0FEFA4  and.w	#$8000,d0
0FEFA8  beq.w	loc_FEFC6
0FEFAC  move.w	($FFFFB75E).w,d0
0FEFB0  sub.w	$14(a3),d0
0FEFB4  cmpnw	 $1E,d0
0FEFB8  bgt.w	loc_FEFC6
0FEFBC  move.w	($FFFFB774).w,d1
0FEFC0  eor.w	d1,d0
0FEFC2  and.w	#$8000,d0
0FEFC6  movem.w	(sp)+,d0-d1
0FEFCA  rts
```

## `$011924` -> `ai_DecompressTileRun`  (confidence 0.5, 17 insns)

**Evidence.** ai_DecompressTiles handler for a raw run: d1 = tile count (0 means 256), advances the destination d3 by count*2 words... and writes the tiles from a1 through the remap routine (a5) when an inline nibble map is set in (a4), else through DoDMApro (a6)

**Callers.** none found
**Callees.** loc_1194C

```
011924  movem.l	d0-d1/a0-a1,-(sp)
011928  move.w	d1,d0
01192A  bne.w	loc_11932
01192E  move.w	#$100,d0
011932  lsr.w	#1,d0
011934  move.w	d3,d1
011936  add.w	d0,d3
011938  add.w	d0,d3
01193A  move.l	a1,a0
01193C  tst.l	(a4)
01193E  beq.w	loc_1194A
011942  move.l	(a4),a1
011944  jsr	(a5)
011946  bra.w	loc_1194C
01194A  jsr	(a6)
01194C  movem.l	(sp)+,d0-d1/a0-a1
011950  rts
```

