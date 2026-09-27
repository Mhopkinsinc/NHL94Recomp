# Name review: names-batch-13.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$01173C` -> `ai_LoadTilesCore`  (confidence 0.7, 19 insns)

**Evidence.** body shared by LoadAsset / ai_LoadAssetInline: a2 = asset, d4 = destination tile: reads the count word; 0 ends, a negative count (& $7FFF) is a compressed block decoded by sub_1177A, a positive count is raw 4bpp tiles sent by DoDMApro, or by remap when an inline nibble map pointer is set in $CF32; d4 is advanced by the tile count; caller ai_LoadAssetInline (and LoadAsset by fall-through)

**Callers.** ai_LoadAssetInline
**Callees.** remap, sub_1177A

```
01173C  movem.l	d0-d1/a0-a6,-(sp)
011740  move.l	a2,a0
011742  move.w	d4,d1
011744  asl.w	#5,d1
011746  move.w	(a0)+,d0
011748  beq.w	loc_11774
01174C  bmi.w	loc_1176A
011750  add.w	d0,d4
011752  asl.w	#4,d0
011754  pea	(loc_11774).l
01175A  tst.l	($FFFFCF32).w
01175E  beq.w	loc_113D0
011762  move.l	($FFFFCF32).w,a1
011766  bra.w	loc_10EE0
01176A  and.w	#$7FFF,d0
01176E  add.w	d0,d4
011770  bsr.w	sub_1177A
011774  movem.l	(sp)+,d0-d1/a0-a6
011778  rts
```

## `$012EF6` -> `ai_AverageOnIceEnergy`  (confidence 0.8, 19 insns)

**Evidence.** for the six objects of team a2 (from $22(a2)) with a positive position slot $34, sums the energy words $32(a2, 2*$66(obj)) and returns the average in d0 (0 when nobody is on the ice); caller ai_CpuLineChangeCheck

**Callers.** ai_CpuLineChangeCheck
**Callees.** none

```
012EF6  movem.l	d1-d3/a0,-(sp)
012EFA  clr.l	d0
012EFC  clr.w	d1
012EFE  moveq	#5,d2
012F00  move.w	$22(a2),a0
012F04  tst.w	$34(a0)
012F08  ble.w	loc_12F1A
012F0C  clr.w	d3
012F0E  move.b	$66(a0),d3
012F12  add.w	d3,d3
012F14  add.w	$32(a2,d3.w),d0
012F18  addq.w	#1,d1
012F1A  add.w	#$80,a0
012F1E  dbf	d2,loc_12F04
012F22  tst.w	d1
012F24  beq.w	loc_12F2A
012F28  divu.w	d1,d0
012F2A  movem.l	(sp)+,d1-d3/a0
012F2E  rts
```

## `$00A88C` -> `ai_ClampCamera`  (confidence 0.8, 17 insns)

**Evidence.** SetRCords helper: clamps Hpos ($BD1C) into -$3C..$3C and Vpos ($BD18) into -$C8..$100, the same limits ai_CenterCameraOnObject applies; caller SetRCords

**Callers.** SetRCords
**Callees.** none
**RAM.** Hpos, Vpos

```
00A88C  move.w	d0,-(sp)
00A88E  move.w	#$3C,d0
00A892  cmp.w	($FFFFBD1C).w,d0
00A896  blt.w	loc_A8A6
00A89A  move.w	#$FFC4,d0
00A89E  cmp.w	($FFFFBD1C).w,d0
00A8A2  ble.w	loc_A8AA
00A8A6  move.w	d0,($FFFFBD1C).w
00A8AA  move.w	#$100,d0
00A8AE  cmp.w	($FFFFBD18).w,d0
00A8B2  blt.w	loc_A8C2
00A8B6  move.w	#$FF38,d0
00A8BA  cmp.w	($FFFFBD18).w,d0
00A8BE  ble.w	loc_A8C6
00A8C2  move.w	d0,($FFFFBD18).w
00A8C6  move.w	(sp)+,d0
00A8C8  rts
```

## `$017652` -> `ai_DrawPlayoffRoundLabel`  (confidence 0.5, 19 insns)

