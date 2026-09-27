# Name review: names-batch-21.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$01A464` -> `ai_ReadPad2Hardware`  (confidence 0.7, 3 insns)

**Evidence.** port-2 controller read: points a0 at $A10005 and joins ai_ReadPad1Hardware's body at loc_1A47A (TH toggling, button packing and remap); caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** loc_1A47A
**Hardware.** pad2

```
01A464  movem.l	d1/a0,-(sp)
01A468  lea	($A10005).l,a0
01A46E  bra.s	loc_1A47A
```

## `$0F8770` -> `ai_SetAwayLogoPanel`  (confidence 0.5, 3 insns)

**Evidence.** loads d4 = tile base $D436 and printx = $18, then joins the panel-frame drawing at loc_F8796 (see ai_DrawSetupPhotoFrame); caller ai_DrawSetupAwayLogo

**Callers.** ai_DrawSetupAwayLogo
**Callees.** loc_F8796
**RAM.** printx

```
0F8770  move.w	($FFFFD436).w,d4
0F8774  move.w	#$18,($FFFFB028).w
0F877A  bra.w	loc_F8796
```

## `$0FD4C0` -> `ai_ResetAdvantageBar`  (confidence 0.8, 3 insns)

**Evidence.** clears the advantage-bar frame counter $D5A6 and step $D5A4 used by ai_AnimateAdvantageBar; caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** none

```
0FD4C0  clr.w	($FFFFD5A6).w
0FD4C4  clr.w	($FFFFD5A4).w
0FD4C8  rts
```

## `$0FE53C` -> `ai_RequestTileAnimation`  (confidence 0.5, 3 insns)

**Evidence.** sets $C2FC bit 0 and stores the requested animation id d0 in $D6BE for the animation player to pick up; caller puckfaceoff

**Callers.** puckfaceoff
**Callees.** none

```
0FE53C  bset	#0,($FFFFC2FC).w
0FE542  move.w	d0,($FFFFD6BE).w
0FE546  rts
```

## `$0FEF5A` -> `ai_BuildPlayedByString2`  (confidence 0.7, 3 insns)

**Evidence.** controller-2 entry of ai_BuildPlayedByString: loads user $D044 and joins its body at loc_FEED0; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** loc_FEED0

```
0FEF5A  movem.l	d0-a0/a2-a6,-(sp)
0FEF5E  move.w	($FFFFD044).w,d0
0FEF62  bra.w	loc_FEED0
```

## `$00868C` -> `ai_PrintEditLinesLayout`  (confidence 0.4, 2 insns)

**Evidence.** prints one long inline control string (attribute/position codes with embedded tile data) that lays out the edit-lines screen furniture; caller loc_8566

**Callers.** loc_8566
**Callees.** printz2

```
00868C  jsr	sub_11A36
008692  dc.w	8
008694  dc.b	$FF
008695  dc.b	2
008696  dc.b	$FD
008697  dc.b	0
008698  dc.b	$FC
008699  dc.b	$A
00869A  dc.b	$70
00869B  dc.b	$28
00869C  dc.b	$72
00869D  dc.b	$12
00869E  dc.b	$34
00869F  dc.b	$3C
0086A0  dc.b	7
0086A1  dc.b	$FF
0086A2  dc.b	$4E
0086A3  dc.b	$B9
0086A4  dc.b	0
0086A5  dc.b	1
0086A6  dc.b	$19
0086A7  dc.b	$7E
0086A8  dc.b	$33
0086A9  dc.b	$F9
0086AA  dc.b	0
0086AB  dc.b	0
0086AC  dc.b	$87
0086AD  dc.b	$A0
0086AE  dc.b	$FF
0086AF  dc.b	$FF
0086B0  dc.b	$B0
0086B1  dc.b	$2A
0086B2  dc.b	$33
0086B3  dc.b	$F9
0086B4  dc.b	0
0086B5  dc.b	0
0086B6  dc.b	$87
0086B7  dc.b	$9E
0086B8  dc.b	$FF
0086B9  dc.b	$FF
0086BA  dc.b	$B0
0086BB  dc.b	$28
0086BC  dc.b	$4A
0086BD  dc.b	$78
0086BE  dc.b	$D0
0086BF  dc.b	$58
0086C0  dc.b	$67
0086C1  dc.b	0
0086C2  dc.b	0
0086C3  dc.b	$C
0086C4  dc.b	$33
0086C5  dc.b	$F9
0086C6  dc.b	0
0086C7  dc.b	0
0086C8  dc.b	$87
0086C9  dc.b	$98
0086CA  dc.b	$FF
0086CB  dc.b	$FF
0086CC  dc.b	$B0
0086CD  dc.b	$28
...
```

## `$01A140` -> `ai_WaitVBlankThunk`  (confidence 0.6, 2 insns)

**Evidence.** jsr vcountwait then rts; a jump-table-friendly wrapper around the V-blank wait; caller InitSaveRAM

