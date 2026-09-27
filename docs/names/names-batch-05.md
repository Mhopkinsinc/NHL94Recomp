# Name review: names-batch-05.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$017CA0` -> `ai_ApplyPlayoffPassword`  (confidence 0.6, 28 insns)

**Evidence.** decodes the SRAM password copy at $D088 with ai_DecodePlayoffPassword; if gamelevel or bosgames is non-zero it rebuilds the bracket (sub_17D80), normalises pojoy (2..7 minus 2 without FourWayPlay, 1->3 and 2->4 with it) and sets $D04A = rounds remaining as 7 (or $B for 4-way play) minus pojoy; callers GameSetUp_3 and sub_F76CE (a jmp thunk used by GameSetUp)

**Callers.** GameSetUp_3, sub_F76CE
**Callees.** MakeTree, ai_DecodePlayoffPassword, loc_17D08
**RAM.** FourWayPlay, OptNOP, bosgames, gamelevel, pojoy

```
017CA0  movem.l	d0-a3,-(sp)
017CA4  move.w	#$D088,a3
017CA8  bsr.w	sub_1803E
017CAC  move.w	($FFFFCEEC).w,d0
017CB0  or.w	($FFFFCEEA).w,d0
017CB4  beq.w	loc_17D10
017CB8  bsr.w	sub_17D80
017CBC  moveq	#7,d0
017CBE  tst.w	($FFFFD046).w
017CC2  beq.w	loc_17CCA
017CC6  move.w	#$B,d0
017CCA  tst.w	($FFFFD046).w
017CCE  bne.w	loc_17CE4
017CD2  cmp.w	#2,($FFFFCEF0).w
017CD8  blt.w	loc_17D08
017CDC  subq.w	#2,($FFFFCEF0).w
017CE0  bra.w	loc_17D08
017CE4  cmp.w	#1,($FFFFCEF0).w
017CEA  bne.w	loc_17CF8
017CEE  move.w	#3,($FFFFCEF0).w
017CF4  bra.w	loc_17D08
017CF8  cmp.w	#2,($FFFFCEF0).w
017CFE  bne.w	loc_17D08
017D02  move.w	#4,($FFFFCEF0).w
017D08  sub.w	($FFFFCEF0).w,d0
017D0C  move.w	d0,($FFFFD04A).w
017D10  movem.l	(sp)+,d0-a3
017D14  rts
```

## `$01833A` -> `ai_UnpackPlayoffStats`  (confidence 0.6, 25 insns)

