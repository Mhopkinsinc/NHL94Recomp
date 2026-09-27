# Name review: names-batch-01.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$011738` -> `ai_LoadAsset`  (confidence 0.7, 1 insns)

**Evidence.** clears the inline-pointer slot $CF32 then falls into the tile loader at $1173C (u16 count + raw/compressed tiles -> VRAM at tile d4, d4 advanced by count); 24 callers incl. setupice, Intermission, PlayoffScreen, dobitmap

**Callers.** ClrHor, Endfaceoff, Intermission, PlayoffScreen, chkprogress, dobitmap, loc_9CDC, loc_FCC76, puckfaceoff2, puckpenshot, setoptions, setupice, sub_11F04, sub_11F12, sub_11F20, sub_16CC4, sub_16CD2, sub_16CE0, sub_16CEE, sub_16CFC, sub_16D0A, sub_16D18, sub_FE2C8, sub_FEA52
**Callees.** none

```
011738  clr.l	($FFFFCF32).w
```

## `$01172C` -> `ai_LoadAssetInline`  (confidence 0.7, 4 insns)

**Evidence.** stores its return address in $CF32 (asset pointer follows the jsr), calls the loader at $1173C, then addq.l #8,(sp) to skip the inline longword pair; 7 callers incl. setupice, setoptions, newTitleScreen

**Callers.** loc_16CAC, loc_9BD8, loc_9CDC, loc_FCC76, newTitleScreen, setoptions, setupice
**Callees.** sub_1173C

```
01172C  move.l	(sp),($FFFFCF32).w
011730  bsr.w	sub_1173C
011734  addq.l	#8,(sp)
011736  rts
```

## `$011DE2` -> `ai_PrintBigInline`  (confidence 0.8, 6 insns)

**Evidence.** same shape as printz ($11B92): takes the text after the jsr via 4(sp), calls the big-font printer $11DF4, writes the advanced pointer back to 4(sp); callers are the error screens AdrErr/DivBy0/InvOpCode and stats screens

**Callers.** AdrErr, DivBy0, InvOpCode, loc_86F8, loc_945C, loc_FC5AE, loc_FC986, loc_FCC76
**Callees.** printbig

```
011DE2  move.l	a1,-(sp)
011DE4  move.l	4(sp),a1
011DE8  bsr.w	sub_11DF4
011DEC  move.l	a1,4(sp)
011DF0  move.l	(sp)+,a1
011DF2  rts
```

## `$013508` -> `ai_PrintNextString`  (confidence 0.6, 2 insns)

**Evidence.** bsr Adda1Offset (advance a1 by its length word) then bra sub_11A48 (print at printx/printy); 12 callers incl. PrintScores1, NewTicker3pt2, puckfaceoff2

**Callers.** NewTicker3pt2, PrintScores1, loc_8280, loc_85EE, loc_961A, puckfaceoff2, sub_11C72, sub_81F2, sub_907C, sub_93C4, sub_99C6, sub_B92E
**Callees.** Adda1Offset, print2

```
013508  bsr.w	sub_13510
01350C  bra.w	sub_11A48
```

## `$0F998E` -> `ai_NumberToDecimalText`  (confidence 0.8, 35 insns)

**Evidence.** divu #100 / #10 chains on d0 writing ASCII digits ('0'+) into the string at a1+2 and counting them in d1; 5 callers in the records/stats screens

**Callers.** loc_FACF0, sub_F98C6, sub_FA75C, sub_FA8AC, sub_FCB9A
**Callees.** none

