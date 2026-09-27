# Name review: names-batch-27.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$01A148` -> `VBcount`  (from the 2016 listing, not AI, 2 insns)

**Evidence.** IDA SYMBOL name at this address ('vblank with counter only'): increments vcount and returns from the interrupt

**Callers.** none found
**Callees.** none
**RAM.** vcount

```
01A148  addq.w	#1,($FFFFB03E).w
01A14C  rte
```

## `$00CBE0` -> `NullSub4`  (from the 2016 listing, not AI, 1 insns)

**Evidence.** IDA's nullsub_4: a bare rts

**Callers.** none found
**Callees.** none

```
00CBE0  rts
```

## `$00CBE2` -> `NullSub5`  (from the 2016 listing, not AI, 1 insns)

**Evidence.** IDA's nullsub_5: a bare rts

**Callers.** none found
**Callees.** none

```
00CBE2  rts
```

## `$015D9A` -> `ai_GameVBlankRoutine`  (confidence 0.7, 40 insns)

**Evidence.** the V-blank routine installed by ai_InitRinkScreen ($B03A): flushes the scroll/sprites unless $BF78 bit 2 (ai_AttractVBlankScroll), sub_10FB6, then during play counts the game clock down (subtracts $AAA from the fraction $C46A and decrements gameclock on borrow, flagging $BF78 bit 3) and triggers the 60-second warning at $3C..$3D; ends with rte

**Callers.** none found
**Callees.** MusicVB, ai_AttractVBlankScroll, cramfade, loc_15E1A, sfx
**RAM.** disflags, gameclock, gmode, sflags, vcount

```
015D9A  movem.l	d0-a6,-(sp)
015D9E  btst	#2,($FFFFBF78).w
015DA4  bne.w	loc_15DBA
015DA8  bclr	#0,($FFFFBF78).w
015DAE  beq.w	loc_15DB6
015DB2  bsr.w	sub_15E6E
015DB6  bsr.w	sub_10FB6
015DBA  btst	#0,($FFFFC2EC).w
015DC0  bne.w	loc_15E1A
015DC4  btst	#2,($FFFFC2FA).w
015DCA  bne.w	loc_15DD8
015DCE  btst	#0,($FFFFC2EA).w
015DD4  bne.w	loc_15E1A
015DD8  btst	#1,($FFFFC2FA).w
015DDE  bne.w	loc_15E2A
015DE2  tst.w	($FFFFC468).w
015DE6  beq.w	loc_15E1A
015DEA  sub.w	#$AAA,($FFFFC46A).w
015DF0  bcc.w	loc_15E1A
015DF4  bset	#3,($FFFFBF78).w
015DFA  subq.w	#1,($FFFFC468).w
015DFE  cmp.w	#$3D,($FFFFC468).w
015E04  bgt.w	loc_15E1A
015E08  cmp.w	#$3C,($FFFFC468).w
015E0E  blt.w	loc_15E1A
015E12  move.w	#2,-(sp)
015E16  bsr.w	sub_11132
015E1A  addq.w	#1,($FFFFB03E).w
015E1E  jsr	sub_1A50A
015E24  movem.l	(sp)+,d0-a6
015E28  rte
015E2A  tst.w	($FFFFD454).w
015E2E  beq.s	loc_15E1A
015E30  sub.w	#$AAA,($FFFFD456).w
015E36  bcc.s	loc_15E1A
015E38  bset	#3,($FFFFBF78).w
015E3E  btst	#7,($FFFFC2FA).w
015E44  bne.s	loc_15E1A
015E46  subq.w	#1,($FFFFD454).w
015E4A  bra.s	loc_15E1A
```

## `$015E4C` -> `ai_AttractVBlankRoutine`  (confidence 0.7, 8 insns)

**Evidence.** the V-blank routine installed by ai_MatchupsScreen: sub_10FB6 unless $BF78 bit 2, increments vcount, sub_1A50A (sound), rte

**Callers.** none found
**Callees.** MusicVB, cramfade
**RAM.** disflags, vcount

```
015E4C  movem.l	d0-a6,-(sp)
015E50  btst	#2,($FFFFBF78).w
015E56  bne.w	loc_15E5E
015E5A  bsr.w	sub_10FB6
015E5E  addq.w	#1,($FFFFB03E).w
015E62  jsr	sub_1A50A
015E68  movem.l	(sp)+,d0-a6
015E6C  rte
```

## `$017692` -> `ai_PlayoffVBlankRoutine`  (confidence 0.7, 19 insns)

**Evidence.** the playoff screen's V-blank routine: DMAs the sprite list at $C018 ($C2E8 entries) and writes the bracket scroll (-$160 + $D5AC) to the scroll table unless $BF78 bit 2, then sub_10FB6, vcount and the sound driver; rte

