# Name review: names-batch-12.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FC516` -> `ai_AdvanceShootoutRound`  (confidence 0.7, 20 insns)

**Evidence.** after each shootout attempt: when the shootout is enabled ($D595 bit 0), at least 5 rounds are done ($D578) and the round scores $D574/$D576 differ, sets $C2FA bit 3 and runs ai_ShootoutWinnersCelebrate; otherwise toggles the shooting side $D594 and, once both sides have shot, advances the shooter index $D586 (wrapping at 5) and the round counter; caller ai_EndShootoutAttempt

**Callers.** ai_EndShootoutAttempt
**Callees.** ai_ShootoutWinnersCelebrate, loc_FC56A

```
0FC516  movem.l	d0-a6,-(sp)
0FC51A  btst	#0,($FFFFD595).w
0FC520  beq.w	loc_FC54A
0FC524  cmp.w	#5,($FFFFD578).w
0FC52A  blt.w	loc_FC54A
0FC52E  move.w	($FFFFD574).w,d0
0FC532  cmp.w	($FFFFD576).w,d0
0FC536  beq.w	loc_FC54A
0FC53A  bset	#3,($FFFFC2FA).w
0FC540  jsr	sub_FD618
0FC546  bra.w	loc_FC56A
0FC54A  eor.w	#1,($FFFFD594).w
0FC550  bne.w	loc_FC56A
0FC554  addq.w	#1,($FFFFD586).w
0FC558  cmp.w	#5,($FFFFD586).w
0FC55E  blt.w	loc_FC566
0FC562  clr.w	($FFFFD586).w
0FC566  addq.w	#1,($FFFFD578).w
0FC56A  movem.l	(sp)+,d0-a6
0FC56E  rts
```

## `$00F37C` -> `ai_EndShootoutAttempt`  (confidence 0.6, 20 insns)

**Evidence.** checkgoal helper: freezes the camera (freezewindow), outside shootout mode sets a $A-frame timer $DEF0 and $C2EE bit 2, sets $C2EA bit 0, clears the stoppage bits of $C2F2 / $C2FA bit 2, restores the shooter's jersey byte $61 (BA_Sktr_SCnum object) from $C31E and calls ai_AdvanceShootoutRound; caller checkgoal

**Callers.** checkgoal
**Callees.** ai_AdvanceShootoutRound, freezewindow
**RAM.** BA_PS_flags, BA_Sktr_SCnum, gmode, sflags2

```
00F37C  jsr	sub_AFB6
00F382  btst	#0,($FFFFC2FA).w
00F388  bne.w	loc_F398
00F38C  move.w	#$A,($FFFFDEF0).w
00F392  bset	#2,($FFFFC2EE).w
00F398  bset	#0,($FFFFC2EA).w
00F39E  bclr	#2,($FFFFC2FA).w
00F3A4  bclr	#2,($FFFFC2F2).w
00F3AA  bclr	#3,($FFFFC2F2).w
00F3B0  bclr	#5,($FFFFC2F2).w
00F3B6  bclr	#4,($FFFFC2F2).w
00F3BC  bclr	#6,($FFFFC2F2).w
00F3C2  movem.l	d0/a0,-(sp)
00F3C6  move.l	#$FFFFB04A,a0
00F3CC  move.w	($FFFFD406).w,d0
00F3D0  asl.w	#7,d0
00F3D2  move.b	($FFFFC31E).w,$61(a0,d0.w)
00F3D8  movem.l	(sp)+,d0/a0
00F3DC  jsr	sub_FC516
00F3E2  rts
```

## `$0FC5AE` -> `ai_PrintShootoutWinner`  (confidence 0.8, 20 insns)

**Evidence.** SetPA: draws a 30x6 box at column 1 row $D, prints 'SHOOTOUT WON BY' in the big font, then the name of HomeTeam or VisTeam (team table $30E, name at offset +4) depending on which round score ($D574 vs $D576) is higher; caller SetPA

**Callers.** SetPA
**Callees.** Framer, ai_PrintBigInline, printbig, printz
**Strings.** SHOOTOUT WON BY | {Select Player}
**RAM.** HomeTeam, VisTeam, printx, printy

