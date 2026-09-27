# Name review: names-batch-04.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$018192` -> `ai_EncodePlayoffPassword`  (confidence 0.7, 29 insns)

**Evidence.** exact inverse of ai_DecodePlayoffPassword: clears the five-word number at a3 (ai_BigNumClear), then folds in postarts (radix $20), bosgames (8), gamelevel (4), potreeteam ($10), pojoy (8), $CEF2 ($4000) and the +4/+6 win counts of the eight playoff series at $CE66 (radix 5 each) with ai_BigNumMulAdd; sub_180FC calls it with a3 = $D088 after a playoff game and then saves the result with ai_SavePlayoffPassword; callers sub_180FC, sub_18380

**Callers.** ai_AdvancePlayoffSeries, ai_AdvancePlayoffsAfterGame
**Callees.** ai_BigNumClear, ai_BigNumMulAdd
**RAM.** bosgames, gamelevel, pojoy, postarts, potreeteam

```
018192  bsr.w	sub_1820E
018196  move.w	($FFFFCEE8).w,d0
01819A  moveq	#$20,d1
01819C  bsr.w	sub_181F6
0181A0  move.w	($FFFFCEEA).w,d0
0181A4  moveq	#8,d1
0181A6  bsr.w	sub_181F6
0181AA  move.w	($FFFFCEEC).w,d0
0181AE  moveq	#4,d1
0181B0  bsr.w	sub_181F6
0181B4  move.w	($FFFFCEEE).w,d0
0181B8  moveq	#$10,d1
0181BA  bsr.w	sub_181F6
0181BE  move.w	($FFFFCEF0).w,d0
0181C2  moveq	#8,d1
0181C4  bsr.w	sub_181F6
0181C8  move.w	($FFFFCEF2).w,d0
0181CC  move.w	#$4000,d1
0181D0  bsr.w	sub_181F6
0181D4  moveq	#5,d1
0181D6  moveq	#7,d2
0181D8  move.w	#$CE66,a1
0181DC  move.w	4(a1),d0
0181E0  bsr.w	sub_181F6
0181E4  move.w	6(a1),d0
0181E8  bsr.w	sub_181F6
0181EC  add.w	#$10,a1
0181F0  dbf	d2,loc_181DC
0181F4  rts
```

## `$0181F6` -> `ai_BigNumMulAdd`  (confidence 0.7, 8 insns)

**Evidence.** number = number * d1 + d0 on the five-word number at a3 (swaps the registers, multiplies via sub_18236, adds via sub_1821A); the mixed-radix accumulator used only by ai_EncodePlayoffPassword

**Callers.** ai_EncodePlayoffPassword
**Callees.** ai_BigNumAdd, ai_BigNumMul

```
0181F6  movem.l	d0-d1,-(sp)
0181FA  exg	d0,d1
0181FC  bsr.w	sub_18236
018200  clr.l	d0
018202  move.w	d1,d0
018204  bsr.w	sub_1821A
018208  movem.l	(sp)+,d0-d1
01820C  rts
```

## `$01820E` -> `ai_BigNumClear`  (confidence 0.8, 5 insns)

**Evidence.** zeroes the five words at a3; callers sub_180FC (before saving an empty password) and ai_EncodePlayoffPassword

**Callers.** ai_AdvancePlayoffsAfterGame, ai_EncodePlayoffPassword
**Callees.** none

```
01820E  move.w	a3,a0
018210  moveq	#4,d0
018212  clr.w	(a0)+
018214  dbf	d0,loc_18212
018218  rts
```

## `$018380` -> `ai_AdvancePlayoffSeries`  (confidence 0.6, 104 insns)

**Evidence.** after a playoff game: stores the home and away scores ($C6DA, $CA3E) into the current series record at $CE66 + $CEE6*$10 (+$A/+$C), then credits the win to the side at +4 or +6 chosen by the score difference and the home/away bit 0 of +$E unless a side already has 4 wins; when bosgames is 7 it takes the loc_184D0 path; only caller sub_180FC (from PeriodOver)

**Callers.** ai_AdvancePlayoffsAfterGame
**Callees.** GetShifter, ai_EncodePlayoffPassword, loc_18438, randomd0
**RAM.** AwGoals, HmGoals, bosgames, gamelevel, gamenum, sflags3

