# Name review: names-batch-20.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$008774` -> `ai_EraseEditLinesBody`  (confidence 0.6, 5 insns)

**Evidence.** sets attribute $BE at (0,0) and erases a 40x10 area with eraser; caller loc_86F8 (edit-lines screen)

**Callers.** loc_86F8
**Callees.** eraser, printz

```
008774  jsr	sub_11B92
00877A  dc.w	6
00877C  dc.b	$BE
00877D  dc.b	0
00877E  dc.b	0
00877F  dc.b	0
008780  moveq	#$28,d0
008782  moveq	#$A,d1
008784  move.w	#$7FF,d2
008788  jmp	sub_1197E
```

## `$0FCA04` -> `ai_EraseStatsBody`  (confidence 0.6, 5 insns)

**Evidence.** byte-identical to ai_EraseEditLinesBody: attribute $BE at (0,0) then a 40x10 erase; caller loc_FC986 (records/stats screen)

**Callers.** loc_FC986
**Callees.** eraser, printz

```
0FCA04  jsr	sub_11B92
0FCA0A  dc.w	6
0FCA0C  dc.b	$BE
0FCA0D  dc.b	0
0FCA0E  dc.b	0
0FCA0F  dc.b	0
0FCA10  moveq	#$28,d0
0FCA12  moveq	#$A,d1
0FCA14  move.w	#$7FF,d2
0FCA18  jmp	sub_1197E
```

## `$00A600` -> `ai_AdvanceLowRamRecord`  (confidence 0.3, 5 insns)

**Evidence.** advances a4 by $62 bytes and, on reaching $AF54, wraps it to $FF0000 (the low RAM area that ai_SnapshotGameState also uses), i.e. steps through a ring of $62-byte records; caller sub_A528 (game init)

**Callers.** sub_A528
**Callees.** none

```
00A600  add.w	#$62,a4
00A604  cmp.l	#$FFFFAF54,a4
00A60A  bne.w	locret_A9D4
00A60E  move.l	#$FFFF0000,a4
00A614  rts
```

## `$013056` -> `ai_SelectSpecialTeamsLinesBoth`  (confidence 0.6, 5 insns)

**Evidence.** Intermission: after sub_15A24 runs ai_SelectSpecialTeamsLine for the home team against the away record and, after swapping a2/a3, for the away team; caller Intermission

**Callers.** Intermission
**Callees.** ResetBench, ai_SelectSpecialTeamsLine

```
013056  bsr.w	sub_15A24
01305A  move.w	#$C6CE,a2
01305E  lea	$364(a2),a3
013062  bsr.w	sub_13068
013066  exg	a2,a3
```

## `$016384` -> `ai_PrintClockLabel`  (confidence 0.5, 5 insns)

**Evidence.** showclock: prints string d0 of the label table off_16396; caller showclock

**Callers.** showclock
**Callees.** print

```
016384  move.l	#off_16396,a1
01638A  asl.w	#2,d0
01638C  add.w	d0,a1
01638E  jsr	sub_11BA4
016394  rts
```

## `$007E36` -> `ai_InstallPauseMenu`  (confidence 0.8, 4 insns)

**Evidence.** stores the item list a0 in $CF24 and the refresh handler a1 in $CF28, and resets the cursor $CF20 and scroll $CF22 for ai_PrintScrollingMenu / ai_PauseMenuInput; caller PauseMode

**Callers.** PauseMode
**Callees.** none

```
007E36  move.l	a0,($FFFFCF24).w
007E3A  move.l	a1,($FFFFCF28).w
007E3E  clr.w	($FFFFCF20).w
007E42  clr.w	($FFFFCF22).w
```

## `$009604` -> `ai_PrintStatRowFromScroll`  (confidence 0.5, 3 insns)

**Evidence.** prints the player stat row for slot VertLineScrolling / 16 with ai_PrintPlayerStatRow; caller sub_9588

**Callers.** sub_9588
**Callees.** ai_PrintPlayerStatRow
**RAM.** VertLineScrolling

