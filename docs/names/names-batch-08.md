# Name review: names-batch-08.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0F9CDE` -> `ai_UpdateGameRecords`  (confidence 0.7, 60 insns)

**Evidence.** Intermission hook, skipped unless ValidSRAM and OptUserRec is off: caches both rosters' attribute counts and sizes (sub_F9FC0/sub_F9FEA), then for the home and away sides updates the per-team records (sub_F9F50 for the scorer fields, ai_UpdateTeamRecords), the user records for the two controllers ($D042/$D044) via ai_UpdateUserWinLoss, and finally sub_1A206; all record I/O goes through the SRAM record helpers with $CF36 as the 16-byte scratch record

**Callers.** Intermission
**Callees.** MakeSRAMChecksum, ai_UpdateTeamRecords, ai_UpdateUserWinLoss, sub_F9F50, sub_F9FC0, sub_F9FEA
**RAM.** HomeTeam, OptUserRec, ValidSRAM, VisTeam

```
0F9CDE  tst.w	($FFFFD458).w
0F9CE2  bmi.w	locret_F9DD8
0F9CE6  tst.w	($FFFFD054).w
0F9CEA  bne.w	locret_F9DD8
0F9CEE  movem.l	d0-a6,-(sp)
0F9CF2  bsr.w	sub_F9FC0
0F9CF6  bsr.w	sub_F9FEA
0F9CFA  move.w	($FFFFC330).w,d1
0F9CFE  ext.l	d1
0F9D00  move.l	#$FFFFCF36,a0
0F9D06  move.l	#$FFFFC6CE,a2
0F9D0C  move.w	($FFFFD448).w,d5
0F9D10  move.w	($FFFFC332).w,d6
0F9D14  bsr.w	sub_F9F50
0F9D18  move.w	($FFFFC332).w,d1
0F9D1C  ext.l	d1
0F9D1E  move.l	#$FFFFCA32,a2
0F9D24  move.w	($FFFFD44A).w,d5
0F9D28  move.w	($FFFFC330).w,d6
0F9D2C  bsr.w	sub_F9F50
0F9D30  clr.w	d7
0F9D32  move.l	#$FFFFC6CE,a1
0F9D38  move.w	($FFFFD042).w,d4
0F9D3C  move.w	($FFFFD044).w,d5
0F9D40  move.w	($FFFFC330).w,d1
0F9D44  move.w	($FFFFC332).w,d2
0F9D48  move.w	($FFFFD448).w,d6
0F9D4C  ext.l	d1
0F9D4E  move.l	#$FFFFCF36,a0
0F9D54  bsr.w	sub_F9EAA
0F9D58  move.l	#$FFFFCA32,a1
0F9D5E  move.w	($FFFFD044).w,d4
0F9D62  move.w	($FFFFD042).w,d5
0F9D66  move.w	($FFFFC332).w,d1
0F9D6A  move.w	($FFFFC330).w,d2
0F9D6E  move.w	($FFFFD44A).w,d6
0F9D72  ext.l	d1
0F9D74  move.l	#$FFFFCF36,a0
0F9D7A  bsr.w	sub_F9EAA
0F9D7E  move.l	#$FFFFCF36,a0
0F9D84  move.w	($FFFFD042).w,d1
0F9D88  ext.l	d1
0F9D8A  move.w	($FFFFD044).w,d2
0F9D8E  move.w	($FFFFC330).w,d3
0F9D92  move.w	($FFFFC332).w,d4
0F9D96  move.l	#$FFFFC6CE,a1
0F9D9C  move.l	#$FFFFCA32,a2
0F9DA2  bsr.w	sub_F9DDA
0F9DA6  move.l	#$FFFFCF36,a0
0F9DAC  move.w	($FFFFD044).w,d1
0F9DB0  ext.l	d1
0F9DB2  move.w	($FFFFD042).w,d2
0F9DB6  move.w	($FFFFC332).w,d3
0F9DBA  move.w	($FFFFC330).w,d4
0F9DBE  move.l	#$FFFFCA32,a1
0F9DC4  move.l	#$FFFFC6CE,a2
0F9DCA  bsr.w	sub_F9DDA
0F9DCE  jsr	sub_1A206
0F9DD4  movem.l	(sp)+,d0-a6
0F9DD8  rts
...
```

## `$0F9DDA` -> `ai_UpdateUserWinLoss`  (confidence 0.6, 62 insns)

**Evidence.** reads the user's 16-byte record from SRAM $D20 + user*16 (sub_F9C20) into a0: increments games played (+$A/+$B, capped at 9000) and, from the goal totals $C(a1) vs $C(a2), wins (+8/+9) or ties (+$C/+$D); then refreshes the best-goals (bytes 0..3) and best-margin (bytes 4..7) entries with the opponent team/user ids and writes the record back with sub_F9C56; caller ai_UpdateGameRecords for each side

**Callers.** ai_UpdateGameRecords
**Callees.** ai_ReadUserRecord, loc_F9E4C, sub_F9C56

