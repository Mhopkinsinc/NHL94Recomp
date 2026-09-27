# Name review: names-batch-09.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0180FC` -> `ai_AdvancePlayoffsAfterGame`  (confidence 0.7, 32 insns)

**Evidence.** PeriodOver hook for playoff mode ($D04A rounds left, $D048 state not 0 or 4): sets $D048/$D074 = 1, records the result (ai_AdvancePlayoffSeries), rebuilds the bracket (sub_17D80), then either encodes the new password into $D088 and saves it (ai_EncodePlayoffPassword, ai_SavePlayoffPassword; decoding $D176 back when $C2F0 bit 2 is set) or, when gamelevel is 4 or the series index $CEE6 is negative, clears the password and moves the state to 2 or 3 (final when bosgames is 7)

**Callers.** PeriodOver
**Callees.** MakeTree, ai_AdvancePlayoffSeries, ai_BigNumClear, ai_DecodePlayoffPassword, ai_EncodePlayoffPassword, ai_SavePlayoffPassword
**RAM.** OptNOP, OptPlayMode, TempOptPlayMode, bosgames, gamelevel, gamenum, sflags3

```
0180FC  tst.w	($FFFFD04A).w
018100  beq.w	locret_15464
018104  tst.w	($FFFFD048).w
018108  beq.w	locret_15464
01810C  cmp.w	#4,($FFFFD048).w
018112  beq.w	locret_15464
018116  move.w	#1,($FFFFD048).w
01811C  move.w	#1,($FFFFD074).w
018122  bsr.w	sub_18380
018126  bsr.w	sub_17D80
01812A  cmp.w	#4,($FFFFCEEC).w
018130  beq.w	loc_18160
018134  tst.w	($FFFFCEE6).w
018138  bmi.w	loc_18160
01813C  move.w	#$D088,a3
018140  bsr.w	sub_18192
018144  jsr	sub_FE696
01814A  btst	#2,($FFFFC2F0).w
018150  beq.w	locret_15464
018154  move.w	#$D176,a3
018158  bsr.w	sub_1803E
01815C  bra.w	sub_17D80
018160  move.w	#$D088,a3
018164  bsr.w	sub_1820E
018168  jsr	sub_FE696
01816E  move.w	#2,($FFFFD048).w
018174  move.w	#2,($FFFFD074).w
01817A  cmp.w	#7,($FFFFCEEA).w
018180  beq.w	locret_15464
018184  move.w	#3,($FFFFD048).w
01818A  move.w	#3,($FFFFD074).w
018190  rts
```

## `$00945C` -> `ai_PrintStatsScreen`  (confidence 0.7, 38 insns)

**Evidence.** stats screen frame: ai_SetupStatsScreenVideo, clears the scroll/selection counters, draws the 30x6 header box, prints 'Playoff  Stats' (d7 != 0, from sub_9428) or 'Player  Stats' with the 'Switch^Teams' hint, then the list via ai_PrintPlayerStatsList; callers sub_9428 and the player-stats menu

**Callers.** ai_ShowPlayoffStats
**Callees.** Framer, ai_DrawTeamBannerTiles, ai_PrintBigInline, ai_PrintPlayerStatsList, ai_PrintScrollArrows, ai_SetupStatsScreenVideo, getpzjoy, loc_94EA, nodiag, printz, printz2, vcountwait
**Strings.** Playoff  Stats | Switch^Teamsù | Player  Stats
**RAM.** DispAttribCtr, PlayerScrollCtr, VertLineScrolling