**Callers.** InitSaveRAM
**Callees.** vcountwait

```
01A140  jsr	sub_80BA
01A146  rts
```

## `$0F9C56` -> `ai_WriteUserRecord`  (confidence 0.8, 2 insns)

**Evidence.** sets the SRAM write flag $C2F8 bit 6 and jumps into ai_ReadUserRecord's body, so the transfer of the 16-byte user record goes through WriteSRAM; caller ai_UpdateUserWinLoss

**Callers.** ai_UpdateUserWinLoss
**Callees.** loc_F9C26

```
0F9C56  bset	#6,($FFFFC2F8).w
0F9C5C  bra.s	loc_F9C26
```

## `$0F9C5E` -> `ai_WriteUserNames`  (confidence 0.8, 2 insns)

**Evidence.** sets the SRAM write flag and jumps into ai_ReadUserNames' body, writing the $80-byte user-name table to SRAM $DA0; caller ai_SaveUserName

**Callers.** ai_SaveUserName
**Callees.** loc_F9C6E

```
0F9C5E  bset	#6,($FFFFC2F8).w
0F9C64  bra.w	loc_F9C6E
```

## `$0FA6E8` -> `ai_PrintCrowdRecordLine`  (confidence 0.7, 2 insns)

**Evidence.** stores the 'dB Crowd Level' label (word_FA6F6) in $BF18 and joins the shared record-line printer at loc_FA7B0; caller ai_PrintRecordsScreen

**Callers.** ai_PrintRecordsScreen
**Callees.** loc_FA7B0
**Strings.** dB Crowd Level

```
0FA6E8  move.l	#word_FA6F6,($FFFFBF18).l
0FA6F2  bra.w	loc_FA7B0
```

## `$0FF87C` -> `ai_ClearPowerPlaySongLatch`  (confidence 0.6, 2 insns)

**Evidence.** clears sflags2 bit 5, the once-only latch of ai_StartPowerPlaySong; caller ai_StartPowerPlaySong

**Callers.** ai_StartPowerPlaySong
**Callees.** none
**RAM.** sflags2

```
0FF87C  bclr	#5,($FFFFC2EE).w
0FF882  rts
```

## `$0F6E38` -> `ai_NopForcePlData`  (confidence 0.8, 1 insns)

**Evidence.** a bare rts reached from forcepldata; an empty hook

**Callers.** forcepldata
**Callees.** none

```
0F6E38  rts
```

## `$0F76CE` -> `ai_ApplyPlayoffPasswordThunk`  (confidence 0.8, 1 insns)

**Evidence.** jmp ai_ApplyPlayoffPassword; caller GameSetUp

**Callers.** GameSetUp
**Callees.** ai_ApplyPlayoffPassword

```
0F76CE  jmp	sub_17CA0
```

## `$0F84F8` -> `ai_NopGameSetUp2`  (confidence 0.8, 1 insns)

**Evidence.** a bare rts reached from GameSetUp_2; an empty hook

**Callers.** GameSetUp_2
**Callees.** none

```
0F84F8  rts
```

## `$00EE58` -> `ai_PickBestAvailableSkater`  (confidence 0.6, 89 insns)

**Evidence.** for BA_Team's roster walks the player records, skipping goalies (position nibble of byte 5 <= 1) and anyone whose status $66 is not -2/-1 (not available), sums the rating nibbles of bytes 1, 2, 3, 5, 6, 7 and keeps the best (compared against $D40A), leaving the winner in BA_Skater_Offset / BA_Sktr_SCnum; the 'best available' skater used for penalty shots and shootouts

**Callers.** none found
**Callees.** loc_EF88, loc_EF8C
**RAM.** BA_Skater_Offset, BA_Sktr_SCnum, BA_Team

