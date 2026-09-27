# Name review: names-batch-26.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FBD86` -> `ai_PrintUserRecordsTitle`  (confidence 0.6, 9 insns)

**Evidence.** prints the user-records page title by the mode $BF12: word_FBDB2 ('ALL win records') when 0, word_FBE54 when 2, otherwise word_FBE04 (the 'O QUALIFY' variants)

**Callers.** none found
**Callees.** print2
**Strings.** ALL win recordsý | O QUALIFY    ý | O QUALIFY    ý

```
0FBD86  move.l	#word_FBDB2,a1
0FBD8C  tst.w	($FFFFBF12).w
0FBD90  beq.w	loc_FBDAA
0FBD94  move.l	#word_FBE54,a1
0FBD9A  cmp.w	#2,($FFFFBF12).w
0FBDA0  beq.w	loc_FBDAA
0FBDA4  move.l	#word_FBE04,a1
0FBDAA  jsr	sub_11A48
0FBDB0  rts
```

## `$0FBD7A` -> `ai_DispatchUserRecordsPage`  (confidence 0.6, 3 insns)

**Evidence.** branches on the user-records mode $BF12: 0 goes to the standings printer (ai_PrintUserStandings), anything else to loc_FBFDE

**Callers.** none found
**Callees.** loc_FBFDE

```
0FBD7A  tst.w	($FFFFBF12).w
0FBD7E  beq.w	loc_FBEA4
0FBD82  bra.w	loc_FBFDE
```

## `$009F7E` -> `ai_GetGoalieCount`  (confidence 0.5, 8 insns)

**Evidence.** returns the high nibble of byte 3 of the team data block at offset +8 (the roster count word; ai_CountRatingNibblesPlusGoalies adds the same value), believed to be the number of goalies

**Callers.** none found
**Callees.** none

```
009F7E  movem.l	a0,-(sp)
009F82  move.l	$1E(a2),a0
009F86  add.w	8(a0),a0
009F8A  move.b	3(a0),d0
009F8E  lsr.w	#4,d0
009F90  and.w	#$F,d0
009F94  movem.l	(sp)+,a0
009F98  rts
```

## `$0137FC` -> `ai_ResetLinesForFaceoff`  (confidence 0.5, 8 insns)

**Evidence.** refills the line energy (ai_ResetLineEnergy), re-applies the personnel (SetPersonel), sub_159A8, then sets team a2's +$18/+$1A/+$1C flags to -1 and clears $C2FE bit 7

**Callers.** none found
**Callees.** SetPersonel, ai_ResetLineEnergy, forcepldata

```
0137FC  jsr	sub_130BE
013802  bsr.w	sub_15788
013806  bsr.w	sub_159A8
01380A  st	$18(a2)
01380E  bclr	#7,($FFFFC2FE).w
013814  st	$1A(a2)
013818  st	$1C(a2)
01381C  rts
```

## `$011B28` -> `ai_PrintCtl_SetPlane`  (confidence 0.6, 7 insns)

**Evidence.** print control-code handler: takes the next byte & 3, converts it to the plane descriptor offset (4*n - 4) in printm ($B02E) and continues with xyVmMap; one of the $F8..$FF control codes of the inline print strings

**Callers.** none found
**Callees.** xyVmMap
**RAM.** printm

```
011B28  move.b	(a1)+,d0
011B2A  subq.w	#1,d3
011B2C  and.w	#3,d0
011B30  asl.w	#2,d0
011B32  subq.w	#4,d0
011B34  move.w	d0,($FFFFB02E).w
011B38  bra.w	sub_11952
```

## `$011B3C` -> `ai_PrintCtl_SetPalette`  (confidence 0.6, 6 insns)

**Evidence.** print control-code handler: takes the next byte & 7 rotated into bits 13..15 as the palette/priority attribute printa ($B02C)

**Callers.** none found
**Callees.** none
**RAM.** printa

```
011B3C  move.b	(a1)+,d2
011B3E  and.w	#7,d2
011B42  subq.w	#1,d3
011B44  ror.w	#3,d2
011B46  move.w	d2,($FFFFB02C).w
011B4A  rts
```