```
018380  move.w	($FFFFCEE6).w,d0
018384  mulu.w	#$10,d0
018388  move.w	#$CE66,a0
01838C  move.w	($FFFFC6DA).w,$A(a0,d0.w)
018392  move.w	($FFFFCA3E).w,$C(a0,d0.w)
018398  bsr.w	sub_1828A
01839C  move.w	#$CE66,a0
0183A0  moveq	#$10,d3
0183A2  mulu.w	d1,d3
0183A4  add.w	d3,a0
0183A6  cmp.w	#7,($FFFFCEEA).w
0183AC  beq.w	loc_184D0
0183B0  cmp.w	#4,4(a0)
0183B6  beq.w	loc_183E8
0183BA  cmp.w	#4,6(a0)
0183C0  beq.w	loc_183E8
0183C4  clr.w	d3
0183C6  btst	#0,$E(a0)
0183CC  beq.w	loc_183D4
0183D0  eor.w	#2,d3
0183D4  move.w	$A(a0),d0
0183D8  sub.w	$C(a0),d0
0183DC  bpl.w	loc_183E4
0183E0  eor.w	#2,d3
0183E4  addq.w	#1,4(a0,d3.w)
0183E8  suba.w	#$10,a0
0183EC  dbf	d1,loc_183B0
0183F0  addq.w	#1,($FFFFCEEA).w
0183F4  cmp.w	#7,($FFFFCEEA).w
0183FA  beq.w	loc_1848A
0183FE  move.w	($FFFFCEE6).w,d0
018402  mulu.w	#$10,d0
018406  move.w	#$CE66,a0
01840A  add.w	d0,a0
01840C  cmp.w	#4,4(a0)
018412  beq.w	loc_18420
018416  cmp.w	#4,6(a0)
01841C  bne.w	locret_15464
018420  cmp.w	#3,($FFFFCEEC).w
018426  bge.w	loc_1848A
01842A  bsr.w	sub_1828A
01842E  move.w	#$CE66,a0
018432  moveq	#$10,d3
018434  mulu.w	d1,d3
018436  add.w	d3,a0
018438  cmp.w	($FFFFCEE6).w,d1
01843C  beq.w	loc_18474
018440  cmp.w	#4,4(a0)
018446  beq.w	loc_18474
01844A  cmp.w	#4,6(a0)
018450  beq.w	loc_18474
018454  addq.w	#1,4(a0)
018458  move.l	#$C8,d0
01845E  jsr	sub_11086
018464  and.w	#1,d0
018468  beq.s	loc_18438
01846A  subq.w	#1,4(a0)
01846E  addq.w	#1,6(a0)
018472  bra.s	loc_18438
018474  suba.w	#$10,a0
...
```

## `$0FE696` -> `ai_SavePlayoffPassword`  (confidence 0.7, 11 insns)

**Evidence.** WriteSRAM of $100 bytes from $D076 (the buffer holding the encoded password at $D088) to SRAM offset $1EF6, then sub_1A206, clears $C2EC bit 4 and resets $C016/$B036; only caller sub_180FC right after ai_EncodePlayoffPassword

**Callers.** ai_AdvancePlayoffsAfterGame
**Callees.** MakeSRAMChecksum, WriteSRAM
**RAM.** lastsfx, recbpr, sflags

```
0FE696  movem.l	d0-d1/a0,-(sp)
0FE69A  move.l	#$100,d1
0FE6A0  move.l	#$1EF6,d0
0FE6A6  move.l	#$FFFFD076,a0
0FE6AC  jsr	sub_1A1E4
0FE6B2  jsr	sub_1A206
0FE6B8  bclr	#4,($FFFFC2EC).w
0FE6BE  move.w	#$FFFF,($FFFFC016).w
0FE6C4  move.l	#$FFFF0000,($FFFFB036).w
0FE6CC  movem.l	(sp)+,d0-d1/a0
0FE6D0  rts
```

## `$0FAE26` -> `ai_GetPlayerPhoto`  (confidence 0.7, 44 insns)

**Evidence.** d0 = player index, d1 = team index: scans the per-team table off_F92F4[team] of (photo pointer, player index) pairs and returns the photo in a0 when the player has one; otherwise walks the team's roster (team table $30E) to the player record and returns one of four generic images (unk_C6F02, unk_C726C, unk_C6B98, unk_C682E) chosen by bit 0 of the record's +4 byte and by whether the index is below the count derived from the +$A word (goalie vs skater); callers loc_FAEBC and ai_DrawRatingsPictures, whose sub_FD14A then decodes the image with ai_UnpackPhotoTiles

**Callers.** ai_DrawRatingsPictures, ai_DrawRecordsPlayerPhoto
**Callees.** loc_FAE50, loc_FAE70, loc_FAEB6

```
0FAE26  movem.l	d0-d7/a1-a6,-(sp)
0FAE2A  move.l	#off_F92F4,a0
0FAE30  move.w	d1,d2
0FAE32  asl.w	#2,d2
0FAE34  move.l	(a0,d2.w),a0
0FAE38  move.w	#$FFFF,d2
0FAE3C  bra.w	loc_FAE50
0FAE40  cmp.w	4(a0),d0
0FAE44  bne.w	loc_FAE4E
0FAE48  move.l	(a0),a0
0FAE4A  bra.w	loc_FAEB6
0FAE4E  addq.l	#6,a0
0FAE50  addq.w	#1,d2
0FAE52  tst.l	(a0)
0FAE54  bne.s	loc_FAE40
0FAE56  move.l	#$30E,a0
0FAE5C  asl.w	#2,d1
0FAE5E  move.l	(a0,d1.w),a0
0FAE62  move.l	a0,a6
0FAE64  move.w	d0,d6
0FAE66  add.w	(a6),a6
0FAE68  bra.w	loc_FAE70
0FAE6C  add.w	(a6),a6
0FAE6E  addq.w	#8,a6
0FAE70  dbf	d6,loc_FAE6C
0FAE74  add.w	(a6),a6
0FAE76  add.w	$A(a0),a0
0FAE7A  move.w	(a0),d1
0FAE7C  clr.w	d3
0FAE7E  addq.w	#1,d3
0FAE80  asl.w	#4,d1
0FAE82  bne.s	loc_FAE7E
0FAE84  move.l	#unk_C6F02,a0
0FAE8A  btst	#0,4(a6)
0FAE90  bne.w	loc_FAE9A
0FAE94  move.l	#unk_C726C,a0
0FAE9A  cmp.w	d3,d0
0FAE9C  blt.w	loc_FAEB6
0FAEA0  move.l	#unk_C6B98,a0
0FAEA6  btst	#0,4(a6)
0FAEAC  bne.w	loc_FAEB6
0FAEB0  move.l	#unk_C682E,a0
0FAEB6  movem.l	(sp)+,d0-d7/a1-a6
0FAEBA  rts
```