```
00EE58  movem.l	d0-a6,-(sp)
00EE5C  move.l	#$FFFFC6CE,a0
00EE62  tst.w	($FFFFD404).w
00EE66  beq.w	loc_EE70
00EE6A  move.l	#$FFFFCA32,a0
00EE70  move.w	#0,d1
00EE74  move.w	#$FFFF,d6
00EE78  move.w	#$FFFF,d5
00EE7C  move.l	$1E(a0),a2
00EE80  add.w	(a2),a2
00EE82  cmp.w	#2,(a2)
00EE86  beq.w	loc_EF4C
00EE8A  add.w	(a2),a2
00EE8C  move.w	d1,d7
00EE8E  asl.w	#1,d7
00EE90  move.b	5(a2),d0
00EE94  and.w	#$F,d0
00EE98  cmpnb	 1,d0
00EE9C  ble.w	loc_EF40
00EEA0  btst	#0,($FFFFC2FA).w
00EEA6  bne.w	loc_EF56
00EEAA  cmp.w	#$FFFE,$66(a0,d7.w)
00EEB0  beq.w	loc_EEBE
00EEB4  cmp.w	#$FFFF,$66(a0,d7.w)
00EEBA  bne.w	loc_EF40
00EEBE  clr.w	d3
00EEC0  clr.w	d0
00EEC2  move.b	1(a2),d0
00EEC6  and.w	#$F,d0
00EECA  add.w	d0,d3
00EECC  move.b	2(a2),d0
00EED0  and.w	#$F,d0
00EED4  add.w	d0,d3
00EED6  move.b	2(a2),d0
00EEDA  and.w	#$F0,d0
00EEDE  lsr.w	#4,d0
00EEE0  add.w	d0,d3
00EEE2  move.b	3(a2),d0
00EEE6  and.w	#$F,d0
00EEEA  add.w	d0,d3
00EEEC  move.b	3(a2),d0
00EEF0  and.w	#$F0,d0
00EEF4  lsr.w	#4,d0
00EEF6  add.w	d0,d3
00EEF8  move.b	5(a2),d0
00EEFC  and.w	#$F,d0
00EF00  add.w	d0,d3
00EF02  move.b	5(a2),d0
00EF06  and.w	#$F0,d0
00EF0A  lsr.w	#4,d0
00EF0C  add.w	d0,d3
00EF0E  move.b	6(a2),d0
00EF12  and.w	#$F0,d0
00EF16  lsr.w	#4,d0
00EF18  add.w	d0,d3
00EF1A  move.b	7(a2),d0
00EF1E  and.w	#$F0,d0
00EF22  lsr.w	#4,d0
00EF24  add.w	d0,d3
00EF26  cmp.w	($FFFFD40A).w,d1
...
```

## `$0FC184` -> `ai_RankUsersByRecord`  (confidence 0.6, 75 insns)

**Evidence.** from the eight 16-byte user records loaded at $CF36 computes win percentage (wins bytes 8/9 * 100 / games bytes $A/$B) into $D54A, copies ties (+$C/$D) to $D552 and games to $D562, then bubble-sorts the index list $D542 (1..7) by percentage, ties and games; feeds ai_PrintUserStandings

**Callers.** none found
**Callees.** loc_FC1CC

```
0FC184  movem.l	d0-a6,-(sp)
0FC188  move.l	#$FFFFCF36,a0
0FC18E  move.l	#$FFFFD54A,a1
0FC194  move.l	#$FFFFD552,a6
0FC19A  move.l	#$FFFFD562,a5
0FC1A0  move.w	#7,d7
0FC1A4  move.b	8(a0),d0
0FC1A8  lsl.w	#8,d0
0FC1AA  move.b	9(a0),d0
0FC1AE  move.b	$A(a0),d1
0FC1B2  lsl.w	#8,d1
0FC1B4  move.b	$B(a0),d1
0FC1B8  move.w	d1,(a5)+
0FC1BA  tst.w	d1
0FC1BC  bne.w	loc_FC1C6
0FC1C0  clr.w	d0
0FC1C2  bra.w	loc_FC1CC
0FC1C6  mulu.w	#$64,d0
0FC1CA  divu.w	d1,d0
0FC1CC  move.b	d0,(a1)+
0FC1CE  move.b	$C(a0),(a6)+
0FC1D2  move.b	$D(a0),(a6)+
0FC1D6  add.w	#$10,a0
0FC1DA  dbf	d7,loc_FC1A4
0FC1DE  move.l	#$FFFFD542,a1
0FC1E4  move.l	a1,-(sp)
0FC1E6  move.w	#1,d0
0FC1EA  move.w	#6,d7
0FC1EE  move.b	d0,(a1)+
0FC1F0  addq.w	#1,d0
0FC1F2  dbf	d7,loc_FC1EE
0FC1F6  move.l	(sp),a1
0FC1F8  move.l	#$FFFFD54A,a0
0FC1FE  move.l	#$FFFFD552,a6
0FC204  move.l	#$FFFFD562,a5
0FC20A  move.l	(sp),a1
0FC20C  move.w	#5,d7
0FC210  clr.w	d6
0FC212  move.b	(a1)+,d1
0FC214  ext.w	d1
0FC216  move.b	(a1),d2
0FC218  ext.w	d2
0FC21A  move.b	(a0,d1.w),d0
0FC21E  move.b	(a0,d2.w),d3
0FC222  cmp.b	d3,d0
0FC224  bgt.w	loc_FC272
0FC228  blt.w	loc_FC264
0FC22C  movem.l	d1-d3,-(sp)
0FC230  add.w	d1,d1
0FC232  add.w	d2,d2
0FC234  move.w	(a6,d1.w),d0
0FC238  move.w	(a6,d2.w),d3
0FC23C  cmp.w	d3,d0
0FC23E  movem.l	(sp)+,d1-d3
0FC242  bgt.w	loc_FC272
0FC246  blt.w	loc_FC264
0FC24A  movem.l	d1-d3,-(sp)
0FC24E  add.w	d1,d1
0FC250  add.w	d2,d2
0FC252  move.w	(a5,d1.w),d0
...
```

## `$0FBEA4` -> `ai_PrintUserStandings`  (confidence 0.7, 59 insns)

