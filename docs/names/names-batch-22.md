# Name review: names-batch-22.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FB4C4` -> `ai_PrintNameEntryHelp`  (confidence 0.7, 37 insns)

**Evidence.** name-entry screen: erases the 22x7 help area at column 1 row $14 and, toggling $D6C5 bit 0 each call, alternately prints the letter grid (the alphabet 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.12 -' laid out five per row from column $19) or the instructions 'D-Pad to a letter.', 'C to select letter.', 'A to go back.', 'B to cancel.', 'START when done.'

**Callers.** none found
**Callees.** Framer, eraser, print, printz
**Strings.** D-Pad to a letter. | C to select letter. | A to go back. | B to cancel. | START when done.
**RAM.** printx, printy

```
0FB4C4  movem.l	d0-a6,-(sp)
0FB4C8  jsr	sub_11B92
0FB4CE  dc.w	6
0FB4D0  dc.b	$BF
0FB4D1  dc.b	1
0FB4D2  dc.b	$14
0FB4D3  dc.b	0
0FB4D4  move.w	#$16,d0
0FB4D8  move.w	#7,d1
0FB4DC  move.w	#$7FF,d2
0FB4E0  jsr	sub_1197E
0FB4E6  bchg	#0,($FFFFD6C5).w
0FB4EC  bne.w	loc_FB5F0
0FB4F0  jsr	sub_11B92
0FB4F6  dc.w	6
0FB4F8  dc.b	$BF
0FB4F9  dc.b	$19
0FB4FA  dc.b	$11
0FB4FB  dc.b	0
0FB4FC  move.l	#aAbcdefghijklmnopqrstu,a0
0FB502  moveq	#4,d0
0FB504  moveq	#5,d1
0FB506  move.l	#$FFFFBFA4,a1
0FB50C  move.w	#$E,(a1)+
0FB510  move.b	(a0)+,(a1)+
0FB512  move.b	#$20,(a1)+
0FB516  dbf	d1,loc_FB510
0FB51A  move.w	#$BFA4,a1
0FB51E  jsr	sub_11BA4
0FB524  addq.w	#2,($FFFFB02A).w
0FB528  sub.w	#$C,($FFFFB028).w
0FB52E  dbf	d0,loc_FB504
0FB532  jsr	sub_11B92
0FB538  dc.w	6
0FB53A  dc.b	$FE
0FB53B  dc.b	1
0FB53C  dc.b	$14
0FB53D  dc.b	0
0FB53E  moveq	#$16,d0
0FB540  moveq	#7,d1
0FB542  jsr	sub_119B8
0FB548  jsr	sub_11B92
0FB54E  dc.w	$18
0FB550  dc.b	$BF
0FB551  dc.b	2
0FB552  dc.b	$15
0FB553  aDPadToALetter_: dc.b	'D-Pad to a letter.',0
0FB566  move.w	#2,($FFFFB028).w
0FB56C  addq.w	#1,($FFFFB02A).w
0FB570  move.w	($FFFFB028).w,-(sp)
0FB574  jsr	sub_11B92
0FB57A  dc.w	$16
0FB57C  aCToSelectLetter_: dc.b	'C to select letter.',0
0FB590  move.w	(sp),($FFFFB028).w
0FB594  addq.w	#1,($FFFFB02A).w
0FB598  jsr	sub_11B92
0FB59E  dc.w	$10
0FB5A0  aAToGoBack_:	dc.b	'A to go back.',0
0FB5AE  move.w	(sp),($FFFFB028).w
0FB5B2  addq.w	#1,($FFFFB02A).w
...
```

## `$0F98C6` -> `ai_BuildPlayerRecordText`  (confidence 0.6, 34 insns)

**Evidence.** builds the 'Record: N goal(s)/save(s)' text for a player in the string at a1: copies the 'Record' label word_F9950, reads the record value with ai_ReadPlayerRecordValue (an empty string when 0), converts it (NumberToDecimalText) and appends 'goal'/'goals' (word_F995A/word_F996A) or 'save'/'saves' (word_F9972) by the goalie flag and count

**Callers.** none found
**Callees.** ai_CopyLenString, ai_NumberToDecimalText, ai_ReadPlayerRecordValue, appstring, loc_F994A
**Strings.** Record | goals | goal | saves | save

```
0F98C6  movem.l	d0-d7/a1-a6,-(sp)
0F98CA  move.l	a1,-(sp)
0F98CC  move.l	a1,a3
0F98CE  move.l	#word_F9950,a1
0F98D4  movem.l	d0-d1,-(sp)
0F98D8  bsr.w	sub_F997A
0F98DC  movem.l	(sp)+,d0-d1
0F98E0  bsr.w	sub_F99F2
0F98E4  tst.w	d0
0F98E6  bne.w	loc_F98F4
0F98EA  move.l	(sp)+,a1
0F98EC  move.w	#2,(a1)
0F98F0  bra.w	loc_F994A
0F98F4  move.l	#$FFFFBF20,a1
0F98FA  move.w	d0,($FFFFBF14).w
0F98FE  bsr.w	sub_F998E
0F9902  move.l	(sp),a3
0F9904  move.l	#$FFFFBF20,a1
0F990A  jsr	sub_11D9E
0F9910  move.w	($FFFFBF14).w,d0
0F9914  move.l	#word_F996A,a1
0F991A  cmpnw	 1,d0
0F991E  bne.w	loc_F9928
0F9922  move.l	#word_F9972,a1
0F9928  tst.w	d1
0F992A  bne.w	loc_F9942
0F992E  move.l	#word_F995A,a1
0F9934  cmpnw	 1,d0
0F9938  bne.w	loc_F9942
0F993C  move.l	#word_F9962,a1
0F9942  move.l	(sp)+,a3
0F9944  jsr	sub_11D9E
0F994A  movem.l	(sp)+,d0-d7/a1-a6
0F994E  rts
```

## `$01ABAA` -> `ai_SetChannelVolume`  (confidence 0.5, 32 insns)

**Evidence.** sound driver: volume = 2(a2) * the track's volume entry 4(a3, channel*8) / 128; for FM channels (byte 3 < $60) maps it through the attenuation table byte_1ABF0 ($1A, $18, $16 ... descending) and stores it in $D187[channel] with the update bits $D184/$D180

**Callers.** none found
**Callees.** none
**Hardware.** Z80 busreq

```
01ABAA  movem.l	d0,-(sp)
01ABAE  clr.w	d0
01ABB0  move.b	2(a2),d0
01ABB4  clr.w	d1
01ABB6  move.b	(a2),d1
01ABB8  asl.w	#3,d1
01ABBA  mulu.w	4(a3,d1.w),d0
01ABBE  lsr.w	#7,d0
01ABC0  cmp.b	#$60,3(a2)
01ABC6  bge.w	loc_1AC00
01ABCA  lea	byte_1ABF0(pc),a4
01ABCE  lsr.w	#3,d0
01ABD0  move.b	(a4,d0.w),d0
01ABD4  clr.w	d3
01ABD6  move.b	4(a2),d3
01ABDA  move.w	#$D187,a4
01ABDE  move.b	d0,(a4,d3.w)
01ABE2  bset	d3,($FFFFD184).w
01ABE6  st	($FFFFD180).w
01ABEA  movem.l	(sp)+,d0
01ABEE  rts
01ABF0  byte_1ABF0:	dc.b	$1A
01ABF1  dc.b	$18
01ABF2  dc.b	$16
01ABF3  dc.b	$14
01ABF4  dc.b	$12
01ABF5  dc.b	$10
01ABF6  dc.b	$E
01ABF7  dc.b	$C
01ABF8  dc.b	$A
01ABF9  dc.b	8
01ABFA  dc.b	6
01ABFB  dc.b	4
01ABFC  dc.b	3
01ABFD  dc.b	2
01ABFE  dc.b	1
01ABFF  dc.b	0
01AC00  move.w	#$100,($A11100).l
01AC08  btst	#0,($A11100).l
01AC10  bne.s	loc_1AC08
01AC12  lsr.b	#2,d0
01AC14  cmpnw	 3,d0
01AC18  bgt.w	loc_1AC1E
01AC1C  moveq	#3,d0
01AC1E  move.b	d0,($A00083).l
01AC24  clr.w	($A11100).l
01AC2A  movem.l	(sp)+,d0
01AC2E  rts
```

## `$009588` -> `ai_ScrollStatsList`  (confidence 0.6, 31 insns)

**Evidence.** stats screen scroll step: applies PlayerScrollCtr to VertLineScrolling within 0..$D5B2; at every 16-pixel boundary redraws the arrows (ai_PrintScrollArrows) and stops, and when leaving a boundary pre-draws the row entering from above (ai_PrintStatRowFromScroll at $E) or below (ai_PrintStatRowFromScrollPlus6 at 2); finally writes the plane vertical scroll (VSRAM, -$68 + offset)

**Callers.** none found
**Callees.** ai_PrintScrollArrows, ai_PrintStatRowFromScroll, ai_PrintStatRowFromScrollPlus6
**RAM.** PlayerScrollCtr, VertLineScrolling, disflags
**Hardware.** VDP data

```
009588  move.w	($FFFFD5B0).w,d0
00958C  beq.w	locret_A9D4
009590  add.w	($FFFFD5AE).w,d0
009594  bmi.w	locret_A9D4
009598  cmp.w	($FFFFD5B2).w,d0
00959C  bgt.w	locret_A9D4
0095A0  move.w	($FFFFD5AE).w,d1
0095A4  move.w	d0,($FFFFD5AE).w
0095A8  and.w	#$F,d0
0095AC  bne.w	loc_95B8
0095B0  bsr.w	sub_99C6
0095B4  clr.w	($FFFFD5B0).w
0095B8  and.w	#$F,d1
0095BC  bne.w	loc_95DC
0095C0  move.w	d0,-(sp)
0095C2  cmpnw	 $E,d0
0095C6  bne.w	loc_95CE
0095CA  bsr.w	sub_9604
0095CE  move.w	(sp)+,d0
0095D0  cmpnw	 2,d0
0095D4  bne.w	loc_95DC
0095D8  bsr.w	sub_960E
0095DC  move.w	($FFFFBF78).w,-(sp)
0095E0  bset	#2,($FFFFBF78).w
0095E6  move.l	#$C00000,a0
0095EC  move.l	#$40020010,4(a0)
0095F4  move.w	#$FF98,d0
0095F8  add.w	($FFFFD5AE).w,d0
0095FC  move.w	d0,(a0)
0095FE  move.w	(sp)+,($FFFFBF78).w
009602  rts
```

## `$008FB8` -> `ai_ScrollSummaryList`  (confidence 0.6, 28 insns)

**Evidence.** scoring-summary scroll step with a 32-pixel row pitch: updates VertLineScrolling to d0, redraws the arrows (ai_PrintSummaryScrollArrows) at a boundary, pre-draws the row entering from above (ai_PrintSummaryRowAbove at $1E) or below (ai_PrintSummaryRowAt at 2), and writes the vertical scroll (-$50 + offset)

**Callers.** none found
**Callees.** ai_PrintSummaryRowAbove, ai_PrintSummaryRowAt, ai_PrintSummaryScrollArrows
**RAM.** PlayerScrollCtr, VertLineScrolling, disflags
**Hardware.** VDP data

```
008FB8  move.w	($FFFFD5AE).w,d1
008FBC  move.w	d0,($FFFFD5AE).w
008FC0  ext.l	d0
008FC2  divs.w	#$20,d0
008FC6  swap	d0
008FC8  tst.w	d0
008FCA  bne.w	loc_8FD6
008FCE  bsr.w	sub_93C4
008FD2  clr.w	($FFFFD5B0).w
008FD6  and.w	#$1F,d1
008FDA  bne.w	loc_8FFA
008FDE  move.l	d0,-(sp)
008FE0  cmpnw	 $1E,d0
008FE4  bne.w	loc_8FEC
008FE8  bsr.w	sub_9020
008FEC  move.l	(sp)+,d0
008FEE  cmpnw	 2,d0
008FF2  bne.w	loc_8FFA
008FF6  bsr.w	sub_904C
008FFA  move.w	($FFFFBF78).w,-(sp)
008FFE  bset	#2,($FFFFBF78).w
009004  move.l	#$C00000,a0
00900A  move.l	#$40020010,4(a0)
009012  moveq	#$FFFFFFB0,d0
009014  add.w	($FFFFD5AE).w,d0
009018  move.w	d0,(a0)
00901A  move.w	(sp)+,($FFFFBF78).w
00901E  rts
```

## `$008B1C` -> `ai_ScrollEditLinesPages`  (confidence 0.6, 25 insns)

**Evidence.** edit-lines page scroll with a 128-pixel pitch: updates VertLineScrolling to d0, stops the velocity at a boundary, pre-draws the page entering from above (ai_ShowEditLinesPage at $7E) or below (ai_ShowEditLinesPageNext at 2), and writes the vertical scroll (-$70 + offset)

**Callers.** none found
**Callees.** ai_ShowEditLinesPage, ai_ShowEditLinesPageNext
**RAM.** PlayerScrollCtr, VertLineScrolling, disflags
**Hardware.** VDP data

```
008B1C  move.w	($FFFFD5AE).w,d1
008B20  move.w	d0,($FFFFD5AE).w
008B24  ext.l	d0
008B26  divs.w	#$80,d0
008B2A  swap	d0
008B2C  tst.w	d0
008B2E  bne.w	loc_8B36
008B32  clr.w	($FFFFD5B0).w
008B36  and.w	#$7F,d1
008B3A  bne.w	loc_8B56
008B3E  cmpnw	 $7E,d0
008B42  bne.w	loc_8B4A
008B46  bsr.w	sub_8B84
008B4A  cmpnw	 2,d0
008B4E  bne.w	loc_8B56
008B52  bsr.w	sub_8B94
008B56  move.w	($FFFFBF78).w,-(sp)
008B5A  bset	#2,($FFFFBF78).w
008B60  move.l	#$C00000,a0
008B66  move.l	#$40020010,4(a0)
008B6E  move.w	#$FF90,d0
008B72  add.w	($FFFFD5AE).w,d0
008B76  move.w	d0,(a0)
008B78  move.w	(sp)+,($FFFFBF78).w
008B7C  rts
```

## `$0FACF0` -> `ai_PrintGoalsAssistsBox`  (confidence 0.7, 31 insns)

**Evidence.** records screen: at (d1,d2) prints 'Goals' and 'Assists' with the player d0's season totals from the selected team's +$B4 (goals) and +$CE (assists) columns (ai_GetRecordsTeam, NumberToDecimalText)

**Callers.** none found
**Callees.** ai_GetRecordsTeam, ai_NumberToDecimalText, print2, printz2
**Strings.** Goals | Assists
**RAM.** printx, printy

```
0FACF0  movem.l	d0-a6,-(sp)
0FACF4  bsr.w	sub_FAF50
0FACF8  move.l	a0,-(sp)
0FACFA  add.l	#$B4,a0
0FAD00  move.b	(a0,d0.w),d3
0FAD04  ext.w	d3
0FAD06  move.l	(sp)+,a0
0FAD08  add.l	#$CE,a0
0FAD0E  move.b	(a0,d0.w),d4
0FAD12  ext.w	d4
0FAD14  move.w	d1,($FFFFB028).w
0FAD18  move.w	d2,($FFFFB02A).w
0FAD1C  move.w	d1,-(sp)
0FAD1E  jsr	sub_11A36
0FAD24  dc.w	$C
0FAD26  aGoals_2:	dc.b	'Goals    ',0
0FAD30  move.w	d0,-(sp)
0FAD32  move.w	d3,d0
0FAD34  move.l	#$FFFFBFA4,a1
0FAD3A  bsr.w	sub_F998E
0FAD3E  move.w	(sp)+,d0
0FAD40  move.l	#$FFFFBFA4,a1
0FAD46  jsr	sub_11A48
0FAD4C  move.w	(sp)+,($FFFFB028).w
0FAD50  addq.w	#1,($FFFFB02A).w
0FAD54  jsr	sub_11A36
0FAD5A  dc.w	$C
0FAD5C  aAssists_0:	dc.b	'Assists  ',0
0FAD66  move.w	d4,d0
0FAD68  move.l	#$FFFFBFA4,a1
0FAD6E  bsr.w	sub_F998E
0FAD72  move.l	#$FFFFBFA4,a1
0FAD78  jsr	sub_11A48
0FAD7E  movem.l	(sp)+,d0-a6
0FAD82  rts
```

## `$008566` -> `ai_RefreshEditLinesRows`  (confidence 0.5, 30 insns)

**Evidence.** edit-lines refresh: derives the row-visibility mask from unk_85E7 by the cursor $D5B8 (shifted one entry with OptLine), redraws the layout (ai_PrintEditLinesLayout) when the mask changes ($C012), reprints each visible line with ai_PrintLineRoster for mask bits 6..0, then the header at column 8

**Callers.** none found
**Callees.** Framer, ai_PrintEditLinesLayout, ai_PrintLineRoster, getname, print2, printz2
**RAM.** OptLine, printa, printx

```
008566  moveq	#6,d5
008568  lea	unk_85E7(pc),a0
00856C  move.w	($FFFFD5B8).w,d0
008570  lsr.w	#3,d0
008572  add.w	d0,a0
008574  tst.w	($FFFFD058).w
008578  beq.w	loc_857E
00857C  subq.w	#1,a0
00857E  move.b	(a0),d0
008580  cmp.b	($FFFFC012).w,d0
008584  beq.w	loc_8590
008588  move.b	d0,($FFFFC012).w
00858C  bsr.w	loc_868C
008590  btst	d5,($FFFFC012).w
008594  beq.w	loc_859C
008598  bsr.w	loc_85EE
00859C  dbf	d5,loc_8590
0085A0  jsr	sub_11A36
0085A6  dc.w	$A
0085A8  dc.b	$F8
0085A9  dc.b	4
0085AA  dc.b	2
0085AB  dc.b	8
0085AC  dc.b	7
0085AD  dc.b	$F9
0085AE  dc.b	1
0085AF  dc.b	0
0085B0  moveq	#$18,d0
0085B2  moveq	#3,d1
0085B4  jsr	sub_119B8
0085BA  jsr	sub_11A36
0085C0  dc.w	6
0085C2  dc.b	$FD
0085C3  dc.b	$15
0085C4  dc.b	$FC
0085C5  dc.b	8
0085C6  dc.b	$30
0085C7  dc.b	6
0085C8  jsr	sub_18A90
0085CE  move.w	(a1),d0
0085D0  lsr.w	#1,d0
0085D2  sub.w	d0,($FFFFB028).w
0085D6  move.w	d7,($FFFFB02C).w
0085DA  jsr	sub_11A48
0085E0  clr.w	($FFFFB030).w
0085E4  rts
```

## `$0FAC90` -> `ai_BuildJerseyNumberText`  (confidence 0.6, 30 insns)

**Evidence.** walks the selected team's roster (home, or away by $D4F6) to player d0 and writes his jersey number (the BCD byte after the name; a leading zero shown as a space) as a 4-byte string at a1

**Callers.** none found
**Callees.** loc_FACDC

```
0FAC90  movem.l	d0-a6,-(sp)
0FAC94  move.l	#$FFFFC6CE,a0
0FAC9A  tst.w	($FFFFD4F6).w
0FAC9E  beq.w	loc_FACA8
0FACA2  move.l	#$FFFFCA32,a0
0FACA8  move.l	$1E(a0),a0
0FACAC  move.w	(a0),d1
0FACAE  ext.l	d1
0FACB0  add.l	d1,a0
0FACB2  move.w	(a0),d1
0FACB4  ext.l	d1
0FACB6  add.l	d1,a0
0FACB8  addq.l	#8,a0
0FACBA  dbf	d0,loc_FACB2
0FACBE  subq.l	#8,a0
0FACC0  move.w	#4,(a1)+
0FACC4  move.b	(a0),d0
0FACC6  lsr.w	#4,d0
0FACC8  and.w	#$F,d0
0FACCC  bne.w	loc_FACD8
0FACD0  move.b	#$20,d0
0FACD4  bra.w	loc_FACDC
0FACD8  add.b	#$30,d0
0FACDC  move.b	d0,(a1)+
0FACDE  move.b	(a0),d0
0FACE0  and.w	#$F,d0
0FACE4  add.b	#$30,d0
0FACE8  move.b	d0,(a1)+
0FACEA  movem.l	(sp)+,d0-a6
0FACEE  rts
```

## `$0FF3F8` -> `ai_ScrollTitleLines`  (confidence 0.5, 28 insns)

**Evidence.** title screen: every time the $BF14 countdown expires walks the $E0 per-line scroll words built by ai_InitTitleScrollTable ($B04A..): lines above $8F move by Hscroll and reset to 0 when they leave the $FC00 band, the others move back toward 0

**Callers.** none found
**Callees.** loc_FF458
**RAM.** Hscroll

```
0FF3F8  subq.w	#1,($FFFFBF14).w
0FF3FC  bmi.w	loc_FF402
0FF400  rts
0FF402  clr.w	($FFFFBF14).w
0FF406  movem.l	d0-d2/a0,-(sp)
0FF40A  move.w	#$DF,d0
0FF40E  move.w	#$B04A,a0
0FF412  tst.l	(a0)+
0FF414  cmpnw	 $28,d0
0FF418  ble.w	loc_FF458
0FF41C  move.w	($FFFFBD1E).w,d1
0FF420  cmpnw	 $8F,d0
0FF424  blt.w	loc_FF44C
0FF428  move.w	-2(a0),d2
0FF42C  beq.w	loc_FF458
0FF430  add.w	d1,d2
0FF432  move.w	d2,-2(a0)
0FF436  and.w	#$FC00,d2
0FF43A  cmpnw	 $FC00,d2
0FF43E  beq.w	loc_FF458
0FF442  move.w	#0,-2(a0)
0FF448  bra.w	loc_FF458
0FF44C  sub.w	d1,-2(a0)
0FF450  bpl.w	loc_FF458
0FF454  clr.w	-2(a0)
0FF458  dbf	d0,loc_FF412
0FF45C  movem.l	(sp)+,d0-d2/a0
0FF460  rts
```

## `$0FA2C0` -> `ai_PrintRecordsPage`  (confidence 0.7, 25 insns)

**Evidence.** records page: loads the selected team's logo palette from word_F8BF4 (+$26) into $BD4A, starts a fade, erases the 40x21 body at row 7 and, depending on the first word of the record list a0, prints the 'Records' / 'This Game' sections through ai_PrintRecordsScreen

**Callers.** none found
**Callees.** ai_PrintRecordsScreen, eraser, loc_FA328, loc_FA330, printz
**Strings.** Records | ----------- | This Game | -----------
**RAM.** HomeTeam, VisTeam, palcount

```
0FA2C0  movem.l	d0-d7/a1-a6,-(sp)
0FA2C4  move.l	a0,-(sp)
0FA2C6  move.w	($FFFFC330).w,d0
0FA2CA  tst.w	($FFFFD4F6).w
0FA2CE  beq.w	loc_FA2D6
0FA2D2  move.w	($FFFFC332).w,d0
0FA2D6  asl.w	#6,d0
0FA2D8  move.l	#word_F8BF4,a6
0FA2DE  move.l	$26(a6,d0.w),($FFFFBD4A).w
0FA2E4  move.w	#$64,($FFFFBD26).w
0FA2EA  jsr	sub_11B92
0FA2F0  dc.w	6
0FA2F2  dc.b	$BE
0FA2F3  dc.b	0
0FA2F4  dc.b	7
0FA2F5  dc.b	0
0FA2F6  move.w	#$28,d0
0FA2FA  move.w	#$15,d1
0FA2FE  move.w	#$7FF,d2
0FA302  jsr	sub_1197E
0FA308  jsr	sub_11B92
0FA30E  dc.w	6
0FA310  dc.b	$BE
0FA311  dc.b	0
0FA312  dc.b	0
0FA313  dc.b	0
0FA314  move.l	(sp),a0
0FA316  tst.w	(a0)
0FA318  bne.w	loc_FA324
0FA31C  bsr.w	loc_FA550
0FA320  bra.w	loc_FA328
0FA324  bsr.w	loc_FA330
0FA328  move.l	(sp)+,a0
0FA32A  movem.l	(sp)+,d0-d7/a1-a6
0FA32E  rts
```

## `$0FA8AC` -> `ai_PrintOverallRatingBox`  (confidence 0.7, 25 insns)

**Evidence.** records screen: at (d1,d2) prints 'Overall' and 'Rating' then the selected team's rating (sub_FA9F8 summed over the attribute mask dword_19420, or dword_19582 for the per-position view) as a percentage via sub_FEF7C and NumberToDecimalText

**Callers.** none found
**Callees.** AttribAdjust, CalcAttrib, ai_NumberToDecimalText, print2, printz2
**Strings.** Overall | Rating
**RAM.** printx, printy

```
0FA8AC  movem.l	d0-a6,-(sp)
0FA8B0  move.w	d1,($FFFFB028).w
0FA8B4  move.w	d2,($FFFFB02A).w
0FA8B8  move.w	d1,-(sp)
0FA8BA  jsr	sub_11A36
0FA8C0  dc.w	$A
0FA8C2  aOverall_1:	dc.b	'Overall',0
0FA8CA  move.w	(sp)+,($FFFFB028).w
0FA8CE  addq.w	#1,($FFFFB02A).w
0FA8D2  jsr	sub_11A36
0FA8D8  dc.w	$C
0FA8DA  aRating_0:	dc.b	'Rating   ',0
0FA8E4  move.l	#$FFFFC6CE,a2
0FA8EA  tst.w	($FFFFD4F6).w
0FA8EE  beq.w	loc_FA8F8
0FA8F2  move.l	#$FFFFCA32,a2
0FA8F8  move.l	(dword_19420).l,d4
0FA8FE  tst.w	($FFFFD598).w
0FA902  beq.w	loc_FA90C
0FA906  move.l	(dword_19582).l,d4
0FA90C  bsr.w	sub_FA9F8
0FA910  mulu.w	#$64,d0
0FA914  divu.w	d1,d0
0FA916  bsr.w	sub_FEF7C
0FA91A  move.l	#$FFFFBFA4,a1
0FA920  bsr.w	sub_F998E
0FA924  move.l	#$FFFFBFA4,a1
0FA92A  jsr	sub_11A48
0FA930  movem.l	(sp)+,d0-a6
```