**Callers.** none found
**Callees.** DoDMA, MusicVB, Vmaddr, cramfade
**Strings.** Playoffs | Quarterfinals | Semifinals | Finals | Champions
**RAM.** DispAttribCtr, VSCRLPM, VSPRITES, disflags, vcount

```
017692  movem.l	d0-a6,-(sp)
017696  btst	#2,($FFFFBF78).w
01769C  bne.w	loc_176CE
0176A0  move.w	#$C018,a0
0176A4  move.w	($FFFFC2E8).w,d0
0176A8  beq.w	loc_176CA
0176AC  clr.w	($FFFFC2E8).w
0176B0  move.w	($FFFFB002).w,d1
0176B4  bsr.w	sub_113E4
0176B8  move.w	($FFFFB000).w,d0
0176BC  bsr.w	VDP_SetAddress
0176C0  move.w	#$FEA0,d0
0176C4  add.w	($FFFFD5AC).w,d0
0176C8  move.w	d0,(a0)
0176CA  bsr.w	sub_10FB6
0176CE  addq.w	#1,($FFFFB03E).w
0176D2  jsr	sub_1A50A
0176D8  movem.l	(sp)+,d0-a6
0176DC  rte
```

## `$009FD0` -> `ai_InstantReplay`  (confidence 0.6, 245 insns)

**Evidence.** instant replay entry: sets $C2EE bit 3, clears the sprite table (sub_11544), loads the replay overlay tiles unk_BB4F6 at ExtraChars, ai_DrawRinkAuxBitmap, then from the write pointer recbpr steps the frame ring backwards with ai_StepReplayBack until it stops, sub_1702E and a fade before running the playback loop

**Callers.** none found
**Callees.** ClrHor, DoFill, SetHor, SetRCords, SprSort, ai_CenterCameraOnObject, ai_DrawPauseMenuBackdrop, ai_DrawRinkAuxBitmap, ai_EraseCornerBox16x11, ai_EraseCornerBox8x4, ai_LoadAsset, ai_LoadCrowdSpriteTiles, ai_LoadHudTiles, ai_LoadMenuTiles55BFE, ai_LoadMenuTiles5C410, ai_LoadRinkGraphics, ai_LoadRinkTiles, ai_LoadTilesA78B6, ai_ReinitRinkAndReplay, ai_SetPlayerBE78Bits, ai_StepReplayBack, forceblack, getpzjoy, loc_A058, setvideo, sfx, vtoa
**RAM.** ExtraChars, Hpos, VmMap3, Vpos, disflags, lastsfx, oldvcount, padcont, palcount, recbpr, sflags, sflags2, sflags3, vcount

```
009FD0  bclr	#0,($FFFFC2F6).w
009FD6  bsr.w	sub_10F32
009FDA  move.w	($FFFFBF78).w,-(sp)
009FDE  bset	#3,($FFFFC2EE).w
009FE4  bclr	#4,($FFFFC2F4).w
009FEA  jsr	sub_12B40
009FF0  move.w	#$400,d0
009FF4  move.w	($FFFFB00C).w,d1
009FF8  move.w	#$7FF,d2
009FFC  bsr.w	sub_11544
00A000  move.w	($FFFFB026).w,d4
00A004  move.l	#unk_BB4F6,a2
00A00A  jsr	sub_11738
00A010  jsr	sub_A448
00A016  bclr	#5,($FFFFC2EC).w
00A01C  bclr	#5,($FFFFC2F0).w
00A022  st	($FFFFBE1E).w
00A026  move.l	($FFFFB036).w,a4
00A02A  bsr.w	sub_A4F6
00A02E  tst.w	d7
00A030  bne.s	loc_A02A
00A032  jsr	sub_1702E
00A038  jsr	sub_15EC0
00A03E  bclr	#1,($FFFFC2F0).w
00A044  clr.l	($FFFFBE7A).w
00A048  clr.l	($FFFFBE7E).w
00A04C  clr.l	($FFFFBE82).w
00A050  move.w	#$18,($FFFFBD26).w
00A056  moveq	#1,d7
00A058  move.w	($FFFFB03E).w,d0
00A05C  sub.w	($FFFFB040).w,d0
00A060  cmp.w	d0,d7
00A062  bhi.s	loc_A058
00A064  move.w	($FFFFB03E).w,($FFFFB040).w
00A06A  tst.w	($FFFFDEB4).w
00A06E  bmi.w	loc_A084
00A072  sub.w	d7,($FFFFDEB4).w
00A076  bpl.w	loc_A084
00A07A  clr.w	($FFFFDEB4).w
00A07E  jsr	loc_A48A
00A084  movem.l	d0/a3,-(sp)
00A088  move.l	#$FFFFB64A,a3
00A08E  move.w	#1,8(a3)
00A094  move.l	#$FFFFB6CA,a3
00A09A  move.w	#1,8(a3)
00A0A0  movem.l	(sp)+,d0/a3
00A0A4  moveq	#1,d7
00A0A6  bsr.w	sub_A41E
00A0AA  btst	#0,($FFFFC2F6).w
00A0B0  beq.w	loc_A0C4
00A0B4  and.w	#$FFF0,d0
00A0B8  or.w	#8,d0
00A0BC  and.w	#$FFF0,d1
00A0C0  and.w	#$FFF0,d3
00A0C4  move.w	#$BE08,a5
00A0C8  btst	#5,($FFFFC2F0).w
00A0CE  beq.w	loc_A0DC
00A0D2  move.w	d1,d5
00A0D4  and.w	#$F,d5
00A0D8  beq.w	loc_A25E
...
```