**Evidence.** prints the seven ranked users from $D542: rank and name (ai_PrintRankedUserName) at column 2, percentage (3 digits) at $13, wins at $1A, losses (games - wins - ties, computed into $BF4C) at $1F and ties at $24, skipping users with no games

**Callers.** none found
**Callees.** DeterStrLength?, ai_PrintRankedUserName, loc_FBF8C, print2, printz2
**RAM.** printx, printy

```
0FBEA4  movem.l	d0-a6,-(sp)
0FBEA8  jsr	sub_11A36
0FBEAE  dc.w	$A
0FBEB0  dc.b	$F8
0FBEB1  dc.b	4
0FBEB2  dc.b	2
0FBEB3  dc.b	2
0FBEB4  dc.b	$A
0FBEB5  dc.b	$F9
0FBEB6  dc.b	0
0FBEB7  dc.b	0
0FBEB8  move.w	#6,d7
0FBEBC  move.l	#$FFFFD542,a0
0FBEC2  move.l	#$FFFFD54A,a2
0FBEC8  move.l	#$FFFFCF36,a5
0FBECE  move.w	#2,($FFFFB028).w
0FBED4  move.b	(a0)+,d0
0FBED6  ext.w	d0
0FBED8  move.b	(a2,d0.w),d5
0FBEDC  asl.w	#4,d0
0FBEDE  move.b	$A(a5,d0.w),d4
0FBEE2  lsl.w	#8,d4
0FBEE4  move.b	$B(a5,d0.w),d4
0FBEE8  move.w	d4,-(sp)
0FBEEA  move.b	$C(a5,d0.w),d4
0FBEEE  lsl.w	#8,d4
0FBEF0  move.b	$D(a5,d0.w),d4
0FBEF4  move.w	d4,($FFFFBF4A).w
0FBEF8  move.b	8(a5,d0.w),d4
0FBEFC  lsl.w	#8,d4
0FBEFE  move.b	9(a5,d0.w),d4
0FBF02  move.w	d4,($FFFFBF4E).w
0FBF06  add.w	($FFFFBF4A).w,d4
0FBF0A  sub.w	(sp),d4
0FBF0C  neg.w	d4
0FBF0E  move.w	d4,($FFFFBF4C).w
0FBF12  move.w	(sp)+,d4
0FBF14  tst.w	d4
0FBF16  beq.w	loc_FBF86
0FBF1A  bsr.w	sub_FC136
0FBF1E  move.w	#$13,($FFFFB028).w
0FBF24  move.w	d0,-(sp)
0FBF26  move.w	d5,d0
0FBF28  move.w	#3,d1
0FBF2C  jsr	sub_11D3A
0FBF32  jsr	sub_11A48
0FBF38  move.w	#$1A,($FFFFB028).w
0FBF3E  move.w	($FFFFBF4E).w,d0
0FBF42  move.w	#4,d1
0FBF46  jsr	sub_11D3A
0FBF4C  jsr	sub_11A48
0FBF52  move.w	#$1F,($FFFFB028).w
0FBF58  move.w	($FFFFBF4C).w,d0
0FBF5C  move.w	#4,d1
0FBF60  jsr	sub_11D3A
0FBF66  jsr	sub_11A48
0FBF6C  move.w	#$24,($FFFFB028).w
0FBF72  move.w	($FFFFBF4A).w,d0
0FBF76  move.w	#3,d1
0FBF7A  jsr	sub_11D3A
...
```

## `$016BAC` -> `ai_InitRinkScreen`  (confidence 0.6, 55 insns)

**Evidence.** rink screen start: sub_10F32, resets the camera (Hpos/Vpos = 0, $BD1A = $7D0), loads the palettes (sub_16DA2, ai_LoadRinkPalette), flips every player's facing bit when $C2EA bit 1 (rink flipped), sub_1720C, resets the per-player indicator words $BE78..$BE86, loads the rink tiles, initialises six $1C-byte indicator records at $BDB4 with sub_167AA, sets the sprite list pointer $BD14, sub_15E82, a fade ($BD26 = $1C) and installs sub_15D9A as the V-blank routine before enabling interrupts

**Callers.** none found
**Callees.** DoDMAlist, SetTeamColors, addframe2, ai_LoadRinkPalette, ai_LoadRinkTiles, defaultsprites, forceblack
**RAM.** DMAlistend, Hpos, Oldrow, Vpos, c1playernum, c2playernum, disflags, gmode, padcont, palcount, sflags, vbint, zamx

