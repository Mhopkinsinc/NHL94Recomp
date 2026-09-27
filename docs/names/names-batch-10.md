# Name review: names-batch-10.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$007E88` -> `ai_PauseMenuInput`  (confidence 0.7, 30 insns)

**Evidence.** PauseMode: d1 = new pad bits; Start (bit 7) returns with the carry flag toggled (exit), Down/Up (bits 1/0) move the cursor $CF20 and redraw via ai_PrintScrollingMenu, C (bit 5) resolves the controlling team (ai_GetControllingTeam), walks the item list $CF24 to entry $CF20 and calls its handler, then redraws the menu unless $C2F6 bit 1 was set; returns Z from the cursor value; caller PauseMode

**Callers.** PauseMode
**Callees.** ai_GetControllingTeam, ai_PrintScrollingMenu, loc_7E46, loc_7ECE

```
007E88  btst	#7,d1
007E8C  bne.w	loc_7EEC
007E90  btst	#1,d1
007E94  beq.w	loc_7EA0
007E98  addq.w	#1,($FFFFCF20).w
007E9C  bra.w	loc_7EF2
007EA0  btst	#0,d1
007EA4  beq.w	loc_7EB0
007EA8  subq.w	#1,($FFFFCF20).w
007EAC  bra.w	loc_7EF2
007EB0  btst	#5,d1
007EB4  beq.w	loc_7EEC
007EB8  bsr.w	sub_7E0E
007EBC  move.w	($FFFFCF20).w,d0
007EC0  move.l	($FFFFCF24).w,a0
007EC4  add.w	(a0),a0
007EC6  add.w	(a0),a0
007EC8  bra.w	loc_7ECE
007ECC  addq.w	#4,a0
007ECE  add.w	(a0),a0
007ED0  dbf	d0,loc_7ECC
007ED4  move.l	(a0),a0
007ED6  jsr	(a0)
007ED8  bclr	#1,($FFFFC2F6).w
007EDE  bne.w	loc_7EE6
007EE2  bsr.w	loc_7E46
007EE6  tst.w	($FFFFCF20).w
007EEA  rts
007EEC  eor	#4,ccr
007EF0  rts
```

## `$0F78A2` -> `ai_RefreshSetupOptions`  (confidence 0.5, 26 insns)

**Evidence.** GameSetUp helper: forces OptUserRec on in playoff state 4 or outside playoffs ($D04A = 0), resets the OptGoalie/$D05A/$D05C options to 1 outside playoffs, reprints the row labels (ai_PrintSetupMenuLabels) when the scroll offset $D422 changed, then redraws the option values with sub_F7B20 under $C2F8 bit 3; caller GameSetUp

**Callers.** GameSetUp
**Callees.** ai_PrintSetupMenuLabels, sub_F7B20
**RAM.** OptGoalie, OptNOP, OptPlayMode, OptUserRec

```
0F78A2  movem.l	d0-a6,-(sp)
0F78A6  cmp.w	#4,($FFFFD048).w
0F78AC  bne.w	loc_F78B6
0F78B0  move.w	#1,($FFFFD054).w
0F78B6  tst.w	($FFFFD04A).w
0F78BA  bne.w	loc_F78C4
0F78BE  move.w	#1,($FFFFD054).w
0F78C4  tst.w	($FFFFD04A).w
0F78C8  bne.w	loc_F78F8
0F78CC  move.w	#0,($FFFFD052).w
0F78D2  move.w	#0,($FFFFD05A).w
0F78D8  move.w	#0,($FFFFD05C).w
0F78DE  tst.w	($FFFFD04A).w
0F78E2  bne.w	loc_F78F8
0F78E6  move.w	#1,($FFFFD052).w
0F78EC  move.w	#1,($FFFFD05A).w
0F78F2  move.w	#1,($FFFFD05C).w
0F78F8  move.w	($FFFFD422).w,d0
0F78FC  cmp.w	($FFFFD424).w,d0
0F7900  beq.w	loc_F7908
0F7904  bsr.w	sub_F8070
0F7908  bset	#3,($FFFFC2F8).w
0F790E  bsr.w	sub_F7B20
0F7912  bclr	#3,($FFFFC2F8).w
0F7918  movem.l	(sp)+,d0-a6
0F791C  rts
```

