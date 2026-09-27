# Name review: names-batch-25.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FB722` -> `ai_SnapEntryCharToAlphabet`  (confidence 0.6, 12 insns)

**Evidence.** name entry: converts the current character $D4DA to its alphabet index (ai_CharToEntryIndex); an unknown character becomes index 0 ('A'), otherwise the character is rewritten from the alphabet table so it is canonical; returns the index in d5

**Callers.** none found
**Callees.** ai_CharToEntryIndex, loc_FB74A

```
0FB722  movem.l	d0-d4/a0-a6,-(sp)
0FB726  move.b	($FFFFD4DA).w,d0
0FB72A  bsr.w	sub_FB750
0FB72E  cmpnw	 $1E,d0
0FB732  blt.w	loc_FB73C
0FB736  clr.w	d5
0FB738  bra.w	loc_FB74A
0FB73C  move.w	d0,d5
0FB73E  move.l	#aAbcdefghijklmnopqrstu,a0
0FB744  move.b	(a0,d5.w),($FFFFD4DA).w
0FB74A  movem.l	(sp)+,d0-d4/a0-a6
0FB74E  rts
```

## `$0FB7CA` -> `ai_PositionEntryCursor`  (confidence 0.6, 12 insns)

**Evidence.** name entry: positions the letter-grid cursor for alphabet index d5 (row = index / 6 * 2 from row $10, column = index mod 6 * 2 from $18) and returns the 3x3 cursor box size; 'Enter new name:' / 'Select or replace:' strings sit next to it

**Callers.** none found
**Callees.** printz
**Strings.** Enter new name: | Select or replace:
**RAM.** printx, printy

```
0FB7CA  jsr	sub_11B92
0FB7D0  dc.w	6
0FB7D2  dc.b	$BF
0FB7D3  dc.b	$18
0FB7D4  dc.b	$10
0FB7D5  dc.b	0
0FB7D6  move.w	d5,d0
0FB7D8  ext.l	d0
0FB7DA  divu.w	#6,d0
0FB7DE  asl.w	#1,d0
0FB7E0  add.w	d0,($FFFFB02A).w
0FB7E4  swap	d0
0FB7E6  asl.w	#1,d0
0FB7E8  add.w	d0,($FFFFB028).w
0FB7EC  moveq	#3,d0
0FB7EE  moveq	#3,d1
0FB7F0  rts
```

## `$0FB8EC` -> `ai_CountEnteredChars`  (confidence 0.7, 12 insns)

**Evidence.** name entry: counts the characters of the typed name $D4DA up to the first '-' or zero (max 12) into $D4E8

**Callers.** none found
**Callees.** none

```
0FB8EC  movem.l	d0-a6,-(sp)
0FB8F0  move.w	#$B,d3
0FB8F4  move.l	#$FFFFD4DA,a0
0FB8FA  clr.w	($FFFFD4E8).w
0FB8FE  cmp.b	#$2D,(a0)
0FB902  beq.w	loc_FB914
0FB906  tst.b	(a0)+
0FB908  beq.w	loc_FB914
0FB90C  addq.w	#1,($FFFFD4E8).w
0FB910  dbf	d3,loc_FB8FE
0FB914  movem.l	(sp)+,d0-a6
0FB918  rts
```

## `$007DCE` -> `ai_PauseScreenSetup`  (confidence 0.5, 11 insns)

**Evidence.** sets the window/plane registers ($91 = 0, $92 = $1C), calls sub_12B94, fades with sub_15EC0, resets the PSG noise (PSG_SetupNoise), positions at (0,0) via the inline string and erases a 32x28 area, i.e. clears the display for the pause menu

**Callers.** none found
**Callees.** KillCrowd, SetHor, eraser, printz2, setvideo
**Hardware.** VDP data

```
007DCE  move.l	#$C00000,a0
007DD4  move.w	#$9100,4(a0)
007DDA  move.w	#$921C,4(a0)
007DE0  jsr	sub_12B94
007DE6  jsr	sub_15EC0
007DEC  jsr	PSG_SetupNoise
007DF2  jsr	sub_11A36
007DF8  dc.w	8
007DFA  dc.b	$FF
007DFB  dc.b	3
007DFC  dc.b	$FD
007DFD  dc.b	0
007DFE  dc.b	$FC
007DFF  dc.b	0
007E00  moveq	#$20,d0
007E02  moveq	#$1C,d1
007E04  move.w	#$7FF,d2
007E08  jmp	sub_1197E
```