```
0F9DDA  movem.l	d0-a6,-(sp)
0F9DDE  bsr.w	sub_F9C20
0F9DE2  st	d7
0F9DE4  movem.w	d0,-(sp)
0F9DE8  clr.w	d0
0F9DEA  move.b	$A(a0),d0
0F9DEE  lsl.w	#8,d0
0F9DF0  move.b	$B(a0),d0
0F9DF4  cmpnw	 $2328,d0
0F9DF8  bge.w	loc_F9E4C
0F9DFC  addq.w	#1,d0
0F9DFE  move.b	d0,$B(a0)
0F9E02  lsr.w	#8,d0
0F9E04  move.b	d0,$A(a0)
0F9E08  move.w	$C(a1),d0
0F9E0C  cmp.w	$C(a2),d0
0F9E10  bgt.w	loc_F9E34
0F9E14  blt.w	loc_F9E4C
0F9E18  clr.w	d0
0F9E1A  move.b	$C(a0),d0
0F9E1E  lsl.w	#8,d0
0F9E20  move.b	$D(a0),d0
0F9E24  addq.w	#1,d0
0F9E26  move.b	d0,$D(a0)
0F9E2A  lsr.w	#8,d0
0F9E2C  move.b	d0,$C(a0)
0F9E30  bra.w	loc_F9E4C
0F9E34  clr.w	d0
0F9E36  move.b	8(a0),d0
0F9E3A  lsl.w	#8,d0
0F9E3C  move.b	9(a0),d0
0F9E40  addq.w	#1,d0
0F9E42  move.b	d0,9(a0)
0F9E46  lsr.w	#8,d0
0F9E48  move.b	d0,8(a0)
0F9E4C  movem.w	(sp)+,d0
0F9E50  movem.w	d0,-(sp)
0F9E54  move.w	$C(a1),d0
0F9E58  cmp.w	$C(a2),d0
0F9E5C  movem.w	(sp)+,d0
0F9E60  ble.w	loc_F9EA0
0F9E64  move.w	$C(a1),d5
0F9E68  cmp.b	(a0),d5
0F9E6A  ble.w	loc_F9E7E
0F9E6E  st	d7
0F9E70  move.b	d5,(a0)
0F9E72  move.b	d3,1(a0)
0F9E76  move.b	d4,2(a0)
0F9E7A  move.b	d2,3(a0)
0F9E7E  move.w	$C(a2),d5
0F9E82  move.w	(a2),d6
0F9E84  sub.w	d5,d6
0F9E86  cmp.b	4(a0),d6
0F9E8A  ble.w	loc_F9EA0
0F9E8E  st	d7
0F9E90  move.b	d6,4(a0)
0F9E94  move.b	d3,5(a0)
0F9E98  move.b	d4,6(a0)
0F9E9C  move.b	d2,7(a0)
0F9EA0  bsr.w	sub_F9C56
...
```

## `$0F9EAA` -> `ai_UpdateTeamRecords`  (confidence 0.5, 46 insns)

**Evidence.** reads team d1's 16-byte record from SRAM $B60 + team*16 (ReadTeamRecord) and updates three entries when beaten: most goals in a game (bytes 0..3 from $C(a1)), best single-player goals-minus-... margin computed over the roster from the +$E8 and +$B4 stat columns (bytes 4..7), and for the home team the loudest crowd CrowdPeak (bytes 8..$B); writes back with sub_F9C18 when anything changed; caller ai_UpdateGameRecords

**Callers.** ai_UpdateGameRecords
**Callees.** ReadTeamRecord, ai_WriteTeamRecord
**RAM.** CrowdPeak, HomeTeam

```
0F9EAA  movem.l	d0-a6,-(sp)
0F9EAE  bsr.w	sub_F9BE2
0F9EB2  move.w	$C(a1),d3
0F9EB6  cmp.b	(a0),d3
0F9EB8  ble.w	loc_F9ECC
0F9EBC  move.b	d3,(a0)
0F9EBE  move.b	d4,1(a0)
0F9EC2  move.b	d5,3(a0)
0F9EC6  move.b	d2,2(a0)
0F9ECA  st	d7
0F9ECC  subq.w	#1,d6
0F9ECE  clr.w	d3
0F9ED0  move.w	d6,d0
0F9ED2  add.w	#$E8,d0
0F9ED6  move.b	(a1,d0.w),($FFFFBF12).w
0F9EDC  add.w	#-$34,d0
0F9EE0  move.b	(a1,d0.w),d0
0F9EE4  sub.b	d0,($FFFFBF12).w
0F9EE8  cmp.b	($FFFFBF12).w,d3
0F9EEC  bge.w	loc_F9EF4
0F9EF0  move.b	($FFFFBF12).w,d3
0F9EF4  dbf	d6,loc_F9ED0
0F9EF8  cmp.b	4(a0),d3
0F9EFC  ble.w	loc_F9F12
0F9F00  st	d7
0F9F02  move.b	d3,4(a0)
0F9F06  move.b	d4,5(a0)
0F9F0A  move.b	d5,7(a0)
0F9F0E  move.b	d2,6(a0)
0F9F12  cmp.w	($FFFFC330).w,d1
0F9F16  bne.w	loc_F9F40
0F9F1A  move.b	8(a0),d3
0F9F1E  and.w	#$FF,d3
0F9F22  cmp.w	($FFFFC314).w,d3
0F9F26  bge.w	loc_F9F40
0F9F2A  move.w	($FFFFC314).w,d3
0F9F2E  st	d7
0F9F30  move.b	d3,8(a0)
0F9F34  move.b	d4,9(a0)
0F9F38  move.b	d5,$B(a0)
0F9F3C  move.b	d2,$A(a0)
0F9F40  tst.w	d7
0F9F42  beq.w	loc_F9F4A
0F9F46  bsr.w	sub_F9C18
0F9F4A  movem.l	(sp)+,d0-a6
0F9F4E  rts
```

