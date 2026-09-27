# Name review: names-batch-14.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FB91A` -> `ai_PrintNameEntryField`  (confidence 0.7, 17 insns)

**Evidence.** name-entry screen: builds a 12-character string in $CF36 from the letters typed so far (a1, count $D4E8) padded with '-' and prints it; the character set 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.12 -' sits next to it; caller loc_FB822

**Callers.** loc_FB822
**Callees.** print
**Strings.** ABCDEFGHIJKLMNOPQRSTUVWXYZ.12 -

```
0FB91A  movem.l	d0-a6,-(sp)
0FB91E  move.l	#$FFFFCF36,a0
0FB924  move.w	($FFFFD4E8).w,d0
0FB928  move.w	#0,d3
0FB92C  move.w	#$E,(a0)+
0FB930  move.b	(a1,d3.w),d1
0FB934  cmp.w	($FFFFD4E8).w,d3
0FB938  blt.w	loc_FB940
0FB93C  move.b	#$2D,d1
0FB940  move.b	d1,(a0)+
0FB942  addq.w	#1,d3
0FB944  cmpnw	 $C,d3
0FB948  blt.s	loc_FB930
0FB94A  move.l	#$FFFFCF36,a1
0FB950  jsr	sub_11BA4
0FB956  movem.l	(sp)+,d0-a6
0FB95A  rts
```

## `$0FC570` -> `ai_LoadShootoutShooters`  (confidence 0.6, 17 insns)

**Evidence.** shootout setup: takes the six-entry lineup list (team data offset +6) of HomeTeam, or VisTeam when the side flag $D594 is set, and stores the six player indexes (minus 1) as words below $D586 or $D594, the shooter lists that ai_AdvanceShootoutRound indexes with $D586; caller sub_FC47C

**Callers.** sub_FC47C
**Callees.** none
**RAM.** HomeTeam, VisTeam

```
0FC570  move.l	#$FFFFD586,a0
0FC576  move.w	($FFFFC330).w,d0
0FC57A  tst.w	($FFFFD594).w
0FC57E  beq.w	loc_FC58C
0FC582  move.w	($FFFFC332).w,d0
0FC586  move.l	#$FFFFD594,a0
0FC58C  move.l	#$30E,a1
0FC592  asl.w	#2,d0
0FC594  move.l	(a1,d0.w),a1
0FC598  add.w	6(a1),a1
0FC59C  move.w	#5,d0
0FC5A0  clr.w	d1
0FC5A2  move.b	(a1)+,d1
0FC5A4  subq.w	#1,d1
0FC5A6  move.w	d1,-(a0)
0FC5A8  dbf	d0,loc_FC5A0
0FC5AC  rts
```

## `$0FCB9A` -> `ai_BuildCrowdRecordText`  (confidence 0.6, 17 insns)

**Evidence.** ticker helper: reads the home team's record (ReadTeamRecord into $CFFE), takes the loudest-crowd byte 8 (defaulting to $50 when unset) and converts it to decimal text in $BF20 with NumberToDecimalText for the 'by' phrase; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** ReadTeamRecord, ai_NumberToDecimalText
**Strings.** by
**RAM.** HomeTeam

```
0FCB9A  movem.l	d0-a0/a2-a6,-(sp)
0FCB9E  move.w	($FFFFC330).w,d1
0FCBA2  ext.l	d1
0FCBA4  move.l	#$FFFFCFFE,a0
0FCBAA  move.l	a0,-(sp)
0FCBAC  jsr	sub_F9BE2
0FCBB2  move.l	(sp)+,a0
0FCBB4  move.l	#$FFFFBF20,a1
0FCBBA  clr.w	d0
0FCBBC  move.b	8(a0),d0
0FCBC0  bne.w	loc_FCBC8
0FCBC4  move.b	#$50,d0
0FCBC8  move.l	a1,-(sp)
0FCBCA  jsr	sub_F998E
0FCBD0  move.l	(sp)+,a1
0FCBD2  movem.l	(sp)+,d0-a0/a2-a6
0FCBD6  rts
```