## `$009F5C` -> `ai_CountRatingNibblesPlusGoalies`  (confidence 0.5, 11 insns)

**Evidence.** ai_CountRatingNibbles plus the high nibble of byte 3 of the team data block at offset +8 (the roster count word, believed to hold the goalie count), returning the sum in d0

**Callers.** none found
**Callees.** ai_CountRatingNibbles

```
009F5C  movem.l	a0,-(sp)
009F60  bsr.s	sub_9F40
009F62  move.w	d0,-(sp)
009F64  move.l	$1E(a2),a0
009F68  add.w	8(a0),a0
009F6C  move.b	3(a0),d0
009F70  lsr.w	#4,d0
009F72  and.w	#$F,d0
009F76  add.w	(sp)+,d0
009F78  movem.l	(sp)+,a0
009F7C  rts
```

## `$017AC8` -> `ai_SetPlayoffRoundFromRemaining`  (confidence 0.6, 11 insns)

**Evidence.** in playoff states 2 and 3 sets pojoy ($CEF0) = 7 (or $B with FourWayPlay) minus the rounds remaining $D04A, the inverse of the computation in ai_ApplyPlayoffPassword

**Callers.** none found
**Callees.** none
**RAM.** FourWayPlay, OptNOP, OptPlayMode, pojoy

```
017AC8  cmp.w	#2,($FFFFD048).w
017ACE  blt.w	locret_15464
017AD2  cmp.w	#4,($FFFFD048).w
017AD8  beq.w	locret_15464
017ADC  moveq	#7,d0
017ADE  tst.w	($FFFFD046).w
017AE2  beq.w	loc_17AEA
017AE6  move.w	#$B,d0
017AEA  sub.w	($FFFFD04A).w,d0
017AEE  move.w	d0,($FFFFCEF0).w
017AF2  rts
```

## `$0FB6F0` -> `ai_PrintEntryPrompt`  (confidence 0.6, 11 insns)

**Evidence.** name entry: prints word_FB7F2 ('Enter new name:') when user entry $D4EA is empty in the table $D45A, else word_FB80A ('Select or replace:')

**Callers.** none found
**Callees.** print

```
0FB6F0  movem.l	d0-a6,-(sp)
0FB6F4  move.w	($FFFFD4EA).w,d0
0FB6F8  mulu.w	#$C,d0
0FB6FC  move.l	#$FFFFD45A,a0
0FB702  move.l	#word_FB7F2,a1
0FB708  tst.b	(a0,d0.w)
0FB70C  beq.w	loc_FB716
0FB710  move.l	#word_FB80A,a1
0FB716  jsr	sub_11BA4
0FB71C  movem.l	(sp)+,d0-a6
0FB720  rts
```

## `$013098` -> `ai_ResetLineEnergyExceptOut`  (confidence 0.5, 10 insns)

**Evidence.** variant of ai_ResetLineEnergy: refills all 26 energy words $32+2i of team a2 to $1000 except slots whose status $66+2i is -3 and -4 at once (the unreachable double test means every slot is refilled)

**Callers.** none found
**Callees.** loc_130B8

```
013098  moveq	#$32,d0
01309A  cmp.w	#$FFFD,$66(a2,d0.w)
0130A0  bne.w	loc_130B2
0130A4  cmp.w	#$FFFC,$66(a2,d0.w)
0130AA  bne.w	loc_130B2
0130AE  bra.w	loc_130B8
0130B2  move.w	#$1000,$32(a2,d0.w)
0130B8  subq.w	#2,d0
0130BA  bpl.s	loc_1309A
0130BC  rts
```

## `$0FB634` -> `ai_PrintUserListHelp`  (confidence 0.7, 10 insns)

**Evidence.** prints the user-list instructions 'D-Pad up/down to' / 'move arrows.' at column 2 rows $15/$16 and 'Press START to' / 'select name.' / 'Press B to edit.' below

**Callers.** none found
**Callees.** printz
**Strings.** D-Pad up/down to | move arrows. | Press START to | select name. | Press B to edit.
**RAM.** printx, printy