## `$0F9C18` -> `ai_WriteTeamRecord`  (confidence 0.8, 2 insns)

**Evidence.** sets the SRAM write flag $C2F8 bit 6 and jumps into the shared body of ReadTeamRecord (which is really the team-record reader: SRAM $B60 + team*16, 16 bytes), so the flag selects WriteSRAM; caller ai_UpdateTeamRecords

**Callers.** ai_UpdateTeamRecords
**Callees.** loc_F9BE8

```
0F9C18  bset	#6,($FFFFC2F8).w
0F9C1E  bra.s	loc_F9BE8
```

## `$0F9C20` -> `ai_ReadUserRecord`  (confidence 0.7, 13 insns)

**Evidence.** clears the write flag and transfers 16 bytes between SRAM $D20 + d1*16 and a0 (always ReadSRAM from this entry; sub_F9C56 is the writing twin that sets the flag first); caller ai_UpdateUserWinLoss

**Callers.** ai_UpdateUserWinLoss
**Callees.** ReadSRAM, WriteSRAM, loc_F9C50

```
0F9C20  bclr	#6,($FFFFC2F8).w
0F9C26  movem.l	d0-d1/a0-a1,-(sp)
0F9C2A  move.l	d1,d0
0F9C2C  asl.w	#4,d0
0F9C2E  add.l	#$D20,d0
0F9C34  moveq	#$10,d1
0F9C36  btst	#6,($FFFFC2F8).w
0F9C3C  beq.w	loc_F9C4A
0F9C40  jsr	sub_1A1E4
0F9C46  bra.w	loc_F9C50
0F9C4A  jsr	sub_1A244
0F9C50  movem.l	(sp)+,d0-d1/a0-a1
0F9C54  rts
```

## `$0FA550` -> `ai_PrintRecordsScreen`  (confidence 0.7, 59 insns)

**Evidence.** records screen: draws both team logos with sub_FA66E at columns $21 and 1, the team name box (sub_FAC3E), the records grid (loc_FA936), ai_PrintTeamRatingBox, the 'Records' / '-----------' heading at column $15, then reads the selected team's record (ReadTeamRecord with $D4F6 choosing home or away) and prints its lines with ai_PrintGoalRecordLine; caller sub_FA2C0

**Callers.** sub_FA2C0
**Callees.** ReadTeamRecord, ai_PrintGoalRecordLine, ai_PrintTeamRatingBox, loc_FA936, printz, printz2, sub_FA66E, sub_FA6E8, sub_FA708, sub_FAC3E
**Strings.** Records | -----------
**RAM.** HomeTeam, VisTeam, palcount, printx, printy

```
0FA550  movem.l	d0-a6,-(sp)
0FA554  move.w	#$21,d0
0FA558  move.w	#8,d1
0FA55C  jsr	sub_FA66E
0FA562  move.w	#1,d0
0FA566  move.w	#8,d1
0FA56A  bset	#0,($FFFFC2F8).w
0FA570  jsr	sub_FA66E
0FA576  bclr	#0,($FFFFC2F8).w
0FA57C  move.w	#$64,($FFFFBD26).w
0FA582  jsr	sub_11B92
0FA588  dc.w	6
0FA58A  dc.b	$BE
0FA58B  dc.b	0
0FA58C  dc.b	0
0FA58D  dc.b	0
0FA58E  move.w	#8,d1
0FA592  jsr	sub_FAC3E
0FA598  move.w	#3,d0
0FA59C  move.w	#$F,d1
0FA5A0  jsr	loc_FA936
0FA5A6  move.w	#8,d0
0FA5AA  move.w	#$B,d1
0FA5AE  jsr	sub_FABDC
0FA5B4  move.w	#$15,($FFFFB028).w
0FA5BA  move.w	#$C,($FFFFB02A).w
0FA5C0  move.w	($FFFFB028).w,-(sp)
0FA5C4  jsr	sub_11A36
0FA5CA  dc.w	$C
0FA5CC  aRecords_0:	dc.b	'  Records',0
0FA5D6  move.w	(sp)+,($FFFFB028).w
0FA5DA  addq.w	#1,($FFFFB02A).w
0FA5DE  jsr	sub_11A36
0FA5E4  dc.w	$E
0FA5E6  dc.b	'-----------',0
0FA5F2  move.w	($FFFFC330).w,d1
0FA5F6  tst.w	($FFFFD4F6).w
0FA5FA  beq.w	loc_FA602
0FA5FE  move.w	($FFFFC332).w,d1
0FA602  ext.l	d1
0FA604  move.l	#$FFFFCF36,a0
0FA60A  move.l	a0,-(sp)
0FA60C  jsr	sub_F9BE2
0FA612  move.w	#$15,d0
0FA616  move.w	#$E,d1
0FA61A  move.b	(a0),d2
0FA61C  move.b	1(a0),d3
0FA620  move.b	3(a0),d4
0FA624  move.b	2(a0),d5
0FA628  bsr.w	sub_FA75C
0FA62C  move.l	(sp),a0
0FA62E  move.w	#$15,d0
0FA632  move.w	#$12,d1
0FA636  move.b	4(a0),d2
0FA63A  move.b	5(a0),d3
0FA63E  move.b	7(a0),d4
0FA642  move.b	6(a0),d5
0FA646  bsr.w	sub_FA708
0FA64A  move.l	(sp)+,a0
0FA64C  move.w	#$15,d0
...
```