## `$0FEC5E` -> `ai_FindLoudestCrowdTeam`  (confidence 0.7, 17 insns)

**Evidence.** scans the 28 team records (ReadTeamRecord into $CF36) for the highest crowd byte 8 (unset counts as $50) and returns d0 = that team and d7 = the value; caller loc_9B4A (crowd meter / records display)

**Callers.** $009B4A
**Callees.** ReadTeamRecord

```
0FEC5E  movem.l	d1-a6,-(sp)
0FEC62  move.w	#$1B,d1
0FEC66  ext.l	d1
0FEC68  clr.w	d7
0FEC6A  move.l	#$FFFFCF36,a0
0FEC70  jsr	sub_F9BE2
0FEC76  clr.w	d2
0FEC78  move.b	8(a0),d2
0FEC7C  bne.w	loc_FEC84
0FEC80  move.w	#$50,d2
0FEC84  cmp.w	d7,d2
0FEC86  ble.w	loc_FEC8E
0FEC8A  move.w	d2,d7
0FEC8C  move.w	d1,d0
0FEC8E  dbf	d1,loc_FEC70
0FEC92  movem.l	(sp)+,d1-a6
0FEC96  rts
```

## `$008280` -> `ai_PrintSelectPlayerArrows`  (confidence 0.6, 16 insns)

**Evidence.** same shape as ai_PrintScrollArrows: chooses one of the four strings at word_82BC (none / down / up / both) from VertLineScrolling against $D5B2 and prints it in the '{Select  Player}' header of the edit-lines player picker; caller sub_8198

**Callers.** sub_8198
**Callees.** ai_PrintNextString, printz2
**Strings.** {Select  Player}
**RAM.** VertLineScrolling

```
008280  movem.l	d0-d1/a1,-(sp)
008284  jsr	sub_11A36
00828A  dc.w	$A
00828C  dc.b	$F8
00828D  dc.b	4
00828E  dc.b	3
00828F  dc.b	4
008290  dc.b	6
008291  dc.b	$F9
008292  dc.b	1
008293  dc.b	0
008294  clr.w	d0
008296  move.w	($FFFFD5AE).w,d1
00829A  tst.w	d1
00829C  sgt	d0
00829E  neg.b	d0
0082A0  cmp.w	($FFFFD5B2).w,d1
0082A4  slt	d1
0082A6  neg.b	d1
0082A8  add.b	d1,d0
0082AA  add.b	d1,d0
0082AC  lea	word_82BC(pc),a1
0082B0  jsr	sub_13508
0082B6  movem.l	(sp)+,d0-d1/a1
0082BA  rts
```

## `$0093C4` -> `ai_PrintSummaryScrollArrows`  (confidence 0.6, 16 insns)

**Evidence.** same shape as ai_PrintScrollArrows for the scoring-summary list: chooses one of the four strings at word_9400 from VertLineScrolling against $D5B2 and prints it at column 4 row 9; caller sub_8FB8 (summary page handler)

**Callers.** sub_8FB8
**Callees.** ai_PrintNextString, printz2
**RAM.** VertLineScrolling

```
0093C4  movem.l	d0-d1/a1,-(sp)
0093C8  jsr	sub_11A36
0093CE  dc.w	$A
0093D0  dc.b	$F8
0093D1  dc.b	4
0093D2  dc.b	3
0093D3  dc.b	4
0093D4  dc.b	9
0093D5  dc.b	$F9
0093D6  dc.b	1
0093D7  dc.b	0
0093D8  clr.w	d0
0093DA  move.w	($FFFFD5AE).w,d1
0093DE  tst.w	d1
0093E0  sgt	d0
0093E2  neg.b	d0
0093E4  cmp.w	($FFFFD5B2).w,d1
0093E8  slt	d1
0093EA  neg.b	d1
0093EC  add.b	d1,d0
0093EE  add.b	d1,d0
0093F0  lea	word_9400(pc),a1
0093F4  jsr	sub_13508
0093FA  movem.l	(sp)+,d0-d1/a1
0093FE  rts
```

