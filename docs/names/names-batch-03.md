# Name review: names-batch-03.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$011044` -> `VDP_FlushPalette`  (from the 2016 listing, not AI, 13 insns)

**Evidence.** label from the 2016 listing; the IDA export has no name at this entry

**Callers.** EASportsScreen
**Callees.** none
**RAM.** disflags, palcount
**Hardware.** VDP data

```
011044  movem.l	d0/a0-a1,-(sp)
011048  move.w	($FFFFBF78).w,-(sp)
01104C  bset	#2,($FFFFBF78).w
011052  move.w	#$BD28,a1
011056  move.l	#$C00000,a0
01105C  move.l	#$C0000000,4(a0)
011064  moveq	#$1F,d0
011066  move.l	(a1)+,(a0)
011068  dbf	d0,loc_11066
01106C  st	($FFFFBD26).w
011070  move.w	(sp)+,($FFFFBF78).w
011074  movem.l	(sp)+,d0/a0-a1
011078  rts
```

## `$01381E` -> `VDP_ReadHVCounter`  (from the 2016 listing, not AI, 10 insns)

**Evidence.** label from the 2016 listing; the IDA export has no name at this entry

**Callers.** none found
**Callees.** none
**Hardware.** HV counter

```
01381E  move.w	$A(a0),d0
013822  cmp.w	$C(a0),d0
013826  bne.w	loc_13840
01382A  move.w	($C00008).l,d0
013830  and.w	#1,d0
013834  add.w	d0,$A(a0)
013838  eor.w	#1,d0
01383C  add.w	d0,$C(a0)
013840  move.w	#5,8(a0)
013846  rts
```

## `$01A574` -> `Z80_WriteVolume`  (from the 2016 listing, not AI, 17 insns)

**Evidence.** label from the 2016 listing; the IDA export has no name at this entry. Requests the Z80 bus, checks the driver handshake bytes at Z80 RAM $96/$97 ($7D/0), writes $D1/0 back and copies the 33 bytes at $D182 into Z80 RAM $98

**Callers.** AllSndOff, MusicVB, ai_StopSound30
**Callees.** none
**Hardware.** Z80 RAM, Z80 busreq

```
01A574  move.w	#$100,($A11100).l
01A57C  btst	#0,($A11100).l
01A584  bne.s	loc_1A57C
01A586  move.l	#$A00000,a0
01A58C  cmp.b	#0,$97(a0)
01A592  bne.s	loc_1A568
01A594  cmp.b	#$7D,$96(a0)
01A59A  bne.s	loc_1A568
01A59C  move.b	#$D1,$96(a0)
01A5A2  move.b	#0,$97(a0)
01A5A8  add.w	#2,a0
01A5AC  move.w	#$D182,a1
01A5B0  moveq	#$20,d0
01A5B2  move.b	(a1)+,(a0)+
01A5B4  dbf	d0,loc_1A5B2
01A5B8  clr.w	($A11100).l
01A5BE  rts
```

## `$01A66E` -> `Z80_ClearFlagUnknown`  (from the 2016 listing, not AI, 6 insns)

**Evidence.** label from the 2016 listing; the IDA export has no name at this entry

**Callers.** AllSndOff
**Callees.** none
**Hardware.** Z80 busreq

```
01A66E  move.w	#$100,($A11100).l
01A676  btst	#0,($A11100).l
01A67E  bne.s	loc_1A676
01A680  clr.b	($A0008E).l
01A686  clr.w	($A11100).l
01A68C  rts
```

## `$009F9A` -> `ai_CountRosterPlayers`  (confidence 0.7, 11 insns)

**Evidence.** a2 = team record; follows $1E(a2) to the team data block and its first offset word to the player list, then walks the length-prefixed player records (name part + 8 attribute bytes) counting them in d0 until the terminator record whose length word is 2; callers SetPlList, loc_961A (edit lines), sub_F9FEA (records)

**Callers.** SetPlList, loc_961A, sub_F9FEA
**Callees.** none