```
00945C  moveq	#$D,d0
00945E  moveq	#$16,d1
009460  bsr.w	loc_9BD8
009464  clr.w	($FFFFD5AC).w
009468  clr.w	($FFFFD5AE).w
00946C  clr.w	($FFFFD5B0).w
009470  jsr	sub_11B92
009476  dc.w	6
009478  dc.b	$BD
009479  dc.b	5
00947A  dc.b	1
00947B  dc.b	0
00947C  moveq	#$1E,d0
00947E  moveq	#6,d1
009480  jsr	sub_119B8
009486  tst.w	d7
009488  beq.w	loc_94AC
00948C  jsr	sub_11DE2
009492  dc.w	$16
009494  dc.b	$BD
009495  dc.b	7
009496  dc.b	4
009497  aPlayoffStats:	dc.b	'Playoff  Stats'
0094A5  dc.b	$BD
0094A6  dc.b	$E
0094A7  dc.b	1
0094A8  bra.w	loc_94EA
0094AC  jsr	sub_11A36
0094B2  dc.w	$1C
0094B4  dc.b	$F8
0094B5  dc.b	6
0094B6  dc.b	3
0094B7  dc.b	$C
0094B8  dc.b	$1A
0094B9  dc.b	$F9
0094BA  dc.b	1
0094BB  dc.b	$41
0094BC  dc.b	$5E
0094BD  dc.b	$2D
0094BE  dc.b	$5E
0094BF  aSwitchTeams:	dc.b	'Switch^Teamsù'
0094CC  dc.b	0
0094CD  dc.b	0
0094CE  jsr	sub_11DE2
0094D4  dc.w	$16
0094D6  dc.b	$BD
0094D7  dc.b	8
0094D8  dc.b	4
0094D9  aPlayerStats:	dc.b	'Player  Stats'
0094E6  dc.b	$BD
0094E7  dc.b	$E
0094E8  dc.b	1
0094E9  dc.b	0
0094EA  clr.w	d0
0094EC  cmp.w	#$C6CE,a2
0094F0  beq.w	loc_94F8
0094F4  move.w	#$2C,d0
0094F8  bsr.w	sub_8078
0094FC  bsr.w	loc_961A
009500  bsr.w	sub_99C6
...
```

## `$0085EE` -> `ai_PrintLineRoster`  (confidence 0.7, 37 insns)

**Evidence.** edit-lines screen: for line d5 prints the line name from word_191A6 plus ' Line' at the position from word_879E (shifted one entry when $D058 is set), then the line's player slots from the team's line table $16A(a2) (8 bytes per line) as padded surnames (ai_FormatPlayerSurnamePadded), highlighting the slot equal to the cursor $D5B8; caller loc_8566 (per-line refresh)

**Callers.** ai_RefreshEditLinesRows
**Callees.** ai_FormatPlayerSurnamePadded, ai_PrintNextString, print2, printz2
**Strings.** Line
**RAM.** OptLine, printa, printx, printy

```
0085EE  moveq	#6,d0
0085F0  mulu.w	d5,d0
0085F2  lea	word_879E(pc),a0
0085F6  add.w	d0,a0
0085F8  tst.w	($FFFFD058).w
0085FC  beq.w	loc_8602
008600  subq.w	#6,a0
008602  move.w	(a0),($FFFFB028).w
008606  move.w	2(a0),($FFFFB02A).w
00860C  move.w	d5,d0
00860E  move.l	#word_191A6,a1
008614  move.w	#$8000,($FFFFB02C).w
00861A  jsr	sub_13508
008620  jsr	sub_11A36
008626  dc.w	8
008628  aLine:		dc.b	' Line',0
00862E  move.w	(a0),($FFFFB028).w
008632  move.w	d5,d4
008634  asl.w	#3,d4
008636  addq.w	#1,d4
008638  move.w	2(a0),($FFFFB02A).w
00863E  move.w	4(a0),d3
008642  lea	$16A(a2),a3
008646  move.w	(a0),($FFFFB028).w
00864A  jsr	sub_11A36
008650  dc.w	8
008652  dc.b	$FB
008653  dc.b	$FF
008654  dc.b	$FA
008655  dc.b	2
008656  dc.b	$FE
008657  dc.b	6
008658  clr.w	d0
00865A  move.b	(a3,d4.w),d0
00865E  subq.w	#1,d0
008660  jsr	sub_18B6E
008666  cmp.w	($FFFFD5B8).w,d4
00866A  bne.w	loc_867A
00866E  move.w	d0,d6
008670  move.w	($FFFFB02C).w,d7
008674  move.w	#2,($FFFFB030).w
00867A  jsr	sub_11A48
008680  clr.w	($FFFFB030).w
008684  addq.w	#1,d4
008686  dbf	d3,loc_8646
00868A  rts
```

