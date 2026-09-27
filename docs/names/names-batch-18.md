# Name review: names-batch-18.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$016226` -> `ai_EmitCrowdSections`  (confidence 0.6, 10 insns)

**Evidence.** showcrowd: for up to four crowd sections (d2 & $F, capped at 3) starting at d3 emits each section's visible sprites with ai_EmitCrowdSprites; caller showcrowd

**Callers.** showcrowd
**Callees.** ai_EmitCrowdSprites, loc_16240

```
016226  and.w	#$F,d2
01622A  cmpnw	 3,d2
01622E  bls.w	loc_16234
016232  moveq	#3,d2
016234  bra.w	loc_16240
016238  move.w	d3,d0
01623A  add.w	d2,d0
01623C  bsr.w	sub_16246
016240  dbf	d2,loc_16238
016244  rts
```

## `$01A430` -> `ai_ReadPad2Hardware`  (confidence 0.7, 10 insns)

**Evidence.** port-2 twin of ai_ReadPad1Hardware: requests the Z80 bus (with the reset retry), writes $3C to $A10005 (TH high) and joins the port-1 reader's body at loc_1A498 with a0 = $A10003 to pack and remap the buttons; caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** ai_Z80_ResetAndRequestBus, loc_1A498
**Hardware.** Z80 busreq, pad1, pad2

```
01A430  move.w	#$100,($A11100).l
01A438  move.w	#$64,d0
01A43C  btst	#0,($A11100).l
01A444  beq.s	loc_1A44E
01A446  dbf	d0,loc_1A43C
01A44A  bsr.w	sub_1A4EE
01A44E  move.b	#$3C,($A10005).l
01A456  movem.l	d1/a0,-(sp)
01A45A  lea	($A10003).l,a0
01A460  bra.w	loc_1A498
```

## `$0F72DA` -> `ai_CopyBestSixIndexes`  (confidence 0.6, 10 insns)

**Evidence.** copies the six player indexes (every other byte) from the rating-sorted pairs at $BF20 to a0 as word entries (best first); caller ai_BuildRatingsStartingSix

**Callers.** ai_BuildRatingsStartingSix
**Callees.** none

```
0F72DA  movem.l	d0-d1/a0-a1,-(sp)
0F72DE  move.l	#$FFFFBF20,a1
0F72E4  move.w	#0,d0
0F72E8  clr.b	(a0)+
0F72EA  move.b	(a1),d1
0F72EC  move.b	d1,(a0)+
0F72EE  tst.w	(a1)+
0F72F0  dbf	d0,loc_F72E8
0F72F4  movem.l	(sp)+,d0-d1/a0-a1
0F72F8  rts
```

## `$0F72FA` -> `ai_CopyWorstSixIndexes`  (confidence 0.6, 9 insns)

**Evidence.** copies the six player indexes from the sorted pairs at $BF20 in reverse order (starting at $BF2A, worst first) to a0 as word entries; caller ai_BuildRatingsStartingSix

**Callers.** ai_BuildRatingsStartingSix
**Callees.** none

```
0F72FA  movem.l	d0/a0-a1,-(sp)
0F72FE  move.l	#$FFFFBF2A,a1
0F7304  move.w	#0,d0
0F7308  clr.b	(a0)+
0F730A  move.b	(a1),(a0)+
0F730C  tst.w	-(a1)
0F730E  dbf	d0,loc_F7308
0F7312  movem.l	(sp)+,d0/a0-a1
0F7316  rts
```

## `$009BB4` -> `ai_PrintCrowdMeterValue`  (confidence 0.5, 9 insns)

**Evidence.** crowd meter: prints sqrt(4 * d0) + $41 (sroot) as a 3-digit number followed by the inline ' dB' string; caller loc_9A84 (crowd meter display)

**Callers.** loc_9A84
**Callees.** DeterStrLength?, print, printz, sroot

