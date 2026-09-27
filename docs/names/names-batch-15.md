# Name review: names-batch-15.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$018002` -> `ai_SeedPlayoffBracket`  (confidence 0.6, 15 insns)

**Evidence.** FigureJoy: sets the series index $CEE6 to -1, builds a bit mask of the two user teams (HomeTeam, VisTeam) in d3, then fills the eight series records at $CE66 ($10 bytes apart) with two teams each drawn by sub_18032 (random team not yet in the mask); caller FigureJoy

**Callers.** FigureJoy
**Callees.** OptionRNG
**RAM.** HomeTeam, VisTeam, gamenum

```
018002  st	($FFFFCEE6).w
018006  clr.l	d3
018008  move.w	($FFFFC330).w,d1
01800C  bset	d1,d3
01800E  move.w	($FFFFC332).w,d1
018012  bset	d1,d3
018014  move.w	#$CE66,a1
018018  moveq	#7,d2
01801A  bsr.w	sub_18032
01801E  move.w	d0,(a1)
018020  bsr.w	sub_18032
018024  move.w	d0,2(a1)
018028  add.w	#$10,a1
01802C  dbf	d2,loc_1801A
018030  rts
```

## `$017E04` -> `ai_SetSeriesTeams`  (confidence 0.6, 14 insns)

**Evidence.** MakeTree: copies the next two team bytes from a0 into the series record a1 (+1 and +3) and sets or clears the home-advantage bit 0 of +$E, with the order swapped when bosgames is 2, 3 or 5; caller MakeTree

**Callers.** MakeTree
**Callees.** none
**RAM.** bosgames

```
017E04  cmp.w	#2,($FFFFCEEA).w
017E0A  beq.w	loc_17E32
017E0E  cmp.w	#3,($FFFFCEEA).w
017E14  beq.w	loc_17E32
017E18  cmp.w	#5,($FFFFCEEA).w
017E1E  beq.w	loc_17E32
017E22  bset	#0,$E(a1)
017E28  move.b	(a0)+,3(a1)
017E2C  move.b	(a0)+,1(a1)
017E30  rts
017E32  bclr	#0,$E(a1)
017E38  move.b	(a0)+,1(a1)
017E3C  move.b	(a0)+,3(a1)
017E40  rts
```

## `$017626` -> `ai_DrawPlayoffTreeBitmap`  (confidence 0.6, 14 insns)

**Evidence.** PlayoffScreen: draws the bracket background bitmap unk_B3640 (2 columns x $17 rows) with dobitmap at tile base $B026; caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** dobitmap
**RAM.** ExtraChars

```
017626  movem.l	d0-a3,-(sp)
01762A  move.l	#unk_B3640,a0
017630  move.l	a0,a1
017632  add.l	(a0),a0
017634  add.l	4(a1),a1
017638  move.w	#$30A,a2
01763C  clr.w	d1
01763E  moveq	#2,d2
017640  moveq	#$17,d3
017642  move.w	($FFFFB026).w,d4
017646  moveq	#0,d5
017648  bsr.w	sub_1169A
01764C  movem.l	(sp)+,d0-a3
017650  rts
```

## `$0F7864` -> `ai_PositionSetupCursor`  (confidence 0.6, 15 insns)

**Evidence.** ai_MoveSetupCursor helper: sets the print row to $E + cursor row d3 - 2*scroll ($D422) after the inline attribute string, and returns the cursor box size d0 = $17, d1 = 3 (5 for row 4 in playoff states 2 and 3, the taller 'Continue Playoffs' entry); caller ai_MoveSetupCursor

**Callers.** ai_MoveSetupCursor
**Callees.** printz
**RAM.** OptPlayMode, printy

```
0F7864  jsr	sub_11B92
0F786A  dc.w	6
0F786C  dc.b	$FF
0F786D  dc.b	$10
0F786E  dc.b	$E
0F786F  dc.b	0
0F7870  add.w	d3,($FFFFB02A).w
0F7874  move.w	($FFFFD422).w,d0
0F7878  add.w	d0,d0
0F787A  sub.w	d0,($FFFFB02A).w
0F787E  moveq	#$17,d0
0F7880  moveq	#3,d1
0F7882  cmp.w	#2,($FFFFD048).w
0F7888  blt.w	locret_F78A0
0F788C  cmp.w	#4,($FFFFD048).w
0F7892  beq.w	locret_F78A0
0F7896  cmpnw	 4,d3
0F789A  bne.w	locret_F78A0
0F789E  moveq	#5,d1
0F78A0  rts
```