## `$0088C8` -> `ai_UnpackLinesFromPassword`  (confidence 0.5, 31 insns)

**Evidence.** reads nibbles from $D076 + 1 (the playoff password buffer) through the slot table at $898A, rebuilding player indexes from the attribute count (ai_CountRatingNibbles) and goalie count (ai_GetGoalieCount) offsets; the inverse of ai_PackLinesToPassword, so custom lines travel inside the password

**Callers.** none found
**Callees.** ai_CountRatingNibbles, ai_GetGoalieCount, ai_SwapLineSlot, loc_88E8, loc_8900

```
0088C8  movem.l	d0-d4/a0/a3,-(sp)
0088CC  move.w	#$D076,a0
0088D0  addq.w	#1,a0
0088D2  bsr.w	sub_9F40
0088D6  move.w	d0,d1
0088D8  bsr.w	sub_9F7E
0088DC  move.w	d0,d3
0088DE  move.l	#$898A,a3
0088E4  clr.w	d4
0088E6  clr.w	d2
0088E8  move.b	(a3),d2
0088EA  bmi.w	loc_8922
0088EE  bchg	#0,d4
0088F2  bne.w	loc_88FC
0088F6  move.b	(a0),d0
0088F8  bra.w	loc_8900
0088FC  move.b	(a0)+,d0
0088FE  lsr.w	#4,d0
008900  and.w	#$F,d0
008904  add.b	d1,d0
008906  and.w	#7,d2
00890A  cmpnw	 2,d2
00890E  bgt.w	loc_8914
008912  add.b	d3,d0
008914  addq.b	#1,d0
008916  and.w	#$FF,d0
00891A  move.b	(a3)+,d2
00891C  bsr.w	sub_8898
008920  bra.s	loc_88E8
008922  movem.l	(sp)+,d0-d4/a0/a3
008926  rts
```

## `$008928` -> `ai_PackLinesToPassword`  (confidence 0.5, 31 insns)

**Evidence.** writes team a2's id + 1 and then, guided by the slot table at $898A, the line table $16A(a2) as nibbles (index minus the attribute/goalie count offsets) into $D076; inverse of ai_UnpackLinesFromPassword

**Callers.** none found
**Callees.** ai_CountRatingNibbles, ai_GetGoalieCount, ai_SavePlayoffPassword, loc_8950
**Strings.** Roster | Pos.^Player | Rating | Switch^Teams

```
008928  movem.l	d0-d4/a0-a3,-(sp)
00892C  move.w	#$D076,a0
008930  move.w	$28(a2),d0
008934  addq.w	#1,d0
008936  move.b	d0,(a0)+
008938  lea	$16A(a2),a1
00893C  bsr.w	sub_9F40
008940  move.w	d0,d1
008942  bsr.w	sub_9F7E
008946  move.l	#$898A,a3
00894C  clr.w	d4
00894E  clr.w	d2
008950  move.b	(a3)+,d2
008952  bmi.w	loc_897E
008956  move.b	(a1,d2.w),d3
00895A  subq.b	#1,d3
00895C  sub.b	d1,d3
00895E  and.w	#7,d2
008962  cmpnw	 2,d2
008966  bgt.w	loc_896C
00896A  sub.b	d0,d3
00896C  bchg	#0,d4
008970  bne.w	loc_8978
008974  move.b	d3,(a0)
008976  bra.s	loc_8950
008978  asl.b	#4,d3
00897A  or.b	d3,(a0)+
00897C  bra.s	loc_8950
00897E  jsr	sub_FE696
008984  movem.l	(sp)+,d0-d4/a0-a3
008988  rts
```

## `$008D82` -> `ai_RestoreRegsReturn`  (confidence 0.6, 2 insns)

**Evidence.** shared epilogue jumped to by the attribute lookup handlers: movem.l (sp)+,d0-d4/a0-a1/a4-a5 then rts

**Callers.** none found
**Callees.** none
**Strings.** Ice | Bench | Injury P | Injury G |  | C