## `$011B4C` -> `ai_PrintCtl_SetColumn`  (confidence 0.6, 5 insns)

**Evidence.** print control-code handler: takes the next byte as printx and recomputes the VRAM position with xyVmMap

**Callers.** none found
**Callees.** xyVmMap
**RAM.** printx

```
011B4C  clr.w	d0
011B4E  move.b	(a1)+,d0
011B50  subq.w	#1,d3
011B52  move.w	d0,($FFFFB028).w
011B56  bra.w	sub_11952
```

## `$013862` -> `ai_RestoreGameState`  (confidence 0.6, 7 insns)

**Evidence.** inverse of ai_SnapshotGameState: copies the $5BE words saved at $FF0000 back to $C2EA and restores ScoreSumbytes; run after a highlight replay

**Callers.** none found
**Callees.** none
**RAM.** ScoreSumbytes

```
013862  move.w	#$5BD,d0
013866  move.w	#$C2EA,a2
01386A  move.l	#$FFFF0000,a1
013870  move.w	(a1)+,(a2)+
013872  dbf	d0,loc_13870
013876  move.w	(a1)+,($FFFFC472).w
01387A  rts
```

## `$008B04` -> `ai_ScrollEditLinesPagesCheck`  (confidence 0.5, 6 insns)

**Evidence.** entry of the edit-lines page scroller: applies PlayerScrollCtr to VertLineScrolling and, within 0..$380, continues into ai_ScrollEditLinesPages; otherwise loc_8B7E

**Callers.** none found
**Callees.** none
**RAM.** PlayerScrollCtr, VertLineScrolling

```
008B04  move.w	($FFFFD5B0).w,d0
008B08  beq.w	locret_A9D4
008B0C  add.w	($FFFFD5AE).w,d0
008B10  bmi.w	loc_8B7E
008B14  cmpnw	 $380,d0
008B18  bgt.w	loc_8B7E
```

## `$008FA0` -> `ai_ScrollSummaryListCheck`  (confidence 0.5, 6 insns)

**Evidence.** entry of the scoring-summary scroller: applies PlayerScrollCtr to VertLineScrolling and, within 0..$D5B2, continues into ai_ScrollSummaryList

**Callers.** none found
**Callees.** none
**RAM.** PlayerScrollCtr, VertLineScrolling

```
008FA0  move.w	($FFFFD5B0).w,d0
008FA4  beq.w	locret_A9D4
008FA8  add.w	($FFFFD5AE).w,d0
008FAC  bmi.w	locret_A9D4
008FB0  cmp.w	($FFFFD5B2).w,d0
008FB4  bgt.w	locret_A9D4
```

## `$0FB77A` -> `ai_PrintEntryCursorMarker`  (confidence 0.5, 6 insns)

**Evidence.** name entry: positions at column 4 + d4 on row $13 and, when the blink flag $D6C4 is set, prints ' < ' as the cursor marker under the current letter

**Callers.** none found
**Callees.** printz
**RAM.** printx

```
0FB77A  jsr	sub_11B92
0FB780  dc.w	6
0FB782  dc.b	$BF
0FB783  dc.b	4
0FB784  dc.b	$13
0FB785  dc.b	0
0FB786  add.w	d4,($FFFFB028).w
0FB78A  tst.w	($FFFFD6C4).w
0FB78E  beq.w	locret_FB79E
0FB792  jsr	sub_11B92
0FB798  dc.w	6
0FB79A  dc.b	$20
0FB79B  dc.b	$3C
0FB79C  dc.b	$20
0FB79D  dc.b	0
0FB79E  rts
```

## `$00A48A` -> `ai_EraseCornerBox8x4`  (confidence 0.4, 5 insns)

**Evidence.** positions at (2,2) with attribute $BD and erases an 8x4 area

**Callers.** none found
**Callees.** eraser, printz

```
00A48A  jsr	sub_11B92
00A490  dc.w	6
00A492  dc.b	$BD
00A493  dc.b	2
00A494  dc.b	2
00A495  dc.b	0
00A496  move.w	#8,d0
00A49A  move.w	#4,d1
00A49E  move.w	#$7FF,d2
00A4A2  jmp	sub_1197E
```