## `$0FD14A` -> `ai_LoadPlayerPhoto`  (confidence 0.7, 15 insns)

**Evidence.** a0 = photo asset from ai_GetPlayerPhoto: resolves its two block offsets (using the generic blocks of off_C63F8 when the second offset is zero), decodes the tiles with ai_UnpackPhotoTiles into $DA1E and joins the 6x6 drawing tail at loc_FD1A4 shared with ai_DrawTeamLogo6x6; caller ai_DrawRatingsPictures

**Callers.** ai_DrawRatingsPictures
**Callees.** ai_UnpackPhotoTiles, loc_FD170, loc_FD1A4

```
0FD14A  move.l	a0,a1
0FD14C  move.l	a0,a2
0FD14E  add.l	(a2)+,a0
0FD150  move.l	#off_C63F8,a0
0FD156  add.l	(a0),a0
0FD158  tst.l	(a2)
0FD15A  bne.w	loc_FD16E
0FD15E  move.l	#off_C63F8,a1
0FD164  add.l	4(a1),a1
0FD168  tst.l	(a2)+
0FD16A  bra.w	loc_FD170
0FD16E  add.l	(a2)+,a1
0FD170  bsr.w	sub_FE98A
0FD174  move.l	#$FFFFDA1E,a2
0FD17A  bra.w	loc_FD1A4
```

## `$007A34` -> `ai_TriggerPeriodSong`  (confidence 0.5, 14 insns)

**Evidence.** periodiceevents: in period 2 (gsp), unless $C2EA bit 4, once gameclock has counted down to the threshold in $B048 marks it done (-1), sets HmTeam = HomeTeam and SongIndex = 5, picks the song with ChooseSong and starts it via sub_11156 with $D6C8; caller periodiceevents

**Callers.** periodiceevents
**Callees.** ChooseSong, song
**RAM.** HmTeam, HomeTeam, SongIndex, SongNum, gameclock, gmode, gsp

```
007A34  cmp.w	#2,($FFFFC466).w
007A3A  bne.w	locret_7A74
007A3E  btst	#4,($FFFFC2EA).w
007A44  bne.w	locret_7A74
007A48  move.w	($FFFFC468).w,d0
007A4C  cmp.w	($FFFFB048).w,d0
007A50  bgt.w	locret_7A74
007A54  st	($FFFFB048).w
007A58  move.w	($FFFFC330).w,($FFFFD6CA).w
007A5E  move.w	#5,($FFFFD6CC).w
007A64  jsr	sub_FE556
007A6A  move.w	($FFFFD6C8).w,-(sp)
007A6E  jsr	sub_11156
007A74  rts
```

## `$00904C` -> `ai_PrintSummaryRowAt`  (confidence 0.6, 14 insns)

**Evidence.** scoring summary page: prints entry (d0 high word + 4) * 6 of ScoreSum at the row derived from VertLineScrolling (/8 + $10, mod 32) through ai_PrintScoringSummaryRow; caller sub_8FB8 (summary page handler, together with sub_9020 for row 30)

**Callers.** sub_8FB8
**Callees.** ai_PrintScoringSummaryRow, printz
**RAM.** VertLineScrolling, printy

```
00904C  move.l	d0,-(sp)
00904E  swap	d0
009050  addq.w	#4,d0
009052  moveq	#6,d3
009054  mulu.w	d0,d3
009056  jsr	sub_11B92
00905C  dc.w	6
00905E  dc.b	$BE
00905F  dc.b	0
009060  dc.b	0
009061  dc.b	0
009062  move.w	($FFFFD5AE).w,d0
009066  lsr.w	#3,d0
009068  add.w	#$10,d0
00906C  and.w	#$1F,d0
009070  move.w	d0,($FFFFB02A).w
009074  bsr.w	sub_907C
009078  move.l	(sp)+,d0
00907A  rts
```

