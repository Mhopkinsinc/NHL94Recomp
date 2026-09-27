# Name review: names-batch-24.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0F9A64` -> `ai_BuildRecordByUserText`  (confidence 0.6, 17 insns)

**Evidence.** copies the ' by' label word_F9AA6 into the string at a1 and appends the record holder's user name (ai_AppendRecordUserName via $BF20); when the record is empty (length 2) the output string is emptied instead

**Callers.** none found
**Callees.** ai_AppendRecordUserName, ai_CopyLenString, appstring, loc_F9AA0
**Strings.** by

```
0F9A64  movem.l	d0-d7/a1-a6,-(sp)
0F9A68  move.l	a1,-(sp)
0F9A6A  move.l	a1,a3
0F9A6C  move.l	#word_F9AA6,a1
0F9A72  movem.l	d0-d1,-(sp)
0F9A76  bsr.w	sub_F997A
0F9A7A  movem.l	(sp)+,d0-d1
0F9A7E  move.l	#$FFFFBF20,a1
0F9A84  bsr.w	sub_F9AE4
0F9A88  move.l	(sp)+,a3
0F9A8A  cmp.w	#2,(a1)
0F9A8E  bne.w	loc_F9A9A
0F9A92  move.w	#2,(a3)
0F9A96  bra.w	loc_F9AA0
0F9A9A  jsr	sub_11D9E
0F9AA0  movem.l	(sp)+,d0-d7/a1-a6
0F9AA4  rts
```

## `$0F9AAC` -> `ai_BuildRecordVsText`  (confidence 0.6, 13 insns)

**Evidence.** copies the ' vs.' label word_F9ADE into the string at a1 and appends the record holder's user name and opponent team (ai_AppendRecordHolderText via $BF20)

**Callers.** none found
**Callees.** ai_AppendRecordHolderText, ai_CopyLenString, appstring
**Strings.** vs.

```
0F9AAC  movem.l	d0-d7/a1-a6,-(sp)
0F9AB0  move.l	a1,-(sp)
0F9AB2  move.l	a1,a3
0F9AB4  move.l	#word_F9ADE,a1
0F9ABA  movem.l	d0-d1,-(sp)
0F9ABE  bsr.w	sub_F997A
0F9AC2  movem.l	(sp)+,d0-d1
0F9AC6  move.l	#$FFFFBF20,a1
0F9ACC  bsr.w	sub_F9B2A
0F9AD0  move.l	(sp)+,a3
0F9AD2  jsr	sub_11D9E
0F9AD8  movem.l	(sp)+,d0-d7/a1-a6
0F9ADC  rts
```

## `$0123DE` -> `ai_CountAvailableSkaters`  (confidence 0.6, 16 insns)

**Evidence.** team a2: for the 26 status words $66+2i with a positive value clears bit 5 and, unless bit 6 (major) or bit 4 is set, decrements the count from 6 (floor 4); stores the result as the active skater count $24(a2)

**Callers.** none found
**Callees.** none

```
0123DE  moveq	#6,d1
0123E0  moveq	#$32,d0
0123E2  tst.w	$66(a2,d0.w)
0123E6  ble.w	loc_1240E
0123EA  bclr	#5,$66(a2,d0.w)
0123F0  btst	#6,$66(a2,d0.w)
0123F6  bne.w	loc_1240E
0123FA  btst	#4,$66(a2,d0.w)
012400  bne.w	loc_1240E
012404  cmpnw	 4,d1
012408  beq.w	loc_1240E
01240C  subq.w	#1,d1
01240E  subq.w	#2,d0
012410  bpl.s	loc_123E2
012412  move.w	d1,$24(a2)
012416  rts
```

## `$0FC47C` -> `ai_InitShootout`  (confidence 0.7, 16 insns)

**Evidence.** clears the object area $B04A ($400 words) and $DED0, sets round 1 ($D578), clears the decided flag ($C2FA bit 3), both round scores $D574/$D576, the shooter index $D586 and side $D594, then loads the shooter lists for both sides with ai_LoadShootoutShooters