```
0FB634  movem.l	d0-a6,-(sp)
0FB638  jsr	sub_11B92
0FB63E  dc.w	$1A
0FB640  dc.b	$BF
0FB641  dc.b	2
0FB642  dc.b	$15
0FB643  aDPadUpDownTo:	dc.b	'D-Pad up/down to    ',0
0FB658  jsr	sub_11B92
0FB65E  dc.w	$1A
0FB660  dc.b	$BF
0FB661  dc.b	2
0FB662  dc.b	$16
0FB663  aMoveArrows_:	dc.b	'move arrows.        ',0
0FB678  move.w	#2,($FFFFB028).w
0FB67E  move.w	($FFFFB028).w,-(sp)
0FB682  addq.w	#1,($FFFFB02A).w
0FB686  jsr	sub_11B92
0FB68C  dc.w	$16
0FB68E  aPressStartTo:	dc.b	'Press START to      '
0FB6A2  addq.w	#1,($FFFFB02A).w
0FB6A6  move.w	(sp),($FFFFB028).w
0FB6AA  jsr	sub_11B92
```

## `$0FB874` -> `ai_MoveUserListCursor`  (confidence 0.5, 10 insns)

**Evidence.** when the user-list selection $D4EA changed from the previous $D4EC, redraws the old row and the new one (ai_RedrawUserListRow with word_FB8E4 then word_FB8DC, the arrow and blank markers)

**Callers.** none found
**Callees.** ai_RedrawUserListRow

```
0FB874  movem.l	d0-a6,-(sp)
0FB878  move.w	($FFFFD4EA).w,d0
0FB87C  cmp.w	($FFFFD4EC).w,d0
0FB880  beq.w	loc_FB898
0FB884  move.l	#word_FB8E4,a1
0FB88A  bsr.w	loc_FB89E
0FB88E  move.l	#word_FB8DC,a1
0FB894  bsr.w	loc_FB89E
0FB898  movem.l	(sp)+,d0-a6
0FB89C  rts
```

## `$0FCA28` -> `ai_PrintShootersHeader`  (confidence 0.7, 10 insns)

**Evidence.** shootout screen: prints the 'Shooters' heading at column $C and the numbered rows '1. ' .. '5. ' at column $E

**Callers.** none found
**Callees.** printz2
**Strings.** Shooters | 1. | 2. | 3. | 4. | 5.

```
0FCA28  jsr	sub_11A36
0FCA2E  dc.w	8
0FCA30  dc.b	$FF
0FCA31  dc.b	2
0FCA32  dc.b	$FD
0FCA33  dc.b	0
0FCA34  dc.b	$FC
0FCA35  dc.b	$A
0FCA36  jsr	sub_11A36
0FCA3C  dc.w	4
0FCA3E  dc.b	'þ',4
0FCA40  jsr	sub_11A36
0FCA46  dc.w	$E
0FCA48  dc.b	$FD
0FCA49  dc.b	7
0FCA4A  dc.b	$FC
0FCA4B  dc.b	$C
0FCA4C  aShooters:	dc.b	'Shooters'
0FCA54  jsr	sub_11A36
0FCA5A  dc.w	$A
0FCA5C  dc.b	$FD
0FCA5D  dc.b	3
0FCA5E  dc.b	$FC
0FCA5F  dc.b	$E
0FCA60  a1_:		dc.b	'1. ',0
0FCA64  jsr	sub_11A36
0FCA6A  dc.w	$A
0FCA6C  dc.b	$FD
0FCA6D  dc.b	3
0FCA6E  dc.b	$FC
0FCA6F  dc.b	$10
0FCA70  a2_:		dc.b	'2. ',0
0FCA74  jsr	sub_11A36
0FCA7A  dc.w	$A
0FCA7C  dc.b	$FD
0FCA7D  dc.b	3
0FCA7E  dc.b	$FC
0FCA7F  dc.b	$12
0FCA80  a3_:		dc.b	'3. ',0
0FCA84  jsr	sub_11A36
0FCA8A  dc.w	$A
0FCA8C  dc.b	$FD
0FCA8D  dc.b	3
0FCA8E  dc.b	$FC
0FCA8F  dc.b	$14
0FCA90  a4_:		dc.b	'4. ',0
0FCA94  jsr	sub_11A36
0FCA9A  dc.w	$A
0FCA9C  dc.b	$FD
0FCA9D  dc.b	3
0FCA9E  dc.b	$FC
0FCA9F  dc.b	$16
0FCAA0  a5_:		dc.b	'5. ',0
0FCAA4  jsr	sub_11A36
0FCAAA  dc.w	$C
0FCAAC  dc.b	$FD
0FCAAD  dc.b	$1A
0FCAAE  dc.b	$FC
0FCAAF  dc.b	$C
0FCAB0  aGoalie_0:	dc.b	'Goalie'
...
```