```
009604  move.w	($FFFFD5AE).w,d3
009608  lsr.w	#4,d3
00960A  bra.w	sub_9744
```

## `$00960E` -> `ai_PrintStatRowFromScrollPlus6`  (confidence 0.5, 4 insns)

**Evidence.** prints the player stat row for slot VertLineScrolling / 16 + 6 with ai_PrintPlayerStatRow; caller sub_9588

**Callers.** sub_9588
**Callees.** ai_PrintPlayerStatRow
**RAM.** VertLineScrolling

```
00960E  move.w	($FFFFD5AE).w,d3
009612  lsr.w	#4,d3
009614  addq.w	#6,d3
009616  bra.w	sub_9744
```

## `$0F780C` -> `ai_SetupCursorBoxDefault`  (confidence 0.5, 4 insns)

**Evidence.** ai_MoveSetupCursor helper: positions at column $10 row $E (attribute $FF) and returns the default cursor box size d0 = $17, d1 = $D; caller ai_MoveSetupCursor

**Callers.** ai_MoveSetupCursor
**Callees.** printz

```
0F780C  jsr	sub_11B92
0F7812  dc.w	6
0F7814  dc.b	$FF
0F7815  dc.b	$10
0F7816  dc.b	$E
0F7817  dc.b	0
0F7818  move.w	#$17,d0
0F781C  move.w	#$D,d1
0F7820  rts
```

## `$011F20` -> `ai_LoadPlayoffTiles`  (confidence 0.5, 3 insns)

**Evidence.** loads asset unk_ABA1C at tile 2 with LoadAsset; caller PlayoffScreen (ai_DrawPlayoffRoundLabel draws its labels at tile base 2)

**Callers.** PlayoffScreen
**Callees.** ai_LoadAsset

```
011F20  moveq	#2,d4
011F22  move.l	#unk_ABA1C,a2
011F28  bra.w	sub_11738
```

## `$0134D8` -> `ai_EraseTickerArea`  (confidence 0.7, 3 insns)

**Evidence.** Intermission: positions with ai_TickerAreaSetup and erases the returned $1A x 5 area; caller Intermission

**Callers.** Intermission
**Callees.** ai_TickerAreaSetup, eraser

```
0134D8  bsr.w	sub_134E4
0134DC  move.w	#$7FF,d2
0134E0  bra.w	sub_1197E
```

## `$016CC4` -> `ai_LoadHudTiles`  (confidence 0.5, 3 insns)

**Evidence.** loads asset unk_AB928 at tile base $B016, the base that ai_DrawLineEnergyBar (bitmap unk_AB920, same family) and the playoff cursor sprites use; caller ai_LoadRinkGraphics

**Callers.** ai_LoadRinkGraphics
**Callees.** ai_LoadAsset

```
016CC4  move.w	($FFFFB016).w,d4
016CC8  move.l	#unk_AB928,a2
016CCE  bra.w	sub_11738
```

## `$016CD2` -> `ai_LoadCrowdSpriteTiles`  (confidence 0.5, 3 insns)

**Evidence.** loads asset unk_A4B5C at tile base $B01A, the base ai_EmitCrowdSprites adds to every crowd sprite tile; caller ai_LoadRinkGraphics

**Callers.** ai_LoadRinkGraphics
**Callees.** ai_LoadAsset

```
016CD2  move.w	($FFFFB01A).w,d4
016CD6  move.l	#unk_A4B5C,a2
016CDC  bra.w	sub_11738
```

## `$016CE0` -> `ai_LoadPauseMenuTiles`  (confidence 0.5, 3 insns)

**Evidence.** loads asset unk_5CF6C at tile base ExtraChars ($B026); caller PauseMode

**Callers.** PauseMode
**Callees.** ai_LoadAsset
**RAM.** ExtraChars

```
016CE0  move.w	($FFFFB026).w,d4
016CE4  move.l	#unk_5CF6C,a2
016CEA  bra.w	sub_11738
```