**Evidence.** PlayoffScreen: d1 = label index; when it equals twice the current-round byte $CEF4[potreeteam] the palette is switched to $6000 (highlight), then draws the 2-row label bitmap from off_ABA14's second block with dobitmap at tile base 2 (the 'Playoffs' / 'Quarterfinals' / 'Semifinals' / 'Finals' / 'Champions' strings sit next to it); caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** dobitmap
**Strings.** Playoffs | Quarterfinals | Semifinals | Finals | Champions
**RAM.** potreeteam, printa

```
017652  movem.l	d0-a3,-(sp)
017656  move.w	#$CEF4,a0
01765A  move.w	($FFFFCEEE).w,d0
01765E  move.b	(a0,d0.w),d0
017662  add.b	d0,d0
017664  cmp.b	d0,d1
017666  bne.w	loc_17670
01766A  move.w	#$6000,($FFFFB02C).w
017670  move.l	#off_ABA14,a1
017676  add.l	4(a1),a1
01767A  move.w	#$30A,a2
01767E  clr.w	d0
017680  move.w	(a1),d2
017682  moveq	#2,d3
017684  moveq	#2,d4
017686  moveq	#0,d5
017688  bsr.w	sub_1169A
01768C  movem.l	(sp)+,d0-a3
017690  rts
```

## `$0FED2A` -> `ai_BuildPlayoffCursorSprites`  (confidence 0.5, 19 insns)

**Evidence.** PlayoffScreen: builds the sprite list at $C018 from frame 1 of the sprite asset unk_F3098 with SetSframe at ($B8AE, $B8B0) (the scrolled bracket position) and tile base $B016 | $8000, terminates the list (clearing two longs when nothing was emitted) and stores the sprite count in $C2E8; caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** SetSframe

```
0FED2A  move.w	#$C018,a6
0FED2E  moveq	#1,d6
0FED30  move.l	#unk_F3098,a0
0FED36  move.w	($FFFFB016).w,d3
0FED3A  or.w	#$8000,d3
0FED3E  move.w	($FFFFB8AE).w,d0
0FED42  move.w	($FFFFB8B0).w,d1
0FED46  move.w	#1,d2
0FED4A  jsr	sub_16178
0FED50  cmp.w	#$C018,a6
0FED54  bne.w	loc_FED5C
0FED58  clr.l	(a6)+
0FED5A  clr.l	(a6)+
0FED5C  clr.b	-5(a6)
0FED60  move.l	a6,d0
0FED62  sub.l	#$FFFFC018,d0
0FED68  lsr.w	#1,d0
0FED6A  move.w	d0,($FFFFC2E8).w
0FED6E  rts
```

## `$0F878C` -> `ai_DrawSetupPhotoFrame`  (confidence 0.6, 18 insns)

**Evidence.** draws the 8x8-tile photo panel frame bitmap off_BF702 at column 8 row 5 with tile base $D438 (the entry at $F8796 is shared by ai_SetHomePhotoPanel / ai_SetAwayPhotoPanel, which set their own base and column first) under $C2F8 bit 0; caller ai_DrawSetupHomeLogo

**Callers.** ai_DrawSetupHomeLogo
**Callees.** dobitmap
**RAM.** printa, printx, printy

```
0F878C  move.w	($FFFFD438).w,d4
0F8790  move.w	#8,($FFFFB028).w
0F8796  clr.w	($FFFFB02C).w
0F879A  move.w	#5,($FFFFB02A).w
0F87A0  move.l	#off_BF702,a0
0F87A6  move.l	a0,a1
0F87A8  move.l	a0,a2
0F87AA  add.l	(a2)+,a0
0F87AC  add.l	(a2)+,a1
0F87AE  move.w	#8,d3
0F87B2  move.w	#8,d2
0F87B6  clr.w	d0
0F87B8  clr.w	d1
0F87BA  move.w	#0,d5
0F87BE  bset	#0,($FFFFC2F8).w
0F87C4  jsr	sub_1169A
0F87CA  bclr	#0,($FFFFC2F8).w
0F87D0  rts
```