## `$017AF4` -> `ai_RefreshSetupTeamLogos`  (confidence 0.5, 28 insns)

**Evidence.** sub_F7B20 helper: in playoff state 0 or 4 copies Opt1Team/Opt2Team into HomeTeam/VisTeam, then for the away and home teams loads the logo palette from word_F8BF4 (64 bytes per team: +$26 away, +2 home) into $BD4E/$BD4A, draws the logo bitmap from off_AFE12 with sub_17B78 at tile bases $D43A and 2, calls sub_17190 and starts a palette fade ($BD26 = $64); caller sub_F7B20

**Callers.** sub_F7B20
**Callees.** printz, sub_17190, sub_17B78
**RAM.** HomeTeam, Opt1Team, Opt2Team, OptPlayMode, VisTeam, palcount

```
017AF4  movem.l	d0-a2,-(sp)
017AF8  cmp.w	#4,($FFFFD048).w
017AFE  beq.w	loc_17B0A
017B02  tst.w	($FFFFD048).w
017B06  bne.w	loc_17B16
017B0A  move.w	($FFFFD04C).w,($FFFFC330).w
017B10  move.w	($FFFFD04E).w,($FFFFC332).w
017B16  bsr.w	sub_11B92
017B1A  dc.w	6
017B1C  dc.b	$BF
017B1D  dc.b	7
017B1E  dc.b	1
017B1F  dc.b	0
017B20  move.w	($FFFFC332).w,d1
017B24  move.w	d1,d0
017B26  asl.w	#6,d0
017B28  move.l	#word_F8BF4,a0
017B2E  move.l	$26(a0,d0.w),($FFFFBD4E).w
017B34  move.w	($FFFFD43A).w,d4
017B38  bsr.w	sub_17B78
017B3C  bsr.w	sub_11B92
017B40  dc.w	6
017B42  dc.b	$BF
017B43  dc.b	$16
017B44  dc.b	1
017B45  dc.b	0
017B46  move.w	($FFFFC330).w,d1
017B4A  move.w	d1,d0
017B4C  asl.w	#6,d0
017B4E  move.l	#word_F8BF4,a0
017B54  move.l	2(a0,d0.w),($FFFFBD4A).w
017B5A  move.w	#$EEE,($FFFFBD52).w
017B60  move.w	#2,d4
017B64  bsr.w	sub_17B78
017B68  bsr.w	sub_17190
017B6C  move.w	#$64,($FFFFBD26).w
017B72  movem.l	(sp)+,d0-a2
017B76  rts
```

## `$0F7318` -> `ai_ComputeTeamAdvantage`  (confidence 0.7, 26 insns)

**Evidence.** sums the starting-six ratings of the home and away teams (ai_SumStartingSixRatings) into $BF12/$BF14, sets $BF50 = 1 when the away side is stronger, and returns d0 = -1 (even), $22 (difference at least $5E) or $23 (at least $BD), the message id printed after 'ADVANTAGE:' on the matchups screen; caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** ai_SumStartingSixRatings

```
0F7318  movem.l	d1-a6,-(sp)
0F731C  move.l	#$FFFFC6CE,a0
0F7322  bsr.w	sub_F737E
0F7326  move.w	d1,($FFFFBF12).w
0F732A  move.l	#$FFFFCA32,a0
0F7330  bsr.w	sub_F737E
0F7334  move.w	d1,($FFFFBF14).w
0F7338  move.w	($FFFFBF12).w,d1
0F733C  move.w	($FFFFBF14).w,d2
0F7340  sub.w	d1,d2
0F7342  move.w	#0,($FFFFBF50).w
0F7348  tst.w	d2
0F734A  bmi.w	loc_F7354
0F734E  move.w	#1,($FFFFBF50).w
0F7354  tst.w	d2
0F7356  bpl.w	loc_F735C
0F735A  neg.w	d2
0F735C  move.w	#$FFFF,d0
0F7360  cmpnw	 $5E,d2
0F7364  blt.w	loc_F7378
0F7368  move.w	#$22,d0
0F736C  cmpnw	 $BD,d2
0F7370  blt.w	loc_F7378
0F7374  move.w	#$23,d0
0F7378  movem.l	(sp)+,d1-a6
0F737C  rts
```