## `$0F99F2` -> `ai_ReadPlayerRecordValue`  (confidence 0.5, 38 insns)

**Evidence.** d0 = team, d1 = player index: walks the team's roster to the player, reads his record field with ReadRecordField into (a0), returns d0 = the record's value byte and d1 = 1 when the player index is above the team's attribute-column count (the goalie slot) else 0; caller sub_F98C6 (prints 'Record ... goals/saves' lines)

**Callers.** ai_BuildPlayerRecordText
**Callees.** ai_ReadRecordField, loc_F9A10, loc_F9A5E

```
0F99F2  movem.l	d2-a6,-(sp)
0F99F6  move.w	d0,-(sp)
0F99F8  move.l	#$30E,a2
0F99FE  asl.w	#2,d0
0F9A00  move.l	(a2,d0.w),a2
0F9A04  add.w	(a2),a2
0F9A06  move.w	d1,d0
0F9A08  bra.w	loc_F9A10
0F9A0C  add.w	(a2),a2
0F9A0E  addq.w	#8,a2
0F9A10  dbf	d0,loc_F9A0C
0F9A14  move.w	d1,d0
0F9A16  move.w	(sp)+,d1
0F9A18  move.w	d0,d5
0F9A1A  move.w	d1,d4
0F9A1C  ext.l	d0
0F9A1E  move.l	#$FFFF0000,a0
0F9A24  bsr.w	sub_F9B94
0F9A28  move.b	(a0),d0
0F9A2A  ext.w	d0
0F9A2C  move.l	#$30E,a5
0F9A32  asl.w	#2,d4
0F9A34  move.l	(a5,d4.w),a5
0F9A38  add.w	$A(a5),a5
0F9A3C  move.w	(a5),d1
0F9A3E  movem.w	d0,-(sp)
0F9A42  clr.w	d0
0F9A44  addq.w	#1,d0
0F9A46  asl.w	#4,d1
0F9A48  bne.s	loc_F9A44
0F9A4A  cmp.w	d5,d0
0F9A4C  movem.w	(sp)+,d0
0F9A50  bgt.w	loc_F9A5A
0F9A54  clr.w	d1
0F9A56  bra.w	loc_F9A5E
0F9A5A  move.w	#1,d1
0F9A5E  movem.l	(sp)+,d2-a6
0F9A62  rts
```

## `$0F9F50` -> `ai_UpdateScorerRecords`  (confidence 0.6, 31 insns)

**Evidence.** for the 26 roster slots of team a2 compares each player's game total (goals from column +$B4, or for the goalie slots saves = +$E8 shots minus +$B4 goals against) with his stored record byte (ReadRecordField) and, when beaten, writes the new value with the two user ids ($D043/$D045, swapped for the away team) and the opponent team d6 through WriteRecordField; caller ai_UpdateGameRecords

**Callers.** ai_UpdateGameRecords
**Callees.** ai_ReadRecordField, ai_WriteRecordField, loc_F9F84

```
0F9F50  clr.l	d0
0F9F52  move.w	#$19,d2
0F9F56  bsr.w	sub_F9B94
0F9F5A  cmp.w	d5,d0
0F9F5C  blt.w	loc_F9F70
0F9F60  move.w	d0,-(sp)
0F9F62  add.w	#$B4,d0
0F9F66  move.b	(a2,d0.w),d4
0F9F6A  move.w	(sp)+,d0
0F9F6C  bra.w	loc_F9F84
0F9F70  move.w	d0,-(sp)
0F9F72  add.w	#$E8,d0
0F9F76  move.b	(a2,d0.w),d4
0F9F7A  add.w	#-$34,d0
0F9F7E  sub.b	(a2,d0.w),d4
0F9F82  move.w	(sp)+,d0
0F9F84  move.b	(a0),d3
0F9F86  cmp.b	d3,d4
0F9F88  ble.w	loc_F9FB8
0F9F8C  move.b	d4,(a0)
0F9F8E  move.b	($FFFFD043).w,1(a0)
0F9F94  move.b	($FFFFD045).w,3(a0)
0F9F9A  cmp.l	#$FFFFC6CE,a2
0F9FA0  beq.w	loc_F9FB0
0F9FA4  move.b	($FFFFD045).w,1(a0)
0F9FAA  move.b	($FFFFD043).w,3(a0)
0F9FB0  move.b	d6,2(a0)
0F9FB4  bsr.w	sub_F9BDA
0F9FB8  addq.w	#1,d0
0F9FBA  dbf	d2,loc_F9F56
0F9FBE  rts
```