```
008D82  movem.l	(sp)+,d0-d4/a0-a1/a4-a5
008D86  rts
```

## `$009232` -> `ai_ScrollPenaltySummaryCheck`  (confidence 0.5, 6 insns)

**Evidence.** entry of the penalty-summary scroller: applies PlayerScrollCtr to VertLineScrolling within 0..$D5B2 and continues into ai_ScrollPenaltySummary

**Callers.** none found
**Callees.** none
**RAM.** PlayerScrollCtr, VertLineScrolling

```
009232  move.w	($FFFFD5B0).w,d0
009236  beq.w	locret_A9D4
00923A  add.w	($FFFFD5AE).w,d0
00923E  bmi.w	locret_A9D4
009242  cmp.w	($FFFFD5B2).w,d0
009246  bgt.w	locret_A9D4
```

## `$00924A` -> `ai_ScrollPenaltySummary`  (confidence 0.6, 31 insns)

**Evidence.** penalty summary scroll step with a 24-pixel pitch: updates VertLineScrolling, redraws the arrows (ai_PrintSummaryScrollArrows) at a boundary, pre-draws the row entering from above (ai_PrintPenaltyRowAbove at $16) or below (ai_PrintPenaltyRowBelow at 2), then writes the vertical scroll

**Callers.** none found
**Callees.** ai_PrintPenaltyRowAbove, ai_PrintPenaltyRowBelow, ai_PrintSummaryScrollArrows
**RAM.** PlayerScrollCtr, VertLineScrolling, disflags
**Hardware.** VDP data

```
00924A  move.w	($FFFFD5AE).w,d1
00924E  move.w	d0,($FFFFD5AE).w
009252  ext.l	d0
009254  divs.w	#$18,d0
009258  swap	d0
00925A  tst.w	d0
00925C  bne.w	loc_9268
009260  bsr.w	sub_93C4
009264  clr.w	($FFFFD5B0).w
009268  ext.l	d1
00926A  divs.w	#$18,d1
00926E  swap	d1
009270  tst.w	d1
009272  bne.w	loc_9292
009276  move.l	d0,-(sp)
009278  cmpnw	 $16,d0
00927C  bne.w	loc_9284
009280  bsr.w	sub_92BA
009284  move.l	(sp)+,d0
009286  cmpnw	 2,d0
00928A  bne.w	loc_9292
00928E  bsr.w	sub_92E6
009292  move.w	($FFFFBF78).w,-(sp)
009296  bset	#2,($FFFFBF78).w
00929C  move.l	#$C00000,a0
0092A2  move.l	#$40020010,4(a0)
0092AA  move.w	#$FFB0,d0
0092AE  add.w	($FFFFD5AE).w,d0
0092B2  move.w	d0,(a0)
0092B4  move.w	(sp)+,($FFFFBF78).w
0092B8  rts
```

## `$0092BA` -> `ai_PrintPenaltyRowBelow`  (confidence 0.5, 5 insns)

**Evidence.** prints penalty summary entry (d0 high word) * 4 via the shared row printer ai_PrintPenaltySummaryRow; the row entering at the bottom of the list

**Callers.** ai_ScrollPenaltySummary
**Callees.** printz

```
0092BA  move.l	d0,-(sp)
0092BC  swap	d0
0092BE  move.w	d0,d3
0092C0  asl.w	#2,d3
0092C2  jsr	sub_11B92
```

## `$0092E6` -> `ai_PrintPenaltyRowAbove`  (confidence 0.5, 6 insns)

**Evidence.** prints penalty summary entry (d0 high word + 5) * 4 via ai_PrintPenaltySummaryRow; the row entering at the top of the list

**Callers.** ai_ScrollPenaltySummary
**Callees.** printz

```
0092E6  move.l	d0,-(sp)
0092E8  swap	d0
0092EA  addq.w	#5,d0
0092EC  move.w	d0,d3
0092EE  asl.w	#2,d3
0092F0  jsr	sub_11B92
```

## `$009316` -> `ai_PrintPenaltySummaryRow`  (confidence 0.6, 38 insns)

**Evidence.** one row of the penalty summary from the table at $C5DE (entry d3: time word, team flag bit 7, penalty type in the low bits): erases the 40x3 row, prints the time (ai_PrintPeriodAndTime), the team name, the penalty description from the string table word_18E0C and its minutes (PushNumber)

**Callers.** none found
**Callees.** PushNumber, ai_FormatPlayerInitialSurname, ai_PrintPeriodAndTime, eraser, print
**RAM.** printa, printx, printy