## `$011EDA` -> `ai_WriteBigFontTile`  (confidence 0.7, 14 insns)

**Evidence.** ai_PrintBigChar helper: writes the name-table word d3 + d6 (tile plus attribute) at plane position (row d5 << width-shift + column d4) * 2 in the plane described at $B004 + printm; caller ai_PrintBigChar

**Callers.** ai_PrintBigChar
**Callees.** Vmaddr
**RAM.** printm

```
011EDA  add.w	d6,d3
011EDC  movem.l	d1/a0,-(sp)
011EE0  move.w	d5,d0
011EE2  move.l	#$FFFFB004,a0
011EE8  add.w	($FFFFB02E).w,a0
011EEC  move.w	2(a0),d1
011EF0  asl.w	d1,d0
011EF2  add.w	d4,d0
011EF4  asl.w	#1,d0
011EF6  add.w	(a0),d0
011EF8  bsr.w	VDP_SetAddress
011EFC  move.w	d3,(a0)
011EFE  movem.l	(sp)+,d1/a0
011F02  rts
```

## `$01674A` -> `ai_EmitLabelTile`  (confidence 0.6, 14 insns)

**Evidence.** ai_BuildPlayerLabelSprites helper: appends one entry (pointer to tile d2 of Art_BoardText, size $10, x = (d0 + $12(a0)) * 32) to the label list at a5; caller ai_BuildPlayerLabelSprites

**Callers.** ai_BuildPlayerLabelSprites
**Callees.** none

```
01674A  move.l	#Art_BoardText,a3
016750  add.l	4(a3),a3
016754  add.w	d2,d2
016756  move.w	4(a3,d2.w),d2
01675A  and.w	#$7FF,d2
01675E  asl.w	#5,d2
016760  move.l	#Art_BoardText,a3
016766  lea	$A(a3,d2.w),a3
01676A  move.l	a3,(a5)+
01676C  move.w	#$10,(a5)+
016770  add.w	$12(a0),d0
016774  asl.w	#5,d0
016776  move.w	d0,(a5)+
016778  rts
```

## `$013454` -> `ai_PrintTickerTeamScore`  (confidence 0.6, 14 insns)

**Evidence.** NewTicker3pt2 helper: at the column passed on the stack and the next row prints team d0's name (team table $30E, name at +4) and, $15 columns to the right, the score d1 as a 2-digit number; caller NewTicker3pt2

**Callers.** NewTicker3pt2
**Callees.** DeterStrLength?, print
**Strings.** EA Hockey Night | Stanley Cup Qualifier | Quarterfinal | Stanley Cup Semifinal
**RAM.** printx, printy

```
013454  arg_0		=	4
013454  move.w	arg_0(sp),($FFFFB028).w
01345A  addq.w	#1,($FFFFB02A).w
01345E  move.w	#$30E,a1
013462  asl.w	#2,d0
013464  move.l	(a1,d0.w),a1
013468  add.w	4(a1),a1
01346C  bsr.w	sub_11BA4
013470  move.w	arg_0(sp),($FFFFB028).w
013476  add.w	#$15,($FFFFB028).w
01347C  move.w	d1,d0
01347E  moveq	#2,d1
013480  bsr.w	sub_11D3A
013484  bra.w	sub_11BA4
```

## `$0FD5AE` -> `ai_GetTeamNameOrSide`  (confidence 0.5, 14 insns)

**Evidence.** ticker helper: for team record a2 returns a1 = its name string unless the name entry is empty (length word 2), in which case it returns 'Home' (word_FD5E4) for the home record or 'Visitors' (word_FD5EA); caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none
**Strings.** Home | Visitors

```
0FD5AE  movem.l	d0/a0/a2,-(sp)
0FD5B2  move.l	a2,a1
0FD5B4  move.l	$1E(a1),a1
0FD5B8  add.w	4(a1),a1
0FD5BC  add.w	(a1),a1
0FD5BE  add.w	(a1),a1
0FD5C0  cmp.w	#2,(a1)
0FD5C4  bne.w	loc_FD5DE
0FD5C8  move.l	#word_FD5E4,a1
0FD5CE  cmp.l	#$FFFFC6CE,a2
0FD5D4  beq.w	loc_FD5DE
0FD5D8  move.l	#word_FD5EA,a1
0FD5DE  movem.l	(sp)+,d0/a0/a2
0FD5E2  rts
```