## `$0FD084` -> `ai_DrawRatingsPictures`  (confidence 0.6, 42 insns)

**Evidence.** team ratings screen pictures: when $D598 is zero draws the away ($C332) and home ($C330) team logos through ai_GetTeamLogoAsset + ai_DrawTeamLogo6x6 at tile bases $D432/$D430 and columns 2/$20, row $F; otherwise draws the selected away/home player photos ($D59E/$D59C) through ai_GetPlayerPhoto + sub_FD14A; sets the palette-fade counter $BD26 to $64; callers loc_FCC76, sub_FCF86

**Callers.** ai_ChangeRatingsPosition, ai_MatchupsScreen
**Callees.** ai_DrawTeamLogo6x6, ai_GetPlayerPhoto, ai_GetTeamLogoAsset, ai_LoadPlayerPhoto, loc_FD144
**RAM.** HomeTeam, VisTeam, palcount, printa, printx, printy

```
0FD084  movem.l	d0-a6,-(sp)
0FD088  tst.w	($FFFFD598).w
0FD08C  bne.w	loc_FD0E6
0FD090  move.w	($FFFFC332).w,d3
0FD094  bsr.w	sub_FD1F0
0FD098  move.w	#2,($FFFFB028).w
0FD09E  move.w	#$F,($FFFFB02A).w
0FD0A4  move.w	($FFFFD432).w,d4
0FD0A8  move.w	#4,d5
0FD0AC  move.w	#$6000,($FFFFB02C).w
0FD0B2  bsr.w	sub_FD17E
0FD0B6  move.w	($FFFFC330).w,d3
0FD0BA  bsr.w	sub_FD1F0
0FD0BE  move.w	#$20,($FFFFB028).w
0FD0C4  move.w	#$F,($FFFFB02A).w
0FD0CA  move.w	($FFFFD430).w,d4
0FD0CE  move.w	#0,($FFFFB02C).w
0FD0D4  move.w	#2,d5
0FD0D8  bsr.w	sub_FD17E
0FD0DC  move.w	#$64,($FFFFBD26).w
0FD0E2  bra.w	loc_FD144
0FD0E6  move.w	($FFFFC332).w,d1
0FD0EA  move.w	($FFFFD59E).w,d0
0FD0EE  jsr	sub_FAE26
0FD0F4  move.w	#2,($FFFFB028).w
0FD0FA  move.w	#$F,($FFFFB02A).w
0FD100  move.w	($FFFFD432).w,d4
0FD104  move.w	#2,d5
0FD108  move.w	#0,($FFFFB02C).w
0FD10E  bsr.w	sub_FD14A
0FD112  move.w	($FFFFC330).w,d1
0FD116  move.w	($FFFFD59C).w,d0
0FD11A  jsr	sub_FAE26
0FD120  move.w	#$20,($FFFFB028).w
0FD126  move.w	#$F,($FFFFB02A).w
0FD12C  move.w	($FFFFD430).w,d4
0FD130  move.w	#0,d5
0FD134  move.w	#0,($FFFFB02C).w
0FD13A  bsr.w	sub_FD14A
0FD13E  move.w	#$64,($FFFFBD26).w
0FD144  movem.l	(sp)+,d0-a6
0FD148  rts
```

## `$0FD1F0` -> `ai_GetTeamLogoAsset`  (confidence 0.8, 4 insns)

**Evidence.** returns a0 = off_F86F2[d3] (d3 = team id), the same logo table sub_F8608 indexes with $D428; only caller ai_DrawRatingsPictures

**Callers.** ai_DrawRatingsPictures
**Callees.** none

```
0FD1F0  asl.w	#2,d3
0FD1F2  move.l	#off_F86F2,a0
0FD1F8  move.l	(a0,d3.w),a0
0FD1FC  rts
```

## `$0FD17E` -> `ai_DrawTeamLogo6x6`  (confidence 0.7, 28 insns)

**Evidence.** a0 = logo asset (offset pair header), d3 = team id, d5 = 4 or 2 (palette line): builds the 6x6-tile map from the asset via sub_1169A using the tile-name template at unk_FF462 + d3*8 - $40 or - $20, then positions the caption at column 2 or $20, row $19 and erases 8x3 there; only caller ai_DrawRatingsPictures

**Callers.** ai_DrawRatingsPictures
**Callees.** dobitmap, eraser, loc_FD19A, loc_FD1D4
**RAM.** printx

```
0FD17E  move.l	a0,a1
0FD180  move.l	a0,a2
0FD182  add.l	(a2)+,a0
0FD184  asl.w	#3,d3
0FD186  cmpnw	 4,d5
0FD18A  beq.w	loc_FD196
0FD18E  sub.w	#$20,d3
0FD192  bra.w	loc_FD19A
0FD196  sub.w	#$40,d3
0FD19A  move.l	#unk_FF462,a0
0FD1A0  add.w	d3,a0
0FD1A2  add.l	(a2)+,a1
0FD1A4  move.w	#6,d3
0FD1A8  move.w	#6,d2
0FD1AC  clr.w	d0
0FD1AE  clr.w	d1
0FD1B0  jsr	sub_1169A
0FD1B6  cmp.w	#$14,($FFFFB028).w
0FD1BC  bgt.w	loc_FD1CC
0FD1C0  move.w	#2,($FFFFB028).l
0FD1C8  bra.w	loc_FD1D4
0FD1CC  move.w	#$20,($FFFFB028).l
0FD1D4  move.w	#$19,($FFFFB02A).l
0FD1DC  move.w	#8,d0
0FD1E0  move.w	#3,d1
0FD1E4  move.w	#$7FF,d2
0FD1E8  jsr	sub_1197E
0FD1EE  rts
```