```
0FC5AE  movem.l	d0-a6,-(sp)
0FC5B2  jsr	sub_11B92
0FC5B8  dc.w	6
0FC5BA  dc.b	$BF
0FC5BB  dc.b	1
0FC5BC  dc.b	$D
0FC5BD  dc.b	0
0FC5BE  move.w	#6,d1
0FC5C2  move.w	#$1E,d0
0FC5C6  jsr	sub_119B8
0FC5CC  jsr	sub_11DE2
0FC5D2  dc.w	$14
0FC5D4  dc.b	$BF
0FC5D5  dc.b	2
0FC5D6  dc.b	$E
0FC5D7  aShootoutWonBy:	dc.b	'SHOOTOUT WON BY'
0FC5E6  addq.w	#2,($FFFFB02A).w
0FC5EA  move.w	($FFFFC330).w,d1
0FC5EE  move.w	($FFFFD574).w,d0
0FC5F2  cmp.w	($FFFFD576).w,d0
0FC5F6  bgt.w	loc_FC5FE
0FC5FA  move.w	($FFFFC332).w,d1
0FC5FE  asl.w	#2,d1
0FC600  move.l	#$30E,a1
0FC606  move.l	(a1,d1.w),a1
0FC60A  add.w	4(a1),a1
0FC60E  move.w	#2,($FFFFB028).w
0FC614  jsr	sub_11DF4
0FC61A  movem.l	(sp)+,d0-a6
0FC61E  rts
```

## `$0FD73C` -> `ai_ClearGameState`  (confidence 0.7, 21 insns)

**Evidence.** GameSetUp: zeroes the shootout block $D572 (19 words), both team records ($C6CE, 2 x $364 bytes), the penalty message buffer $C3A4 ($25 words), the state flag words $C2F2/$C2F4/$C2F8/$C2FA, the setup-screen flags $D42E and the photo index $D43E; caller GameSetUp

**Callers.** GameSetUp
**Callees.** none
**RAM.** BA_PS_flags

```
0FD73C  movem.l	d0-a6,-(sp)
0FD740  move.l	#$FFFFD572,a0
0FD746  moveq	#$12,d0
0FD748  clr.w	(a0)+
0FD74A  dbf	d0,loc_FD748
0FD74E  move.l	#$FFFFC6CE,a0
0FD754  move.w	#$363,d0
0FD758  clr.w	(a0)+
0FD75A  dbf	d0,loc_FD758
0FD75E  move.l	#$FFFFC3A4,a0
0FD764  moveq	#$24,d0
0FD766  clr.w	(a0)+
0FD768  dbf	d0,loc_FD766
0FD76C  clr.w	($FFFFC2F2).w
0FD770  clr.w	($FFFFC2F4).w
0FD774  clr.w	($FFFFC2F8).w
0FD778  clr.w	($FFFFC2FA).w
0FD77C  clr.w	($FFFFD42E).w
0FD780  clr.w	($FFFFD43E).w
0FD784  movem.l	(sp)+,d0-a6
0FD788  rts
```

## `$0F7B20` -> `ai_RedrawSetupValues`  (confidence 0.5, 20 insns)

**Evidence.** for the setup rows -2..$10 in steps of 2 calls GameSetUp_3 (option value logic) and, when the row is within the scrolled window ($D422), GameSetUp_4 (prints the value), then sub_F7BFA (the team names / 'Regular Season' / 'Continue Playoffs' entries), ai_RefreshSetupTeamLogos and, unless $D42E bit 0, ai_ResetPhotoRotateTimer; caller ai_RefreshSetupOptions

**Callers.** ai_RefreshSetupOptions
**Callees.** GameSetUp_3, GameSetUp_4, ai_RefreshSetupTeamLogos, ai_ResetPhotoRotateTimer, sub_F7BFA

```
0F7B20  move.w	d7,d6
0F7B22  moveq	#$FFFFFFFE,d7
0F7B24  addq.w	#2,d7
0F7B26  clr.w	d2
0F7B28  bsr.w	sub_F7942
0F7B2C  movem.l	d7,-(sp)
0F7B30  asr.w	#1,d7
0F7B32  cmp.w	($FFFFD422).w,d7
0F7B36  movem.l	(sp)+,d7
0F7B3A  blt.w	loc_F7B42
0F7B3E  bsr.w	sub_F7B66
0F7B42  cmpnw	 $10,d7
0F7B46  bne.s	loc_F7B24
0F7B48  bsr.w	sub_F7BFA
0F7B4C  move.w	d6,d7
0F7B4E  jsr	sub_17AF4
0F7B54  btst	#0,($FFFFD42E).w
0F7B5A  bne.w	locret_F7B64
0F7B5E  jsr	sub_F87D2
0F7B64  rts
```

## `$0FBB88` -> `ai_PromptUserRecordSelect`  (confidence 0.5, 20 insns)

**Evidence.** PeriodOver, only when OptUserRec is off: clears the user ids $D042/$D044 and, for each controller with a team selected (cont1team, and cont2team when it differs), sets $D4EE = team - 1 and runs the user-name selection screen loc_FB018 (installs loc_17C42 as the V-blank routine and rebuilds the planes); caller PeriodOver

**Callers.** PeriodOver
**Callees.** loc_FB018
**RAM.** OptUserRec, cont1team, cont2team