## `$0FA75C` -> `ai_PrintGoalRecordLine`  (confidence 0.6, 57 insns)

**Evidence.** prints one record entry: chooses ' Goals ' / ' Goal ' (d3 = 0) or ' Goals by' / ' Goal by' (d3 != 0, plural when d2 != 1), builds the number (NumberToDecimalText) + label + user name (ai_BuildUserNameString with $C2F8 bit 7 for trimming) + 'vs.' + team name in $BFA4 and prints it at (d0,d1); caller ai_PrintRecordsScreen

**Callers.** ai_PrintRecordsScreen
**Callees.** ai_AppendTeamName, ai_BuildUserNameString, ai_NumberToDecimalText, appstring, loc_FA7B0, print2
**Strings.** Goals | Goal | Goals by | Goal by | vs.
**RAM.** TempMaxSpd, printx, printy

```
0FA75C  movem.l	a1-a3,-(sp)
0FA760  move.l	#word_FA788,a1
0FA766  tst.w	d3
0FA768  beq.w	loc_FA772
0FA76C  move.l	#word_FA79A,a1
0FA772  cmpnb	 1,d2
0FA776  bne.w	loc_FA77C
0FA77A  add.w	(a1),a1
0FA77C  move.l	a1,($FFFFBF18).w
0FA780  movem.l	(sp)+,a1-a3
0FA784  bra.w	loc_FA7B0
0FA788  word_FA788:	dc.w	$A
0FA78A  aGoals_1:	dc.b	' Goals ',0
0FA792  dc.w	8
0FA794  aGoal_1:	dc.b	' Goal '
0FA79A  word_FA79A:	dc.w	$C
0FA79C  aGoalsBy:	dc.b	' Goals by',0
0FA7A6  dc.w	$A
0FA7A8  aGoalBy:	dc.b	' Goal by'
0FA7B0  tst.b	d2
0FA7B2  bne.w	loc_FA7B8
0FA7B6  rts
0FA7B8  move.w	d0,($FFFFB028).w
0FA7BC  move.w	d1,($FFFFB02A).w
0FA7C0  move.w	d2,d0
0FA7C2  and.w	#$FF,d0
0FA7C6  move.l	#$FFFFBFA4,a1
0FA7CC  move.l	a1,-(sp)
0FA7CE  jsr	sub_F998E
0FA7D4  move.l	(sp)+,a1
0FA7D6  move.l	a1,a3
0FA7D8  move.l	($FFFFBF18).w,a1
0FA7DC  jsr	sub_11D9E
0FA7E2  move.w	($FFFFB028).w,-(sp)
0FA7E6  move.l	#$FFFFBFA4,a1
0FA7EC  jsr	sub_11A48
0FA7F2  move.w	(sp)+,($FFFFB028).w
0FA7F6  addq.w	#1,($FFFFB02A).w
0FA7FA  move.l	#$FFFFBFA4,a1
0FA800  move.w	d3,d2
0FA802  ext.w	d2
0FA804  bset	#7,($FFFFC2F8).w
0FA80A  jsr	sub_FA014
0FA810  move.l	a1,a3
0FA812  move.l	#word_FA876,a1
0FA818  jsr	sub_11D9E
0FA81E  move.w	($FFFFB028).w,-(sp)
0FA822  move.l	#$FFFFBFA4,a1
0FA828  jsr	sub_11A48
0FA82E  move.w	(sp)+,($FFFFB028).w
0FA832  addq.w	#1,($FFFFB02A).w
0FA836  move.w	d4,d2
0FA838  ext.w	d2
0FA83A  move.l	#$FFFFBFA4,a1
0FA840  bset	#7,($FFFFC2F8).w
0FA846  jsr	sub_FA014
0FA84C  move.l	a1,a3
0FA84E  move.l	#word_FA87C,a1
0FA854  jsr	sub_11D9E
0FA85A  move.w	d5,d0
...
```

## `$01850A` -> `ai_StarsOfTheGameScreen`  (confidence 0.8, 47 insns)

**Evidence.** post-game 'Stars of the Game' panel: once RefCnt is above $40 and $C2EA bit 7 was clear, waits a frame, draws a 28x9 box, prints the title, draws the star bitmap from off_5605A at tile base $B018, scores every player with sub_18620 / ai_ScorePlayerForStars and prints the three stars with sub_185E0; caller UpdatePA

**Callers.** UpdatePA
**Callees.** Framer, dobitmap, getname, print, printz, song, sub_185E0, sub_18620
**Strings.** Stars of the Game
**RAM.** AwGoals, HmGoals, RefCnt, disflags, gmode, printx, printy, rinkvrcset, vcount