## `$0F8608` -> `ai_DrawSetupHomeLogo`  (confidence 0.6, 53 insns)

**Evidence.** game-setup screen, home side: after ai_ClearSetupLogoPanels clears $D42E bit 2 (away) and sets bits 3/7, calls sub_F878C, prints the panel caption at column $18, loads $D440 = $B4, then (shared tail loc_F865C) draws the logo of team $D428 from off_F86F2 as a 6x6 tile map through sub_1169A at tile base $D430 (or $D432 when bit 2 is set, the away entry ai_DrawSetupAwayLogo), using the template at unk_FF462 and preserving the palette longs $BD4A/$BD4E; callers GameSetUp, GameSetUp_2

**Callers.** GameSetUp, GameSetUp_2
**Callees.** ai_ClearSetupLogoPanels, ai_DrawSetupPhotoFrame, dobitmap, loc_F86AE, printz
**RAM.** palcount, printx, printy

```
0F8608  movem.l	d0-a6,-(sp)
0F860C  bsr.w	sub_F84FC
0F8610  bset	#3,($FFFFD42E).w
0F8616  bset	#7,($FFFFD42E).w
0F861C  bsr.w	sub_F878C
0F8620  bclr	#2,($FFFFD42E).w
0F8626  beq.w	loc_F864A
0F862A  jsr	sub_11B92
0F8630  dc.w	6
0F8632  dc.b	$EF
0F8633  dc.b	0
0F8634  dc.b	0
0F8635  dc.b	0
0F8636  move.w	#$18,($FFFFB028).w
0F863C  move.w	#5,($FFFFB02A).w
0F8642  moveq	#8,d0
0F8644  moveq	#8,d1
0F8646  move.w	#$7FF,d2
0F864A  jsr	sub_11B92
0F8650  dc.w	6
0F8652  dc.b	$CF
0F8653  dc.b	0
0F8654  dc.b	0
0F8655  dc.b	0
0F8656  move.w	#9,($FFFFB028).w
0F865C  move.w	#$B4,($FFFFD440).w
0F8662  move.w	#6,($FFFFB02A).w
0F8668  move.w	($FFFFD430).w,d4
0F866C  btst	#2,($FFFFD42E).w
0F8672  bne.w	loc_F867A
0F8676  move.w	($FFFFD432).w,d4
0F867A  move.w	($FFFFD428).w,d3
0F867E  asl.w	#2,d3
0F8680  move.l	#off_F86F2,a0
0F8686  move.l	(a0,d3.w),a0
0F868A  move.l	a0,a1
0F868C  move.l	a0,a2
0F868E  add.l	(a2)+,a0
0F8690  asl.w	#3,d3
0F8692  move.l	#unk_FF462,a0
0F8698  btst	#2,($FFFFD42E).w
0F869E  beq.w	loc_F86AA
0F86A2  sub.w	#$20,d3
0F86A6  bra.w	loc_F86AE
0F86AA  sub.w	#$40,d3
0F86AE  add.w	d3,a0
0F86B0  add.l	(a2)+,a1
0F86B2  move.w	#6,d3
0F86B6  move.w	#6,d2
0F86BA  clr.w	d0
0F86BC  clr.w	d1
0F86BE  move.l	($FFFFBD4A).w,-(sp)
0F86C2  move.l	($FFFFBD4E).w,-(sp)
0F86C6  move.w	#4,d5
0F86CA  btst	#2,($FFFFD42E).w
0F86D0  beq.w	loc_F86D8
0F86D4  move.w	#2,d5
0F86D8  jsr	sub_1169A
0F86DE  move.l	(sp)+,($FFFFBD4E).w
0F86E2  move.l	(sp)+,($FFFFBD4A).w
...
```

## `$0F84FC` -> `ai_ClearSetupLogoPanels`  (confidence 0.4, 33 insns)

**Evidence.** when $D42E bit 0 was set: clears bits 6/7 and erases the 8x8 logo panel at column 3 or $1C (chosen by $D42E bit 1) and the 25x8 caption area next to it, using the attribute prefixes $EF/$FF; callers ai_DrawSetupAwayLogo and ai_DrawSetupHomeLogo

**Callers.** ai_DrawSetupAwayLogo, ai_DrawSetupHomeLogo
**Callees.** eraser, loc_F85AA, printz
**RAM.** printx, printy