## `$0081CA` -> `ai_WritePlayerPickerScroll`  (confidence 0.6, 9 insns)

**Evidence.** writes the player picker's vertical scroll (-$30 + VertLineScrolling) to VSRAM entry 1 with $BF78 bit 2 held; tail of ai_ScrollPlayerPicker

**Callers.** none found
**Callees.** none
**RAM.** VertLineScrolling, disflags
**Hardware.** VDP data

```
0081CA  move.w	($FFFFBF78).w,-(sp)
0081CE  bset	#2,($FFFFBF78).w
0081D4  move.l	#$C00000,a0
0081DA  move.l	#$40020010,4(a0)
0081E2  move.w	#$FFD0,d0
0081E6  add.w	($FFFFD5AE).w,d0
0081EA  move.w	d0,(a0)
0081EC  move.w	(sp)+,($FFFFBF78).w
0081F0  rts
```

## `$016468` -> `ai_PushNumberTile`  (confidence 0.5, 9 insns)

**Evidence.** takes the tile word $64(a1, 2*index) for the digit in the high word of d0, adds the font base $B012 and the priority bit and pushes it at -(a0); part of the on-ice number/clock sprite builders

**Callers.** none found
**Callees.** none

```
016468  swap	d0
01646A  asl.w	#1,d0
01646C  move.w	$64(a1,d0.w),d0
016470  add.w	($FFFFB012).w,d0
016474  or.w	#$8000,d0
016478  move.w	d0,-(a0)
01647A  swap	d0
01647C  ext.l	d0
01647E  rts
```

## `$018AC6` -> `ai_FormatCheckedPlayerName`  (confidence 0.6, 9 insns)

**Evidence.** takes TempPlOffset ($C470; negative = away record, low byte = index) and formats that player's 'I. Surname' with ai_FormatPlayerInitialSurname; the checked/hit player message

**Callers.** none found
**Callees.** ai_FormatPlayerInitialSurname
**RAM.** TempPlOffset

```
018AC6  movem.l	d0/a2,-(sp)
018ACA  move.w	#$C6CE,a2
018ACE  move.w	($FFFFC470).w,d0
018AD2  bpl.w	loc_18ADE
018AD6  and.w	#$FF,d0
018ADA  add.w	#$364,a2
018ADE  bsr.w	sub_18AE8
018AE2  movem.l	(sp)+,d0/a2
018AE6  rts
```

## `$0FAFBA` -> `ai_SplitBothRostersByLineup`  (confidence 0.7, 9 insns)

**Evidence.** runs ai_SplitRosterByLineup for the home record into $D4FA and the away record into $D514

**Callers.** none found
**Callees.** ai_SplitRosterByLineup

```
0FAFBA  movem.l	d0-a6,-(sp)
0FAFBE  move.l	#$FFFFD4FA,a1
0FAFC4  move.l	#$FFFFC6CE,a0
0FAFCA  bsr.w	sub_FAFE4
0FAFCE  move.l	#$FFFFD514,a1
0FAFD4  move.l	#$FFFFCA32,a0
0FAFDA  bsr.w	sub_FAFE4
0FAFDE  movem.l	(sp)+,d0-a6
0FAFE2  rts
```

## `$0FB7A0` -> `ai_PrintEntryCursorChar`  (confidence 0.6, 9 insns)

**Evidence.** name entry: when the blink flag $D6C4 is set prints the single alphabet character at index d5 (as a 1-character string in $CF36) at the cursor

**Callers.** none found
**Callees.** print

```
0FB7A0  tst.w	($FFFFD6C4).w
0FB7A4  beq.s	locret_FB79E
0FB7A6  move.l	#$FFFFCF36,a1
0FB7AC  move.w	#4,(a1)
0FB7B0  move.b	#0,3(a1)
0FB7B6  move.l	#aAbcdefghijklmnopqrstu,a0
0FB7BC  move.b	(a0,d5.w),d0
0FB7C0  move.b	d0,2(a1)
0FB7C4  jmp	sub_11BA4
```