```
01850A  cmp.w	#$40,($FFFFC3F0).w
018510  bgt.w	locret_15464
018514  bset	#7,($FFFFC2EA).w
01851A  bne.w	locret_15464
01851E  movem.l	d0/a1,-(sp)
018522  bset	#3,($FFFFBF78).w
018528  move.w	($FFFFB03E).w,d0
01852C  cmp.w	($FFFFB03E).w,d0
018530  beq.s	loc_1852C
018532  movem.l	(sp)+,d0/a1
018536  movem.l	d0-d5/a0-a4,-(sp)
01853A  bsr.w	sub_11B92
01853E  dc.w	6
018540  dc.b	$BF
018541  dc.b	2
018542  dc.b	$E
018543  dc.b	0
018544  moveq	#$1C,d0
018546  moveq	#9,d1
018548  bsr.w	sub_119B8
01854C  bsr.w	sub_11B92
018550  dc.w	$1A
018552  dc.b	$BF
018553  dc.b	9
018554  dc.b	$10
018555  aStarsOfTheGame: dc.b	'Stars of the Game'
018566  dc.b	$BF
018567  dc.b	3
018568  dc.b	$F
018569  dc.b	0
01856A  move.l	#off_5605A,a1
018570  move.w	#$30A,a2
018574  add.l	4(a1),a1
018578  moveq	#$D,d0
01857A  moveq	#$5B,d1
01857C  moveq	#6,d2
01857E  moveq	#4,d3
018580  move.w	($FFFFB018).w,d4
018584  clr.w	d5
018586  bsr.w	sub_1169A
01858A  bsr.w	sub_18620
01858E  move.w	#$12,($FFFFB02A).w
018594  moveq	#2,d2
018596  bsr.w	sub_185E0
01859A  move.w	#$1A,($FFFFB028).w
0185A0  addq.w	#1,($FFFFB02A).w
0185A4  move.l	$1E(a2),a1
0185A8  add.w	4(a1),a1
0185AC  add.w	(a1),a1
0185AE  bsr.w	sub_11BA4
0185B2  bsr.w	sub_18A90
0185B6  move.w	#3,($FFFFB028).w
0185BC  bsr.w	sub_11BA4
0185C0  dbf	d2,loc_18596
0185C4  move.w	($FFFFC6DA).w,d0
0185C8  sub.w	($FFFFCA3E).w,d0
0185CC  ble.w	loc_185DA
0185D0  move.w	#$F,-(sp)
0185D4  jsr	sub_11156
0185DA  movem.l	(sp)+,d0-d5/a0-a4
...
```

## `$01867E` -> `ai_ScorePlayerForStars`  (confidence 0.6, 50 insns)

**Evidence.** computes a player's star-of-the-game value into (a4): base = team score difference (d3), then for skaters goals (+$B4 column) * $2AF8, assists (+$CE) * $2774, shots (+$E8) * 10 (* 100 more for a losing side) plus the +$136 rating; for the goalie slot (index above the attribute count) awards $7D00 when the save percentage is high and $124F8 more for a shutout; caller sub_18620 (from ai_StarsOfTheGameScreen)

**Callers.** sub_18620
**Callees.** ai_CountRatingNibbles, loc_18710
**Strings.** Injury to: | Out for period | Injury to: | Out for game | the game

```
01867E  move.w	a2,a1
018680  move.w	$C(a2),d3
018684  sub.w	$C(a3),d3
018688  ext.l	d3
01868A  moveq	#$19,d4
01868C  jsr	sub_9F40
018692  neg.w	d0
018694  add.w	d4,d0
018696  move.l	d3,(a4)
018698  cmp.w	d0,d4
01869A  bhi.w	loc_186D8
01869E  clr.w	d1
0186A0  move.b	$B4(a2),d1
0186A4  mulu.w	#$2AF8,d1
0186A8  add.l	d1,(a4)
0186AA  clr.w	d1
0186AC  move.b	$CE(a2),d1
0186B0  mulu.w	#$2774,d1
0186B4  add.l	d1,(a4)
0186B6  clr.w	d1
0186B8  move.b	$E8(a2),d1
0186BC  mulu.w	#$A,d1
0186C0  tst.w	d3
0186C2  bne.w	loc_186D2
0186C6  mulu.w	#$64,d1
0186CA  add.l	d1,(a4)
0186CC  clr.l	d1
0186CE  add.w	$136(a1),d1
0186D2  add.l	d1,(a4)
0186D4  bra.w	loc_18710
0186D8  cmp.w	$136(a1),d5
0186DC  bhi.w	loc_18710
0186E0  clr.w	d1
0186E2  move.b	$B4(a2),d1
0186E6  mulu.w	#$64,d1
0186EA  clr.w	d2
0186EC  move.b	$E8(a2),d2
0186F0  beq.w	loc_18710
0186F4  divu.w	d2,d1
0186F6  cmpnw	 4,d1
0186FA  bhi.w	loc_18710
0186FE  add.l	#$7D00,(a4)
018704  tst.w	d1
018706  bne.w	loc_18710
01870A  add.l	#$124F8,(a4)
018710  addq.w	#2,a1
018712  addq.w	#1,a2
018714  addq.w	#4,a4
018716  dbf	d4,loc_18696
01871A  rts
```