```
009F9A  movem.l	a0,-(sp)
009F9E  move.l	$1E(a2),a0
009FA2  add.w	(a0),a0
009FA4  clr.w	d0
009FA6  addq.w	#1,d0
009FA8  add.w	(a0),a0
009FAA  addq.w	#8,a0
009FAC  cmp.w	#2,(a0)
009FB0  bne.s	loc_9FA6
009FB2  movem.l	(sp)+,a0
009FB6  rts
```

## `$0FEA52` -> `ai_LoadHomeCenterIceLogo`  (confidence 0.8, 10 insns)

**Evidence.** indexes the logo table off_FEA74 by HomeTeam ($C330), skips the 8-byte header and loads the tiles with LoadAsset at tile d4-$18; the same table was confirmed as the centre-ice logo art while prototyping the HUD overlay; callers ClrHor, loc_9CDC, setupice (rink setup)

**Callers.** ClrHor, loc_9CDC, setupice
**Callees.** ai_LoadAsset
**RAM.** HomeTeam

```
0FEA52  move.w	d0,-(sp)
0FEA54  sub.w	#$18,d4
0FEA58  move.l	#off_FEA74,a2
0FEA5E  move.w	($FFFFC330).w,d0
0FEA62  asl.w	#2,d0
0FEA64  move.l	(a2,d0.w),a2
0FEA68  addq.w	#8,a2
0FEA6A  jsr	sub_11738
0FEA70  move.w	(sp)+,d0
0FEA72  rts
```

## `$018BAE` -> `ai_FinishNameBuffer`  (confidence 0.7, 9 insns)

**Evidence.** terminates the length-prefixed string being built at $BFA4 (text from $BFA6): computes the length from a1, pads with a zero byte to an even length and stores the length word at $BFA4; called by the three name formatters sub_18AE8, sub_18B26, sub_18B6E

**Callers.** ai_FormatPlayerInitialSurname, ai_FormatPlayerNumberName, ai_FormatPlayerSurnamePadded
**Callees.** none

```
018BAE  move.w	a1,d0
018BB0  sub.w	#$BFA4,d0
018BB4  btst	#0,d0
018BB8  beq.w	loc_18BC0
018BBC  clr.b	(a1)+
018BBE  addq.w	#1,d0
018BC0  move.w	#$BFA4,a1
018BC4  move.w	d0,(a1)
018BC6  rts
```

## `$018B26` -> `ai_FormatPlayerNumberName`  (confidence 0.6, 19 insns)

**Evidence.** builds the string at $BFA4: jersey number (sub_18BDC from the byte after the name), a space, then the player's name from the record found by sub_18BC8, copied from after its first space (the surname), and closes it with FinishNameBuffer; callers ai_PrintPlayerStatRow and sub_FD89A (team ratings screen)

**Callers.** ai_PrintPlayerStatRow, sub_FD89A
**Callees.** ai_FinishNameBuffer, d0toascii, getplayername

```
018B26  movem.l	d0-d3/a0/a2,-(sp)
018B2A  bsr.w	sub_18BC8
018B2E  move.l	a0,-(sp)
018B30  move.w	#$BFA6,a1
018B34  add.w	(a0),a0
018B36  move.b	(a0),d0
018B38  bsr.w	sub_18BDC
018B3C  move.b	#$20,(a1)+
018B40  move.l	(sp)+,a0
018B42  move.w	(a0)+,d0
018B44  lea	-2(a0,d0.w),a2
018B48  cmp.b	#$20,(a0)+
018B4C  bne.s	loc_18B48
018B4E  move.b	(a0)+,(a1)+
018B50  cmp.l	a0,a2
018B52  bne.s	loc_18B4E
018B54  bsr.w	sub_18BAE
018B58  movem.l	(sp)+,d0-d3/a0/a2
018B5C  rts
```

## `$018AE8` -> `ai_FormatPlayerInitialSurname`  (confidence 0.6, 21 insns)

**Evidence.** same as FormatPlayerNumberName but writes the first letter of the name, then '. ' ($2E20), then the surname after the first space; callers sub_18AC6, sub_9112

**Callers.** sub_18AC6, sub_9112
**Callees.** ai_FinishNameBuffer, d0toascii, getplayername