```
009316  move.w	($FFFFB02A).w,-(sp)
00931A  moveq	#$28,d0
00931C  moveq	#3,d1
00931E  move.w	#$7FF,d2
009322  jsr	sub_1197E
009328  move.w	(sp)+,($FFFFB02A).w
00932C  move.w	#$C5DE,a0
009330  move.w	(a0,d3.w),d0
009334  move.w	#1,($FFFFB028).w
00933A  jsr	sub_11C72
009340  move.w	#$C6CE,a2
009344  btst	#7,2(a0,d3.w)
00934A  beq.w	loc_9352
00934E  add.w	#$364,a2
009352  move.l	$1E(a2),a1
009356  add.w	4(a1),a1
00935A  add.w	(a1),a1
00935C  move.w	#$C,($FFFFB028).w
009362  jsr	sub_11BA4
009368  move.b	2(a0,d3.w),d0
00936C  and.w	#$7F,d0
009370  move.l	#word_18E0C,a3
009376  add.w	(a3,d0.w),a3
00937A  clr.w	d0
00937C  move.b	1(a3),d0
009380  jsr	sub_11D06
009386  move.w	#$23,($FFFFB028).w
00938C  jsr	sub_11BA4
009392  move.w	#$10,($FFFFB028).w
009398  clr.w	d0
00939A  move.b	3(a0,d3.w),d0
00939E  jsr	sub_18AE8
0093A4  jsr	sub_11BA4
0093AA  addq.w	#1,($FFFFB02A).w
0093AE  move.w	#$13,($FFFFB028).w
0093B4  move.w	#$E000,($FFFFB02C).w
0093BA  lea	2(a3),a1
0093BE  jmp	sub_11BA4
```

## `$0FDE24` -> `ai_PrintGameStatsScreen`  (confidence 0.6, 31 insns)

**Evidence.** game statistics screen: draws both team banners (ai_DrawTeamBannerTiles at columns 2 and $1A), writes the scroll, then prints the $E stat rows from the descriptor table word_FDFAA ('Score', 'Shots', 'Shooting Pct', 'Power Play', 'PP Minutes', 'PP Shots', ...) with ai_PrintGameStatValue, honouring OptPen ($D056)

**Callers.** none found
**Callees.** ai_DrawTeamBannerTiles, ai_PrintGameStatValue, ai_WriteGameStatsScroll, print, printz
**RAM.** OptPen, printx, printy

```
0FDE24  jsr	sub_11B92
0FDE2A  dc.w	6
0FDE2C  dc.b	$BD
0FDE2D  dc.b	2
0FDE2E  dc.b	7
0FDE2F  dc.b	0
0FDE30  move.w	#$2C,d0
0FDE34  jsr	sub_8078
0FDE3A  jsr	sub_11B92
0FDE40  dc.w	6
0FDE42  dc.b	$BD
0FDE43  dc.b	$1A
0FDE44  dc.b	7
0FDE45  dc.b	0
0FDE46  moveq	#0,d0
0FDE48  jsr	sub_8078
0FDE4E  bsr.w	sub_FDD6A
0FDE52  jsr	sub_11B92
0FDE58  dc.w	6
0FDE5A  dc.b	$BE
0FDE5B  dc.b	0
0FDE5C  dc.b	0
0FDE5D  dc.b	0
0FDE5E  moveq	#$E,d6
0FDE60  lea	word_FDFAA(pc),a1
0FDE64  tst.w	($FFFFD056).w
0FDE68  bne.w	loc_FDE74
0FDE6C  move.w	#$A,d6
0FDE70  lea	word_FE098(pc),a1
0FDE74  move.w	(a1),d0
0FDE76  lsr.w	#1,d0
0FDE78  neg.w	d0
0FDE7A  add.w	#$15,d0
0FDE7E  move.w	d0,($FFFFB028).w
0FDE82  jsr	sub_11BA4
0FDE88  move.l	a1,a0
0FDE8A  move.w	#$22,($FFFFB028).w
0FDE90  move.w	#$C6CE,a2
0FDE94  bsr.w	sub_FDEB4
0FDE98  move.w	#9,($FFFFB028).w
0FDE9E  lea	$364(a2),a2
0FDEA2  bsr.w	sub_FDEB4
0FDEA6  lea	4(a0),a1
0FDEAA  addq.w	#2,($FFFFB02A).w
0FDEAE  dbf	d6,loc_FDE74
0FDEB2  rts
```

## `$0FDB8C` -> `ai_PrintPeriodStatColumns`  (confidence 0.6, 23 insns)

**Evidence.** game stats header: from the per-period stat block at a2 + $342 (or +$34A for the second view $D598) prints the column headers for each period played (gsp) with ai_PrintPeriodStatHeader at columns $B, $10, $15, the OT column at $1A when $C2FC bit 1, and 'Total' at $21

**Callers.** none found
**Callees.** ai_PrintPeriodStatHeader, printz
**Strings.** 
**RAM.** gsp, printx