## `$0FF8DE` -> `ai_DrawBestWorstPlayerIcon`  (confidence 0.6, 48 insns)

**Evidence.** if the player $DEE8 is the first (best) entry of the team's rating-sorted list $BF5C/$BF5E draws the bitmap unk_F5AF6 at tile base $DEE4, if he is the first of the reverse (worst) list $BF60/$BF62 draws unk_F5D1C at $DEE6, otherwise erases the 8x3 area; column 2 for the away record, $20 for home, row $19; caller sub_FD89A (per-position ratings)

**Callers.** sub_FD89A
**Callees.** dobitmap, eraser, loc_FF978, loc_FF9A2
**RAM.** printx, printy

```
0FF8DE  movem.l	d0/a0-a1,-(sp)
0FF8E2  move.l	#$FFFFBF5C,a0
0FF8E8  move.w	#2,($FFFFDEEA).w
0FF8EE  cmp.l	#$FFFFC6CE,a2
0FF8F4  bne.w	loc_FF904
0FF8F8  move.l	#$FFFFBF5E,a0
0FF8FE  move.w	#$20,($FFFFDEEA).w
0FF904  move.w	#0,d0
0FF908  move.w	(a0)+,d1
0FF90A  cmp.w	($FFFFDEE8).w,d1
0FF90E  beq.w	loc_FF960
0FF912  dbf	d0,loc_FF908
0FF916  move.l	#$FFFFBF60,a0
0FF91C  cmp.l	#$FFFFC6CE,a2
0FF922  bne.w	loc_FF92C
0FF926  move.l	#$FFFFBF62,a0
0FF92C  move.w	#0,d0
0FF930  move.w	(a0)+,d1
0FF932  cmp.w	($FFFFDEE8).w,d1
0FF936  beq.w	loc_FF96E
0FF93A  dbf	d0,loc_FF930
0FF93E  move.w	($FFFFDEEA).w,($FFFFB028).w
0FF944  move.w	#$19,($FFFFB02A).w
0FF94A  move.w	#8,d0
0FF94E  move.w	#3,d1
0FF952  move.w	#$7FF,d2
0FF956  jsr	sub_1197E
0FF95C  bra.w	loc_FF9A2
0FF960  move.w	($FFFFDEE4).w,d4
0FF964  move.l	#unk_F5AF6,a0
0FF96A  bra.w	loc_FF978
0FF96E  move.w	($FFFFDEE6).w,d4
0FF972  move.l	#unk_F5D1C,a0
0FF978  move.w	($FFFFDEEA).w,($FFFFB028).w
0FF97E  move.w	#$19,($FFFFB02A).w
0FF984  move.l	a0,a1
0FF986  move.l	a0,a2
0FF988  add.l	(a2)+,a0
0FF98A  add.l	(a2)+,a1
0FF98C  move.w	#$30A,a2
0FF990  clr.w	d0
0FF992  clr.w	d1
0FF994  move.w	(a1),d2
0FF996  move.w	2(a1),d3
0FF99A  moveq	#0,d5
0FF99C  jsr	sub_1169A
0FF9A2  movem.l	(sp)+,d0/a0-a1
0FF9A6  rts
```

## `$01354C` -> `ai_PlayHighlightFromGame`  (confidence 0.6, 43 insns)

**Evidence.** sets up a stored playoff game as a highlight: after sub_13848/sub_13396/sub_133B2, draws a 24x3 box and prints 'Highlight from game:', waits $B4 frames (abort on button bit 7), then loads HomeTeam/VisTeam, the period gsp, HmGoals/AwGoals and a random clock (gameclock = $3C + random 0..$77) from the series record a0, clears the controller teams and reinitialises the teams (sub_17102, sub_77F4); caller sub_1351C, which runs it for every finished series flagged in $CE66..$CED6 bit 1 of +$E

**Callers.** sub_1351C
**Callees.** Framer, NewTicker3, NewTicker3pt2, clearTeamStats, printz, randomd0, sub_13848, waitxsr
**Strings.** Highlight from game:
**RAM.** AwGoals, CwdExciteLvl, HmGoals, HomeTeam, VisTeam, c1playernum, c2playernum, cont1team, cont2team, gameclock, gsp, printx, printy, sflags3, zamx