```
016BAC  movem.l	d0-a6,-(sp)
016BB0  bsr.w	sub_10F32
016BB4  bclr	#0,($FFFFC2EC).w
016BBA  move.w	($FFFFBF78).w,-(sp)
016BBE  bset	#2,($FFFFBF78).w
016BC4  clr.w	($FFFFBD1C).w
016BC8  clr.w	($FFFFBD18).w
016BCC  move.w	#$7D0,($FFFFBD1A).w
016BD2  st	($FFFFB8AC).w
016BD6  move.w	($FFFFB024).w,d4
016BDA  bsr.w	sub_16DA2
016BDE  bsr.w	sub_16C96
016BE2  btst	#1,($FFFFC2EA).w
016BE8  beq.w	loc_16C00
016BEC  move.w	#$B04A,a3
016BF0  moveq	#$B,d0
016BF2  bchg	#7,$62(a3)
016BF8  add.w	#$80,a3
016BFC  dbf	d0,loc_16BF2
016C00  bsr.w	sub_1720C
016C04  move.w	#$FFFF,($FFFFBE78).w
016C0A  move.w	#$FFFF,($FFFFBE86).w
016C10  clr.l	($FFFFBE7A).w
016C14  clr.l	($FFFFBE7E).w
016C18  clr.l	($FFFFBE82).w
016C1C  st	($FFFFC320).w
016C20  st	($FFFFC322).w
016C24  bsr.w	loc_16CAC
016C28  move.w	#$B8B4,a5
016C2C  move.w	#$C018,a6
016C30  moveq	#1,d6
016C32  move.w	#$BDB4,a3
016C36  clr.w	d0
016C38  clr.w	d1
016C3A  bsr.w	sub_167AA
016C3E  add.w	#$1C,a3
016C42  bsr.w	sub_167AA
016C46  add.w	#$1C,a3
016C4A  bsr.w	sub_167AA
016C4E  add.w	#$1C,a3
016C52  bsr.w	sub_167AA
016C56  add.w	#$1C,a3
016C5A  bsr.w	sub_167AA
016C5E  add.w	#$1C,a3
016C62  bsr.w	sub_167AA
016C66  move.l	a5,($FFFFBD14).w
016C6A  bsr.w	sub_15E82
016C6E  move.w	#$1C,($FFFFBD26).w
016C74  move.w	(sp)+,($FFFFBF78).w
016C78  move.l	#sub_15D9A,($FFFFB03A).w
016C80  bclr	#0,($FFFFBF78).w
016C86  bclr	#2,($FFFFBF78).w
016C8C  move	#$2300,sr
016C90  movem.l	(sp)+,d0-a6
016C94  rts
```

## `$01A7D8` -> `ai_SetChannelFrequency`  (confidence 0.5, 55 insns)

**Evidence.** sound driver: converts the note byte 1(a2) into octave and semitone (word_1A890 table), scales by the channel's pitch entry in (a3) and the instrument's detune from unk_2C248, and for FM channels (byte 3 < $60) stores the frequency word in $D18E[channel] with the update bits $D185/$D180, while for PSG channels with bit 0 of +6 set writes the attenuation byte straight to Z80 RAM $8E under bus request

**Callers.** none found
**Callees.** none
**Hardware.** Z80 busreq

```
01A7D8  clr.l	d3
01A7DA  move.b	1(a2),d3
01A7DE  divu.w	#$C,d3
01A7E2  move.w	d3,-(sp)
01A7E4  swap	d3
01A7E6  add.w	d3,d3
01A7E8  lea	word_1A890(pc),a4
01A7EC  move.w	(a4,d3.w),d2
01A7F0  clr.w	d1
01A7F2  move.b	(a2),d1
01A7F4  asl.w	#3,d1
01A7F6  move.w	(a3,d1.w),d3
01A7FA  beq.w	loc_1A834
01A7FE  moveq	#$C,d1
01A800  cmp.b	#$60,3(a2)
01A806  bge.w	loc_1A81C
01A80A  move.b	3(a2),d1
01A80E  asl.w	#5,d1
01A810  lea	(unk_2C248).l,a4
01A816  move.b	$1E(a4,d1.w),d1
01A81A  ext.w	d1
01A81C  muls.w	d1,d3
01A81E  asr.l	#2,d3
01A820  asr.w	#7,d3
01A822  add.w	#$C0,d3
01A826  add.w	d3,d3
01A828  lea	word_1A8A8(pc),a4
01A82C  mulu.w	(a4,d3.w),d2
01A830  asl.l	#1,d2
01A832  swap	d2
01A834  move.w	(sp)+,d3
01A836  cmp.b	#$60,3(a2)
01A83C  bge.w	loc_1A860
01A840  asl.w	#3,d3
01A842  asl.w	#8,d3
01A844  or.w	d3,d2
01A846  clr.w	d3
01A848  move.b	4(a2),d3
01A84C  bset	d3,($FFFFD185).w
01A850  add.w	d3,d3
01A852  move.w	#$D18E,a4
01A856  move.w	d2,(a4,d3.w)
01A85A  st	($FFFFD180).w
01A85E  rts
01A860  btst	#0,6(a2)
01A866  beq.w	locret_1A88E
01A86A  move.w	#$100,($A11100).l
01A872  btst	#0,($A11100).l
01A87A  bne.s	loc_1A872
01A87C  neg.w	d3
01A87E  addq.w	#8,d3
01A880  lsr.w	d3,d2
01A882  move.b	d2,($A0008E).l
01A888  clr.w	($A11100).l
01A88E  rts
```