## `$0100A6` -> `ai_CheckZoneCleared`  (confidence 0.5, 16 insns)

**Evidence.** ChkOffsides helper: while $30(a2) bit 4 (team in the attacking zone) is set, scans team a2's six objects with a non-negative slot and clears the bit once none of them is deeper than y = $58 (after the side flip), i.e. the team has left the zone; caller ChkOffsides

**Callers.** ChkOffsides
**Callees.** none

```
0100A6  btst	#4,$30(a2)
0100AC  beq.w	locret_15464
0100B0  move.w	$22(a2),a0
0100B4  moveq	#5,d1
0100B6  tst.w	$34(a0)
0100BA  bmi.w	loc_100CE
0100BE  move.w	$14(a0),d0
0100C2  btst	#7,$62(a0)
0100C8  bne.w	loc_100CE
0100CC  neg.w	d0
0100CE  add.w	#$80,a0
0100D2  cmpnw	 $58,d0
0100D6  dbgt	d1,loc_100B6
0100DA  bgt.w	locret_15464
0100DE  bclr	#4,$30(a2)
0100E4  rts
```

## `$01177A` -> `ai_DecompressTiles`  (confidence 0.7, 16 insns)

**Evidence.** tile decompressor used by ai_LoadTilesCore for negative-count blocks: with the scratch buffer $CF36, the inline map slot $CF32 and the writers remap / DoDMApro in a5/a6, reads control bytes from a0 and dispatches on their high nibble through the jump table word_117B2 until the block is done; caller ai_LoadTilesCore

**Callers.** ai_LoadTilesCore
**Callees.** loc_1179C

```
01177A  move.w	#$CF36,a1
01177E  move.w	#$CF36,a3
011782  move.w	#$CF32,a4
011786  move.l	#loc_10EE0,a5
01178C  move.l	#loc_113D0,a6
011792  movem.l	d0-d3/a0-a2,-(sp)
011796  move.w	d1,d3
011798  clr.w	d1
01179A  clr.w	d2
01179C  move.b	(a0)+,d0
01179E  and.w	#$F0,d0
0117A2  lsr.w	#3,d0
0117A4  lea	word_117B2(pc),a2
0117A8  move.w	(a2,d0.w),d0
0117AC  jsr	(a2,d0.w)
0117B0  bra.s	loc_1179C
```

## `$012DDE` -> `ai_PrintPenaltyList`  (confidence 0.7, 16 insns)

**Evidence.** walks the penalized-player list $9A(a2) twice, printing minors (status $66 bit 6 clear) first and majors second with ai_PrintPenaltyRow; caller loc_12DA6 (penalty box display)

**Callers.** loc_12DA6
**Callees.** ai_PrintPenaltyRow, loc_12DE2, loc_12DFC

```
012DDE  lea	$9A(a2),a0
012DE2  clr.w	d0
012DE4  move.b	(a0)+,d0
012DE6  bmi.w	loc_12DF8
012DEA  btst	#6,$66(a2,d0.w)
012DF0  bne.s	loc_12DE2
012DF2  bsr.w	sub_12E12
012DF6  bra.s	loc_12DE2
012DF8  lea	$9A(a2),a0
012DFC  clr.w	d0
012DFE  move.b	(a0)+,d0
012E00  bmi.w	locret_15464
012E04  btst	#6,$66(a2,d0.w)
012E0A  beq.s	loc_12DFC
012E0C  bsr.w	sub_12E12
012E10  bra.s	loc_12DFC
```

## `$0F7BFA` -> `ai_PrintSetupModeRow`  (confidence 0.5, 16 insns)