```
0FBB88  tst.w	($FFFFD054).w
0FBB8C  bne.w	locret_FBBDC
0FBB90  clr.w	($FFFFD042).w
0FBB94  clr.w	($FFFFD044).w
0FBB98  tst.w	($FFFFC328).w
0FBB9C  beq.w	loc_FBBB0
0FBBA0  move.w	($FFFFC328).w,($FFFFD4EE).w
0FBBA6  subq.w	#1,($FFFFD4EE).w
0FBBAA  jsr	loc_FB018
0FBBB0  tst.w	($FFFFC32A).w
0FBBB4  beq.w	locret_FBBDC
0FBBB8  movem.w	d0,-(sp)
0FBBBC  move.w	($FFFFC328).w,d0
0FBBC0  cmp.w	($FFFFC32A).w,d0
0FBBC4  movem.w	(sp)+,d0
0FBBC8  beq.w	locret_FBBDC
0FBBCC  move.w	($FFFFC32A).w,($FFFFD4EE).w
0FBBD2  subq.w	#1,($FFFFD4EE).w
0FBBD6  jsr	loc_FB018
0FBBDC  rts
```

## `$016D18` -> `ai_LoadTeamBanners`  (confidence 0.7, 21 insns)

**Evidence.** setupice: records the banner tile base in $B022, loads asset off_ABA14 (the banner font/tiles) into VRAM with the name-table buffer $C334 as a1, then builds the home ($C330) and away ($C332) banner rows with ai_BuildTeamBannerTiles at tile offsets $B022*32 and ($B022+$16)*32; returns d4 = $B022 + $2C (next free tile); caller setupice

**Callers.** setupice
**Callees.** ai_BuildTeamBannerTiles, ai_LoadAsset
**RAM.** HomeTeam, VisTeam

```
016D18  move.w	d4,($FFFFB022).w
016D1C  add.w	#$2C,d4
016D20  move.w	#$C334,a1
016D24  move.l	#off_ABA14,a0
016D2A  lea	8(a0),a2
016D2E  bsr.w	sub_11738
016D32  add.l	4(a0),a0
016D36  move.l	a0,-(sp)
016D38  move.w	($FFFFC330).w,d0
016D3C  move.w	($FFFFB022).w,d1
016D40  asl.w	#5,d1
016D42  bsr.w	sub_16D64
016D46  move.l	(sp)+,a0
016D48  move.w	($FFFFC332).w,d0
016D4C  move.w	($FFFFB022).w,d1
016D50  add.w	#$16,d1
016D54  asl.w	#5,d1
016D56  bsr.w	sub_16D64
016D5A  move.w	($FFFFB022).w,d4
016D5E  add.w	#$2C,d4
016D62  rts
```

## `$016D64` -> `ai_BuildTeamBannerTiles`  (confidence 0.6, 20 insns)

**Evidence.** d0 = team id, d1 = destination VRAM address: takes the team's 44-byte banner row (44 * team + 4 in the asset) and for its 22 entries writes a name-table word (priority/palette from the entry byte, tile = destination/32 | $8000) into the $C334 buffer at a1 and copies the referenced source tile (entry & $7FF + $B022 + $2C) to the destination with ai_VDP_VramCopyDMA; caller ai_LoadTeamBanners

**Callers.** ai_LoadTeamBanners
**Callees.** ai_VDP_VramCopyDMA

```
016D64  mulu.w	#$2C,d0
016D68  lea	4(a0,d0.w),a0
016D6C  move.w	#$15,d3
016D70  moveq	#$20,d0
016D72  move.w	d1,-(sp)
016D74  move.b	(a0),(a1)
016D76  and.w	#$F800,(a1)
016D7A  lsr.w	#5,d1
016D7C  or.w	#$8000,d1
016D80  or.w	d1,(a1)+
016D82  move.w	(sp)+,d1
016D84  move.w	(a0)+,d2
016D86  and.w	#$7FF,d2
016D8A  add.w	($FFFFB022).w,d2
016D8E  add.w	#$2C,d2
016D92  asl.w	#5,d2
016D94  bsr.w	sub_114B8
016D98  add.w	#$20,d1
016D9C  dbf	d3,loc_16D70
016DA0  rts
```

## `$0185E0` -> `ai_TakeTopStar`  (confidence 0.7, 20 insns)

**Evidence.** scans the 52 star scores at $CF36, picks the highest, clears it so the next call returns the runner-up, and returns d0 = the player index (0..$19) with a2 = the home record, or the away record for indexes $1A and up; caller ai_StarsOfTheGameScreen (three times)

**Callers.** ai_StarsOfTheGameScreen
**Callees.** none