## `$0FA66E` -> `ai_DrawRecordsTeamLogo`  (confidence 0.7, 32 insns)

**Evidence.** records screen: at (d0,d1) draws the 6x6 logo of the selected team (HomeTeam, or VisTeam when $D4F6 is set) from off_F86F2 through dobitmap at tile base $D450 with the unk_FF462 template, preserving the palette longs $BD4A/$BD4E; caller ai_PrintRecordsScreen (once per side)

**Callers.** ai_PrintRecordsScreen
**Callees.** dobitmap, printz
**RAM.** HomeTeam, VisTeam, printx, printy

```
0FA66E  movem.l	d0-a6,-(sp)
0FA672  jsr	sub_11B92
0FA678  dc.w	6
0FA67A  dc.b	$BE
0FA67B  dc.b	0
0FA67C  dc.b	0
0FA67D  dc.b	0
0FA67E  move.w	d0,($FFFFB028).w
0FA682  move.w	d1,($FFFFB02A).w
0FA686  move.w	($FFFFD450).w,d4
0FA68A  move.w	($FFFFC330).w,d3
0FA68E  tst.w	($FFFFD4F6).w
0FA692  beq.w	loc_FA69A
0FA696  move.w	($FFFFC332).w,d3
0FA69A  asl.w	#2,d3
0FA69C  move.l	#off_F86F2,a0
0FA6A2  move.l	(a0,d3.w),a0
0FA6A6  move.l	a0,a1
0FA6A8  move.l	a0,a2
0FA6AA  add.l	(a2)+,a0
0FA6AC  asl.w	#3,d3
0FA6AE  move.l	#unk_FF462,a0
0FA6B4  sub.w	#$20,d3
0FA6B8  add.w	d3,a0
0FA6BA  add.l	(a2)+,a1
0FA6BC  move.w	#6,d3
0FA6C0  move.w	#6,d2
0FA6C4  clr.w	d0
0FA6C6  clr.w	d1
0FA6C8  move.l	($FFFFBD4A).w,-(sp)
0FA6CC  move.l	($FFFFBD4E).w,-(sp)
0FA6D0  move.w	#2,d5
0FA6D4  jsr	sub_1169A
0FA6DA  move.l	(sp)+,($FFFFBD4E).w
0FA6DE  move.l	(sp)+,($FFFFBD4A).w
0FA6E2  movem.l	(sp)+,d0-a6
0FA6E6  rts
```

## `$0FD618` -> `ai_ShootoutWinnersCelebrate`  (confidence 0.5, 35 insns)

**Evidence.** called by sub_FC516 when the shootout is decided ($D595 bit 0, at least 5 rounds in $D578 and the round scores $D574/$D576 differ): sets $C2EE bit 2, $DED0 = $60, then for the five skaters of the team with the higher score (object block $B04A or +6*$80) sets slot $34 = 2, places them at x = 0 and y = Vpos +-$F0, starts animation 7 (sub_10658) and clears their state flags; caller sub_FC516

**Callers.** ai_AdvanceShootoutRound
**Callees.** assinsert, freezewindow, loc_FD6A4, setplayer
**RAM.** Vpos, sflags2