## `$00A528` -> `ai_ReinitRinkAndReplay`  (confidence 0.5, 46 insns)

**Evidence.** when $C2F4 bit 6 requests it: toggles bit 4, saves the camera, sub_10F5C, waits two frames, reloads the rink graphics (ai_LoadRinkGraphics), fades in with sub_15EC0, restores the camera, marks both nets' objects ($B64A, +$80) with +8 = 1, sub_A67C and ai_DrawRinkAuxBitmap; then handles the replay frame ring: advances the read pointer with ai_AdvanceReplayFrame and stops at recbpr ($B036), otherwise sub_A68C

**Callers.** none found
**Callees.** RevReplayAdj, SetRCords, ai_AdvanceReplayFrame, ai_DrawRinkAuxBitmap, ai_LoadRinkGraphics, forceblack2, setvideo, vcountwait
**RAM.** Hpos, Oldrow, Vpos, palcount, recbpr, sflags, sflags2

```
00A528  bclr	#6,($FFFFC2F4).w
00A52E  beq.w	loc_A5D4
00A532  movem.l	d0-a6,-(sp)
00A536  bchg	#4,($FFFFC2F4).w
00A53C  move.w	($FFFFBD1C).w,-(sp)
00A540  move.w	($FFFFBD18).w,-(sp)
00A544  bsr.w	sub_10F5C
00A548  jsr	sub_80BA
00A54E  jsr	sub_80BA
00A554  jsr	loc_9CDC
00A55A  clr.w	($FFFFBD1C).w
00A55E  clr.w	($FFFFBD18).w
00A562  move.w	#$7D0,($FFFFBD1A).w
00A568  move.w	#1,d0
00A56C  jsr	sub_15EC0
00A572  jsr	sub_80BA
00A578  dbf	d0,loc_A56C
00A57C  move.w	(sp)+,($FFFFBD18).w
00A580  move.w	(sp)+,($FFFFBD1C).w
00A584  move.w	#1,d0
00A588  jsr	sub_15EC0
00A58E  jsr	sub_80BA
00A594  dbf	d0,loc_A58E
00A598  movem.l	a0,-(sp)
00A59C  move.l	#$FFFFB64A,a0
00A5A2  move.w	#1,8(a0)
00A5A8  add.w	#$80,a0
00A5AC  move.w	#1,8(a0)
00A5B2  movem.l	(sp)+,a0
00A5B6  bsr.w	sub_A67C
00A5BA  btst	#5,($FFFFC2EC).w
00A5C0  beq.w	*+4
00A5C4  jsr	sub_A448
00A5CA  move.w	#$64,($FFFFBD26).w
00A5D0  movem.l	(sp)+,d0-a6
00A5D4  clr.w	d7
00A5D6  btst	#2,($FFFFC2EE).w
00A5DC  beq.w	loc_A5F4
00A5E0  movem.l	a4,-(sp)
00A5E4  bsr.w	sub_A600
00A5E8  cmp.l	($FFFFB036).w,a4
00A5EC  movem.l	(sp)+,a4
00A5F0  beq.w	locret_A9D4
00A5F4  cmp.l	($FFFFB036).w,a4
00A5F8  beq.w	locret_A9D4
00A5FC  bsr.w	sub_A68C
```

## `$0FC282` -> `ai_RankUsersByRecordByte`  (confidence 0.5, 45 insns)

**Evidence.** reads the $80-byte user-record block from SRAM $D20 into $CF36, fills the index list $D532 (or $D53A when $C2F8 bit 6) with 1..7 and bubble-sorts it descending by record byte 0 (or byte 4 with the flag), the goals / saves record fields

**Callers.** none found
**Callees.** ReadSRAM
**Strings.** vs.¿ | Round | SHOOTOUT MODE