## `$017572` -> `ai_ScrollPlayoffBracket`  (confidence 0.6, 29 insns)

**Evidence.** PlayoffScreen: applies the scroll velocity PlayerScrollCtr ($D5B0) to the bracket offset $D5AC, clamped to +-$70 per round (gamelevel, at most 3 rounds), publishes the shifted offset in $B8AE when within $40..$200, and stops the velocity once the offset is a multiple of $70 (a round column); caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** none
**RAM.** DispAttribCtr, PlayerScrollCtr, gamelevel

```
017572  move.w	($FFFFD5B0).w,d0
017576  beq.w	locret_15464
01757A  add.w	($FFFFD5AC).w,d0
01757E  move.w	($FFFFCEEC).w,d1
017582  cmpnw	 3,d1
017586  bls.w	loc_1758C
01758A  moveq	#3,d1
01758C  mulu.w	#$70,d1
017590  cmp.w	d1,d0
017592  bgt.w	locret_15464
017596  neg.w	d1
017598  cmp.w	d1,d0
01759A  blt.w	locret_15464
01759E  move.w	d0,($FFFFD5AC).w
0175A2  clr.w	($FFFFB8AE).w
0175A6  move.w	d0,d1
0175A8  add.w	#$100,d1
0175AC  cmpnw	 $40,d1
0175B0  blt.w	loc_175C0
0175B4  cmpnw	 $200,d1
0175B8  bgt.w	loc_175C0
0175BC  move.w	d1,($FFFFB8AE).w
0175C0  ext.l	d0
0175C2  divs.w	#$70,d0
0175C6  swap	d0
0175C8  tst.w	d0
0175CA  bne.w	locret_15464
0175CE  clr.w	($FFFFD5B0).w
0175D2  rts
```

## `$009CDC` -> `ai_LoadRinkGraphics`  (confidence 0.6, 30 insns)

**Evidence.** sub_A528 helper (game start): programs the scroll registers from VSCRLPM ($8D/$8C, $B00E = 5), loads the crowd tiles (unk_56062, or unk_B5188 when $C2F4 bit 4 is set) at rinkvrcset, the home centre-ice logo (ai_LoadHomeCenterIceLogo), the font, the frame tiles, the rink tiles and palette (ai_LoadRinkTiles, sub_16CC4, sub_16CD2, ai_LoadRinkPalette) and finishes in sub_1720C; caller sub_A528

**Callers.** sub_A528
**Callees.** SetTeamColors, Vmaddr, ai_LoadAsset, ai_LoadAssetInline, ai_LoadFrameTiles, ai_LoadHomeCenterIceLogo, ai_LoadRinkPalette, ai_LoadRinkTiles, sub_16CC4, sub_16CD2
**Strings.** Timeout |  | no goalie
**RAM.** Map3col1, VSCRLPM, disflags, framercset, rinkvrcset

```
009CDC  move.w	($FFFFBF78).w,-(sp)
009CE0  bset	#2,($FFFFBF78).w
009CE6  move.w	($FFFFB000).w,d0
009CEA  bsr.w	VDP_SetAddress
009CEE  move.l	#0,(a0)
009CF4  move.w	#$8D00,d0
009CF8  move.b	($FFFFB000).w,d0
009CFC  lsr.b	#2,d0
009CFE  move.w	d0,4(a0)
009D02  move.w	#$8C00,4(a0)
009D08  move.w	#5,($FFFFB00E).w
009D0E  move.w	(sp)+,($FFFFBF78).w
009D12  bset	#1,($FFFFBF78).w
009D18  move.w	($FFFFB018).w,d4
009D1C  move.l	#unk_56062,a2
009D22  btst	#4,($FFFFC2F4).w
009D28  beq.w	loc_9D32
009D2C  move.l	#unk_B5188,a2
009D32  bsr.w	sub_11738
009D36  jsr	sub_FEA52
009D3C  move.w	($FFFFB012).w,d4
009D40  move.l	#unk_AAC5A,a2
009D46  bsr.w	sub_1172C
009D4A  dc.w	$4343
009D4C  dc.w	$4567
009D4E  dc.w	$89AB
009D50  dc.w	$CDEF
009D52  move.w	($FFFFB01E).w,d4
009D56  jsr	sub_11F12
009D5C  jsr	loc_16CAC
009D62  jsr	sub_16CC4
009D68  jsr	sub_16CD2
009D6E  jsr	sub_16C96
009D74  jmp	sub_1720C
```