**Callers.** none found
**Callees.** ai_LoadShootoutShooters

```
0FC47C  move.l	#$FFFFB04A,a0
0FC482  move.w	#$3FF,d0
0FC486  clr.w	(a0)+
0FC488  dbf	d0,loc_FC486
0FC48C  clr.w	($FFFFDED0).w
0FC490  move.w	#1,($FFFFD578).w
0FC496  bclr	#3,($FFFFC2FA).w
0FC49C  clr.w	($FFFFD574).w
0FC4A0  clr.w	($FFFFD576).w
0FC4A4  clr.w	($FFFFD586).w
0FC4A8  clr.w	($FFFFD594).w
0FC4AC  bsr.w	sub_FC570
0FC4B0  move.w	#1,($FFFFD594).w
0FC4B6  bsr.w	sub_FC570
0FC4BA  clr.w	($FFFFD594).w
0FC4BE  rts
```

## `$0FE6D2` -> `ai_ClearUserRecordsSram`  (confidence 0.7, 16 insns)

**Evidence.** zeroes the wins/games bytes 8..$B of the eight 16-byte user records in $CF36 and writes the $80-byte block back to SRAM $D20 (WriteSRAM), then sub_1A206

**Callers.** none found
**Callees.** MakeSRAMChecksum, WriteSRAM

```
0FE6D2  movem.l	d0-a6,-(sp)
0FE6D6  move.l	#$FFFFCF36,a0
0FE6DC  move.w	#7,d7
0FE6E0  clr.b	8(a0)
0FE6E4  clr.b	9(a0)
0FE6E8  clr.b	$A(a0)
0FE6EC  clr.b	$B(a0)
0FE6F0  add.w	#$10,a0
0FE6F4  dbf	d7,loc_FE6E0
0FE6F8  move.l	#$D20,d0
0FE6FE  move.l	#$80,d1
0FE704  move.l	#$FFFFCF36,a0
0FE70A  jsr	sub_1A1E4
0FE710  jsr	sub_1A206
0FE716  movem.l	(sp)+,d0-a6
0FE71A  rts
```

## `$0FEE60` -> `ai_CountPassAttempt`  (confidence 0.4, 16 insns)

**Evidence.** unless $C2EA bit 0: increments the attempt counter at $DEA4 (or $DEAC when d4 is set) and, when the direction code in $BF12 is not 8 and differs from the player's facing $54(a3), also the second counter at +4; a pass/shot direction statistic

**Callers.** none found
**Callees.** none
**RAM.** gmode

```
0FEE60  movem.l	d1-a0,-(sp)
0FEE64  btst	#0,($FFFFC2EA).w
0FEE6A  bne.w	loc_FEE9A
0FEE6E  move.w	($FFFFBF12).w,d1
0FEE72  move.l	#$FFFFDEA4,a0
0FEE78  tst.w	d4
0FEE7A  beq.w	loc_FEE84
0FEE7E  move.l	#$FFFFDEAC,a0
0FEE84  addq.l	#1,(a0)
0FEE86  cmpnw	 8,d1
0FEE8A  beq.w	loc_FEE9A
0FEE8E  cmp.w	$54(a3),d1
0FEE92  beq.w	loc_FEE9A
0FEE96  addq.l	#1,4(a0)
0FEE9A  movem.l	(sp)+,d1-a0
0FEE9E  rts
```

## `$0FBBDE` -> `ai_SkipOwnUserEntry`  (confidence 0.5, 15 insns)

**Evidence.** user selection: if the entry $D4EA equals the user already chosen by the other controller ($D042 or $D044 by $D4EE), steps $D4EA one further in the direction of the sign of d0 and returns d0 = 0 (consumed); otherwise leaves d0

**Callers.** none found
**Callees.** none
**Strings.** Record | Holders | Nameù