```
009BB4  ext.l	d0
009BB6  asl.w	#2,d0
009BB8  bsr.w	sub_110BE
009BBC  add.w	#$41,d0
009BC0  moveq	#3,d1
009BC2  jsr	sub_11D3A
009BC8  bsr.w	sub_11BA4
009BCC  bsr.w	sub_11B92
009BD0  dc.w	6
009BD2  dc.b	$20
009BD3  dc.b	$64
009BD4  dc.b	$42
009BD5  dc.b	0
009BD6  rts
```

## `$012D0E` -> `ai_PrintTeamNameAndScore`  (confidence 0.7, 9 insns)

**Evidence.** PrintScores1: prints team a2's name (record +$1E data, name via the +4 offset) then its score $C(a2) as a 2-digit number at column $1C; caller PrintScores1

**Callers.** PrintScores1
**Callees.** DeterStrLength?, print
**RAM.** printx

```
012D0E  move.l	$1E(a2),a1
012D12  add.w	4(a1),a1
012D16  add.w	(a1),a1
012D18  bsr.w	sub_11BA4
012D1C  move.w	#$1C,($FFFFB028).w
012D22  move.w	$C(a2),d0
012D26  moveq	#2,d1
012D28  bsr.w	sub_11D3A
012D2C  bra.w	sub_11BA4
```

## `$01721C` -> `ai_LoadTeamPaletteLine`  (confidence 0.7, 9 insns)

**Evidence.** SetTeamColors: copies eight longs (one 32-byte CRAM line) from team a0's palette block (data offset +2, plus d1) into the palette buffer at $BD68 + d1; caller SetTeamColors

**Callers.** SetTeamColors
**Callees.** none

```
01721C  move.l	$1E(a0),a2
017220  add.w	2(a2),a2
017224  add.w	d1,a2
017226  move.w	#$BD68,a1
01722A  add.w	d1,a1
01722C  moveq	#7,d0
01722E  move.l	(a2)+,(a1)+
017230  dbf	d0,loc_1722E
017234  rts
```

## `$0175D8` -> `ai_BlinkAndWaitFrame`  (confidence 0.6, 9 insns)

**Evidence.** PlayoffScreen: when the fade counter $BD26 is negative toggles palette entry $BD6A with $EE (blinking the cursor colour) and reloads $BD26 = $18, then waits until vcount ($B03E) differs from oldvcount ($B040) and stores the new value; caller PlayoffScreen

**Callers.** PlayoffScreen
**Callees.** none
**RAM.** oldvcount, palcount, vcount

```
0175D8  tst.w	($FFFFBD26).w
0175DC  bpl.w	loc_175EC
0175E0  eor.w	#$EE,($FFFFBD6A).w
0175E6  move.w	#$18,($FFFFBD26).w
0175EC  move.w	($FFFFB03E).w,d0
0175F0  cmp.w	($FFFFB040).w,d0
0175F4  beq.s	loc_175EC
0175F6  move.w	d0,($FFFFB040).w
0175FA  rts
```

## `$01821A` -> `ai_BigNumAdd`  (confidence 0.8, 9 insns)

**Evidence.** adds the 32-bit d0 to the low end of the five-word number at a3 and ripples the carry through the upper words (dbcc loop); caller ai_BigNumMulAdd

**Callers.** ai_BigNumMulAdd
**Callees.** loc_1822C

```
01821A  movem.l	d1/a0,-(sp)
01821E  lea	$A(a3),a0
018222  moveq	#3,d1
018224  add.l	d0,-(a0)
018226  bra.w	loc_1822C
01822A  addq.w	#1,-(a0)
01822C  dbcc	d1,loc_1822A
018230  movem.l	(sp)+,d1/a0
018234  rts
```

## `$018A6E` -> `ai_ShowCheckedPlayerMessage`  (confidence 0.5, 9 insns)

**Evidence.** UpdatePA: takes TempPlOffset ($C470); a negative value selects the away record (index in the low byte), then calls sub_18A90 with the player index and team record (the message builder for the last check/hit); caller UpdatePA