```
0F84FC  movem.l	d0-d7,-(sp)
0F8500  bclr	#0,($FFFFD42E).w
0F8506  beq.w	loc_F85AA
0F850A  bclr	#6,($FFFFD42E).w
0F8510  bclr	#7,($FFFFD42E).w
0F8516  jsr	sub_11B92
0F851C  dc.w	6
0F851E  dc.b	$EF
0F851F  dc.b	0
0F8520  dc.b	0
0F8521  dc.b	0
0F8522  move.w	#5,($FFFFB02A).w
0F8528  moveq	#8,d0
0F852A  moveq	#8,d1
0F852C  move.w	#$7FF,d2
0F8530  btst	#1,($FFFFD42E).w
0F8536  beq.w	loc_F8574
0F853A  move.w	#3,($FFFFB028).w
0F8540  jsr	sub_1197E
0F8546  jsr	sub_11B92
0F854C  dc.w	6
0F854E  dc.b	$FF
0F854F  dc.b	0
0F8550  dc.b	0
0F8551  dc.b	0
0F8552  move.w	#$B,($FFFFB028).w
0F8558  move.w	#5,($FFFFB02A).w
0F855E  move.w	#$19,d0
0F8562  move.w	#8,d1
0F8566  move.w	#$7FF,d2
0F856A  jsr	sub_1197E
0F8570  bra.w	loc_F85AA
0F8574  move.w	#$1C,($FFFFB028).w
0F857A  jsr	sub_1197E
0F8580  jsr	sub_11B92
0F8586  dc.w	6
0F8588  dc.b	$FF
0F8589  dc.b	0
0F858A  dc.b	0
0F858B  dc.b	0
0F858C  move.w	#3,($FFFFB028).w
0F8592  move.w	#5,($FFFFB02A).w
0F8598  move.w	#$19,d0
0F859C  move.w	#8,d1
0F85A0  move.w	#$7FF,d2
0F85A4  jsr	sub_1197E
0F85AA  movem.l	(sp)+,d0-d7
0F85AE  rts
```

## `$0F71F0` -> `ai_RateStartingSix`  (confidence 0.5, 44 insns)

**Evidence.** a0 = team record: takes the six player indexes listed at team data offset +6, and for each sums attribute nibbles 3..$F of its 16-byte row in the rating table at team+$1A2 (skipping 9 and $D), writing (index-1, sum) byte pairs to $BF20, then bubble-sorts the six pairs by sum descending; callers ai_BuildRatingsStartingSix and ai_SumStartingSixRatings

**Callers.** ai_BuildRatingsStartingSix, ai_SumStartingSixRatings
**Callees.** none

```
0F71F0  movem.l	d0-a6,-(sp)
0F71F4  move.l	a0,a2
0F71F6  add.l	#$1A2,a2
0F71FC  move.l	$1E(a0),a0
0F7200  add.w	6(a0),a0
0F7204  move.l	#$FFFFBF20,a1
0F720A  move.w	#5,d0
0F720E  move.b	(a0)+,d1
0F7210  subq.b	#1,d1
0F7212  move.b	d1,(a1)+
0F7214  ext.w	d1
0F7216  asl.w	#4,d1
0F7218  clr.b	(a1)
0F721A  addq.w	#3,d1
0F721C  move.w	#3,d7
0F7220  clr.w	d2
0F7222  move.b	(a2,d1.w),d2
0F7226  cmpnb	 9,d7
0F722A  beq.w	loc_F7238
0F722E  cmpnb	 $D,d7
0F7232  beq.w	loc_F7238
0F7236  add.b	d2,(a1)
0F7238  addq.w	#1,d1
0F723A  addq.w	#1,d7
0F723C  cmpnb	 $10,d7
0F7240  bne.s	loc_F7220
0F7242  tst.b	(a1)+
0F7244  dbf	d0,loc_F720E
0F7248  move.l	#$FFFFBF20,a1
0F724E  clr.w	d1
0F7250  move.w	#4,d0
0F7254  move.b	3(a1),d6
0F7258  cmp.b	1(a1),d6
0F725C  ble.w	loc_F726C
0F7260  st	d1
0F7262  move.w	2(a1),d2
0F7266  move.w	(a1),2(a1)
0F726A  move.w	d2,(a1)
0F726C  tst.w	(a1)+
0F726E  dbf	d0,loc_F7254
0F7272  tst.w	d1
0F7274  bne.s	loc_F7248
0F7276  movem.l	(sp)+,d0-a6
0F727A  rts
```

## `$0F737E` -> `ai_SumStartingSixRatings`  (confidence 0.6, 10 insns)

**Evidence.** runs ai_RateStartingSix for team a0 and returns d1 = the sum of the six rating totals at $BF20; sub_F7318 calls it for home and away, stores them in $BF12/$BF14 and derives the stronger side in $BF50 and an advantage bracket

**Callers.** ai_ComputeTeamAdvantage
**Callees.** ai_RateStartingSix

```
0F737E  bsr.w	sub_F71F0
0F7382  move.w	#6,d0
0F7386  move.l	#$FFFFBF20,a0
0F738C  clr.w	d1
0F738E  move.b	1(a0),d2
0F7392  ext.w	d2
0F7394  add.w	d2,d1
0F7396  tst.w	(a0)+
0F7398  dbf	d0,loc_F738E
0F739C  rts
```

## `$0F71A2` -> `ai_BuildRatingsStartingSix`  (confidence 0.5, 17 insns)

**Evidence.** clears $BF54/$BF56, then for the home ($C6CE) and away ($CA32) teams runs ai_RateStartingSix and copies the sorted index list to $BF5E/$BF5C (sub_F72DA) and the sums to $BF62/$BF60 (sub_F72FA); caller loc_FCC76 (ratings screen setup)

**Callers.** ai_MatchupsScreen
**Callees.** ai_CopyBestSixIndexes, ai_CopyWorstSixIndexes, ai_RateStartingSix