## `$00A616` -> `ai_CenterCameraOnObject`  (confidence 0.7, 27 insns)

**Evidence.** SetRCords helper: copies object a3's x/y (negated when the rink is flipped, $C2F4 bit 7) into the camera target a5, then sets Hpos = x clamped to -$3C..$3C and Vpos = y clamped to -$C8..$100; caller SetRCords

**Callers.** SetRCords
**Callees.** none
**RAM.** Hpos, Vpos

```
00A616  movem.l	d0-d2,-(sp)
00A61A  move.w	(a3),d0
00A61C  btst	#7,($FFFFC2F4).w
00A622  beq.w	loc_A628
00A626  neg.w	d0
00A628  move.w	d0,(a5)
00A62A  move.w	$14(a3),d1
00A62E  btst	#7,($FFFFC2F4).w
00A634  beq.w	loc_A63A
00A638  neg.w	d1
00A63A  move.w	d1,$14(a5)
00A63E  cmpnw	 $3C,d0
00A642  blt.w	loc_A64A
00A646  move.w	#$3C,d0
00A64A  cmpnw	 $FFC4,d0
00A64E  bgt.w	loc_A656
00A652  move.w	#$FFC4,d0
00A656  move.w	d0,($FFFFBD1C).w
00A65A  cmpnw	 $100,d1
00A65E  blt.w	loc_A666
00A662  move.w	#$100,d1
00A666  cmpnw	 $FF38,d1
00A66A  bgt.w	loc_A672
00A66E  move.w	#$FF38,d1
00A672  move.w	d1,($FFFFBD18).w
00A676  movem.l	(sp)+,d0-d2
00A67A  rts
```

## `$0166E6` -> `ai_BuildPlayerLabelSprites`  (confidence 0.6, 29 insns)

**Evidence.** uppads helper: from the packed value d1 (tens digit in bits 4..7, units in bits 0..3, position code in bits 8..10) emits three sprite-tile entries at a5 via sub_1674A (tile pointer into Art_BoardText, size $10, x from $12(a0)): the two jersey digits (blank when the tens digit is 0 or the units are $F, narrowing 2(a0)) and the position letter from unk_1677A (' ', 'D', 'D', 'L', ...; suppressed by $C2FC bit 7); caller uppads (the jersey number / position labels over the players)

**Callers.** uppads
**Callees.** sub_1674A

```
0166E6  lea	unk_1677A(pc),a4
0166EA  clr.w	2(a0)
0166EE  move.w	d1,d2
0166F0  lsr.w	#4,d2
0166F2  and.w	#$F,d2
0166F6  bne.w	loc_16702
0166FA  move.w	#$FFF0,d2
0166FE  subq.w	#4,2(a0)
016702  add.w	#$30,d2
016706  clr.w	d0
016708  bsr.w	sub_1674A
01670C  move.w	d1,d2
01670E  and.w	#$F,d2
016712  cmpnw	 $F,d2
016716  bne.w	loc_1671E
01671A  move.w	#$FFF0,d2
01671E  add.w	#$30,d2
016722  moveq	#1,d0
016724  bsr.w	sub_1674A
016728  move.w	d1,d2
01672A  btst	#7,($FFFFC2FC).w
016730  beq.w	loc_16736
016734  clr.w	d2
016736  lsr.w	#8,d2
016738  and.w	#7,d2
01673C  bne.w	loc_16744
016740  addq.w	#4,2(a0)
016744  move.b	(a4,d2.w),d2
016748  moveq	#2,d0
```