```
0FDB8C  lea	$342(a2),a0
0FDB90  tst.w	($FFFFD598).w
0FDB94  beq.w	loc_FDB9C
0FDB98  lea	$34A(a2),a0
0FDB9C  clr.w	($FFFFD5A8).w
0FDBA0  move.w	#$B,($FFFFB028).w
0FDBA6  bsr.w	sub_FDC28
0FDBAA  cmp.w	#1,($FFFFC466).w
0FDBB0  blt.w	loc_FDBF0
0FDBB4  move.w	#$10,($FFFFB028).w
0FDBBA  bsr.w	sub_FDC28
0FDBBE  cmp.w	#2,($FFFFC466).w
0FDBC4  blt.w	loc_FDBF0
0FDBC8  move.w	#$15,($FFFFB028).w
0FDBCE  bsr.w	sub_FDC28
0FDBD2  cmp.w	#3,($FFFFC466).w
0FDBD8  blt.w	loc_FDBF0
0FDBDC  btst	#1,($FFFFC2FC).w
0FDBE2  beq.w	loc_FDBF0
0FDBE6  move.w	#$1A,($FFFFB028).w
0FDBEC  bsr.w	sub_FDC28
0FDBF0  move.w	#$21,($FFFFB028).w
0FDBF6  jsr	sub_11B92
```

## `$0FDC28` -> `ai_PrintPeriodStatHeader`  (confidence 0.5, 3 insns)

**Evidence.** takes the next word from (a0)+ and adds it to $D5A8, then prints the inline column label; called once per period column by ai_PrintPeriodStatColumns

**Callers.** ai_PrintPeriodStatColumns
**Callees.** printz
**Strings.**  | Game  Statistics

```
0FDC28  move.w	(a0)+,d0
0FDC2A  add.w	d0,($FFFFD5A8).w
0FDC2E  jsr	sub_11B92
```

## `$0FDD1A` -> `ai_ScrollGameStats`  (confidence 0.6, 21 insns)

**Evidence.** game stats scroll step with a 16-pixel pitch: applies PlayerScrollCtr to VertLineScrolling within 0..$D59E, stops at a boundary, computes the entering row slot (ai_GameStatsRowSlot / ai_GameStatsRowSlotPlus6) and writes the scroll with ai_WriteGameStatsScroll

**Callers.** none found
**Callees.** ai_GameStatsRowSlot, ai_GameStatsRowSlotPlus6
**RAM.** PlayerScrollCtr, VertLineScrolling

```
0FDD1A  move.w	($FFFFD5B0).w,d0
0FDD1E  beq.w	locret_FE14A
0FDD22  add.w	($FFFFD5AE).w,d0
0FDD26  bmi.w	locret_FE14A
0FDD2A  cmp.w	($FFFFD59E).w,d0
0FDD2E  bgt.w	locret_FE14A
0FDD32  move.w	($FFFFD5AE).w,d1
0FDD36  move.w	d0,($FFFFD5AE).w
0FDD3A  and.w	#$F,d0
0FDD3E  bne.w	loc_FDD46
0FDD42  clr.w	($FFFFD5B0).w
0FDD46  and.w	#$F,d1
0FDD4A  bne.w	sub_FDD6A
0FDD4E  move.w	d0,-(sp)
0FDD50  cmpnw	 $E,d0
0FDD54  bne.w	loc_FDD5C
0FDD58  bsr.w	sub_FDD92
0FDD5C  move.w	(sp)+,d0
0FDD5E  cmpnw	 2,d0
0FDD62  bne.w	sub_FDD6A
0FDD66  bsr.w	sub_FDD9C
```

## `$0FDD6A` -> `ai_WriteGameStatsScroll`  (confidence 0.6, 9 insns)

**Evidence.** writes the game stats plane's vertical scroll (-$50 + VertLineScrolling) to VSRAM entry 1 with $BF78 bit 2 held

**Callers.** ai_PrintGameStatsScreen
**Callees.** none
**RAM.** VertLineScrolling, disflags
**Hardware.** VDP data

```
0FDD6A  move.w	($FFFFBF78).w,-(sp)
0FDD6E  bset	#2,($FFFFBF78).w
0FDD74  move.l	#$C00000,a0
0FDD7A  move.l	#$40020010,4(a0)
0FDD82  move.w	#$FFB0,d0
0FDD86  add.w	($FFFFD5AE).w,d0
0FDD8A  move.w	d0,(a0)
0FDD8C  move.w	(sp)+,($FFFFBF78).w
0FDD90  rts
```

## `$0FDD92` -> `ai_GameStatsRowSlot`  (confidence 0.5, 3 insns)

**Evidence.** computes d3 = VertLineScrolling / 16 and returns; the row print that once followed was removed (falls straight to the rts), so it is a leftover of the stats-list scroller pattern

**Callers.** ai_ScrollGameStats
**Callees.** locret_FDDA8
**RAM.** VertLineScrolling