```
0F71A2  clr.w	($FFFFBF54).w
0F71A6  clr.w	($FFFFBF56).w
0F71AA  movem.l	d0-a6,-(sp)
0F71AE  move.l	#$FFFFC6CE,a0
0F71B4  bsr.w	sub_F71F0
0F71B8  move.l	#$FFFFBF5E,a0
0F71BE  bsr.w	sub_F72DA
0F71C2  move.l	#$FFFFBF62,a0
0F71C8  bsr.w	sub_F72FA
0F71CC  move.l	#$FFFFCA32,a0
0F71D2  bsr.w	sub_F71F0
0F71D6  move.l	#$FFFFBF5C,a0
0F71DC  bsr.w	sub_F72DA
0F71E0  move.l	#$FFFFBF60,a0
0F71E6  bsr.w	sub_F72FA
0F71EA  movem.l	(sp)+,d0-a6
0F71EE  rts
```

## `$00907C` -> `ai_PrintScoringSummaryRow`  (confidence 0.7, 33 insns)

**Evidence.** row of the scoring summary: entry d3 of ScoreSum ($C474; word time, byte team flag bit 7 = away and goal type in the low bits, then scorer and two assist indexes): erases the 40x4 row, prints the time (sub_11C72), the team name from the team record ($C6CE or +$364), the goal-type tag from word_912A (SH2, SH, PP, PP2) and the three player names via sub_9112; callers sub_9020 (row 30) and sub_904C

**Callers.** ai_PrintSummaryRowAbove, ai_PrintSummaryRowAt
**Callees.** ai_PrintNextString, ai_PrintPeriodAndTime, ai_PrintSummaryPlayerName, eraser, print
**RAM.** printa, printx, printy

```
00907C  move.w	($FFFFB02A).w,-(sp)
009080  moveq	#$28,d0
009082  moveq	#4,d1
009084  move.w	#$7FF,d2
009088  jsr	sub_1197E
00908E  move.w	(sp)+,($FFFFB02A).w
009092  move.w	#$C474,a0
009096  move.w	(a0,d3.w),d0
00909A  move.w	#1,($FFFFB028).w
0090A0  jsr	sub_11C72
0090A6  move.w	#$C6CE,a2
0090AA  btst	#7,2(a0,d3.w)
0090B0  beq.w	loc_90B8
0090B4  add.w	#$364,a2
0090B8  move.l	$1E(a2),a1
0090BC  add.w	4(a1),a1
0090C0  add.w	(a1),a1
0090C2  move.w	#$C,($FFFFB028).w
0090C8  jsr	sub_11BA4
0090CE  move.w	#$23,($FFFFB028).w
0090D4  lea	word_912A(pc),a1
0090D8  move.b	2(a0,d3.w),d0
0090DC  and.w	#$7F,d0
0090E0  jsr	sub_13508
0090E6  move.w	#$10,($FFFFB028).w
0090EC  move.b	3(a0,d3.w),d0
0090F0  bsr.w	sub_9112
0090F4  move.w	#$E000,($FFFFB02C).w
0090FA  move.w	#$12,($FFFFB028).w
009100  move.b	4(a0,d3.w),d0
009104  bsr.w	sub_9112
009108  move.w	#$12,($FFFFB028).w
00910E  move.b	5(a0,d3.w),d0
```

## `$00B92E` -> `ai_PrintLineChangeMenu`  (confidence 0.6, 37 insns)

**Evidence.** in-game line change box: prints the header (sub_B9C2, plus sub_18A56 when printy < $F), then for lines 2..0 asks getlchoice for the line state, prints 'line N' from the text at unk_44120 with the digit added, the line label from word_191A6 and the line energy (sub_12E66), marking the active line $16(a2) or the pending one $2E(a2); ends by printing the team name; callers lineinput, sub_F64E

**Callers.** ai_TickLineChangeTimer, lineinput
**Callees.** Framer, ai_DrawLineEnergyBar, ai_PrintNextString, box, getlchoice, loc_B950, print, setlccords
**RAM.** printx, printy, sflags3

```
00B92E  bsr.w	sub_B9C2
00B932  cmp.w	#$F,($FFFFB02A).w
00B938  blt.w	loc_B946
00B93C  bset	#0,($FFFFC2F0).w
00B942  bra.w	loc_B950
00B946  jsr	sub_18A56
00B94C  bsr.w	sub_B9C2
00B950  bsr.w	sub_119B8
00B954  subq.w	#2,($FFFFB02A).w
00B958  addq.w	#1,($FFFFB028).w
00B95C  moveq	#2,d4
00B95E  move.w	d4,d0
00B960  bsr.w	sub_BA04
00B964  tst.w	d0
00B966  bmi.w	loc_B9AC
00B96A  btst	#1,$30(a2)
00B970  bne.w	loc_B980
00B974  cmp.w	$2E(a2),d4
00B978  bne.w	loc_B9A8
00B97C  move.w	$16(a2),d0
00B980  move.w	#$BFA4,a1
00B984  move.l	#unk_44120,(a1)
00B98A  add.b	d4,2(a1)
00B98E  bsr.w	sub_11BA4
00B992  move.w	d0,-(sp)
00B994  move.l	#word_191A6,a1
00B99A  bsr.w	sub_13508
00B99E  move.w	(sp)+,d0
00B9A0  bsr.w	sub_12E66
00B9A4  subq.w	#5,($FFFFB028).w
00B9A8  subq.w	#1,($FFFFB02A).w
00B9AC  dbf	d4,loc_B95E
00B9B0  move.l	$1E(a2),a1
00B9B4  add.w	4(a1),a1
00B9B8  add.w	(a1),a1
00B9BA  addq.w	#2,($FFFFB028).w
00B9BE  bra.w	sub_11BA4
```