```
0FBBDE  movem.w	d0,-(sp)
0FBBE2  move.w	($FFFFD044).w,d0
0FBBE6  tst.w	($FFFFD4EE).w
0FBBEA  beq.w	loc_FBBF2
0FBBEE  move.w	($FFFFD042).w,d0
0FBBF2  cmp.w	($FFFFD4EA).w,d0
0FBBF6  bne.w	loc_FBC0E
0FBBFA  move.w	#1,d0
0FBBFE  tst.w	(sp)
0FBC00  bpl.w	loc_FBC08
0FBC04  move.w	#$FFFF,d0
0FBC08  add.w	d0,($FFFFD4EA).w
0FBC0C  clr.w	d0
0FBC0E  movem.w	(sp)+,d0
0FBC12  rts
```

## `$008198` -> `ai_ScrollPlayerPicker`  (confidence 0.6, 14 insns)

**Evidence.** player picker scroll step with a 24-pixel pitch: applies PlayerScrollCtr to VertLineScrolling within 0..$D5B2; at a row boundary redraws the arrows (ai_PrintSelectPlayerArrows) and stops, otherwise continues in sub_81CA

**Callers.** none found
**Callees.** ai_PrintSelectPlayerArrows
**RAM.** PlayerScrollCtr, VertLineScrolling

```
008198  move.w	($FFFFD5B0).w,d0
00819C  beq.w	locret_A9D4
0081A0  add.w	($FFFFD5AE).w,d0
0081A4  bmi.w	locret_A9D4
0081A8  cmp.w	($FFFFD5B2).w,d0
0081AC  bgt.w	locret_A9D4
0081B0  move.w	d0,($FFFFD5AE).w
0081B4  ext.l	d0
0081B6  divu.w	#$18,d0
0081BA  swap	d0
0081BC  tst.w	d0
0081BE  bne.w	sub_81CA
0081C2  bsr.w	loc_8280
0081C6  clr.w	($FFFFD5B0).w
```

## `$010E88` -> `ai_UnpackNibblesToWords`  (confidence 0.7, 14 insns)

**Evidence.** expands d0 + 1 nibbles from a0 (high nibble first) into words at the weight table $D036, the table ai_WeightedRandomIndex draws from

**Callers.** none found
**Callees.** loc_10EAA

```
010E88  movem.l	d0-d2/a0-a1,-(sp)
010E8C  move.w	#$D036,a1
010E90  clr.w	d2
010E92  bra.w	loc_10EAA
010E96  move.b	(a0)+,d1
010E98  bchg	#0,d2
010E9C  bne.w	loc_10EA4
010EA0  subq.w	#1,a0
010EA2  lsr.w	#4,d1
010EA4  and.w	#$F,d1
010EA8  move.w	d1,(a1)+
010EAA  dbf	d0,loc_10E96
010EAE  movem.l	(sp)+,d0-d2/a0-a1
010EB2  rts
```

## `$008898` -> `ai_SwapLineSlot`  (confidence 0.6, 13 insns)

**Evidence.** edit lines: puts player d0 into slot d2 of team a2's line table $16A; if that player already occupies another slot of the same 8-byte line, the displaced player is moved into the vacated slot (a swap)

**Callers.** none found
**Callees.** none
**Strings.** Roster | Pos.^Player | Rating | Switch^Teams

```
008898  movem.l	d0-d2/a0-a1,-(sp)
00889C  lea	$16A(a2),a0
0088A0  move.w	d2,d1
0088A2  and.w	#$FFF8,d1
0088A6  lea	(a0,d1.w),a1
0088AA  moveq	#5,d1
0088AC  cmp.b	1(a1,d1.w),d0
0088B0  dbeq	d1,loc_88AC
0088B4  bne.w	loc_88BE
0088B8  move.b	(a0,d2.w),1(a1,d1.w)
0088BE  move.b	d0,(a0,d2.w)
0088C2  movem.l	(sp)+,d0-d2/a0-a1
0088C6  rts
```

## `$0FBFA0` -> `ai_EraseUserListArea`  (confidence 0.6, 13 insns)

**Evidence.** erases the 40x18 user list area from row $A (inline position string) while preserving printx/printy/printm; used by the user records screens

**Callers.** none found
**Callees.** eraser, printz2
**Strings.**  | by | vs.
**RAM.** printm, printx, printy