```
0FDD92  move.w	($FFFFD5AE).w,d3
0FDD96  lsr.w	#4,d3
0FDD98  bra.w	locret_FDDA8
```

## `$0FDD9C` -> `ai_GameStatsRowSlotPlus6`  (confidence 0.5, 5 insns)

**Evidence.** computes d3 = VertLineScrolling / 16 + 6 and returns (bra to the next instruction, then rts); the row print was removed like ai_GameStatsRowSlot

**Callers.** ai_ScrollGameStats
**Callees.** none
**RAM.** VertLineScrolling

```
0FDD9C  move.w	($FFFFD5AE).w,d3
0FDDA0  lsr.w	#4,d3
0FDDA2  addq.w	#6,d3
0FDDA4  bra.w	*+4
0FDDA8  rts
```

## `$0FDEB4` -> `ai_PrintGameStatValue`  (confidence 0.6, 52 insns)

**Evidence.** prints one game stat into $BFA4: a descriptor of -1 prints the shooting percentage (a2[$C] * 100 / a2[0]) with '%', otherwise the value at a2[(a0)] formatted as a time when the descriptor is $352 (ai_PushTimeThunk), a plain number for $A, or a number with the following text

**Callers.** ai_PrintGameStatsScreen
**Callees.** PushNumber, ai_PushNumberThunk, ai_PushTimeThunk, appendz, appstring, loc_FDF26, loc_FDF8E, print
**RAM.** printx

```
0FDEB4  move.w	#$BFA4,a3
0FDEB8  move.w	#2,(a3)
0FDEBC  cmp.w	#$FFFF,(a0)
0FDEC0  bne.w	loc_FDEF8
0FDEC4  move.w	#$C,d0
0FDEC8  move.w	(a2,d0.w),d0
0FDECC  mulu.w	#$64,d0
0FDED0  move.w	#0,d1
0FDED4  move.w	(a2,d1.w),d1
0FDED8  beq.w	loc_FDEDE
0FDEDC  divu.w	d1,d0
0FDEDE  jsr	sub_11D06
0FDEE4  jsr	sub_11D9E
0FDEEA  jsr	sub_11D96
0FDEF0  dc.w	4
0FDEF2  dc.b	'%',0
0FDEF4  bra.w	loc_FDF8E
0FDEF8  move.w	(a0),d0
0FDEFA  move.w	(a2,d0.w),d0
0FDEFE  cmp.w	#$352,(a0)
0FDF02  bne.w	loc_FDF0E
0FDF06  bsr.w	sub_FDFA4
0FDF0A  bra.w	loc_FDF26
0FDF0E  cmp.w	#$A,(a0)
0FDF12  beq.w	loc_FDF1A
0FDF16  bsr.w	sub_FDF9E
0FDF1A  cmp.w	#$A,(a0)
0FDF1E  bne.w	loc_FDF26
0FDF22  bsr.w	sub_FDFA4
0FDF26  jsr	sub_11D9E
0FDF2C  move.w	2(a0),d0
0FDF30  bmi.w	loc_FDF8E
0FDF34  jsr	sub_11D96
0FDF3A  dc.w	4
0FDF3C  dc.b	'/',0
0FDF3E  move.w	(a2,d0.w),d0
0FDF42  jsr	sub_11D06
0FDF48  jsr	sub_11D9E
0FDF4E  cmp.w	#$14,(a0)
0FDF52  bne.w	loc_FDF8E
0FDF56  jsr	sub_11D96
0FDF5C  dc.w	4
0FDF5E  dc.b	' ('
0FDF60  move.w	(a0),d0
0FDF62  move.w	(a2,d0.w),d0
0FDF66  mulu.w	#$64,d0
0FDF6A  move.w	2(a0),d1
0FDF6E  move.w	(a2,d1.w),d1
0FDF72  beq.w	loc_FDF78
0FDF76  divu.w	d1,d0
0FDF78  jsr	sub_11D06
0FDF7E  jsr	sub_11D9E
0FDF84  jsr	sub_11D96
0FDF8A  dc.w	4
0FDF8C  dc.b	'%)'
0FDF8E  move.w	a3,a1
0FDF90  move.w	(a1),d0
0FDF92  lsr.w	#1,d0
0FDF94  sub.w	d0,($FFFFB028).w
0FDF98  jmp	sub_11BA4
...
```

## `$0FDF9E` -> `ai_PushNumberThunk`  (confidence 0.8, 1 insns)

**Evidence.** jmp PushNumber; a jump-table-friendly wrapper used by ai_PrintGameStatValue

**Callers.** ai_PrintGameStatValue
**Callees.** PushNumber

```
0FDF9E  jmp	sub_11D06
```

## `$0FDFA4` -> `ai_PushTimeThunk`  (confidence 0.8, 1 insns)