```
018AE8  movem.l	d0-d3/a0/a2,-(sp)
018AEC  bsr.w	sub_18BC8
018AF0  move.l	a0,-(sp)
018AF2  move.w	#$BFA6,a1
018AF6  add.w	(a0),a0
018AF8  move.b	(a0),d0
018AFA  bsr.w	sub_18BDC
018AFE  move.b	#$20,(a1)+
018B02  move.l	(sp)+,a0
018B04  move.w	(a0)+,d0
018B06  lea	-2(a0,d0.w),a2
018B0A  move.b	(a0)+,(a1)+
018B0C  move.w	#$2E20,(a1)+
018B10  cmp.b	#$20,(a0)+
018B14  bne.s	loc_18B10
018B16  move.b	(a0)+,(a1)+
018B18  cmp.l	a0,a2
018B1A  bne.s	loc_18B16
018B1C  bsr.w	sub_18BAE
018B20  movem.l	(sp)+,d0-d3/a0/a2
018B24  rts
```

## `$018B6E` -> `ai_FormatPlayerSurnamePadded`  (confidence 0.6, 20 insns)

**Evidence.** builds the string at $BFA4 as a space followed by the surname (text after the first space of the record's name), then pads with spaces up to $BFB2 (12 characters) before FinishNameBuffer; caller loc_85EE

**Callers.** loc_85EE
**Callees.** ai_FinishNameBuffer, getplayername, loc_18B9E

```
018B6E  movem.l	d0-d3/a0/a2,-(sp)
018B72  bsr.w	sub_18BC8
018B76  move.w	#$BFA6,a1
018B7A  move.b	#$20,(a1)+
018B7E  move.w	(a0)+,d0
018B80  lea	-2(a0,d0.w),a2
018B84  cmp.b	#$20,(a0)+
018B88  bne.s	loc_18B84
018B8A  move.b	(a0)+,(a1)+
018B8C  cmp.l	a0,a2
018B8E  beq.w	loc_18B9E
018B92  tst.b	(a0)
018B94  bne.s	loc_18B8A
018B96  bra.w	loc_18B9E
018B9A  move.b	#$20,(a1)+
018B9E  cmp.w	#$BFB2,a1
018BA2  blt.s	loc_18B9A
018BA4  bsr.w	sub_18BAE
018BA8  movem.l	(sp)+,d0-d3/a0/a2
018BAC  rts
```

## `$016C96` -> `ai_LoadRinkPalette`  (confidence 0.5, 7 insns)

**Evidence.** copies 16 longwords (64 bytes = two CRAM lines) from ROM $59924 (off_5605A plus its own offset word) to $BD28; $BD28 also receives colour $EEE elsewhere and is cleared at reset, so it is a palette buffer; callers loc_9CDC, setupice, sub_16BAC, all rink setup

**Callers.** loc_9CDC, setupice, sub_16BAC
**Callees.** none

```
016C96  move.l	#off_5605A,a0
016C9C  add.l	(a0),a0
016C9E  moveq	#$F,d0
016CA0  move.w	#$BD28,a1
016CA4  move.l	(a0)+,(a1)+
016CA6  dbf	d0,loc_16CA4
016CAA  rts
```

## `$016CAC` -> `ai_LoadRinkTiles`  (confidence 0.5, 4 insns)

**Evidence.** loads asset unk_B3538 at the tile base $B020 via ai_LoadAssetInline with the inline nibble map $7123 $4567 $89AB $CDEF; same three callers as LoadRinkPalette (loc_9CDC, setupice, sub_16BAC) during rink setup

**Callers.** loc_9CDC, setupice, sub_16BAC
**Callees.** ai_LoadAssetInline

```
016CAC  move.w	($FFFFB020).w,d4
016CB0  move.l	#unk_B3538,a2
016CB6  bsr.w	sub_1172C
016CBA  dc.w	$7123
016CBC  dc.w	$4567
016CBE  dc.w	$89AB
016CC0  dc.w	$CDEF
016CC2  rts
```

## `$011F04` -> `ai_LoadFontTiles`  (confidence 0.8, 3 insns)

**Evidence.** stores d4 in $B012 and loads asset unk_AAC5A there with LoadAsset; $B012 is the tile base the text printer (print, $11C4E) adds to every character index, so unk_AAC5A is the text font; callers PlayoffScreen, loc_9BD8, loc_FCC76

**Callers.** PlayoffScreen, loc_9BD8, loc_FCC76
**Callees.** ai_LoadAsset

```
011F04  move.w	d4,($FFFFB012).w
011F08  move.l	#unk_AAC5A,a2
011F0E  bra.w	sub_11738
```

## `$0F87D2` -> `ai_ResetCountdownD43C`  (confidence 0.4, 5 insns)

**Evidence.** reloads the frame countdown $D43C with $AA, or $53 when $D42E bit 5 is set; sub_F87EA decrements it every frame and toggles $D42E bit 1 when it reaches $52 (what the countdown drives is not yet identified); callers GameSetUp_2, sub_F7B20, sub_F87EA

**Callers.** GameSetUp_2, sub_F7B20, sub_F87EA
**Callees.** none

```
0F87D2  move.w	#$AA,($FFFFD43C).w
0F87D8  btst	#5,($FFFFD42E).w
0F87DE  beq.w	locret_F87E8
0F87E2  move.w	#$53,($FFFFD43C).w
0F87E8  rts
```

## `$0FD1FE` -> `ai_PrintTeamRatingsScreen`  (confidence 0.7, 83 insns)

**Evidence.** prints the pre-game team comparison: the category labels from word_FCFFA (Shooting, Skating, Passing, Defense, Checking, Fighting, Goalkeeping, Power Play Adv., Home Team Adv., Overall), the home ($C6CE) and away ($CA32) team names via sub_FCFB8 with the overall values kept in $D5A0/$D5A2; when $D598 is non-zero it prints the per-position comparison (center, left forward, right forward, ...) instead; callers loc_FCC76, sub_FCF86

**Callers.** loc_FCC76, sub_FCF86
**Callees.** AttribAdjust, CalcAttrib, DeterStrLength?, loc_FD252, loc_FD2E4, locret_FD3FE, print2, printz, printz2, sub_FCFB8, sub_FCFDC, sub_FD89A
**Strings.**  |  | center | left forward | right forward | left defenseman
**RAM.** printx, printy

```
0FD1FE  tst.w	($FFFFD598).w
0FD202  bne.w	loc_FD2D2
0FD206  jsr	sub_11A36
0FD20C  dc.w	$A
0FD20E  dc.b	$F8
0FD20F  dc.b	0
0FD210  dc.b	1
0FD211  dc.b	$16
0FD212  dc.b	$16
0FD213  dc.b	$F9
0FD214  dc.b	1
0FD215  dc.b	0
0FD216  lea	word_FCFFA(pc),a1
0FD21A  move.w	#0,d7
0FD21E  move.w	(a1),d0
0FD220  asr.w	#1,d0
0FD222  neg.w	d0
0FD224  add.w	#$16,d0
0FD228  move.w	d0,($FFFFB028).w
0FD22C  cmpnw	 9,d7
0FD230  beq.w	loc_FD23A
0FD234  add.w	(a1),a1
0FD236  bra.w	loc_FD252
0FD23A  move.w	#2,($FFFFB030).w
0FD240  move.w	($FFFFB02A).w,-(sp)
0FD244  subq.w	#3,($FFFFB02A).w
0FD248  jsr	sub_11A48
0FD24E  move.w	(sp)+,($FFFFB02A).w
0FD252  addq.w	#1,d7
0FD254  tst.w	(a1)
0FD256  bpl.s	loc_FD21E
0FD258  move.w	#2,($FFFFB030).w
0FD25E  jsr	sub_11B92
0FD264  dc.w	$2E
0FD266  dc.b	$FF
0FD267  dc.b	0
0FD268  dc.b	$17
0FD269  dc.b	'                                        ',0
0FD292  jsr	sub_11B92
0FD298  dc.w	6
0FD29A  dc.b	$FF
0FD29B  dc.b	$22
0FD29C  dc.b	$16
0FD29D  dc.b	0
0FD29E  move.l	#$FFFFC6CE,a0
0FD2A4  move.l	#$FFFFCA32,a2
0FD2AA  bsr.w	sub_FCFB8
0FD2AE  move.w	d0,($FFFFD5A0).w
0FD2B2  move.w	#2,($FFFFB030).w
0FD2B8  jsr	sub_11B92
0FD2BE  dc.w	6
0FD2C0  dc.b	$FF
0FD2C1  dc.b	4
0FD2C2  dc.b	$16
0FD2C3  dc.b	0
0FD2C4  exg	a0,a2
0FD2C6  bsr.w	sub_FCFB8
0FD2CA  move.w	d0,($FFFFD5A2).w
0FD2CE  bra.w	locret_FD3FE
0FD2D2  move.w	($FFFFD598).w,d0
...
```

## `$008BA6` -> `ai_DrawEditLinesHeader`  (confidence 0.6, 60 insns)

**Evidence.** edit-lines screen: prints the line title from word_8CBE indexed by $D5B2 (Goalies, Scoring 1, Scoring 2, Checking, Power Play 1, Power Play 2), the attribute column headers from word_193F8/word_1955A chosen by DispAttribCtr, erases the 40x16 body, and initialises the slot list at $C018 from the team's line table at $16A(a2); callers sub_8B84, sub_8B94

**Callers.** sub_8B84, sub_8B94
**Callees.** Adda1Offset, ai_CountRatingNibbles, eraser, getNameandAttrib, loc_8BD6, loc_8BF6, print, print2, printz2
**Strings.** Goalies    } | {  Scoring  1  } | {  Scoring  2  } | {   Checking   } | { Power Play 1 } | { Power Play 2 }
**RAM.** DispAttribCtr, printx, printy