```
01354C  movem.l	d0-a6,-(sp)
013550  btst	#3,($FFFFC2F0).w
013556  bne.w	loc_137F6
01355A  bsr.w	sub_13848
01355E  move.w	d1,d3
013560  bsr.w	sub_13396
013564  bsr.w	sub_133B2
013568  btst	#3,($FFFFC2F0).w
01356E  bne.w	loc_137EC
013572  move.w	#4,($FFFFB028).w
013578  subq.w	#6,($FFFFB02A).w
01357C  moveq	#$18,d0
01357E  moveq	#3,d1
013580  bsr.w	sub_119B8
013584  addq.w	#1,($FFFFB028).w
013588  subq.w	#2,($FFFFB02A).w
01358C  bsr.w	sub_11B92
013590  dc.w	$16
013592  aHighlightFromGame: dc.b 'Highlight from game:'
0135A6  move.w	#$B4,d0
0135AA  bsr.w	sub_111D0
0135AE  btst	#7,d1
0135B2  bne.w	loc_137EC
0135B6  st	($FFFFB8AC).w
0135BA  clr.w	($FFFFB8A2).w
0135BE  move.w	(a0),($FFFFC330).w
0135C2  move.w	2(a0),($FFFFC332).w
0135C8  move.l	a0,-(sp)
0135CA  clr.w	($FFFFC6F4).w
0135CE  clr.w	($FFFFCA58).w
0135D2  jsr	sub_17102
0135D8  jsr	(sub_77F4).w
0135DC  st	($FFFFC320).w
0135E0  st	($FFFFC322).w
0135E4  clr.w	($FFFFC328).w
0135E8  clr.w	($FFFFC32A).w
0135EC  moveq	#$78,d0
0135EE  bsr.w	sub_11086
0135F2  add.w	#$3C,d0
0135F6  move.w	d0,($FFFFC468).w
0135FA  move.l	(sp),a0
0135FC  move.w	8(a0),($FFFFC466).w
013602  subq.w	#1,($FFFFC466).w
013606  move.w	$A(a0),($FFFFC6DA).w
01360C  move.w	$C(a0),($FFFFCA3E).w
```

## `$0164D6` -> `ai_PlaceOffscreenIndicator`  (confidence 0.5, 62 insns)

**Evidence.** checksso helper for the player-indicator sprites (tiles $180/$183): a0 = indicator record, a3 = its sprite slot; when the tracked object is on-screen returns, otherwise classifies which edges of the camera window ($74/-$74 by $64/-$64 around Hpos/Vpos, or fixed bounds on the menu screen) the object lies beyond, converts that to a direction with unk_113C0 and places the sprite at the edge position from word_165BC (+$100/+$F0 screen offsets) before tail-calling sub_167AA; caller checksso

**Callers.** checksso
**Callees.** addframe2, loc_1653C
**RAM.** BA_PS_flags, Hpos, Vpos, sflags, sflags2

```
0164D6  tst.w	$18(a0)
0164DA  bmi.w	locret_15464
0164DE  st	6(a3)
0164E2  move.w	(a0),d0
0164E4  btst	#0,($FFFFC2FA).w
0164EA  bne.w	loc_16502
0164EE  btst	#3,($FFFFC2EE).w
0164F4  bne.w	loc_16502
0164F8  btst	#2,($FFFFC2F2).w
0164FE  beq.w	loc_1651A
016502  move.w	d0,-(sp)
016504  tst.w	d0
016506  bpl.w	loc_1650C
01650A  neg.w	d0
01650C  cmpnw	 $A6,d0
016510  blt.w	loc_16518
016514  move.w	(sp)+,d0
016516  rts
016518  move.w	(sp)+,d0
01651A  move.w	$14(a0),d1
01651E  btst	#7,($FFFFC2EC).w
016524  beq.w	loc_16534
016528  exg	d0,d1
01652A  neg.w	d0
01652C  sub.w	#$C5,d1
016530  bra.w	loc_1653C
016534  sub.w	($FFFFBD1C).w,d0
016538  sub.w	($FFFFBD18).w,d1
01653C  clr.w	d2
01653E  cmpnw	 $74,d0
016542  blt.w	loc_1654A
016546  bset	#3,d2
01654A  cmpnw	 $FF8C,d0
01654E  bgt.w	loc_16556
016552  bset	#2,d2
016556  cmpnw	 $64,d1
01655A  blt.w	loc_16562
01655E  bset	#0,d2
016562  cmpnw	 $FF9C,d1
016566  bgt.w	loc_1656E
01656A  bset	#1,d2
01656E  tst.w	d2
016570  beq.w	locret_15464
016574  move.l	#unk_113C0,a1
01657A  move.b	(a1,d2.w),d2
01657E  asl.w	#3,d2
016580  move.l	#word_165BC,a1
016586  move.w	(a1,d2.w),d4
01658A  beq.w	loc_16590
01658E  move.w	d4,d0
016590  add.w	#$100,d0
016594  move.w	d0,(a3)
016596  move.w	2(a1,d2.w),d4
01659A  beq.w	loc_165A0
01659E  move.w	d4,d1
0165A0  neg.w	d1
0165A2  add.w	#$F0,d1
0165A6  move.w	d1,2(a3)
0165AA  add.w	4(a1,d2.w),d3
0165AE  move.w	d3,6(a3)
...
```

## `$0FE8EC` -> `ai_WaypointScriptActive`  (confidence 0.4, 40 insns)

**Evidence.** asspuckc helper returning d0 = 0 (keep the script) or 1 (drop it): requires $C2FA bit 1, the player's $52(a3) state equal to puckc's $B7AA, $D454 above 3 and a live script ($DA16 != $80); with the end flag $C2FC bit 3 it checks the player is within $DA1C of the last point, otherwise it needs $B772/$B774 clear and $D454 >= $F

**Callers.** asspuckc
**Callees.** loc_FE980, loc_FE984
**RAM.** puckc, puckvx, puckvy