```
0FD618  movem.l	d0-a6,-(sp)
0FD61C  bset	#2,($FFFFC2EE).w
0FD622  jsr	sub_AFB6
0FD628  move.w	#$60,($FFFFDED0).w
0FD62E  move.l	#$FFFFB04A,a3
0FD634  move.w	#0,d0
0FD638  move.w	($FFFFD574).w,d2
0FD63C  cmp.w	($FFFFD576).w,d2
0FD640  bgt.w	loc_FD648
0FD644  move.w	#6,d0
0FD648  asl.w	#7,d0
0FD64A  add.w	d0,a3
0FD64C  move.w	#4,d2
0FD650  move.w	#6,d3
0FD654  bra.w	loc_FD6A4
0FD658  movem.w	d2-d3,-(sp)
0FD65C  jsr	sub_15AA4
0FD662  move.w	#2,$34(a3)
0FD668  move.w	#$F0,d0
0FD66C  tst.w	($FFFFBD18).w
0FD670  bmi.w	loc_FD678
0FD674  move.w	#$FF10,d0
0FD678  add.w	($FFFFBD18).w,d0
0FD67C  move.w	d0,$14(a3)
0FD680  move.w	#0,(a3)
0FD684  move.w	#7,d0
0FD688  jsr	sub_10658
0FD68E  bclr	#5,$62(a3)
0FD694  bclr	#1,$63(a3)
0FD69A  bclr	#2,$62(a3)
0FD6A0  movem.w	(sp)+,d2-d3
0FD6A4  add.l	#$80,a3
0FD6AA  dbf	d2,loc_FD658
0FD6AE  movem.l	(sp)+,d0-a6
0FD6B2  rts
```

## `$01592C` -> `ai_SetupPenaltyShotPlayers`  (confidence 0.7, 31 insns)

**Evidence.** puckpenshot: for the six players of team a2 ($22(a2) = first object): the shooter (state $52 equal to BA_Sktr_SCnum) gets slot $34 = 4 and the number byte from $D40B, the goalie (BA_Goalie_SCnum) keeps slot 0, both via sub_15A88 and get their line-status word $66(a2,idx) set to -1 (off the ice list) with sub_15AA4; everyone else is benched (bit 2 of $63, animation $20 via sub_10662); caller puckpenshot

**Callers.** puckpenshot
**Callees.** Setplass, assreplace, loc_1597E, loc_15992, setplayer
**RAM.** BA_Goalie_SCnum, BA_Sktr_SCnum

```
01592C  movem.l	d0-d5/a0-a3,-(sp)
015930  move.w	$22(a2),a3
015934  moveq	#5,d4
015936  move.w	$52(a3),d0
01593A  cmp.w	($FFFFD406).w,d0
01593E  beq.w	loc_1595C
015942  cmp.w	($FFFFD408).w,d0
015946  beq.w	loc_15976
01594A  bset	#2,$63(a3)
015950  move.w	#$20,d0
015954  bsr.w	sub_10662
015958  bra.w	loc_15992
01595C  bsr.w	sub_15A88
015960  move.b	$61(a3),($FFFFC31E).w
015966  move.b	($FFFFD40B).w,$61(a3)
01596C  move.w	#4,$34(a3)
015972  bra.w	loc_1597E
015976  bsr.w	sub_15A88
01597A  clr.w	$34(a3)
01597E  clr.w	d3
015980  move.b	$61(a3),d3
015984  add.w	d3,d3
015986  move.w	#$FFFF,$66(a2,d3.w)
01598C  lsr.w	#1,d3
01598E  bsr.w	sub_15AA4
015992  st	$61(a3)
015996  st	$60(a3)
01599A  add.w	#$80,a3
01599E  dbf	d4,loc_15936
0159A2  movem.l	(sp)+,d0-d5/a0-a3
0159A6  rts
```

## `$0FF7E2` -> `ai_StartPowerPlaySong`  (confidence 0.6, 33 insns)

**Evidence.** puckfaceoff2 helper: compares the active skater counts $24 of the home and away records; when they differ (a power play) and the state bit $C2EE bit 6 changes, sets HmTeam = HomeTeam and SongIndex = 1 (home power play) or 4 (away) and calls ChooseSong, guarded by $C2EE bit 5 so the song starts once; skipped in $C2FA bit 1 mode; caller puckfaceoff2