**Callers.** UpdatePA
**Callees.** getname
**RAM.** TempPlOffset

```
018A6E  movem.l	d0/a2,-(sp)
018A72  move.w	#$C6CE,a2
018A76  move.w	($FFFFC470).w,d0
018A7A  bpl.w	loc_18A86
018A7E  and.w	#$FF,d0
018A82  add.w	#$364,a2
018A86  bsr.w	sub_18A90
018A8A  movem.l	(sp)+,d0/a2
018A8E  rts
```

## `$0F7B0A` -> `ai_WrapOptionValue`  (confidence 0.6, 9 insns)

**Evidence.** GameSetUp_3 helper: d3 = value + step d2 wrapped into the range d4..d5 (below d4 wraps to d5, at or above d5 wraps to d4 - 1... i.e. cycles the option value); caller GameSetUp_3

**Callers.** GameSetUp_3
**Callees.** none

```
0F7B0A  add.w	d2,d3
0F7B0C  cmp.w	d5,d3
0F7B0E  bge.w	loc_F7B16
0F7B12  move.w	d4,d3
0F7B14  subq.w	#1,d3
0F7B16  cmp.w	d4,d3
0F7B18  blt.w	locret_F78A0
0F7B1C  move.w	d5,d3
0F7B1E  rts
```

## `$0F9FC0` -> `ai_CacheAttributeCounts`  (confidence 0.6, 9 insns)

**Evidence.** stores ai_CountRatingNibbles of the home and away records in $D448/$D44A for the record updates; caller ai_UpdateGameRecords

**Callers.** ai_UpdateGameRecords
**Callees.** ai_CountRatingNibbles

```
0F9FC0  movem.l	d0-a6,-(sp)
0F9FC4  move.l	#$FFFFC6CE,a2
0F9FCA  jsr	sub_9F40
0F9FD0  move.w	d0,($FFFFD448).w
0F9FD4  move.l	#$FFFFCA32,a2
0F9FDA  jsr	sub_9F40
0F9FE0  move.w	d0,($FFFFD44A).w
0F9FE4  movem.l	(sp)+,d0-a6
0F9FE8  rts
```

## `$0F9FEA` -> `ai_CacheRosterSizes`  (confidence 0.6, 9 insns)

**Evidence.** stores ai_CountRosterPlayers of the home and away records in $D44C/$D44E for the record updates; caller ai_UpdateGameRecords

**Callers.** ai_UpdateGameRecords
**Callees.** ai_CountRosterPlayers

```
0F9FEA  movem.l	d0-a6,-(sp)
0F9FEE  move.l	#$FFFFC6CE,a2
0F9FF4  jsr	sub_9F9A
0F9FFA  move.w	d0,($FFFFD44C).w
0F9FFE  move.l	#$FFFFCA32,a2
0FA004  jsr	sub_9F9A
0FA00A  move.w	d0,($FFFFD44E).w
0FA00E  movem.l	(sp)+,d0-a6
0FA012  rts
```

## `$0FAC3E` -> `ai_PrintRecordsTeamName`  (confidence 0.6, 9 insns)

**Evidence.** records screen: at row d1 prints the selected team's name (home, or away when $D4F6) through sub_FAC78; caller ai_PrintRecordsScreen

**Callers.** ai_PrintRecordsScreen
**Callees.** sub_FAC78
**RAM.** printy

```
0FAC3E  movem.l	d0-a6,-(sp)
0FAC42  move.w	d1,($FFFFB02A).w
0FAC46  move.l	#$FFFFC6CE,a0
0FAC4C  tst.w	($FFFFD4F6).w
0FAC50  beq.w	loc_FAC5A
0FAC54  move.l	#$FFFFCA32,a0
0FAC5A  move.l	$1E(a0),a0
0FAC5E  add.w	4(a0),a0
0FAC62  bsr.w	sub_FAC78
```