## `$008008` -> `ai_PrintPauseMenuItem`  (confidence 0.7, 17 insns)

**Evidence.** ai_PrintScrollingMenu item printer: an item whose third byte is 'x' is the goalie-control toggle and prints 'Manual Goalie' or 'Auto Goalie' according to the controlling team's option ($D05C for the second controller when sflags bit 1, else $D05A), any other item is printed as-is; caller ai_PrintScrollingMenu

**Callers.** ai_PrintScrollingMenu
**Callees.** loc_8030, locret_804E, print2
**Strings.** Manual Goalie | Auto Goalie
**RAM.** sflags

```
008008  cmp.b	#$78,2(a1)
00800E  bne.w	loc_8048
008012  move.l	a1,-(sp)
008014  move.l	#$8050,a1
00801A  btst	#1,($FFFFC2EC).w
008020  beq.w	loc_802C
008024  tst.w	($FFFFD05C).w
008028  bra.w	loc_8030
00802C  tst.w	($FFFFD05A).w
008030  beq.w	loc_803A
008034  move.l	#$8064,a1
00803A  jsr	sub_11A48
008040  move.l	(sp)+,a1
008042  add.w	(a1),a1
008044  bra.w	locret_804E
008048  jsr	sub_11A48
00804E  rts
```

## `$0FF3B0` -> `ai_InitTitleScrollTable`  (confidence 0.4, 18 insns)

**Evidence.** newTitleScreen: sets Hscroll = $14 and $BF14 = $50, then fills the object area at $B04A with a table of 81 longs alternating $FD80/$FD7F (decrementing every other entry) followed by 97 longs counting up from $100 in steps of 4; the values feed the title screen's per-line scroll effect; caller newTitleScreen

**Callers.** newTitleScreen
**Callees.** none
**RAM.** Hscroll

```
0FF3B0  movem.l	d0-d1,-(sp)
0FF3B4  move.w	#$14,($FFFFBD1E).w
0FF3BA  move.w	#$50,($FFFFBF14).w
0FF3C0  move.w	#$50,d0
0FF3C4  move.l	#$FFFFB04A,a0
0FF3CA  move.l	#$FD80,d1
0FF3D0  move.l	d1,(a0)+
0FF3D2  btst	#0,d0
0FF3D6  bne.w	loc_FF3DC
0FF3DA  subq.w	#1,d1
0FF3DC  dbf	d0,loc_FF3D0
0FF3E0  move.w	#$60,d0
0FF3E4  move.l	#$100,d1
0FF3EA  move.l	d1,(a0)+
0FF3EC  addq.l	#4,d1
0FF3EE  dbf	d0,loc_FF3EA
0FF3F2  movem.l	(sp)+,d0-d1
0FF3F6  rts
```

## `$0FAFE4` -> `ai_SplitRosterByLineup`  (confidence 0.6, 18 insns)

**Evidence.** a0 = team record, a1 = output: for the 26 roster indexes writes those that appear in the six-entry lineup list at team data offset +6 to a1 (starters) and the rest to a1+6 (bench); sub_FAFBA calls it for the home and away teams into $D4FA and $D514; caller sub_FAFBA

**Callers.** sub_FAFBA
**Callees.** loc_FB00E
**Strings.** NAME  ENTRYa

```
0FAFE4  move.l	$1E(a0),a0
0FAFE8  add.w	6(a0),a0
0FAFEC  move.l	a1,a2
0FAFEE  addq.w	#6,a2
0FAFF0  clr.w	d0
0FAFF2  move.w	#5,d1
0FAFF6  move.b	(a0,d1.w),d3
0FAFFA  subq.b	#1,d3
0FAFFC  cmp.b	d3,d0
0FAFFE  beq.w	loc_FB00C
0FB002  dbf	d1,loc_FAFF6
0FB006  move.b	d0,(a2)+
0FB008  bra.w	loc_FB00E
0FB00C  move.b	d0,(a1)+
0FB00E  addq.w	#1,d0
0FB010  cmpnw	 $1A,d0
0FB014  blt.s	loc_FAFF2
0FB016  rts
```