```
0FC282  movem.l	d0-a6,-(sp)
0FC286  move.l	#$D20,d0
0FC28C  move.l	#$80,d1
0FC292  move.l	#$FFFFCF36,a0
0FC298  jsr	sub_1A244
0FC29E  move.l	#$FFFFD532,a1
0FC2A4  btst	#6,($FFFFC2F8).w
0FC2AA  beq.w	loc_FC2B4
0FC2AE  move.l	#$FFFFD53A,a1
0FC2B4  move.l	a1,-(sp)
0FC2B6  move.w	#1,d0
0FC2BA  move.w	#6,d7
0FC2BE  move.b	d0,(a1)+
0FC2C0  addq.w	#1,d0
0FC2C2  dbf	d7,loc_FC2BE
0FC2C6  move.l	(sp),a1
0FC2C8  move.l	#$FFFFCF36,a0
0FC2CE  move.l	(sp),a1
0FC2D0  move.w	#5,d7
0FC2D4  clr.w	d6
0FC2D6  move.b	(a1)+,d1
0FC2D8  ext.w	d1
0FC2DA  move.b	(a1),d2
0FC2DC  ext.w	d2
0FC2DE  asl.w	#4,d1
0FC2E0  asl.w	#4,d2
0FC2E2  move.b	(a0,d1.w),d0
0FC2E6  move.b	(a0,d2.w),d3
0FC2EA  btst	#6,($FFFFC2F8).w
0FC2F0  beq.w	loc_FC2FC
0FC2F4  move.b	4(a0,d1.w),d0
0FC2F8  move.b	4(a0,d2.w),d3
0FC2FC  cmp.b	d3,d0
0FC2FE  bge.w	loc_FC310
0FC302  move.b	(a1),d0
0FC304  move.b	-1(a1),d1
0FC308  move.b	d0,-1(a1)
0FC30C  move.b	d1,(a1)
0FC30E  st	d6
0FC310  dbf	d7,loc_FC2D6
0FC314  tst.w	d6
0FC316  bne.s	loc_FC2CE
0FC318  move.l	(sp)+,a1
0FC31A  movem.l	(sp)+,d0-a6
0FC31E  rts
```

## `$0FB9D4` -> `ai_SaveUserName`  (confidence 0.7, 40 insns)

**Evidence.** name entry confirm: compares the typed name $D4DA ('-' treated as end) with user entry $D4EA in the table $D45A; when it differs copies the new name in, writes the table (ai_WriteUserNames), purges the old user's records (ai_PurgeUserFromRecords) and sub_1A206; finally stores the user index (0 if the name is empty) in the controller's user id $D042 or $D044 ($D4EE selects)

**Callers.** none found
**Callees.** MakeSRAMChecksum, ai_PurgeUserFromRecords, ai_WriteUserNames, loc_FBA4C

```
0FB9D4  movem.l	d0-a6,-(sp)
0FB9D8  move.l	#$FFFFD45A,a0
0FB9DE  move.w	($FFFFD4EA).w,d0
0FB9E2  mulu.w	#$C,d0
0FB9E6  add.w	d0,a0
0FB9E8  move.l	#$FFFFD4DA,a1
0FB9EE  move.w	#$B,d4
0FB9F2  cmp.b	#$2D,(a1)
0FB9F6  bne.w	loc_FB9FE
0FB9FA  move.b	#0,(a1)
0FB9FE  move.b	(a1)+,d1
0FBA00  cmp.b	(a0)+,d1
0FBA02  bne.w	loc_FBA0E
0FBA06  dbf	d4,loc_FB9F2
0FBA0A  bra.w	loc_FBA4C
0FBA0E  move.l	#$FFFFD45A,a0
0FBA14  move.w	($FFFFD4EA).w,d0
0FBA18  mulu.w	#$C,d0
0FBA1C  add.w	d0,a0
0FBA1E  move.l	#$FFFFD4DA,a1
0FBA24  move.w	#$B,d4
0FBA28  move.b	(a1)+,d1
0FBA2A  cmpnb	 $2D,d1
0FBA2E  bne.w	loc_FBA36
0FBA32  move.b	#0,d1
0FBA36  move.b	d1,(a0)+
0FBA38  dbf	d4,loc_FBA28
0FBA3C  bsr.w	sub_F9C5E
0FBA40  jsr	sub_FBA76
0FBA46  jsr	sub_1A206
0FBA4C  move.l	#$FFFFD042,a5
0FBA52  tst.w	($FFFFD4EE).w
0FBA56  beq.w	loc_FBA60
0FBA5A  move.l	#$FFFFD044,a5
0FBA60  tst.b	($FFFFD4DA).w
0FBA64  bne.w	loc_FBA6C
0FBA68  clr.w	($FFFFD4EA).w
0FBA6C  move.w	($FFFFD4EA).w,(a5)
0FBA70  movem.l	(sp)+,d0-a6
0FBA74  rts
```

## `$0FC850` -> `ai_PrintPlayerPickerList`  (confidence 0.5, 40 insns)

**Evidence.** player picker page: prints the column header from word_1940E (or word_19570 when $D5B8 is 5) selected by $D5AC, with the 'Overall ]' variants word_FC91A/word_FC930, then up to six rows from the slot list $C018 starting at PlayerScrollCtr via sub_8D4E, highlighting the row equal to VertLineScrolling

**Callers.** none found
**Callees.** getNameandAttrib, loc_FC85C, loc_FC87E, print, printz, printz2
**Strings.**  | Overall    ] | Overall    ]
**RAM.** DispAttribCtr, PlayerScrollCtr, VertLineScrolling, printa, printy