**Callers.** puckfaceoff2
**Callees.** ChooseSong, ai_ClearPowerPlaySongLatch, loc_FF83A, loc_FF85E, loc_FF884
**RAM.** HmTeam, HomeTeam, SongIndex, sflags2

```
0FF7E2  movem.l	d0/a0-a3,-(sp)
0FF7E6  move.w	($FFFFC2EE).w,-(sp)
0FF7EA  btst	#1,($FFFFC2FA).w
0FF7F0  bne.w	loc_FF884
0FF7F4  move.w	#$C6CE,a2
0FF7F8  lea	$364(a2),a3
0FF7FC  move.w	$24(a2),d0
0FF800  sub.w	$24(a3),d0
0FF804  beq.w	loc_FF884
0FF808  bpl.w	loc_FF824
0FF80C  btst	#6,($FFFFC2EE).w
0FF812  bne.w	loc_FF83A
0FF816  bsr.w	sub_FF87C
0FF81A  bset	#6,($FFFFC2EE).w
0FF820  bra.w	loc_FF83A
0FF824  exg	a2,a3
0FF826  btst	#6,($FFFFC2EE).w
0FF82C  beq.w	loc_FF83A
0FF830  bsr.w	sub_FF87C
0FF834  bclr	#6,($FFFFC2EE).w
0FF83A  bset	#5,($FFFFC2EE).w
0FF840  bne.w	loc_FF884
0FF844  cmp.w	#$C6CE,a3
0FF848  bne.w	loc_FF868
0FF84C  move.w	($FFFFC330).w,($FFFFD6CA).w
0FF852  move.w	#1,($FFFFD6CC).w
0FF858  jsr	sub_FE556
0FF85E  bset	#6,($FFFFC2FE).w
0FF864  bra.w	loc_FF884
0FF868  move.w	($FFFFC330).w,($FFFFD6CA).w
0FF86E  move.w	#4,($FFFFD6CC).w
0FF874  jsr	sub_FE556
0FF87A  bra.s	loc_FF85E
```

## `$0F6778` -> `ai_LaunchPass`  (confidence 0.6, 31 insns)

**Evidence.** passmode: pass speed = sqrt(12 * $D418) (sroot) into puckvz, flight time = speed / 3, then sets puckvx/puckvy = (target $D414/$D416 - puckx/pucky) / time and flips the puck with puckflip; caller passmode after ai_ComputePassTarget

**Callers.** passmode
**Callees.** puckflip, sroot
**RAM.** puckvx, puckvy, puckvz, puckx, pucky

```
0F6778  movem.l	d0-a6,-(sp)
0F677C  move.w	#$C,d0
0F6780  move.w	($FFFFD418).w,d1
0F6784  mulu.w	d1,d0
0F6786  swap	d0
0F6788  and.l	#$FFFF0000,d0
0F678E  jsr	sub_110BE
0F6794  move.w	d0,($FFFFB776).w
0F6798  ext.l	d0
0F679A  move.w	#3,d4
0F679E  divu.w	d4,d0
0F67A0  clr.l	d1
0F67A2  move.w	($FFFFD414).w,d1
0F67A6  sub.w	($FFFFB74A).w,d1
0F67AA  swap	d1
0F67AC  tst.w	d0
0F67AE  bne.w	loc_F67B6
0F67B2  move.w	#1,d0
0F67B6  divs.w	d0,d1
0F67B8  move.w	d1,($FFFFB772).w
0F67BC  clr.l	d1
0F67BE  move.w	($FFFFD416).w,d1
0F67C2  sub.w	($FFFFB75E).w,d1
0F67C6  swap	d1
0F67C8  divs.w	d0,d1
0F67CA  move.w	d1,($FFFFB774).w
0F67CE  move.l	#$FFFFB74A,a3
0F67D4  move.w	($FFFFB776).w,d0
0F67D8  jsr	sub_102D2
0F67DE  movem.l	(sp)+,d0-a6
0F67E2  rts
```