## `$00A4D8` -> `ai_EraseCornerBox16x11`  (confidence 0.4, 5 insns)

**Evidence.** positions at (2,2) with attribute $BD and erases a 16x11 area (the pause menu backdrop size of ai_DrawPauseMenuBackdrop)

**Callers.** none found
**Callees.** eraser, printz

```
00A4D8  jsr	sub_11B92
00A4DE  dc.w	6
00A4E0  dc.b	$BD
00A4E1  dc.b	2
00A4E2  dc.b	2
00A4E3  dc.b	0
00A4E4  move.w	#$10,d0
00A4E8  move.w	#$B,d1
00A4EC  move.w	#$7FF,d2
00A4F0  jmp	sub_1197E
```

## `$0FAD84` -> `ai_PrintSavesBox`  (confidence 0.5, 5 insns)

**Evidence.** records screen: reads the selected team's goalie totals for player d0 (column +$B4 and following) and prints the 'Saves' / 'Save %' box (extent truncated in the IDA database after the first read)

**Callers.** none found
**Callees.** ai_GetRecordsTeam
**Strings.** Saves | Save %

```
0FAD84  movem.l	d0-a6,-(sp)
0FAD88  bsr.w	sub_FAF50
0FAD8C  move.l	a0,-(sp)
0FAD8E  add.l	#$B4,a0
0FAD94  move.b	(a0,d0.w),d3
```

## `$0FB97C` -> `ai_DrawBoxWithEntryFrame`  (confidence 0.5, 5 insns)

**Evidence.** draws a box with sub_119B8 using the alternate frame tile base $D530 in place of $B01E, restoring it afterwards; name-entry screen frame

**Callers.** none found
**Callees.** Framer
**RAM.** framercset

```
0FB97C  move.w	($FFFFB01E).w,-(sp)
0FB980  move.w	($FFFFD530).w,($FFFFB01E).w
0FB986  jsr	sub_119B8
0FB98C  move.w	(sp)+,($FFFFB01E).w
0FB990  rts
```

## `$0FEE4A` -> `ai_GetTeamRecordById`  (confidence 0.7, 5 insns)

**Evidence.** returns a2 = the home record when its team id $28 equals d2, else the away record

**Callers.** none found
**Callees.** none

```
0FEE4A  move.l	#$FFFFC6CE,a2
0FEE50  cmp.w	$28(a2),d2
0FEE54  beq.w	locret_FEE5E
0FEE58  move.l	#$FFFFCA32,a2
0FEE5E  rts
```

## `$015E72` -> `ai_FlushSpriteTable`  (confidence 0.6, 4 insns)

**Evidence.** DMAs the sprite list at $C018 ($C2E8 entries) to the sprite table VRAM address $B002 through sub_113E4; part of the attract-mode V-blank routine

**Callers.** none found
**Callees.** DoDMA
**RAM.** VSPRITES

```
015E72  move.w	#$C018,a0
015E76  move.w	($FFFFC2E8).w,d0
015E7A  move.w	($FFFFB002).w,d1
015E7E  bsr.w	sub_113E4
```

## `$015E6E` -> `ai_AttractVBlankScroll`  (confidence 0.5, 1 insns)

**Evidence.** writes the plane scroll (ai_WritePlaneScroll) and falls into ai_FlushSpriteTable; the V-blank tail used on the attract/menu screens

**Callers.** none found
**Callees.** ai_WritePlaneScroll

```
015E6E  bsr.w	sub_15EA4
```

## `$018B5E` -> `ai_FormatPlayerSurnameOnly`  (confidence 0.5, 4 insns)

**Evidence.** finds the player's record (sub_18BC8) and joins ai_FormatPlayerSurnamePadded's copy loop at loc_18B7E without the leading space

**Callers.** none found
**Callees.** getplayername, loc_18B7E