```
0FBFA0  movem.l	d0-a6,-(sp)
0FBFA4  move.w	($FFFFB028).w,-(sp)
0FBFA8  move.w	($FFFFB02A).w,-(sp)
0FBFAC  move.w	($FFFFB02E).w,-(sp)
0FBFB0  jsr	sub_11A36
0FBFB6  dc.w	8
0FBFB8  dc.b	$F8
0FBFB9  dc.b	4
0FBFBA  dc.b	2
0FBFBB  dc.b	0
0FBFBC  dc.b	$A
0FBFBD  dc.b	0
0FBFBE  move.w	#$28,d0
0FBFC2  move.w	#$12,d1
0FBFC6  jsr	sub_1197E
0FBFCC  move.w	(sp)+,($FFFFB02E).w
0FBFD0  move.w	(sp)+,($FFFFB02A).w
0FBFD4  move.w	(sp)+,($FFFFB028).w
0FBFD8  movem.l	(sp)+,d0-a6
0FBFDC  rts
```

## `$00A4A8` -> `ai_DrawPauseMenuBackdrop`  (confidence 0.5, 12 insns)

**Evidence.** sets $DEB4 = -1 and draws the 16x11-tile bitmap off_BB4EE at (0,0) with tile base ExtraChars ($B026), the base the pause menu tiles were loaded at

**Callers.** none found
**Callees.** dobitmap, printz
**RAM.** ExtraChars

```
00A4A8  st	($FFFFDEB4).w
00A4AC  bsr.w	sub_11B92
00A4B0  dc.w	6
00A4B2  dc.b	$BD
00A4B3  dc.b	2
00A4B4  dc.b	0
00A4B5  dc.b	0
00A4B6  moveq	#0,d0
00A4B8  moveq	#0,d1
00A4BA  moveq	#$10,d2
00A4BC  moveq	#$B,d3
00A4BE  move.w	($FFFFB026).w,d4
00A4C2  move.w	#0,d5
00A4C6  move.l	#off_BB4EE,a1
00A4CC  add.l	4(a1),a1
00A4D0  move.w	#$30A,a2
00A4D4  bra.w	sub_1169A
```

## `$00A4F6` -> `ai_StepReplayBack`  (confidence 0.5, 12 insns)

**Evidence.** replay playback: moves the frame pointer a4 back one $62-byte frame, wrapping from $FF0000 to $AF54 when $C2EC bit 4 allows it; stops (without stepping) when it would reach the write pointer recbpr, and shows the frame with sub_A68C; returns d7 = 0

**Callers.** none found
**Callees.** SetRCords
**RAM.** recbpr, sflags

```
00A4F6  cmp.l	#$FFFF0000,a4
00A4FC  bne.w	loc_A510
00A500  btst	#4,($FFFFC2EC).w
00A506  beq.w	loc_A520
00A50A  move.l	#$FFFFAF54,a4
00A510  suba.w	#$62,a4
00A514  cmp.l	($FFFFB036).w,a4
00A518  bne.w	sub_A68C
00A51C  add.w	#$62,a4
00A520  bsr.w	sub_A68C
00A524  clr.w	d7
00A526  rts
```

## `$0FA2A2` -> `ai_WrapRecordsIndex`  (confidence 0.5, 12 insns)

**Evidence.** wraps the records-page index at (a0): to 0 when it reaches $D4F8 + 1 (the entry count), and to the last entry when it goes negative

**Callers.** none found
**Callees.** none

```
0FA2A2  move.w	d0,-(sp)
0FA2A4  move.w	($FFFFD4F8).w,d0
0FA2A8  addq.w	#1,d0
0FA2AA  cmp.w	(a0),d0
0FA2AC  bne.w	loc_FA2B2
0FA2B0  clr.w	(a0)
0FA2B2  tst.w	(a0)
0FA2B4  bpl.w	loc_FA2BC
0FA2B8  subq.w	#1,d0
0FA2BA  move.w	d0,(a0)
0FA2BC  move.w	(sp)+,d0
0FA2BE  rts
```