## `$0FE864` -> `ai_SteerToWaypoint`  (confidence 0.5, 36 insns)

**Evidence.** asspuckc helper: returns the current waypoint ($DA16/$DA18, flipped for the player's side) in d0/d1 and, when the player object a3 is within $12 (or $A while moving, $28/$2A non-zero) of it in both axes, advances the script with ai_NextWaypoint; caller asspuckc

**Callers.** asspuckc
**Callees.** ai_NextWaypoint

```
0FE864  movem.l	d2-a6,-(sp)
0FE868  cmp.b	#$80,($FFFFDA16).w
0FE86E  beq.w	loc_FE8E6
0FE872  move.w	($FFFFDA16).w,d0
0FE876  move.w	($FFFFDA18).w,d1
0FE87A  btst	#7,$62(a3)
0FE880  bne.w	loc_FE888
0FE884  neg.w	d0
0FE886  neg.w	d1
0FE888  sub.w	(a3),d0
0FE88A  bpl.w	loc_FE890
0FE88E  neg.w	d0
0FE890  tst.w	$28(a3)
0FE894  bne.w	loc_FE8A8
0FE898  tst.w	$2A(a3)
0FE89C  bne.w	loc_FE8A8
0FE8A0  cmpnw	 $12,d0
0FE8A4  ble.w	loc_FE8B0
0FE8A8  cmpnw	 $A,d0
0FE8AC  bgt.w	loc_FE8DE
0FE8B0  sub.w	$14(a3),d1
0FE8B4  bpl.w	loc_FE8BA
0FE8B8  neg.w	d1
0FE8BA  tst.w	$28(a3)
0FE8BE  bne.w	loc_FE8D2
0FE8C2  tst.w	$2A(a3)
0FE8C6  bne.w	loc_FE8D2
0FE8CA  cmpnw	 $12,d1
0FE8CE  ble.w	loc_FE8DA
0FE8D2  cmpnw	 $A,d1
0FE8D6  bgt.w	loc_FE8DE
0FE8DA  bsr.w	sub_FE7FC
0FE8DE  move.w	($FFFFDA16).w,d0
0FE8E2  move.w	($FFFFDA18).w,d1
0FE8E6  movem.l	(sp)+,d2-a6
0FE8EA  rts
```

## `$01A470` -> `ai_ReadPad1Hardware`  (confidence 0.7, 31 insns)

**Evidence.** reads controller port 1 ($A10003) with the Z80 bus held (retrying with Z80_ResetAndRequestBus after $64 polls): TH low then high, packs Start/A from the first read and the directions/B/C from the second, remaps the direction nibble through byte_1A4DE and returns the inverted button byte in d0; caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** ai_Z80_ResetAndRequestBus
**Hardware.** Z80 busreq, pad1

```
01A470  movem.l	d1/a0,-(sp)
01A474  lea	($A10003).l,a0
01A47A  move.w	#$100,($A11100).l
01A482  move.w	#$64,d0
01A486  btst	#0,($A11100).l
01A48E  beq.s	loc_1A498
01A490  dbf	d0,loc_1A486
01A494  bsr.w	sub_1A4EE
01A498  moveq	#0,d0
01A49A  move.b	#0,(a0)
01A49E  nop
01A4A0  nop
01A4A2  move.b	(a0),d0
01A4A4  move.b	#$40,(a0)
01A4A8  nop
01A4AA  nop
01A4AC  move.b	(a0),d1
01A4AE  move.w	#0,($A11100).l
01A4B6  asl.b	#2,d0
01A4B8  and.b	#$C0,d0
01A4BC  and.b	#$3F,d1
01A4C0  or.b	d1,d0
01A4C2  not.b	d0
01A4C4  not.b	d1
01A4C6  and.w	#$F,d1
01A4CA  lea	byte_1A4DE(pc),a0
01A4CE  and.b	#$F0,d0
01A4D2  or.b	(a0,d1.w),d0
01A4D6  not.b	d0
01A4D8  movem.l	(sp)+,d1/a0
01A4DC  rts
```