## `$007EF2` -> `ai_PrintScrollingMenu`  (confidence 0.6, 56 insns)

**Evidence.** generic options list: $CF20 = cursor index (wrapped to the item count), $CF22 = first visible item (kept within 3 of the cursor), $CF24 = length-prefixed item list installed by sub_7E36; walks to the first visible item and prints from row $D using the print2/inline control strings; callers loc_7E46 and loc_7E88 (menu refresh)

**Callers.** ai_PauseMenuInput, ai_RedrawPauseMenu
**Callees.** ai_PrintPauseMenuItem, ai_SetPauseMenuColumn, loc_7F14, loc_7F8A, print2, printz2
**RAM.** printy

```
007EF2  move.w	($FFFFCF20).w,d0
007EF6  bpl.w	loc_7F00
007EFA  clr.w	($FFFFCF20).w
007EFE  clr.w	d0
007F00  move.l	($FFFFCF24).w,a0
007F04  add.w	(a0),a0
007F06  add.w	(a0),a0
007F08  bra.w	loc_7F14
007F0C  add.w	(a0),a0
007F0E  addq.w	#4,a0
007F10  tst.w	2(a0)
007F14  dbmi	d0,loc_7F0C
007F18  addq.w	#1,d0
007F1A  sub.w	d0,($FFFFCF20).w
007F1E  move.w	($FFFFCF20).w,d0
007F22  cmp.w	($FFFFCF22).w,d0
007F26  bge.w	loc_7F2E
007F2A  move.w	d0,($FFFFCF22).w
007F2E  subq.w	#3,d0
007F30  cmp.w	($FFFFCF22).w,d0
007F34  ble.w	loc_7F3C
007F38  move.w	d0,($FFFFCF22).w
007F3C  bsr.w	sub_7E72
007F40  move.w	#$D,($FFFFB02A).w
007F46  move.l	($FFFFCF24).w,a1
007F4A  jsr	sub_11A48
007F50  jsr	sub_11A36
007F56  dc.w	$26
007F58  dc.b	$FB
007F59  dc.b	1
007F5A  dc.b	$20
007F5B  dc.b	$FB
007F5C  dc.b	$FF
007F5D  dc.b	$FA
007F5E  dc.b	1
007F5F  dc.b	$20
007F60  dc.b	$FB
007F61  dc.b	$FF
007F62  dc.b	$FA
007F63  dc.b	1
007F64  dc.b	$20
007F65  dc.b	$FB
007F66  dc.b	$FF
007F67  dc.b	$FA
007F68  dc.b	1
007F69  dc.b	$20
007F6A  dc.b	$FB
007F6B  dc.b	$12
007F6C  dc.b	$20
007F6D  dc.b	$FB
007F6E  dc.b	$FF
007F6F  dc.b	$FA
007F70  dc.b	$FF
007F71  dc.b	$20
007F72  dc.b	$FB
007F73  dc.b	$FF
007F74  dc.b	$FA
007F75  dc.b	$FF
007F76  dc.b	$20
007F77  dc.b	$FB
...
```

## `$016246` -> `ai_EmitCrowdSprites`  (confidence 0.6, 57 insns)

**Evidence.** d0 = crowd section (offset by $1F when $C2EC bit 7), a1 = section offset table, d4/d5 = camera x/y, d6 = sprite count, a6 = sprite table cursor: for every 8-byte crowd record (x, y, tile, attr, size) inside the camera window (x within -$90..+$80, y within -$80..+$70 of the camera) appends a 4-word hardware sprite (y, size/link d6, tile+$B01A, x) until 64 sprites; callers showcrowd and sub_16226

**Callers.** ai_EmitCrowdSections, showcrowd
**Callees.** none
**RAM.** sflags

```
016246  ext.w	d0
016248  beq.w	locret_15464
01624C  btst	#7,($FFFFC2EC).w
016252  beq.w	loc_1625A
016256  add.w	#$1F,d0
01625A  cmpnw	 $40,d6
01625E  bge.w	locret_15464
016262  movem.l	d0-d5,-(sp)
016266  add.w	d0,d0
016268  move.l	a1,a0
01626A  move.w	2(a0,d0.w),d1
01626E  sub.w	(a0,d0.w),d1
016272  lsr.w	#3,d1
016274  subq.w	#1,d1
016276  move.w	d1,-(sp)
016278  add.w	(a0,d0.w),a0
01627C  move.w	d4,d0
01627E  add.w	#$C0,d0
016282  move.w	d0,d1
016284  sub.w	#$90,d0
016288  add.w	#$80,d1
01628C  move.w	#$170,d2
016290  sub.w	d5,d2
016292  move.w	d2,d3
016294  sub.w	#$80,d2
016298  add.w	#$70,d3
01629C  move.w	(sp)+,d4
01629E  cmp.w	2(a0),d2
0162A2  bgt.w	loc_162F2
0162A6  cmp.w	2(a0),d3
0162AA  blt.w	loc_162F2
0162AE  cmp.w	(a0),d0
0162B0  bgt.w	loc_162F2
0162B4  cmp.w	(a0),d1
0162B6  blt.w	loc_162F2
0162BA  move.w	2(a0),d5
0162BE  add.w	#$70,d5
0162C2  sub.w	d2,d5
0162C4  move.w	d5,(a6)+
0162C6  move.b	7(a0),(a6)+
0162CA  move.b	d6,(a6)+
0162CC  move.w	6(a0),d5
0162D0  and.w	#$F800,d5
0162D4  add.w	4(a0),d5
0162D8  add.w	($FFFFB01A).w,d5
0162DC  move.w	d5,(a6)+
0162DE  move.w	(a0),d5
0162E0  add.w	#$70,d5
0162E4  sub.w	d0,d5
0162E6  move.w	d5,(a6)+
0162E8  addq.w	#1,d6
0162EA  cmpnw	 $40,d6
0162EE  beq.w	loc_162F8
0162F2  addq.w	#8,a0
0162F4  dbf	d4,loc_1629E
0162F8  movem.l	(sp)+,d0-d5
0162FC  rts
```