**Evidence.** jmp PushTime; wrapper used by ai_PrintGameStatValue for the time-formatted stats

**Callers.** ai_PrintGameStatValue
**Callees.** PushTime
**Strings.** Score | Shots | Shooting Pct | Power Play | PP Minutes | PP Shots

```
0FDFA4  jmp	sub_11CA2
```

## `$0F84D0` -> `ai_LoadSetupLogoTiles`  (confidence 0.4, 10 insns)

**Evidence.** setoptions: loads asset unk_AFE1A at tile 2 (LoadAsset) and records the base in $D43A, then loads it again through ai_LoadAssetInline; the listing decodes the 8 inline bytes that follow as instructions, which is why the routine looks like it runs into garbage

**Callers.** setoptions
**Callees.** ai_LoadAsset, ai_LoadAssetInline

```
0F84D0  arg_4E6D	=	$4E71
0F84D0  moveq	#2,d4
0F84D2  move.l	#unk_AFE1A,a2
0F84D8  jsr	sub_11738
0F84DE  move.w	d4,($FFFFD43A).w
0F84E2  move.l	#unk_AFE1A,a2
0F84E8  jsr	sub_1172C
0F84EE  bchg	d1,d1
0F84F0  move.l	-(sp),-$7655(a2)
0F84F4  muls.w	4+arg_4E6D(sp),d6
```

## `$0FE1D8` -> `ai_ToggleGoalieControl`  (confidence 0.4, 52 insns)

**Evidence.** pause-menu handler: in playoff mode ($D04A) toggles the goalie-control option of the pausing controller ($D05C when both controllers share a team or sflags bit 1, else $D05A); then, unless in shootout mode or during a stoppage, checks the current best-available skater against the 5-slot limit for each side before continuing at loc_FE2C2

**Callers.** none found
**Callees.** loc_FE20E, loc_FE214, loc_FE254, loc_FE2AC, loc_FE2C2, setc1player, setc2player
**RAM.** BA_PS_flags, BA_Sktr_SCnum, OptNOP, cont1team, cont2team, sflags

```
0FE1D8  movem.l	d0-a6,-(sp)
0FE1DC  tst.w	($FFFFD04A).w
0FE1E0  beq.w	loc_FE214
0FE1E4  move.w	($FFFFC328).w,d0
0FE1E8  cmp.w	($FFFFC32A).w,d0
0FE1EC  bne.w	loc_FE1FA
0FE1F0  eor.w	#1,($FFFFD05C).w
0FE1F6  bra.w	loc_FE20E
0FE1FA  btst	#1,($FFFFC2EC).w
0FE200  beq.w	loc_FE20E
0FE204  eor.w	#1,($FFFFD05C).w
0FE20A  bra.w	loc_FE214
0FE20E  eor.w	#1,($FFFFD05A).w
0FE214  btst	#0,($FFFFC2FA).w
0FE21A  bne.w	loc_FE228
0FE21E  btst	#2,($FFFFC2F2).w
0FE224  beq.w	loc_FE2C2
0FE228  btst	#1,($FFFFC2EC).w
0FE22E  bne.w	loc_FE28A
0FE232  cmp.w	#2,($FFFFD04A).w
0FE238  bne.w	loc_FE24A
0FE23C  cmp.w	#5,($FFFFD406).w
0FE242  bgt.w	loc_FE2C2
0FE246  bra.w	loc_FE254
0FE24A  cmp.w	#5,($FFFFD406).w
0FE250  ble.w	loc_FE2C2
0FE254  move.w	#0,d0
0FE258  cmp.w	#2,($FFFFD04A).w
0FE25E  bne.w	loc_FE266
0FE262  move.w	#6,d0
0FE266  tst.w	($FFFFD05A).w
0FE26A  bne.w	loc_FE280
0FE26E  move.w	#5,d0
0FE272  cmp.w	#2,($FFFFD04A).w
0FE278  bne.w	loc_FE280
0FE27C  move.w	#$B,d0
0FE280  jsr	sub_C0BC
0FE286  bra.w	loc_FE2C2
0FE28A  cmp.w	#2,($FFFFD04A).w
0FE290  bne.w	loc_FE2A2
0FE294  cmp.w	#5,($FFFFD406).w
0FE29A  ble.w	loc_FE2C2
0FE29E  bra.w	loc_FE2AC
0FE2A2  cmp.w	#5,($FFFFD406).w
0FE2A8  bgt.w	loc_FE2C2
0FE2AC  move.w	#6,d0
0FE2B0  tst.w	($FFFFD05C).w
0FE2B4  bne.w	loc_FE2BC
0FE2B8  move.w	#$B,d0
0FE2BC  jsr	sub_C0DA
0FE2C2  movem.l	(sp)+,d0-a6
0FE2C6  rts
```

