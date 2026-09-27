# Name review: names-batch-11.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FD4CA` -> `ai_AnimateAdvantageBar`  (confidence 0.7, 26 insns)

**Evidence.** matchups screen: every 7 frames ($D5A6) advances the bar step $D5A4 (0..5) and prints, at column $13 row $16, the string step of off_FD548 (home overall $D5A0 above away $D5A2), off_FD560 (away ahead) or word_FD5A8 (equal); the strings are the ']', ']]', ']]]' / '[' bracket segments that grow toward the stronger team; caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** loc_FD524, print2, printz
**Strings.**  | ] | ]] | ]]] |  | [

```
0FD4CA  movem.l	d0-a6,-(sp)
0FD4CE  addq.w	#1,($FFFFD5A6).w
0FD4D2  cmp.w	#7,($FFFFD5A6).w
0FD4D8  blt.w	loc_FD4F4
0FD4DC  clr.w	($FFFFD5A6).w
0FD4E0  addq.w	#1,($FFFFD5A4).w
0FD4E4  cmp.w	#6,($FFFFD5A4).w
0FD4EA  blt.w	loc_FD4F4
0FD4EE  move.w	#5,($FFFFD5A4).w
0FD4F4  move.w	($FFFFD5A4).w,d1
0FD4F8  asl.w	#2,d1
0FD4FA  move.l	#off_FD548,a1
0FD500  move.w	($FFFFD5A0).w,d0
0FD504  cmp.w	($FFFFD5A2).w,d0
0FD508  bgt.w	loc_FD516
0FD50C  beq.w	loc_FD51E
0FD510  move.l	#off_FD560,a1
0FD516  move.l	(a1,d1.w),a1
0FD51A  bra.w	loc_FD524
0FD51E  move.l	#word_FD5A8,a1
0FD524  move.w	#2,($FFFFB030).w
0FD52A  jsr	sub_11B92
0FD530  dc.w	6
0FD532  dc.b	$FF
0FD533  dc.b	$13
0FD534  dc.b	$16
0FD535  dc.b	0
0FD536  jsr	sub_11A48
0FD53C  move.w	#0,($FFFFB030).w
0FD542  movem.l	(sp)+,d0-a6
0FD546  rts
```

## `$0FD89A` -> `ai_PrintRatingsPlayerName`  (confidence 0.6, 24 insns)

**Evidence.** per-position ratings entry: stores the player index in $DEE8, formats 'NN Surname' (ai_FormatPlayerNumberName), drops trailing zero bytes from the length, shifts printx left so the text ends before column $29, prints it and draws the best/worst icon (ai_DrawBestWorstPlayerIcon); caller ai_PrintTeamRatingsScreen

**Callers.** ai_PrintTeamRatingsScreen
**Callees.** ai_DrawBestWorstPlayerIcon, ai_FormatPlayerNumberName, print
**Strings.** . | Period Stats | OT¾ | Total | Total
**RAM.** printx

```
0FD89A  movem.l	d0-a6,-(sp)
0FD89E  move.w	d0,($FFFFDEE8).w
0FD8A2  move.l	a2,-(sp)
0FD8A4  jsr	sub_18B26
0FD8AA  move.l	a1,a0
0FD8AC  move.w	(a0),d0
0FD8AE  move.w	d0,d5
0FD8B0  tst.b	-1(a0,d5.w)
0FD8B4  bne.w	loc_FD8C4
0FD8B8  subq.w	#1,d0
0FD8BA  tst.b	-2(a0,d5.w)
0FD8BE  bne.w	loc_FD8C4
0FD8C2  subq.w	#1,d0
0FD8C4  add.w	($FFFFB028).w,d0
0FD8C8  sub.w	#$29,d0
0FD8CC  bmi.w	loc_FD8D6
0FD8D0  neg.w	d0
0FD8D2  add.w	d0,($FFFFB028).w
0FD8D6  move.l	a0,a1
0FD8D8  jsr	sub_11BA4
0FD8DE  move.l	(sp)+,a2
0FD8E0  jsr	sub_FF8DE
0FD8E6  movem.l	(sp)+,d0-a6
0FD8EA  rts
```

## `$00988E` -> `ai_GetPlayerStatValue`  (confidence 0.6, 24 insns)

**Evidence.** d0 = player index, d1 = stat column: for the regular stats (d7 = 0) reads the column's one or two byte offsets from unk_98FA and returns the sum of those roster bytes of team a2 in d2; for playoff stats (d7 != 0) sums two entries through sub_98CE and halves the result; caller ai_PrintPlayerStatRow

**Callers.** ai_PrintPlayerStatRow
**Callees.** ai_SumPlayoffStatColumn

```
00988E  tst.w	d7
009890  bne.w	loc_98BA
009894  lea	unk_98FA(pc),a1
009898  asl.w	#2,d1
00989A  add.w	d1,a1
00989C  move.w	(a1),d1
00989E  add.w	d0,d1
0098A0  clr.w	d2
0098A2  move.b	(a2,d1.w),d2
0098A6  move.w	2(a1),d1
0098AA  bmi.w	locret_A9D4
0098AE  add.w	d0,d1
0098B0  clr.w	d3
0098B2  move.b	(a2,d1.w),d3
0098B6  add.w	d3,d2
0098B8  rts
0098BA  asl.w	#2,d1
0098BC  add.w	d0,d0
0098BE  clr.w	d2
0098C0  bsr.w	sub_98CE
0098C4  addq.w	#2,d1
0098C6  bsr.w	sub_98CE
0098CA  lsr.w	#1,d0
0098CC  rts
```

## `$018620` -> `ai_ScoreAllPlayersForStars`  (confidence 0.7, 25 insns)

**Evidence.** scores every home and away player with ai_ScorePlayerForStars into the long array at $CF36 (period length from ClockLength plus d2), then, when the game ended in period 3 (gsp) with a non-zero margin, forces the game-winning-goal scorer (ScoreSum entry ChkCnt + ScoreSumbytes, +$1A for the away team) to $7FFFFFFF so he is the first star; caller ai_StarsOfTheGameScreen

**Callers.** ai_StarsOfTheGameScreen
**Callees.** ai_ScorePlayerForStars
**RAM.** ScoreSumbytes, gsp

```
018620  move.w	#$CF36,a4
018624  jsr	(sub_784E).w
018628  move.w	d0,d5
01862A  add.w	d2,d5
01862C  move.w	#$C6CE,a2
018630  lea	$364(a2),a3
018634  bsr.w	sub_1867E
018638  move.w	a3,a2
01863A  lea	-$364(a2),a3
01863E  bsr.w	sub_1867E
018642  cmp.w	#3,($FFFFC466).w
018648  bne.w	locret_1867C
01864C  tst.w	d3
01864E  beq.w	locret_1867C
018652  move.w	#$C46E,a0
018656  add.w	($FFFFC472).w,a0
01865A  clr.w	d0
01865C  btst	#7,2(a0)
018662  beq.w	loc_1866A
018666  add.w	#$1A,d0
01866A  add.b	3(a0),d0
01866E  asl.w	#2,d0
018670  move.w	#$CF36,a0
018674  move.l	#$7FFFFFFF,(a0,d0.w)
01867C  rts
```

## `$012E12` -> `ai_PrintPenaltyRow`  (confidence 0.6, 24 insns)

**Evidence.** penalty list line (only while printy <= $A): takes player d0's line-status word $66(a2,d0) & $7FF as the remaining time, finds his roster record (name part + 8 bytes) to print the jersey number (sub_18BDC into $BFA6), then the time with PushTime, and moves to the next row; caller sub_12DDE, which walks the penalized list $9A(a2)

**Callers.** ai_PrintPenaltyList
**Callees.** PushTime, d0toascii, print
**RAM.** printx, printy

```
012E12  cmp.w	#$A,($FFFFB02A).w
012E18  bhi.w	locret_15464
012E1C  move.w	$66(a2,d0.w),d2
012E20  and.w	#$7FF,d2
012E24  move.l	$1E(a2),a1
012E28  add.w	(a1),a1
012E2A  lsr.w	#1,d0
012E2C  add.w	(a1),a1
012E2E  addq.w	#8,a1
012E30  dbf	d0,loc_12E2C
012E34  clr.w	d0
012E36  move.b	-8(a1),d0
012E3A  move.w	($FFFFB028).w,-(sp)
012E3E  move.w	#$BFA6,a1
012E42  bsr.w	sub_18BDC
012E46  move.w	#$BFA4,a1
012E4A  move.w	#4,(a1)
012E4E  bsr.w	sub_11BA4
012E52  move.w	d2,d0
012E54  bsr.w	sub_11CA2
012E58  bsr.w	sub_11BA4
012E5C  move.w	(sp)+,($FFFFB028).w
012E60  addq.w	#1,($FFFFB02A).w
012E64  rts
```

## `$0129D2` -> `ai_ReleasePenalizedPlayer`  (confidence 0.7, 23 insns)

**Evidence.** updatepentime: finds the first object of team a2 whose slot $34 is negative (in the box), increments the active count $24, gives him the position from the priority list off_19286 (skipping the goalie entry when $26 says no goalie), reactivates him with sub_15A88/sub_15AA4, flags $63 bit 2 and marks both team update bits ($C6FE/$CA62 bit 0); caller updatepentime

**Callers.** updatepentime
**Callees.** Setplass, setplayer

```
0129D2  movem.l	d0-d3/a0-a3,-(sp)
0129D6  move.w	$22(a2),a3
0129DA  suba.w	#$80,a3
0129DE  add.w	#$80,a3
0129E2  tst.w	$34(a3)
0129E6  bpl.s	loc_129DE
0129E8  move.w	d0,d3
0129EA  lsr.w	#1,d3
0129EC  move.w	$24(a2),d1
0129F0  addq.w	#1,$24(a2)
0129F4  bset	#0,($FFFFC6FE).w
0129FA  bset	#0,($FFFFCA62).w
012A00  move.l	#off_19286,a0
012A06  tst.w	$26(a2)
012A0A  bpl.w	loc_12A10
012A0E  addq.w	#1,a0
012A10  clr.w	$34(a3)
012A14  move.b	(a0,d1.w),$35(a3)
012A1A  bsr.w	sub_15A88
012A1E  bsr.w	sub_15AA4
012A22  bset	#2,$63(a3)
012A28  movem.l	(sp)+,d0-d3/a0-a3
012A2C  rts
```

## `$01284A` -> `ai_EndPenaltyOnGoal`  (confidence 0.7, 22 insns)

**Evidence.** checkgoal: when the scored-on team a1 has fewer skaters than the scoring team a2, removes the first minor from its penalized list $9A(a1) (entries with status bit 6, majors, are skipped), clears the player's status word, shifts the list (sub_1298C), sets DelayedPen bit 0, bumps a1's active count and the power-play goal counter 2(a2), and marks both team update bits; clears the penalty message buffer (clrPenBuf) when a1 already has 6 skaters; caller checkgoal

**Callers.** checkgoal
**Callees.** clrPenBuf, sub_1298C
**RAM.** DelayedPen

```
01284A  movem.l	d0-d2/a0,-(sp)
01284E  cmp.w	#6,$24(a1)
012854  bne.w	loc_1285C
012858  bsr.w	sub_128A4
01285C  move.w	$24(a2),d2
012860  cmp.w	$24(a1),d2
012864  ble.w	loc_1289E
012868  lea	$9A(a1),a0
01286C  clr.w	d2
01286E  move.b	(a0)+,d2
012870  bmi.w	loc_1289E
012874  btst	#6,$66(a1,d2.w)
01287A  bne.s	loc_1286C
01287C  clr.w	$66(a1,d2.w)
012880  bsr.w	sub_1298C
012884  bset	#0,($FFFFC300).w
01288A  addq.w	#1,$24(a1)
01288E  addq.w	#1,2(a2)
012892  bset	#0,($FFFFC6FE).w
012898  bset	#0,($FFFFCA62).w
01289E  movem.l	(sp)+,d0-d2/a0
0128A2  rts
```

## `$012E66` -> `ai_DrawLineEnergyBar`  (confidence 0.7, 23 insns)

**Evidence.** line change menu: computes the line's energy with sub_12EB4, scales it to 0..15 (energy / $100, capped) and draws row 15 - value of the bar bitmap unk_AB920 (one tile row) with dobitmap at tile base $B016 in palette $8000; caller ai_PrintLineChangeMenu

**Callers.** ai_PrintLineChangeMenu
**Callees.** dobitmap, getlinee
**RAM.** printa

```
012E66  movem.l	d0-d5/a0-a2,-(sp)
012E6A  bsr.w	sub_12EB4
012E6E  move.w	($FFFFB02C).w,-(sp)
012E72  move.w	#$8000,($FFFFB02C).w
012E78  ext.l	d0
012E7A  divu.w	#$100,d0
012E7E  cmpnw	 $F,d0
012E82  bls.w	loc_12E88
012E86  moveq	#$F,d0
012E88  moveq	#$F,d1
012E8A  sub.w	d0,d1
012E8C  clr.w	d0
012E8E  move.l	#unk_AB920,a1
012E94  add.l	4(a1),a1
012E98  move.w	#$30A,a2
012E9C  move.w	(a1),d2
012E9E  moveq	#1,d3
012EA0  move.w	($FFFFB016).w,d4
012EA4  moveq	#0,d5
012EA6  bsr.w	sub_1169A
012EAA  move.w	(sp)+,($FFFFB02C).w
012EAE  movem.l	(sp)+,d0-d5/a0-a2
012EB2  rts
```

## `$0171BE` -> `ai_InitTeamRecord`  (confidence 0.7, 24 insns)

**Evidence.** d0 = team id, a2 = team record: stores the id at +$28 and the team data pointer (table $30E) at +$1E, then copies the line table from data offset +6 into +$16A: with OptLine set the 8-byte goalie entry plus 12 longs, otherwise the 14 longs after it; caller sub_17190 (team initialisation)

**Callers.** ai_InitBothTeamRecords
**Callees.** none
**RAM.** OptLine

```
0171BE  move.w	d0,$28(a2)
0171C2  move.w	#$30E,a0
0171C6  asl.w	#2,d0
0171C8  move.l	(a0,d0.w),$1E(a2)
0171CE  tst.w	($FFFFD058).w
0171D2  beq.w	loc_171F4
0171D6  move.l	$1E(a2),a0
0171DA  add.w	6(a0),a0
0171DE  lea	$16A(a2),a1
0171E2  move.l	(a0)+,(a1)+
0171E4  move.l	(a0)+,(a1)+
0171E6  addq.w	#8,a0
0171E8  move.w	#$B,d0
0171EC  move.l	(a0)+,(a1)+
0171EE  dbf	d0,loc_171EC
0171F2  rts
0171F4  moveq	#$D,d0
0171F6  move.l	$1E(a2),a0
0171FA  add.w	6(a0),a0
0171FE  addq.w	#8,a0
017200  lea	$16A(a2),a1
017204  move.l	(a0)+,(a1)+
017206  dbf	d0,loc_17204
01720A  rts
```

## `$0187B8` -> `ai_ShowGoalBanner`  (confidence 0.7, 23 insns)

**Evidence.** chkprogress: sets $C2FA bit 7 and, in shootout mode (bit 0), jumps to loc_FC320; otherwise clears the message timer (sub_1277A with -1), draws a 27x8 box at column 3 row 2, prints 'GOAL!' in the big font from word_18884, then the scorer (BA_Sktr_SCnum object's roster byte $66) of BA_Team and the 'Assist by:' lines; 'PENALTY SHOT!' is the shootout variant; caller chkprogress

**Callers.** chkprogress
**Callees.** Framer, loc_FC320, prefmes, printbig, printz
**Strings.** PENALTY SHOT! | Assist by: | GOAL!
**RAM.** BA_Sktr_SCnum, BA_Team

```
0187B8  bset	#7,($FFFFC2FA).w
0187BE  btst	#0,($FFFFC2FA).w
0187C4  beq.w	loc_187CE
0187C8  jmp	loc_FC320
0187CE  movem.l	d0-d2/a0-a4,-(sp)
0187D2  move.w	#$FFFF,d0
0187D6  jsr	sub_1277A
0187DC  bsr.w	sub_11B92
0187E0  dc.w	6
0187E2  dc.b	$BF
0187E3  dc.b	3
0187E4  dc.b	2
0187E5  dc.b	0
0187E6  moveq	#$1B,d0
0187E8  moveq	#8,d1
0187EA  bsr.w	sub_119B8
0187EE  lea	word_18884(pc),a1
0187F2  bsr.w	sub_11DF4
0187F6  move.w	($FFFFD406).w,d0
0187FA  asl.w	#7,d0
0187FC  move.l	#$FFFFB04A,a2
018802  add.w	d0,a2
018804  clr.w	d0
018806  move.b	$66(a2),d0
01880A  move.l	#$FFFFC6CE,a2
018810  tst.w	($FFFFD404).w
018814  beq.w	loc_1881E
018818  move.l	#$FFFFCA32,a2
```

## `$0FF2C8` -> `ai_PrintTitleTextBlock`  (confidence 0.5, 23 insns)

**Evidence.** newTitleScreen helper: erases a 32x6 area at the row derived from Vscroll (Vscroll/8 + $1C, mod 32) and prints the length-prefixed lines at a1 centred (column $11 - length/2), one per row, until a line with a negative length; caller newTitleScreen

**Callers.** newTitleScreen
**Callees.** eraser, print
**RAM.** Vscroll, printx, printy

```
0FF2C8  move.w	($FFFFBD20).w,d0
0FF2CC  asr.w	#3,d0
0FF2CE  add.w	#$1C,d0
0FF2D2  and.w	#$1F,d0
0FF2D6  move.w	d0,($FFFFB02A).w
0FF2DA  move.w	d0,-(sp)
0FF2DC  clr.w	($FFFFB028).w
0FF2E0  moveq	#$20,d0
0FF2E2  moveq	#6,d1
0FF2E4  move.w	#$7FF,d2
0FF2E8  jsr	sub_1197E
0FF2EE  move.w	(sp)+,($FFFFB02A).w
0FF2F2  move.w	(a1),d0
0FF2F4  asr.w	#1,d0
0FF2F6  neg.w	d0
0FF2F8  add.w	#$11,d0
0FF2FC  move.w	d0,($FFFFB028).w
0FF300  jsr	sub_11BA4
0FF306  addq.w	#1,($FFFFB02A).w
0FF30A  and.w	#$1F,($FFFFB02A).w
0FF310  tst.w	2(a1)
0FF314  bpl.s	loc_FF2F2
0FF316  rts
```

## `$011E8E` -> `ai_PrintBigChar`  (confidence 0.7, 25 insns)

**Evidence.** printbig helper: maps the character d0 - $20 through unk_1916A to a glyph index (negative = single-tile glyph), then writes the glyph's tiles from the big-font map off_A9A10 in two rows through sub_11EDA (VRAM name table at $B004 + $B02E), advancing d4; caller printbig

**Callers.** printbig
**Callees.** ai_WriteBigFontTile

```
011E8E  sub.w	#$20,d0
011E92  move.l	#unk_1916A,a0
011E98  moveq	#1,d2
011E9A  move.b	(a0,d0.w),d1
011E9E  ext.w	d1
011EA0  bpl.w	loc_11EA8
011EA4  neg.w	d1
011EA6  clr.w	d2
011EA8  asl.w	#1,d1
011EAA  move.l	#off_A9A10,a0
011EB0  add.l	4(a0),a0
011EB4  move.w	4(a0,d1.w),d3
011EB8  bsr.w	sub_11EDA
011EBC  move.w	(a0),d7
011EBE  asl.w	#1,d7
011EC0  add.w	d7,d1
011EC2  move.w	4(a0,d1.w),d3
011EC6  sub.w	d7,d1
011EC8  addq.w	#1,d5
011ECA  bsr.w	sub_11EDA
011ECE  subq.w	#1,d5
011ED0  addq.w	#1,d4
011ED2  addq.w	#2,d1
011ED4  dbf	d2,loc_11EB4
011ED8  rts
```