## `$00E1F4` -> `ai_CpuLineChangeCheck`  (confidence 0.6, 26 insns)

**Evidence.** asspuckc helper for a CPU puck carrier: unless $C2FC bit 4, when the puck is 0..$58 ahead of the carrier, one time in four (HV counter & 3), the carrier is not flagged $63 bit 3 and the on-ice energy sum (sub_12EF6) is at most $C00, picks the fresher line with CompLine, applies it with SetPersonel, refreshes the HUD (PrintScores1) and dumps the puck via compshoot?; the listing shows the 'exg a2,a1' at $E246 as dc.w $C549 (data), the recompiler translated it; caller asspuckc

**Callers.** asspuckc
**Callees.** CompLine, PrintScores1, SetPersonel, compshoot?, sub_12EF6
**RAM.** pucky
**Hardware.** HV counter

```
00E1F4  btst	#4,($FFFFC2FC).w
00E1FA  bne.w	locret_15464
00E1FE  move.w	($FFFFB75E).w,d0
00E202  btst	#7,$62(a3)
00E208  bne.w	loc_E20E
00E20C  neg.w	d0
00E20E  tst.w	d0
00E210  bmi.w	locret_15464
00E214  cmpnw	 $58,d0
00E218  bgt.w	locret_15464
00E21C  move.w	($C00008).l,d0
00E222  and.w	#3,d0
00E226  bne.w	locret_15464
00E22A  btst	#3,$63(a3)
00E230  bne.w	locret_15464
00E234  move.w	#$C6CE,a2
00E238  lea	$364(a2),a1
00E23C  btst	#6,$62(a3)
00E242  beq.w	loc_E248
00E246  dc.w	$C549
00E248  bsr.w	sub_12EF6
00E24C  cmpnw	 $C00,d0
00E250  bhi.w	locret_15464
00E254  bsr.w	sub_F790
00E258  bsr.w	sub_15788
00E25C  bsr.w	loc_12C04
00E260  bra.w	sub_E412
```

## `$00F2F4` -> `ai_GoalieFreezePuck`  (confidence 0.5, 30 insns)

**Evidence.** pucknorm helper: when puckc is the goalie (BA_Goalie_SCnum) and $C2F2 bit 5 allows it, counts $C31C down and then sets $C2F2 bit 4 (stoppage), also set when $D454 is 0; the first time (bit 6 latch) posts event $A through sub_11F62 (the message/sound dispatcher used by checkgoal and clockcont); caller pucknorm

**Callers.** pucknorm
**Callees.** loc_F348, sub_11F62
**RAM.** BA_Goalie_SCnum, BA_PS_flags, puckc

```
00F2F4  movem.w	d0,-(sp)
00F2F8  move.w	($FFFFB7AA).w,d0
00F2FC  cmp.w	($FFFFD408).w,d0
00F300  movem.w	(sp)+,d0
00F304  beq.w	loc_F342
00F308  btst	#5,($FFFFC2F2).w
00F30E  beq.w	loc_F348
00F312  btst	#5,($FFFFC2FA).w
00F318  bne.w	loc_F32A
00F31C  tst.w	($FFFFB7AA).w
00F320  bpl.w	loc_F332
00F324  bset	#5,($FFFFC2FA).w
00F32A  tst.w	($FFFFB7AA).w
00F32E  bpl.w	loc_F342
00F332  tst.w	($FFFFC31C).w
00F336  bmi.w	loc_F342
00F33A  subq.w	#1,($FFFFC31C).w
00F33E  bra.w	loc_F348
00F342  bset	#4,($FFFFC2F2).w
00F348  tst.w	($FFFFD454).w
00F34C  bne.w	loc_F356
00F350  bset	#4,($FFFFC2F2).w
00F356  btst	#4,($FFFFC2F2).w
00F35C  bne.w	loc_F362
00F360  rts
00F362  btst	#6,($FFFFC2F2).w
00F368  bne.w	locret_F3E2
00F36C  bset	#6,($FFFFC2F2).w
00F372  move.w	#$A,d0
00F376  jsr	sub_11F62
```

## `$0FEEC8` -> `ai_BuildPlayedByString`  (confidence 0.7, 28 insns)