**Evidence.** bit-stream reader: unpacks 104 words into $CD96 from the packed block ending at $D092 (reads a long at $D092-$22+$100-2*(bit>>4), shifts by bit&15), with field widths cycling through byte_18336 = $C, $E, $A, $A; the packer sub_182A2 uses the same width table; callers AddPOStats and sub_9428 (PeriodOver's playoff stats print)

**Callers.** AddPOStats, sub_9428
**Callees.** none

```
01833A  move.w	#$CD96,a0
01833E  move.l	#byte_18336,a1
018344  move.w	#$D092,a2
018348  moveq	#$67,d0
01834A  clr.w	d4
01834C  move.w	d4,d5
01834E  lsr.w	#4,d5
018350  add.w	d5,d5
018352  neg.w	d5
018354  add.w	#$100,d5
018358  move.l	-$22(a2,d5.w),d1
01835C  move.w	d4,d5
01835E  and.w	#$F,d5
018362  lsr.l	d5,d1
018364  move.w	d0,d2
018366  and.w	#3,d2
01836A  move.b	(a1,d2.w),d2
01836E  add.w	d2,d4
018370  clr.w	d3
018372  bset	d2,d3
018374  subq.w	#1,d3
018376  and.w	d3,d1
018378  move.w	d1,(a0)+
01837A  dbf	d0,loc_1834C
01837E  rts
```

## `$0F8070` -> `ai_PrintSetupMenuLabels`  (confidence 0.8, 23 insns)

**Evidence.** prints the setup menu's row labels from word_F80D4 (Play Mode, Players, Team 1, Team 2, Per. Length, Goalies) at column 3, two rows apart starting at row $F - 2*$D422 (the scroll offset), skipping rows above $F and stopping past $19; $C2F8 bit 3 held while printing; callers GameSetUp and sub_F78A2

**Callers.** GameSetUp, sub_F78A2
**Callees.** loc_F8090, loc_F80C2, print2
**Strings.** Play Mode | Players | Team 1 | Team 2 | Per. Length | Goalies
**RAM.** printa, printm, printx, printy

```
0F8070  movem.l	d0-d1,-(sp)
0F8074  bset	#3,($FFFFC2F8).w
0F807A  move.l	#word_F80D4,a1
0F8080  move.w	#$F,d0
0F8084  move.w	($FFFFD422).w,d1
0F8088  add.w	d1,d1
0F808A  sub.w	d1,d0
0F808C  move.w	d0,($FFFFB02A).w
0F8090  cmp.w	#$F,($FFFFB02A).w
0F8096  bge.w	loc_F80A0
0F809A  add.w	(a1),a1
0F809C  bra.w	loc_F80C2
0F80A0  cmp.w	#$19,($FFFFB02A).w
0F80A6  bgt.w	loc_F80C8
0F80AA  move.w	#3,($FFFFB028).w
0F80B0  move.w	#0,($FFFFB02C).w
0F80B6  move.w	#0,($FFFFB02E).w
0F80BC  jsr	sub_11A48
0F80C2  addq.w	#2,($FFFFB02A).w
0F80C6  bra.s	loc_F8090
0F80C8  bclr	#3,($FFFFC2F8).w
0F80CE  movem.l	(sp)+,d0-d1
0F80D2  rts
```

## `$0F85B0` -> `ai_DrawSetupAwayLogo`  (confidence 0.6, 16 insns)

**Evidence.** away-side twin of ai_DrawSetupHomeLogo: after ai_ClearSetupLogoPanels sets $D42E bits 2 (away) and 6, calls sub_F8770, prints the caption at column 8 or $19 and jumps into the shared logo-drawing tail at loc_F865C, which picks tile base $D432 because bit 2 is set; callers GameSetUp, GameSetUp_2

**Callers.** GameSetUp, GameSetUp_2
**Callees.** ai_ClearSetupLogoPanels, loc_F865C, printz, sub_F8770
**RAM.** printx, printy

```
0F85B0  movem.l	d0-a6,-(sp)
0F85B4  bsr.w	sub_F84FC
0F85B8  bset	#2,($FFFFD42E).w
0F85BE  bset	#6,($FFFFD42E).w
0F85C4  bsr.w	sub_F8770
0F85C8  bclr	#3,($FFFFD42E).w
0F85CE  beq.w	loc_F85F2
0F85D2  jsr	sub_11B92
0F85D8  dc.w	6
0F85DA  dc.b	$EF
0F85DB  dc.b	0
0F85DC  dc.b	0
0F85DD  dc.b	0
0F85DE  move.w	#8,($FFFFB028).w
0F85E4  move.w	#5,($FFFFB02A).w
0F85EA  moveq	#8,d0
0F85EC  moveq	#8,d1
0F85EE  move.w	#$7FF,d2
0F85F2  jsr	sub_11B92
0F85F8  dc.w	6
0F85FA  dc.b	$FF
0F85FB  dc.b	0
0F85FC  dc.b	0
0F85FD  dc.b	0
0F85FE  move.w	#$19,($FFFFB028).w
0F8604  bra.w	loc_F865C
```

## `$0FE2C8` -> `ai_UpdateTileAnimation`  (confidence 0.6, 23 insns)

**Evidence.** per-frame driver for the animation selected in $D6B4 (-1 = none): on first run takes the (frame script, asset) pair from off_FE364[$D6B4], loads the asset at tile $D6AC with LoadAsset and starts frame 0; otherwise counts $D6B2 down by d7 and advances $D6B0 through ai_TileAnimationStep; callers periodiceevents and waitxsr

**Callers.** periodiceevents, waitxsr
**Callees.** ai_LoadAsset, ai_TileAnimationStep, loc_FE320

```
0FE2C8  tst.w	($FFFFD6B4).w
0FE2CC  bmi.w	locret_FE324
0FE2D0  movem.l	d0-a6,-(sp)
0FE2D4  tst.l	($FFFFD6BA).w
0FE2D8  bne.w	loc_FE310
0FE2DC  move.w	($FFFFD6B4).w,d0
0FE2E0  asl.w	#3,d0
0FE2E2  move.l	#off_FE364,a0
0FE2E8  move.l	(a0,d0.w),($FFFFD6B6).w
0FE2EE  move.l	4(a0,d0.w),($FFFFD6BA).w
0FE2F4  move.l	4(a0,d0.w),a2
0FE2F8  addq.w	#8,a2
0FE2FA  move.w	($FFFFD6AC).w,d4
0FE2FE  jsr	sub_11738
0FE304  clr.w	($FFFFD6B0).w
0FE308  bsr.w	sub_FE326
0FE30C  bra.w	loc_FE320
0FE310  sub.w	d7,($FFFFD6B2).w
0FE314  bpl.w	loc_FE320
0FE318  addq.w	#1,($FFFFD6B0).w
0FE31C  bsr.w	sub_FE326
0FE320  movem.l	(sp)+,d0-a6
0FE324  rts
```

## `$0FE326` -> `ai_TileAnimationStep`  (confidence 0.6, 17 insns)

**Evidence.** reads the current frame's (frame index, duration) byte pair from the script at $D6B6 + 2*$D6B0 into $D6AE/$D6B2; -1 restarts the script from frame 0, -2 calls sub_FE548 (script end); only caller ai_UpdateTileAnimation

**Callers.** ai_UpdateTileAnimation
**Callees.** sub_FE548

```
0FE326  move.l	($FFFFD6B6).w,a0
0FE32A  move.w	($FFFFD6B0).w,d0
0FE32E  add.w	d0,d0
0FE330  move.b	(a0,d0.w),d1
0FE334  ext.w	d1
0FE336  move.w	d1,($FFFFD6AE).w
0FE33A  move.b	1(a0,d0.w),d1
0FE33E  ext.w	d1
0FE340  move.w	d1,($FFFFD6B2).w
0FE344  cmp.w	#$FFFF,($FFFFD6AE).w
0FE34A  bne.w	loc_FE354
0FE34E  clr.w	($FFFFD6B0).w
0FE352  bra.s	sub_FE326
0FE354  cmp.w	#$FFFE,($FFFFD6AE).w
0FE35A  bne.w	locret_FE362
0FE35E  bsr.w	sub_FE548
0FE362  rts
```

## `$0FE510` -> `ai_StartTileAnimation`  (confidence 0.7, 9 insns)

**Evidence.** sets $D6B4 = d0 (the animation id) and clears the script/asset pointers $D6B6/$D6BA so ai_UpdateTileAnimation reloads it on the next frame; callers include ROM:$FB4E and sub_14062

**Callers.** FallDown, puckfaceoff2
**Callees.** none

```
0FE510  movem.l	d0-a6,-(sp)
0FE514  move.w	d0,($FFFFD6B4).w
0FE518  move.l	#0,($FFFFD6B6).w
0FE520  move.l	#0,($FFFFD6BA).w
0FE528  move.w	#1,($FFFFD6AE).w
0FE52E  clr.w	($FFFFD6B0).w
0FE532  st	($FFFFD6BE).w
0FE536  movem.l	(sp)+,d0-a6
0FE53A  rts
```

## `$0FE756` -> `ai_StartWaypointScript`  (confidence 0.4, 12 insns)

**Evidence.** picks a random script 0..6 (sub_11086 with d0 = 7) into $DA12, clears $C2FC bit 3, resets the step index $DA14 to -1 and the current x $DA16, and loads the first point via ai_NextWaypoint; only caller sub_FC4C0

**Callers.** sub_FC4C0
**Callees.** ai_NextWaypoint, randomd0

```
0FE756  movem.l	d0-a6,-(sp)
0FE75A  move.w	#7,d0
0FE75E  jsr	sub_11086
0FE764  cmpnw	 6,d0
0FE768  bgt.s	loc_FE75A
0FE76A  move.w	d0,($FFFFDA12).w
0FE76E  bclr	#3,($FFFFC2FC).w
0FE774  move.w	#$FFFF,($FFFFDA14).w
0FE77A  clr.w	($FFFFDA16).w
0FE77E  bsr.w	sub_FE7FC
0FE782  movem.l	(sp)+,d0-a6
0FE786  rts
```

## `$0FE7FC` -> `ai_NextWaypoint`  (confidence 0.4, 23 insns)

**Evidence.** advances $DA14 and reads the next 8-byte entry of script off_FE788[$DA12]: relative x into $DA16 (negated when bit 0 of $76(a3) is set) and y into $DA18; an entry whose byte 4 is $80 ends the script, setting $C2FC bit 3 and copying its bytes 5..7 into $DA1D/$DA1A; sub_FE864 (from asspuckc) steers the player toward the point and calls this when within reach; callers ai_StartWaypointScript, sub_FE864

**Callers.** ai_StartWaypointScript, sub_FE864
**Callees.** none

```
0FE7FC  movem.l	d0-a6,-(sp)
0FE800  cmp.b	#$80,($FFFFDA16).w
0FE806  beq.w	loc_FE85E
0FE80A  addq.w	#1,($FFFFDA14).w
0FE80E  move.w	($FFFFDA14).w,d0
0FE812  asl.w	#2,d0
0FE814  move.l	#off_FE788,a0
0FE81A  move.w	($FFFFDA12).w,d1
0FE81E  asl.w	#2,d1
0FE820  move.l	(a0,d1.w),a0
0FE824  move.w	(a0,d0.w),($FFFFDA16).w
0FE82A  btst	#0,$76(a3)
0FE830  beq.w	loc_FE838
0FE834  neg.w	($FFFFDA16).w
0FE838  move.w	2(a0,d0.w),($FFFFDA18).w
0FE83E  cmp.b	#$80,4(a0,d0.w)
0FE844  bne.w	loc_FE85E
0FE848  bset	#3,($FFFFC2FC).w
0FE84E  clr.w	($FFFFDA1C).w
0FE852  move.b	5(a0,d0.w),($FFFFDA1D).w
0FE858  move.w	6(a0,d0.w),($FFFFDA1A).w
0FE85E  movem.l	(sp)+,d0-a6
0FE862  rts
```

## `$01AD54` -> `ai_InitSoundChannels`  (confidence 0.8, 19 insns)

**Evidence.** fills the eight 6-byte active-sound slots at $D3D4 with -1, then initialises the six 8-byte channel records below it ($D3A4..): hardware channel at +4 = 0,1,2,4,5,6 (skips FM channel 3), +0 and +3 = $FF, +1 and +6 = 0; callers AllSndOff and Z80_LoadROM

**Callers.** AllSndOff, Z80_LoadROM
**Callees.** none

```
01AD54  lea	($FFFFD3D4).w,a0
01AD58  moveq	#7,d0
01AD5A  moveq	#$FFFFFFFF,d1
01AD5C  move.l	d1,(a0)
01AD5E  addq.w	#6,a0
01AD60  dbf	d0,loc_1AD5C
01AD64  moveq	#5,d0
01AD66  move.w	#$D3D4,a0
01AD6A  subq.w	#8,a0
01AD6C  move.b	d0,4(a0)
01AD70  cmpnw	 3,d0
01AD74  blt.w	loc_1AD7C
01AD78  addq.b	#1,4(a0)
01AD7C  st	3(a0)
01AD80  st	(a0)
01AD82  clr.b	1(a0)
01AD86  clr.b	6(a0)
01AD8A  dbf	d0,loc_1AD6A
01AD8E  rts
```

## `$0FEFF0` -> `ai_ClearOneTimer`  (confidence 0.5, 19 insns)

**Evidence.** cancels a one-timer for player object a3: clears $64 bit 3, $62 bit 5, $63 bit 1, zeroes $BF76, sets onetimerplayer ($BF6C) to -1, forces animation state $50C through SetSPA, then calls sub_10646 when the position slot $34(a3) is negative or sub_15A88 otherwise, and resets $5A/$5C; callers assonetimer and setass

**Callers.** assonetimer, setass
**Callees.** SetSPA, Setplass, assexit, loc_FF032
**RAM.** onetimerplayer

```
0FEFF0  movem.l	d0/a0,-(sp)
0FEFF4  bclr	#3,$64(a3)
0FEFFA  bclr	#5,$62(a3)
0FF000  bclr	#1,$63(a3)
0FF006  clr.w	($FFFFBF76).w
0FF00A  st	($FFFFBF6C).w
0FF00E  move.w	d1,-(sp)
0FF010  move.w	#$50C,d1
0FF014  jsr	sub_1073A
0FF01A  tst.w	$34(a3)
0FF01E  bpl.w	loc_FF02C
0FF022  jsr	sub_10646
0FF028  bra.w	loc_FF032
0FF02C  jsr	sub_15A88
0FF032  clr.w	$5A(a3)
0FF036  st	$5C(a3)
0FF03A  move.w	(sp)+,d1
0FF03C  movem.l	(sp)+,d0/a0
0FF040  rts
```

## `$00DB68` -> `ai_GoalieTurnToward`  (confidence 0.6, 15 insns)

**Evidence.** d0 = desired facing 0..7, a3 = goalie object: computes the shortest rotation from the current facing $54(a3), stepping by one (or two when bit 3 of $62(a3) is clear and the special cases in the $DB86..$DBA9 block apply) and stores the new facing masked to 0..7. Note: the 2016 listing shows $DB86..$DBA9 as dc.w data although it is reached by fall-through; the recompiler translated it (it appears in nhl94_part07.c). Callers assgoaliecpu and goalieacc

**Callers.** assgoaliecpu, goalieacc
**Callees.** none

```
00DB68  move.w	$54(a3),d1
00DB6C  sub.w	d1,d0
00DB6E  beq.w	locret_15464
00DB72  neg.w	d0
00DB74  and.w	#4,d0
00DB78  lsr.w	#1,d0
00DB7A  subq.w	#1,d0
00DB7C  btst	#3,$62(a3)
00DB82  bne.w	loc_DBAE
00DB86  dc.w	$33C
00DB88  dc.w	$42
00DB8A  dc.w	$6700
00DB8C  dc.w	$22
00DB8E  dc.w	$D240
00DB90  dc.w	$82B
00DB92  dc.w	7
00DB94  dc.w	$62
00DB96  dc.w	$6600
00DB98  dc.w	$A
00DB9A  dc.w	$33C
00DB9C  dc.w	$83
00DB9E  dc.w	$6000
00DBA0  dc.w	6
00DBA2  dc.w	$33C
00DBA4  dc.w	$38
00DBA6  dc.w	$6700
00DBA8  dc.w	8
00DBAA  neg.w	d0
00DBAC  add.w	d0,d1
00DBAE  add.w	d0,d1
00DBB0  and.w	#7,d1
00DBB4  move.w	d1,$54(a3)
00DBB8  rts
```

## `$0FB992` -> `ai_CopyUserNameDashed`  (confidence 0.6, 17 insns)

**Evidence.** copies the 12-byte user-name entry $D45A + $D4EA*12 to a1, writing '-' for zero bytes and counting only the real characters in $D4E8; used by the name-entry screen loc_FB822 and by sub_FEEC8 for the '(played by ...)' credit

**Callers.** loc_FB822, sub_FEEC8
**Callees.** loc_FB9C2

```
0FB992  movem.l	d0-a6,-(sp)
0FB996  move.l	#$FFFFD45A,a0
0FB99C  move.w	($FFFFD4EA).w,d2
0FB9A0  mulu.w	#$C,d2
0FB9A4  move.w	#0,($FFFFD4E8).w
0FB9AA  move.w	#$B,d3
0FB9AE  move.b	(a0,d2.w),d0
0FB9B2  beq.w	loc_FB9BA
0FB9B6  bra.w	loc_FB9C2
0FB9BA  move.b	#$2D,d0
0FB9BE  subq.w	#1,($FFFFD4E8).w
0FB9C2  move.b	d0,(a1)+
0FB9C4  addq.w	#1,($FFFFD4E8).w
0FB9C8  addq.w	#1,d2
0FB9CA  dbf	d3,loc_FB9AE
0FB9CE  movem.l	(sp)+,d0-a6
0FB9D2  rts
```

## `$0FA880` -> `ai_AppendTeamName`  (confidence 0.7, 14 insns)

**Evidence.** d0 = team index, a1 = destination string: looks up the team record via the table at $30E, follows its +4 offset to the team name string and appends it with appstring; callers sub_F9B2A and sub_FA75C (user records text)

**Callers.** sub_F9B2A, sub_FA75C
**Callees.** appstring

```
0FA880  movem.l	d0/a0-a3,-(sp)
0FA884  ext.w	d0
0FA886  asl.w	#2,d0
0FA888  move.l	#$30E,a0
0FA88E  move.l	(a0,d0.w),a0
0FA892  move.w	4(a0),d0
0FA896  ext.l	d0
0FA898  add.l	d0,a0
0FA89A  add.w	(a0),a0
0FA89C  move.l	a1,a3
0FA89E  move.l	a0,a1
0FA8A0  jsr	sub_11D9E
0FA8A6  movem.l	(sp)+,d0/a0-a3
0FA8AA  rts
```

## `$0099C6` -> `ai_PrintScrollArrows`  (confidence 0.6, 16 insns)

**Evidence.** edit-lines roster: prints one of the four control strings at word_9A02 chosen by d0 = (VertLineScrolling > 0) + 2*(VertLineScrolling < $D5B2), i.e. whether the list can scroll up and/or down, at the header position set by the inline print2 string; callers loc_945C and sub_9588

**Callers.** loc_945C, sub_9588
**Callees.** ai_PrintNextString, printz2
**Strings.** Crowd  Meter
**RAM.** VertLineScrolling

```
0099C6  movem.l	d0-d1/a1,-(sp)
0099CA  jsr	sub_11A36
0099D0  dc.w	$A
0099D2  dc.b	$F8
0099D3  dc.b	4
0099D4  dc.b	3
0099D5  dc.b	2
0099D6  dc.b	$B
0099D7  dc.b	$F9
0099D8  dc.b	1
0099D9  dc.b	0
0099DA  clr.w	d0
0099DC  move.w	($FFFFD5AE).w,d1
0099E0  tst.w	d1
0099E2  sgt	d0
0099E4  neg.b	d0
0099E6  cmp.w	($FFFFD5B2).w,d1
0099EA  slt	d1
0099EC  neg.b	d1
0099EE  add.b	d1,d0
0099F0  add.b	d1,d0
0099F2  lea	word_9A02(pc),a1
0099F6  jsr	sub_13508
0099FC  movem.l	(sp)+,d0-d1/a1
009A00  rts
```