```
018B5E  movem.l	d0-d3/a0/a2,-(sp)
018B62  bsr.w	sub_18BC8
018B66  move.w	#$BFA6,a1
018B6A  bra.w	loc_18B7E
```

## `$0FEAE4` -> `ai_PrintAssistsInParens`  (confidence 0.7, 4 insns)

**Evidence.** assist twin of ai_PrintGoalsInParens: prints ' (' then joins its body with the team's +$CE (assists) column

**Callers.** none found
**Callees.** loc_FEB0C, printz

```
0FEAE4  movem.l	d0/a2,-(sp)
0FEAE8  jsr	sub_11B92
0FEAEE  dc.w	4
0FEAF0  dc.b	' ('
0FEAF2  add.w	#$CE,a2
0FEAF6  bra.w	loc_FEB0C
```

## `$00878E` -> `ai_ClearIndicatorPair`  (confidence 0.4, 3 insns)

**Evidence.** clears the two words $BD82 and $BDA2 (fields of the second and third indicator records at $BDB4 - $1C*n... i.e. per-controller cursor state); byte-identical to ai_ClearIndicatorPair2

**Callers.** none found
**Callees.** none

```
00878E  clr.w	($FFFFBD82).w
008792  clr.w	($FFFFBDA2).w
008796  rts
```

## `$0FCA1E` -> `ai_ClearIndicatorPair2`  (confidence 0.4, 3 insns)

**Evidence.** clears $BD82 and $BDA2, byte-identical to ai_ClearIndicatorPair; shootout screen variant

**Callers.** none found
**Callees.** none

```
0FCA1E  clr.w	($FFFFBD82).w
0FCA22  clr.w	($FFFFBDA2).w
0FCA26  rts
```

## `$016CEE` -> `ai_LoadMenuTiles5C410`  (confidence 0.4, 3 insns)

**Evidence.** loads asset unk_5C410 at tile base ExtraChars ($B026)

**Callers.** none found
**Callees.** ai_LoadAsset
**RAM.** ExtraChars

```
016CEE  move.w	($FFFFB026).w,d4
016CF2  move.l	#unk_5C410,a2
016CF8  bra.w	sub_11738
```

## `$016CFC` -> `ai_LoadTilesA78B6`  (confidence 0.4, 3 insns)

**Evidence.** loads asset unk_A78B6 at tile base $B01C

**Callers.** none found
**Callees.** ai_LoadAsset

```
016CFC  move.w	($FFFFB01C).w,d4
016D00  move.l	#unk_A78B6,a2
016D06  bra.w	sub_11738
```

## `$016D0A` -> `ai_LoadMenuTiles55BFE`  (confidence 0.4, 3 insns)

**Evidence.** loads asset unk_55BFE at tile base ExtraChars ($B026)

**Callers.** none found
**Callees.** ai_LoadAsset
**RAM.** ExtraChars

```
016D0A  move.w	($FFFFB026).w,d4
016D0E  move.l	#unk_55BFE,a2
016D14  bra.w	sub_11738
```

## `$0FB6DC` -> `ai_NameEntryFragment`  (confidence 0.3, 2 insns)

**Evidence.** IDA marks a function at $FB6DC whose body in the listing begins with data; only the register restore and rts at $FB6EA..$FB6EE are code; a fragment of the name-entry code

**Callers.** none found
**Callees.** none

```
0FB6EA  movem.l	(sp)+,d0-a6
0FB6EE  rts
```

## `$0FCB1A` -> `ai_PrintShootoutFragment`  (confidence 0.3, 2 insns)

**Evidence.** saves registers and prints an inline string (extent truncated in the IDA database after the print2 call); part of the shootout screen printers

**Callers.** none found
**Callees.** printz2

```
0FCB1A  movem.l	d0-a6,-(sp)
0FCB1E  jsr	sub_11A36
```

## `$0FA934` -> `ai_NopRecords`  (confidence 0.8, 1 insns)

**Evidence.** a bare rts sitting before the 'Starting Line' / position strings of the records screen; an empty hook

**Callers.** none found
**Callees.** none
**Strings.** Starting Line | G | LD | RD | LW | C

```
0FA934  rts
```