```
008BA6  jsr	sub_11A36
008BAC  dc.w	$A
008BAE  dc.b	$F8
008BAF  dc.b	7
008BB0  dc.b	3
008BB1  dc.b	2
008BB2  dc.b	9
008BB3  dc.b	$F9
008BB4  dc.b	1
008BB5  dc.b	0
008BB6  move.w	($FFFFD5B2).w,d0
008BBA  lea	word_8CBE(pc),a1
008BBE  jsr	sub_13510
008BC4  jsr	sub_11A48
008BCA  jsr	sub_11A36
008BD0  dc.w	6
008BD2  dc.b	$FD
008BD3  dc.b	$16
008BD4  dc.b	$FC
008BD5  dc.b	9
008BD6  move.l	#word_193F8,a1
008BDC  move.w	($FFFFD5AC).w,d0
008BE0  tst.w	($FFFFD5B2).w
008BE4  bne.w	loc_8BF6
008BE8  move.l	#word_1955A,a1
008BEE  bra.w	loc_8BF6
008BF2  add.w	(a1),a1
008BF4  addq.w	#4,a1
008BF6  tst.w	(a1)
008BF8  dbmi	d0,loc_8BF2
008BFC  bpl.w	loc_8C06
008C00  subq.w	#1,($FFFFD5AC).w
008C04  bra.s	loc_8BD6
008C06  jsr	sub_11A48
008C0C  move.l	(a1),d4
008C0E  jsr	sub_11A36
008C14  dc.w	$A
008C16  dc.b	$F8
008C17  dc.b	4
008C18  dc.b	2
008C19  dc.b	0
008C1A  dc.b	0
008C1B  dc.b	$F9
008C1C  dc.b	0
008C1D  dc.b	0
008C1E  btst	#0,($FFFFD5B3).w
008C24  beq.w	loc_8C2E
008C28  add.w	#$10,($FFFFB02A).w
008C2E  move.w	($FFFFB02A).w,-(sp)
008C32  moveq	#$28,d0
008C34  moveq	#$10,d1
008C36  move.w	#$7FF,d2
008C3A  jsr	sub_1197E
008C40  move.w	(sp)+,($FFFFB02A).w
008C44  bsr.w	sub_9F40
008C48  move.w	d0,d1
008C4A  subq.w	#1,d1
008C4C  move.l	#$8CAE,a5
008C52  move.w	#$C018,a3
008C56  move.l	#$1020304,(a3)
...
```