## `$0F9AE4` -> `ai_AppendRecordUserName`  (confidence 0.6, 19 insns)

**Evidence.** given a record (a0, or fetched with ReadRecordField when a0 is null) appends the holder's user name (byte 1) to the string at a1 with ai_BuildUserNameString and trailing-space trimming ($C2F8 bit 7); caller sub_F9A64 (records text)

**Callers.** sub_F9A64
**Callees.** ai_BuildUserNameString, ai_ReadRecordField

```
0F9AE4  movem.l	d0-d7/a1-a2,-(sp)
0F9AE8  cmp.l	#0,a0
0F9AEE  bne.w	loc_F9B14
0F9AF2  movem.l	d0-d7/a1-a6,-(sp)
0F9AF6  move.w	d0,-(sp)
0F9AF8  move.w	d1,d0
0F9AFA  move.w	(sp)+,d1
0F9AFC  ext.l	d1
0F9AFE  ext.l	d0
0F9B00  move.l	#$FFFF0000,a0
0F9B06  bsr.w	sub_F9B94
0F9B0A  move.l	#$FFFF0000,a0
0F9B10  movem.l	(sp)+,d0-d7/a1-a6
0F9B14  move.b	1(a0),d2
0F9B18  ext.w	d2
0F9B1A  bset	#7,($FFFFC2F8).w
0F9B20  bsr.w	sub_FA014
0F9B24  movem.l	(sp)+,d0-d7/a1-a2
0F9B28  rts
```

## `$0FC136` -> `ai_PrintRankedUserName`  (confidence 0.6, 18 insns)

**Evidence.** user-records list: prints the rank as a digit (7 - d7 + '0') followed by '. ' in $BFA4, then the user name of the entry byte -1(a0) via ai_BuildUserNameString without trimming; caller loc_FBEA4 (user list screen)

**Callers.** loc_FBEA4
**Callees.** ai_BuildUserNameString, print2

```
0FC136  move.w	d7,-(sp)
0FC138  neg.w	d7
0FC13A  addq.w	#7,d7
0FC13C  add.w	#$30,d7
0FC140  move.l	#$FFFFBFA4,a1
0FC146  move.w	#6,(a1)
0FC14A  move.b	d7,2(a1)
0FC14E  move.b	#$2E,3(a1)
0FC154  move.b	#$20,4(a1)
0FC15A  move.b	#0,5(a1)
0FC160  jsr	sub_11A48
0FC166  move.w	(sp)+,d7
0FC168  move.b	-1(a0),d2
0FC16C  ext.w	d2
0FC16E  move.l	#$FFFFBFA4,a1
0FC174  bclr	#7,($FFFFC2F8).w
0FC17A  bsr.w	sub_FA014
0FC17E  jmp	sub_11A48
```

## `$012D30` -> `ai_PrintTeamScoreBlock`  (confidence 0.7, 17 insns)

**Evidence.** PrintScores1: draws the team banner tiles (ai_DrawTeamBannerTiles, five columns left of printx) then the team's score $C(a2) two rows down, converted with PushNumber and centred (one column left when 10 or more) in the big font via printbig; caller PrintScores1

**Callers.** PrintScores1
**Callees.** PushNumber, ai_DrawTeamBannerTiles, loc_12D5A, printbig
**RAM.** printx, printy

```
012D30  move.w	($FFFFB028).w,-(sp)
012D34  subq.w	#5,($FFFFB028).w
012D38  jsr	sub_8078
012D3E  move.w	(sp)+,($FFFFB028).w
012D42  addq.w	#2,($FFFFB02A).w
012D46  move.w	$C(a2),d0
012D4A  cmpnw	 $A,d0
012D4E  bge.w	loc_12D56
012D52  bra.w	loc_12D5A
012D56  subq.w	#1,($FFFFB028).w
012D5A  bsr.w	sub_11D06
012D5E  move.w	(a1),d0
012D60  subq.w	#2,d0
012D62  lsr.w	#1,d0
012D64  sub.w	d0,($FFFFB028).w
012D68  addq.w	#1,($FFFFB028).w
012D6C  bra.w	sub_11DF4
```