```
0FE8EC  movem.l	d0-a6,-(sp)
0FE8F0  btst	#1,($FFFFC2FA).w
0FE8F6  beq.w	loc_FE980
0FE8FA  move.w	$52(a3),d0
0FE8FE  cmp.w	($FFFFB7AA).w,d0
0FE902  bne.w	loc_FE980
0FE906  cmp.w	#3,($FFFFD454).w
0FE90C  ble.w	loc_FE97A
0FE910  cmp.b	#$80,($FFFFDA16).w
0FE916  beq.w	loc_FE97A
0FE91A  btst	#3,($FFFFC2FC).w
0FE920  bne.w	loc_FE942
0FE924  tst.w	($FFFFB772).w
0FE928  bne.w	loc_FE980
0FE92C  tst.w	($FFFFB774).w
0FE930  bne.w	loc_FE980
0FE934  cmp.w	#$F,($FFFFD454).w
0FE93A  blt.w	loc_FE97A
0FE93E  bra.w	loc_FE980
0FE942  move.w	($FFFFDA16).w,d0
0FE946  move.w	($FFFFDA18).w,d1
0FE94A  btst	#7,$62(a3)
0FE950  bne.w	loc_FE958
0FE954  neg.w	d0
0FE956  neg.w	d1
0FE958  sub.w	(a3),d0
0FE95A  bpl.w	loc_FE960
0FE95E  neg.w	d0
0FE960  sub.w	$14(a3),d1
0FE964  bpl.w	loc_FE96A
0FE968  neg.w	d1
0FE96A  cmp.w	($FFFFDA1C).w,d0
0FE96E  bgt.w	loc_FE980
0FE972  cmp.w	($FFFFDA1C).w,d1
0FE976  bgt.w	loc_FE980
0FE97A  clr.w	d0
0FE97C  bra.w	loc_FE984
0FE980  move.w	#1,d0
0FE984  movem.l	(sp)+,d0-a6
0FE988  rts
```

## `$009BD8` -> `ai_SetupStatsScreenVideo`  (confidence 0.5, 58 insns)

**Evidence.** loc_945C helper: after sub_10F32, resets the plane scroll (VDP address $B002 and 0 written as zero, registers $8C81/$8D00, $B00E = 6), loads the frame tiles (unk_55B86 at $B01E with nibble map $9123...) and the font (ai_LoadFontTiles), then draws the background bitmap off_54E24 with dobitmap; caller loc_945C (edit lines / stats screens)

**Callers.** loc_945C
**Callees.** Vmaddr, ai_LoadAssetInline, ai_LoadFontTiles, dobitmap, eraser, forceblack, printz
**RAM.** Map3col1, VSPRITES, disflags, framercset, palcount, printy

```
009BD8  movem.l	d0-d1/a2,-(sp)
009BDC  bsr.w	sub_10F32
009BE0  bclr	#0,($FFFFBF78).w
009BE6  move.w	($FFFFBF78).w,-(sp)
009BEA  bset	#2,($FFFFBF78).w
009BF0  move.w	($FFFFB002).w,d0
009BF4  bsr.w	VDP_SetAddress
009BF8  move.l	#0,(a0)
009BFE  move.w	#$8C81,4(a0)
009C04  move.w	#6,($FFFFB00E).w
009C0A  move.w	#$8D00,4(a0)
009C10  clr.w	d0
009C12  bsr.w	VDP_SetAddress
009C16  move.l	#0,(a0)
009C1C  move.w	(sp)+,($FFFFBF78).w
009C20  bclr	#1,($FFFFBF78).w
009C26  move.w	($FFFFB01E).w,d4
009C2A  move.l	#unk_55B86,a2
009C30  bsr.w	sub_1172C
009C34  dc.w	$9123
009C36  dc.w	$4567
009C38  dc.w	$89AB
009C3A  dc.w	$CDEF
009C3C  move.w	($FFFFB012).w,d4
009C40  jsr	sub_11F04
009C46  bsr.w	sub_11B92
009C4A  dc.w	6
009C4C  dc.b	$BD
009C4D  dc.b	0
009C4E  dc.b	0
009C4F  dc.b	0
009C50  move.l	#off_54E24,a1
009C56  add.l	4(a1),a1
009C5A  move.w	#$30A,a2
009C5E  clr.w	d0
009C60  clr.w	d1
009C62  move.w	(a1),d2
009C64  move.w	2(a1),d3
009C68  moveq	#1,d4
009C6A  moveq	#0,d5
009C6C  bsr.w	sub_1169A
009C70  bsr.w	sub_11B92
009C74  dc.w	6
009C76  dc.b	$FD
009C77  dc.b	0
009C78  dc.b	0
009C79  dc.b	0
009C7A  movem.l	(sp),d0-d1/a2
009C7E  add.w	d0,($FFFFB02A).w
009C82  move.l	#off_54E24,a0
009C88  move.l	a0,a1
009C8A  move.l	a0,a2
009C8C  add.l	(a2)+,a0
009C8E  add.l	(a2)+,a1
009C90  move.w	d1,d3
009C92  sub.w	d0,d3
009C94  move.w	d0,d1
009C96  clr.w	d0
009C98  moveq	#$28,d2
009C9A  moveq	#$D,d5
...
```