**Evidence.** setup screen: prints at column 2 row $19 the 'Continue Playoffs' text off_F7C5A (when the scroll is at 3 or the playoff state is 4) or 'Regular Season' off_F7C56, then at row $F the off_F7C5A / off_F7C52 line depending on whether the menu is scrolled; caller ai_RedrawSetupValues

**Callers.** ai_RedrawSetupValues
**Callees.** print
**Strings.** New York Islanders | New York Rangers |  | N/A | Regular Season | Continue Playoffs
**RAM.** OptPlayMode, printx, printy

```
0F7BFA  move.w	#$19,($FFFFB02A).w
0F7C00  move.l	#off_F7C5A,a1
0F7C06  cmp.w	#3,($FFFFD422).w
0F7C0C  beq.w	loc_F7C20
0F7C10  cmp.w	#4,($FFFFD048).w
0F7C16  beq.w	loc_F7C20
0F7C1A  move.l	#off_F7C56,a1
0F7C20  move.w	#2,($FFFFB028).w
0F7C26  jsr	sub_11BA4
0F7C2C  move.l	#off_F7C5A,a1
0F7C32  move.w	#$F,($FFFFB02A).w
0F7C38  tst.w	($FFFFD422).w
0F7C3C  beq.w	loc_F7C46
0F7C40  move.l	#off_F7C52,a1
0F7C46  move.w	#2,($FFFFB028).w
0F7C4C  jmp	sub_11BA4
```

## `$00A448` -> `ai_DrawRinkAuxBitmap`  (confidence 0.3, 15 insns)

**Evidence.** game init (sub_A528): sets $DEB4 = $F0 and draws an 8x4-tile bitmap at column $20 row $55 (beyond the visible rows of the plane) from the second block of off_5605A, or off_B5180 when $C2F4 bit 4 is set, at tile base rinkvrcset; which on-screen element this becomes is not identified; caller sub_A528

**Callers.** sub_A528
**Callees.** dobitmap, printz
**RAM.** rinkvrcset

```
00A448  move.w	#$F0,($FFFFDEB4).w
00A44E  bsr.w	sub_11B92
00A452  dc.w	6
00A454  dc.b	$BD
00A455  dc.b	2
00A456  dc.b	2
00A457  dc.b	0
00A458  moveq	#$20,d0
00A45A  moveq	#$55,d1
00A45C  moveq	#8,d2
00A45E  moveq	#4,d3
00A460  move.w	($FFFFB018).w,d4
00A464  move.w	#0,d5
00A468  move.l	#off_5605A,a1
00A46E  btst	#4,($FFFFC2F4).w
00A474  beq.w	loc_A47E
00A478  move.l	#off_B5180,a1
00A47E  add.l	4(a1),a1
00A482  move.w	#$30A,a2
00A486  bra.w	sub_1169A
```

## `$010EB4` -> `ai_WeightedRandomIndex`  (confidence 0.8, 15 insns)

**Evidence.** d0 = entry count: sums the weight words at $D036, draws a random number below the sum (sub_11086) and walks back through the weights until it goes negative, returning the chosen index in d0; caller getscore (shot outcome selection)

**Callers.** getscore
**Callees.** loc_10EC4, randomd0

```
010EB4  movem.l	d1/a1,-(sp)
010EB8  move.w	#$D036,a1
010EBC  clr.w	d1
010EBE  bra.w	loc_10EC4
010EC2  add.w	(a1)+,d1
010EC4  dbf	d0,loc_10EC2
010EC8  move.w	d1,d0
010ECA  bsr.w	sub_11086
010ECE  sub.w	-(a1),d0
010ED0  bpl.s	loc_10ECE
010ED2  suba.w	#$D036,a1
010ED6  move.w	a1,d0
010ED8  lsr.w	#1,d0
010EDA  movem.l	(sp)+,d1/a1
010EDE  rts
```