## `$0FB89E` -> `ai_RedrawUserListRow`  (confidence 0.4, 14 insns)

**Evidence.** user list screen: if a previous selection $D4EC exists, reprints that row (row 8 + index - 1) with the text at a1 and the following string at column $12 (restoring its unhighlighted look), then records the current selection $D4EA as the previous one; caller sub_FB874

**Callers.** sub_FB874
**Callees.** print, printz
**RAM.** printx, printy

```
0FB89E  tst.w	($FFFFD4EC).w
0FB8A2  beq.w	loc_FB8D4
0FB8A6  jsr	sub_11B92
0FB8AC  dc.w	6
0FB8AE  dc.b	$BF
0FB8AF  dc.b	3
0FB8B0  dc.b	8
0FB8B1  dc.b	0
0FB8B2  move.w	($FFFFD4EC).w,d0
0FB8B6  subq.w	#1,d0
0FB8B8  add.w	d0,($FFFFB02A).w
0FB8BC  move.l	a1,-(sp)
0FB8BE  jsr	sub_11BA4
0FB8C4  move.l	(sp)+,a1
0FB8C6  add.w	(a1),a1
0FB8C8  move.w	#$12,($FFFFB028).w
0FB8CE  jsr	sub_11BA4
0FB8D4  move.w	($FFFFD4EA).w,($FFFFD4EC).w
0FB8DA  rts
```

## `$0FECAA` -> `ai_PickFaceoffSpot`  (confidence 0.5, 14 insns)

**Evidence.** puckfaceoff: draws a random index 0..7 into the table unk_FECE6 and returns its word in d0, unless the faceoff location fox/foy ($BF94/$BF96) lies within -$C0..$C0 of centre, which forces d0 = 6 (the centre-ice case); caller puckfaceoff

**Callers.** puckfaceoff
**Callees.** randomd0
**RAM.** fox, foy

```
0FECAA  movem.l	a0,-(sp)
0FECAE  move.l	#unk_FECE6,a0
0FECB4  move.w	#$64,d0
0FECB8  jsr	sub_11086
0FECBE  and.w	#7,d0
0FECC2  add.w	d0,d0
0FECC4  move.w	(a0,d0.w),d0
0FECC8  cmp.w	#$FFC0,($FFFFBF94).w
0FECCE  bgt.w	loc_FECE0
0FECD2  cmp.w	#$C0,($FFFFBF96).w
0FECD8  bgt.w	loc_FECE0
0FECDC  move.w	#6,d0
0FECE0  movem.l	(sp)+,a0
0FECE4  rts
```

## `$0FF88E` -> `ai_ClearPenaltyState`  (confidence 0.6, 14 insns)

**Evidence.** clockcont: clears the penalty timers Penaltytimer/Pencntdwn/PBnum ($C3EA/$C3E8/$C3E6) and the $44-byte penalty message buffer at $C3A4, then resets each team's penalty data with sub_FF8C8; caller clockcont

**Callers.** clockcont
**Callees.** clrTmPdst
**RAM.** PBnum, Penaltytimer, Pencntdwn

```
0FF88E  movem.l	d0/a0,-(sp)
0FF892  clr.w	($FFFFC3EA).w
0FF896  clr.w	($FFFFC3E8).w
0FF89A  clr.w	($FFFFC3E6).w
0FF89E  move.w	#$10,d0
0FF8A2  move.l	#$FFFFC3A4,a0
0FF8A8  clr.l	(a0)+
0FF8AA  dbf	d0,loc_FF8A8
0FF8AE  move.l	#$FFFFC6CE,a0
0FF8B4  bsr.w	sub_FF8C8
0FF8B8  move.l	#$FFFFCA32,a0
0FF8BE  bsr.w	sub_FF8C8
0FF8C2  movem.l	(sp)+,d0/a0
0FF8C6  rts
```