**Evidence.** builds '(played by <user name>)' in $BF20 for controller 1's user $D042 (ai_CopyUserNameDashed into $D4DC, length in $D4DA, then appstring and the inline ')' via sub_11D96); returns a1 = the empty string word_FEF50 when no user is set; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** ai_CopyLenString, ai_CopyUserNameDashed, appendz, appstring, loc_FEF3C
**Strings.** (played by

```
0FEEC8  movem.l	d0-a0/a2-a6,-(sp)
0FEECC  move.w	($FFFFD042).w,d0
0FEED0  tst.w	d0
0FEED2  beq.w	loc_FEF52
0FEED6  move.l	#$FFFFD4DC,a1
0FEEDC  move.w	d0,($FFFFD4EA).w
0FEEE0  bsr.w	sub_FB992
0FEEE4  add.w	($FFFFD4E8).w,a1
0FEEE8  move.b	#0,(a1)
0FEEEC  addq.w	#1,($FFFFD4E8).w
0FEEF0  and.w	#$FFFE,($FFFFD4E8).w
0FEEF6  addq.w	#2,($FFFFD4E8).w
0FEEFA  move.w	($FFFFD4E8).w,($FFFFD4DA).w
0FEF00  move.l	#$FFFFD4DA,a1
0FEF06  move.l	a1,-(sp)
0FEF08  move.l	#$FFFFBF20,a3
0FEF0E  move.l	#word_FEF42,a1
0FEF14  bsr.w	sub_F997A
0FEF18  move.l	(sp)+,a1
0FEF1A  move.l	#$FFFFBF20,a3
0FEF20  jsr	sub_11D9E
0FEF26  move.l	#$FFFFBF20,a3
0FEF2C  jsr	sub_11D96
0FEF32  dc.w	4
0FEF34  dc.b	')',0
0FEF36  move.l	#$FFFFBF20,a1
0FEF3C  movem.l	(sp)+,d0-a0/a2-a6
0FEF40  rts
0FEF42  word_FEF42:	dc.w	$E
0FEF44  aPlayedBy:	dc.b	'(played by ',0
0FEF50  word_FEF50:	dc.w	2
0FEF52  move.l	#word_FEF50,a1
0FEF58  bra.s	loc_FEF3C
```

## `$0F9B2A` -> `ai_AppendRecordHolderText`  (confidence 0.6, 26 insns)

**Evidence.** given a record (a0, or fetched with ReadRecordField when a0 is null): appends the holder's user name (byte 3, ai_BuildUserNameString with trimming), the separator word_F9B90 and the opponent team name (byte 2, ai_AppendTeamName) to the string at a1; caller sub_F9AAC (records text)

**Callers.** sub_F9AAC
**Callees.** ai_AppendTeamName, ai_BuildUserNameString, ai_ReadRecordField, appstring

```
0F9B2A  movem.l	d0-a6,-(sp)
0F9B2E  cmp.l	#0,a0
0F9B34  bne.w	loc_F9B5A
0F9B38  movem.l	d0-d7/a1-a6,-(sp)
0F9B3C  move.w	d0,-(sp)
0F9B3E  move.w	d1,d0
0F9B40  move.w	(sp)+,d1
0F9B42  ext.l	d1
0F9B44  ext.l	d0
0F9B46  move.l	#$FFFF0000,a0
0F9B4C  bsr.w	sub_F9B94
0F9B50  move.l	#$FFFF0000,a0
0F9B56  movem.l	(sp)+,d0-d7/a1-a6
0F9B5A  move.b	3(a0),d2
0F9B5E  ext.w	d2
0F9B60  movem.l	d0/a1,-(sp)
0F9B64  bset	#7,($FFFFC2F8).w
0F9B6A  bsr.w	sub_FA014
0F9B6E  move.l	a1,a3
0F9B70  move.l	#word_F9B90,a1
0F9B76  jsr	sub_11D9E
0F9B7C  movem.l	(sp)+,d0/a1
0F9B80  move.b	2(a0),d0
0F9B84  jsr	sub_FA880
0F9B8A  movem.l	(sp)+,d0-a6
0F9B8E  rts
```