## `$0114B8` -> `ai_VDP_VramCopyDMA`  (confidence 0.9, 40 insns)

**Evidence.** VRAM-to-VRAM DMA: d0 = length, d2 = source VRAM address, d1 = destination; programs registers $93..$96, $97 = $C0 (copy mode), autoincrement 1, issues the command $4000xxxx | $C0 with the Z80 bus held, waits with VDP_WaitDMA and restores reg 1 = $64 / autoinc 2; $BF78 bit 2 is held during the transfer; callers sub_16D64 (team banner build) and sub_179D2

**Callers.** ai_BuildTeamBannerTiles, ai_ScrollTickerRows
**Callees.** WaitDMA
**RAM.** disflags, dmaram?
**Hardware.** VDP ctrl, Z80 busreq

```
0114B8  movem.l	d0-d3/a1,-(sp)
0114BC  move.w	($FFFFBF78).w,-(sp)
0114C0  bset	#2,($FFFFBF78).w
0114C6  lea	($C00004).l,a1
0114CC  move.w	#$8154,(a1)
0114D0  move.w	#$8F01,(a1)
0114D4  move.w	#$9300,d3
0114D8  move.b	d0,d3
0114DA  move.w	d3,(a1)
0114DC  move.w	#$9400,d3
0114E0  lsr.w	#8,d0
0114E2  move.b	d0,d3
0114E4  move.w	d3,(a1)
0114E6  move.w	#$9500,d3
0114EA  move.b	d2,d3
0114EC  move.w	d3,(a1)
0114EE  move.w	#$9600,d3
0114F2  lsr.w	#8,d2
0114F4  move.b	d2,d3
0114F6  move.w	d3,(a1)
0114F8  move.w	#$97C0,(a1)
0114FC  clr.l	d0
0114FE  move.w	d1,d0
011500  asl.l	#2,d0
011502  lsr.w	#2,d0
011504  swap	d0
011506  or.w	#$C0,d0
01150A  move.l	d0,($FFFFD06A).w
01150E  move.w	#$100,($A11100).l
011516  btst	#0,($A11100).l
01151E  bne.s	loc_11516
011520  move.w	($FFFFD06A).w,(a1)
011524  move.w	($FFFFD06C).w,(a1)
011528  bsr.w	VDP_WaitDMA
01152C  move.w	#$8164,(a1)
011530  move.w	#$8F02,(a1)
011534  clr.w	($A11100).l
01153A  move.w	(sp)+,($FFFFBF78).w
01153E  movem.l	(sp)+,d0-d3/a1
011542  rts
```

## `$0F6C44` -> `ai_PuckOnFacingSide`  (confidence 0.5, 35 insns)

**Evidence.** returns d0 = 1 when pucky ($B75E, the puck's relative y) is on the side the player object a3 faces (sign flipped by bit 7 of $62(a3)), else 0; the block at $F6C62..$F6CA4 comparing passdir against $54(a3) is unreachable (the branch before it is unconditional); callers asspassrec and doinput

**Callers.** asspassrec, doinput
**Callees.** loc_F6CA8, loc_F6CB0, loc_F6CB4
**RAM.** passdir, pucky

```
0F6C44  movem.w	d0-d1,-(sp)
0F6C48  move.w	($FFFFB75E).w,d0
0F6C4C  btst	#7,$62(a3)
0F6C52  bne.w	loc_F6C58
0F6C56  neg.w	d0
0F6C58  tst.w	d0
0F6C5A  bpl.w	loc_F6CB0
0F6C5E  bra.w	loc_F6CA8
0F6C62  move.w	($FFFFBEDC).w,d0
0F6C66  addq.w	#4,d0
0F6C68  and.w	#7,d0
0F6C6C  move.w	$54(a3),d1
0F6C70  cmp.w	d0,d1
0F6C72  bra.w	loc_F6CB0
0F6C76  beq.w	loc_F6CB0
0F6C7A  addq.w	#1,d1
0F6C7C  and.w	#7,d1
0F6C80  cmp.w	d0,d1
0F6C82  beq.w	loc_F6CB0
0F6C86  addq.w	#1,d1
0F6C88  and.w	#7,d1
0F6C8C  cmp.w	d0,d1
0F6C8E  beq.w	loc_F6CB0
0F6C92  subq.w	#3,d1
0F6C94  and.w	#7,d1
0F6C98  cmp.w	d0,d1
0F6C9A  beq.w	loc_F6CB0
0F6C9E  subq.w	#1,d1
0F6CA0  and.w	#7,d1
0F6CA4  beq.w	loc_F6CB0
0F6CA8  move.w	#0,d0
0F6CAC  bra.w	loc_F6CB4
0F6CB0  move.w	#1,d0
0F6CB4  movem.w	(sp)+,d0-d1
0F6CB8  rts
```