```
0FC850  jsr	sub_11B92
0FC856  dc.w	6
0FC858  dc.b	$BE
0FC859  dc.b	$16
0FC85A  dc.b	1
0FC85B  dc.b	0
0FC85C  move.l	#word_1940E,a1
0FC862  cmp.w	#5,($FFFFD5B8).w
0FC868  bne.w	loc_FC872
0FC86C  move.l	#word_19570,a1
0FC872  move.w	($FFFFD5AC).w,d0
0FC876  bra.w	loc_FC87E
0FC87A  add.w	(a1),a1
0FC87C  addq.w	#4,a1
0FC87E  tst.w	(a1)
0FC880  dbmi	d0,loc_FC87A
0FC884  bpl.w	loc_FC88E
0FC888  subq.w	#1,($FFFFD5AC).w
0FC88C  bra.s	loc_FC85C
0FC88E  cmp.l	#word_1940E,a1
0FC894  bne.w	loc_FC89E
0FC898  move.l	#word_FC91A,a1
0FC89E  cmp.l	#word_19570,a1
0FC8A4  bne.w	loc_FC8AE
0FC8A8  move.l	#word_FC930,a1
0FC8AE  jsr	sub_11BA4
0FC8B4  move.l	(a1),d4
0FC8B6  move.w	#$C018,a3
0FC8BA  move.w	($FFFFD5B0).w,d2
0FC8BE  move.w	($FFFFD5B6).w,d1
0FC8C2  sub.w	d2,d1
0FC8C4  cmpnw	 5,d1
0FC8C8  bls.w	loc_FC8CE
0FC8CC  moveq	#5,d1
0FC8CE  move.w	#2,($FFFFB02A).w
0FC8D4  jsr	sub_11A36
0FC8DA  dc.w	$20
0FC8DC  dc.b	$FE
0FC8DD  dc.b	4
0FC8DE  dc.b	$FD
0FC8DF  dc.b	5
0FC8E0  dc.b	$FA
0FC8E1  dc.b	1
0FC8E2  dc.b	'                      '
0FC8F8  dc.b	$FD
0FC8F9  dc.b	5
0FC8FA  cmp.w	($FFFFD5AE).w,d2
0FC8FE  bne.w	loc_FC906
0FC902  move.w	d7,($FFFFB02C).w
0FC906  clr.w	d0
0FC908  move.b	(a3,d2.w),d0
0FC90C  jsr	sub_8D4E
0FC912  addq.w	#1,d2
0FC914  dbf	d1,loc_FC8D4
0FC918  rts
```

## `$0FAEBC` -> `ai_DrawRecordsPlayerPhoto`  (confidence 0.7, 38 insns)

**Evidence.** records screen: selects the player (ai_SelectRecordsPlayer), fetches his photo for the shown side's team (ai_GetPlayerPhoto), decodes it (ai_UnpackPhotoTiles, generic image from off_C63F8 when none), copies the photo's 32-byte palette to $BD68 and draws the 6x6 image at column 1 row 8 with tile base $D452

**Callers.** none found
**Callees.** ai_GetPlayerPhoto, ai_SelectRecordsPlayer, ai_UnpackPhotoTiles, dobitmap, loc_FAF0E, printz
**RAM.** HomeTeam, VisTeam

```
0FAEBC  movem.l	d0-a6,-(sp)
0FAEC0  bsr.w	sub_FAF8C
0FAEC4  move.w	($FFFFC330).w,d1
0FAEC8  tst.w	($FFFFD4F6).w
0FAECC  beq.w	loc_FAED4
0FAED0  move.w	($FFFFC332).w,d1
0FAED4  bsr.w	sub_FAE26
0FAED8  jsr	sub_11B92
0FAEDE  dc.w	6
0FAEE0  dc.b	$8E
0FAEE1  dc.b	1
0FAEE2  dc.b	8
0FAEE3  dc.b	0
0FAEE4  move.w	($FFFFD452).w,d4
0FAEE8  move.l	a0,a1
0FAEEA  move.l	a0,a2
0FAEEC  add.l	(a2)+,a0
0FAEEE  move.l	#off_C63F8,a0
0FAEF4  add.l	(a0),a0
0FAEF6  tst.l	(a2)
0FAEF8  bne.w	loc_FAF0C
0FAEFC  move.l	#off_C63F8,a1
0FAF02  add.l	4(a1),a1
0FAF06  tst.l	(a2)+
0FAF08  bra.w	loc_FAF0E
0FAF0C  add.l	(a2)+,a1
0FAF0E  bsr.w	sub_FE98A
0FAF12  move.l	#$FFFFDA1E,a2
0FAF18  move.w	#6,d3
0FAF1C  move.w	#6,d2
0FAF20  clr.w	d0
0FAF22  clr.w	d1
0FAF24  movem.l	d0/a0-a1,-(sp)
0FAF28  add.w	#$20,a0
0FAF2C  move.l	#$FFFFBD68,a1
0FAF32  move.w	#7,d0
0FAF36  move.l	(a0)+,(a1)+
0FAF38  dbf	d0,loc_FAF36
0FAF3C  movem.l	(sp)+,d0/a0-a1
0FAF40  move.w	#0,d5
0FAF44  jsr	sub_1169A
0FAF4A  movem.l	(sp)+,d0-a6
0FAF4E  rts
```