```
0185E0  movem.l	d1-d2/a1/a4,-(sp)
0185E4  move.w	#$CF36,a4
0185E8  clr.l	d0
0185EA  moveq	#$33,d2
0185EC  cmp.l	(a4)+,d0
0185EE  bge.w	loc_185F8
0185F2  lea	-4(a4),a1
0185F6  move.l	(a1),d0
0185F8  dbf	d2,loc_185EC
0185FC  clr.l	(a1)
0185FE  move.w	a1,d0
018600  sub.w	#$CF36,d0
018604  lsr.w	#2,d0
018606  move.w	#$C6CE,a2
01860A  cmpnw	 $1A,d0
01860E  blt.w	loc_1861A
018612  sub.w	#$1A,d0
018616  add.w	#$364,a2
01861A  movem.l	(sp)+,d1-d2/a1/a4
01861E  rts
```

## `$018236` -> `ai_BigNumMul`  (confidence 0.8, 20 insns)

**Evidence.** multiplies the five-word number at a3 by d0: pops each word, multiplies it by d0 and adds the 32-bit product into the running number with carry propagation (dbcc loop); only caller ai_BigNumMulAdd

**Callers.** ai_BigNumMulAdd
**Callees.** loc_1825E

```
018236  movem.l	d1-d4/a0,-(sp)
01823A  move.w	a3,a0
01823C  moveq	#4,d4
01823E  move.w	(a0),-(sp)
018240  clr.w	(a0)+
018242  dbf	d4,loc_1823E
018246  moveq	#4,d4
018248  move.w	d0,d1
01824A  mulu.w	(sp)+,d1
01824C  lea	2(a3),a0
018250  add.w	d4,a0
018252  add.w	d4,a0
018254  move.w	d4,d2
018256  add.l	d1,-(a0)
018258  bra.w	loc_1825E
01825C  addq.w	#1,-(a0)
01825E  dbcc	d2,loc_1825C
018262  dbf	d4,loc_18248
018266  movem.l	(sp)+,d1-d4/a0
01826A  rts
```

## `$00F5C6` -> `ai_AssignFaceoffPlayer`  (confidence 0.4, 19 insns)

**Evidence.** puckfaceoff helper: with a2/a3 swapped, selects object d0 ($B04A + d0*$80), clears its $63 bit 3, runs SetLCmode (line-change mode when the option allows), and if bit 3 got set records the player's state $52 and a target ($168 into +$42/+$46 for the bit-6 side, $258 into +$40/+$44 for the other) in the faceoff record a2; caller puckfaceoff

**Callers.** puckfaceoff
**Callees.** SetLCmode, loc_F60E

```
00F5C6  exg	a2,a3
00F5C8  asl.w	#7,d0
00F5CA  move.w	#$B04A,a3
00F5CE  add.w	d0,a3
00F5D0  bclr	#3,$63(a3)
00F5D6  move.l	a2,-(sp)
00F5D8  bsr.w	sub_B8F2
00F5DC  move.l	(sp)+,a2
00F5DE  btst	#3,$63(a3)
00F5E4  beq.w	loc_F60E
00F5E8  btst	#6,$62(a3)
00F5EE  beq.w	loc_F602
00F5F2  move.w	#$168,$42(a2)
00F5F8  move.w	$52(a3),$46(a2)
00F5FE  bra.w	loc_F60E
00F602  move.w	#$258,$40(a2)
00F608  move.w	$52(a3),$44(a2)
00F60E  exg	a2,a3
00F610  rts
```

## `$01A5C0` -> `ai_RunMusicTrack`  (confidence 0.7, 22 insns)

**Evidence.** MusicVB sequencer step for track a5: counts the wait 4(a5) down, then reads the next 4-byte command from the track pointer (a5): byte 1 = 0 ends the track (or jumps to the loop pointer at +2 unless -1), otherwise bits 4..6 of byte 1 select a handler from the jump table word_1A60A (8 entries) and the loop continues until a wait is set; caller MusicVB

**Callers.** MusicVB
**Callees.** loc_1A5C8

```
01A5C0  subq.w	#1,4(a5)
01A5C4  bpl.w	locret_1A292
01A5C8  tst.w	(a5)
01A5CA  bmi.w	locret_1A292
01A5CE  move.l	(a5),a0
01A5D0  addq.l	#4,(a5)
01A5D2  clr.w	4(a5)
01A5D6  move.b	4(a0),5(a5)
01A5DC  move.b	1(a0),d0
01A5E0  bne.w	loc_1A5F4
01A5E4  st	(a5)
01A5E6  tst.w	2(a0)
01A5EA  bmi.w	locret_1A292
01A5EE  move.l	2(a0),(a5)
01A5F2  bra.s	loc_1A5C8
01A5F4  move.b	1(a0),d0
01A5F8  and.w	#$70,d0
01A5FC  lsr.w	#3,d0
01A5FE  lea	word_1A60A(pc),a2
01A602  add.w	(a2,d0.w),a2
01A606  jsr	(a2)
01A608  bra.s	sub_1A5C0
```