```
0F998E  movem.w	d0-d6/a0,-(sp)
0F9992  move.l	a1,-(sp)
0F9994  move.w	d0,d6
0F9996  addq.l	#2,a1
0F9998  clr.w	d1
0F999A  ext.l	d0
0F999C  divu.w	#$64,d0
0F99A0  tst.w	d0
0F99A2  beq.w	loc_F99AE
0F99A6  add.w	#$30,d0
0F99AA  move.b	d0,(a1)+
0F99AC  addq.w	#1,d1
0F99AE  swap	d0
0F99B0  ext.l	d0
0F99B2  divu.w	#$A,d0
0F99B6  add.w	#$30,d0
0F99BA  cmpnb	 $30,d0
0F99BE  bne.w	loc_F99CA
0F99C2  cmpnw	 $A,d6
0F99C6  blt.w	loc_F99CE
0F99CA  move.b	d0,(a1)+
0F99CC  addq.w	#1,d1
0F99CE  swap	d0
0F99D0  add.w	#$30,d0
0F99D4  move.b	d0,(a1)+
0F99D6  addq.w	#1,d1
0F99D8  btst	#0,d1
0F99DC  beq.w	loc_F99E6
0F99E0  move.b	#0,(a1)+
0F99E4  addq.w	#1,d1
0F99E6  move.l	(sp)+,a0
0F99E8  addq.w	#2,d1
0F99EA  move.w	d1,(a0)
0F99EC  movem.w	(sp)+,d0-d6/a0
0F99F0  rts
```

## `$0F997A` -> `ai_CopyLenString`  (confidence 0.8, 7 insns)

**Evidence.** copies (a1) bytes from a1 to a3 (length word first), preserving d0; used by the stats/records text builders

**Callers.** sub_F98C6, sub_F9A64, sub_F9AAC, sub_FA014, sub_FEEC8
**Callees.** none

```
0F997A  movem.l	d0,-(sp)
0F997E  move.w	(a1),d0
0F9980  subq.w	#1,d0
0F9982  move.b	(a1)+,(a3)+
0F9984  dbf	d0,loc_F9982
0F9988  movem.l	(sp)+,d0
0F998C  rts
```

## `$01A4EE` -> `ai_Z80_ResetAndRequestBus`  (confidence 0.9, 5 insns)

**Evidence.** writes $100 to $A11200 (Z80 reset release) and $A11100 (bus request) then spins on bit 0 of $A11100; called from the five sound-driver upload routines

**Callers.** sub_1A3B2, sub_1A3DC, sub_1A406, sub_1A430, sub_1A470
**Callees.** none
**Hardware.** Z80 busreq, Z80 reset

```
01A4EE  move.w	#$100,($A11200).l
01A4F6  move.w	#$100,($A11100).l
01A4FE  btst	#0,($A11100).l
01A506  bne.s	loc_1A4FE
01A508  rts
```

## `$0F9B94` -> `ai_SaveRecordField`  (confidence 0.6, 18 insns)

**Evidence.** computes a byte offset from d0*4 plus word_F9CA4[d1]*4 and reads or writes it through ReadSRAM/WriteSRAM depending on bit 6 of $C2F8; callers are the user-records screens

**Callers.** sub_F99F2, sub_F9AE4, sub_F9B2A, sub_F9F50
**Callees.** ReadSRAM, WriteSRAM, loc_F9BD4

```
0F9B94  bclr	#6,($FFFFC2F8).w
0F9B9A  movem.l	d0-d1/a0-a1,-(sp)
0F9B9E  asl.l	#2,d0
0F9BA0  add.l	#0,d0
0F9BA6  move.l	#word_F9CA4,a1
0F9BAC  add.w	d1,d1
0F9BAE  move.w	(a1,d1.w),d1
0F9BB2  asl.w	#2,d1
0F9BB4  ext.l	d1
0F9BB6  add.l	d1,d0
0F9BB8  moveq	#4,d1
0F9BBA  btst	#6,($FFFFC2F8).w
0F9BC0  beq.w	loc_F9BCE
0F9BC4  jsr	sub_1A1E4
0F9BCA  bra.w	loc_F9BD4
0F9BCE  jsr	sub_1A244
0F9BD4  movem.l	(sp)+,d0-d1/a0-a1
0F9BD8  rts
```

