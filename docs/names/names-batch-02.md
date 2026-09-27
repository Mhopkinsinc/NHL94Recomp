# Name review: names-batch-02.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$011318` -> `ai_PadAutoRepeat`  (confidence 0.8, 12 insns)

**Evidence.** after nodiag, implements menu key auto-repeat: d3 = held pad, d2 = previous; a fresh press loads the repeat timer $B042 with $F, otherwise the timer counts down and on expiry reloads 4 and returns d1 = d3 (repeated press); callers GameSetUp_2, PauseMode, waitxsr

**Callers.** GameSetUp_2, PauseMode, waitxsr
**Callees.** nodiag

```
011318  bsr.s	sub_112F0
01131A  tst.w	d3
01131C  beq.w	locret_15464
011320  tst.w	d2
011322  bne.w	loc_11338
011326  subq.w	#1,($FFFFB042).w
01132A  bpl.w	locret_15464
01132E  move.w	#4,($FFFFB042).w
011334  move.w	d3,d1
011336  rts
011338  move.w	#$F,($FFFFB042).w
01133E  rts
```

## `$01826C` -> `ai_RandomMod`  (confidence 0.7, 12 insns)

**Evidence.** 5-word seed at (a3): divides each word by d0 carrying the remainder through, returns the final remainder in d0 (0..d0-1) and leaves the quotients as the new seed; only called by sub_1803E with moduli 5, 8, $10, $20, $4000

**Callers.** ai_RandomizeDemoSetup
**Callees.** none

```
01826C  movem.l	d1-d2/a0,-(sp)
018270  move.w	a3,a0
018272  moveq	#4,d1
018274  clr.l	d2
018276  move.w	(a0),d2
018278  divu.w	d0,d2
01827A  move.w	d2,(a0)+
01827C  dbf	d1,loc_18276
018280  swap	d2
018282  move.w	d2,d0
018284  movem.l	(sp)+,d1-d2/a0
018288  rts
```

## `$01803E` -> `ai_RandomizeDemoSetup`  (confidence 0.6, 51 insns)

**Evidence.** saves the 5-word seed at (a3), draws random values with RandomMod into the eight $10-byte option blocks below $CED6 (fields +4/+6, flag bit 2 when the draw is 4), then $CEF2, pojoy (forced to 4 unless FourWayPlay when it lands on 1 or 2), potreeteam, gamelevel, bosgames, postarts, and restores the seed; callers GameSetUp, sub_17CA0, sub_180FC

**Callers.** GameSetUp, sub_17CA0, sub_180FC
**Callees.** ai_RandomMod
**RAM.** FourWayPlay, bosgames, gamelevel, pojoy, postarts, potreeteam

```
01803E  moveq	#4,d0
018040  lea	$A(a3),a0
018044  move.w	-(a0),-(sp)
018046  dbf	d0,loc_18044
01804A  moveq	#7,d2
01804C  move.w	#$CED6,a1
018050  bclr	#2,$E(a1)
018056  moveq	#5,d0
018058  bsr.w	sub_1826C
01805C  move.w	d0,6(a1)
018060  cmpnw	 4,d0
018064  bne.w	loc_1806E
018068  bset	#2,$E(a1)
01806E  moveq	#5,d0
018070  bsr.w	sub_1826C
018074  move.w	d0,4(a1)
018078  cmpnw	 4,d0
01807C  bne.w	loc_18086
018080  bset	#2,$E(a1)
018086  suba.w	#$10,a1
01808A  dbf	d2,loc_18050
01808E  move.w	#$4000,d0
018092  bsr.w	sub_1826C
018096  move.w	d0,($FFFFCEF2).w
01809A  move.w	#8,d0
01809E  bsr.w	sub_1826C
0180A2  move.w	d0,($FFFFCEF0).w
0180A6  tst.w	($FFFFD046).w
0180AA  bne.w	loc_180C8
0180AE  cmp.w	#1,($FFFFCEF0).w
0180B4  beq.w	loc_180C2
0180B8  cmp.w	#2,($FFFFCEF0).w
0180BE  bne.w	loc_180C8
0180C2  move.w	#4,($FFFFCEF0).w
0180C8  moveq	#$10,d0
0180CA  bsr.w	sub_1826C
0180CE  move.w	d0,($FFFFCEEE).w
0180D2  moveq	#4,d0
0180D4  bsr.w	sub_1826C
0180D8  move.w	d0,($FFFFCEEC).w
0180DC  moveq	#8,d0
0180DE  bsr.w	sub_1826C
0180E2  move.w	d0,($FFFFCEEA).w
0180E6  moveq	#$20,d0
0180E8  bsr.w	sub_1826C
0180EC  move.w	d0,($FFFFCEE8).w
0180F0  moveq	#4,d0
0180F2  lea	(a3),a0
0180F4  move.w	(sp)+,(a0)+
0180F6  dbf	d0,loc_180F4
0180FA  rts
```

## `$01A304` -> `ai_StopSound30`  (confidence 0.6, 30 insns)

**Evidence.** with interrupts masked, searches the 8-slot active-sound table $D3D4 (6 bytes each) for the sound-table pointer stored at off_2C708, which is entry $30 of the sound list off_2C648; if found, marks the slot -1, clears $D182/$D186, releases the six $D3A4 channels owned by that slot via sub_1A64C, resets their volume bytes at $D187 to $7F and calls Z80_WriteVolume. p_initfx calls it before starting any sound >= $30; other callers DoGameFrame, Stop4Pen, checkgoal, clockcont

**Callers.** DoGameFrame, Stop4Pen, checkgoal, clockcont, p_initfx
**Callees.** Z80_WriteVolume, ai_ReleaseSoundChannel

```
01A304  movem.l	d0-d3/a0-a3,-(sp)
01A308  move	sr,-(sp)
01A30A  move	#$2700,sr
01A30E  lea	($FFFFD3D4).w,a1
01A312  moveq	#7,d3
01A314  move.l	(off_2C708).l,a0
01A31A  cmp.l	(a1),a0
01A31C  addq.w	#6,a1
01A31E  dble	d3,loc_1A31A
01A322  bgt.w	loc_1A368
01A326  clr.l	($FFFFD182).w
01A32A  clr.b	($FFFFD186).w
01A32E  move.l	#$FFFFFFFF,-6(a1)
01A336  moveq	#5,d1
01A338  lea	($FFFFD3A4).w,a2
01A33C  move.b	(a2),d2
01A33E  and.w	#7,d2
01A342  cmp.w	d2,d3
01A344  bne.w	loc_1A35E
01A348  bsr.w	sub_1A64C
01A34C  move.b	4(a2),d0
01A350  lea	($FFFFD187).w,a1
01A354  move.b	#$7F,(a1,d0.w)
01A35A  bset	d0,($FFFFD184).w
01A35E  addq.w	#8,a2
01A360  dbf	d1,loc_1A33C
01A364  bsr.w	Z80_WriteVolume
01A368  move	(sp)+,sr
01A36A  movem.l	(sp)+,d0-d3/a0-a3
01A36E  rts
```

## `$01A64C` -> `ai_ReleaseSoundChannel`  (confidence 0.5, 8 insns)

**Evidence.** a2 = 8-byte channel record in $D3A4: clears the active bit 0 of +6; if it was set and the note/type byte +3 is below $60, sets the channel's bit (+4) in the pending-update mask $D182 and flags $D180, otherwise jumps to Z80_ClearFlagUnknown; only called from StopSound30

**Callers.** ai_StopSound30
**Callees.** none

```
01A64C  bclr	#0,6(a2)
01A652  beq.w	locret_1A292
01A656  cmp.b	#$60,3(a2)
01A65C  bge.w	Z80_ClearFlagUnknown
01A660  move.b	4(a2),d0
01A664  bset	d0,($FFFFD182).w
01A668  st	($FFFFD180).w
01A66C  rts
```

## `$008078` -> `ai_DrawTeamBannerTiles`  (confidence 0.6, 17 insns)

**Evidence.** copies a 2-row x 11-tile name-table block from the buffer at $C334+d0 to (printx,printy) via xyVmMap, with $BF78 bit 2 held during the copy and printx advanced by 11; the buffer is filled at $16D20 from asset off_ABA14 for the home team ($C330) at offset 0 and the away team ($C332) at offset $2C, and every caller passes d0 = 0 or $2C

**Callers.** loc_945C, loc_FC986, sub_12D30
**Callees.** xyVmMap
**RAM.** disflags, printx, printy

```
008078  movem.l	d0-d2/a0-a1,-(sp)
00807C  move.w	($FFFFBF78).w,-(sp)
008080  bset	#2,($FFFFBF78).w
008086  move.w	#$C334,a1
00808A  add.w	d0,a1
00808C  moveq	#1,d2
00808E  jsr	sub_11952
008094  move.w	#$A,d1
008098  move.w	(a1)+,(a0)
00809A  dbf	d1,loc_8098
00809E  addq.w	#1,($FFFFB02A).w
0080A2  dbf	d2,loc_808E
0080A6  add.w	#$B,($FFFFB028).w
0080AC  subq.w	#2,($FFFFB02A).w
0080B0  move.w	(sp)+,($FFFFBF78).w
0080B4  movem.l	(sp)+,d0-d2/a0-a1
0080B8  rts
```

## `$009744` -> `ai_PrintPlayerStatRow`  (confidence 0.6, 81 insns)

**Evidence.** edit-lines/roster screen row: a4 = Satt+d3 (player slot), sets printy from d3, erases the 40-column row, returns if the slot byte is negative, prints the jersey/slot number and the player name (sub_18B26), then either the five attribute values (loc_9872 per attribute, the DispAttribCtr-selected one in palette $C000) or, when DispAttribCtr is negative, two stat counters (sub_988E) and their percentage with a '%' suffix; callers sub_9604, sub_960E, loc_961A

**Callers.** loc_961A, sub_9604, sub_960E
**Callees.** DeterStrLength?, eraser, loc_9872, locret_9870, print, printz, sub_18B26, sub_988E
**RAM.** DispAttribCtr, printa, printx, printy

```
009744  move.w	#$C018,a4
009748  add.w	d3,a4
00974A  jsr	sub_11B92
009750  dc.w	6
009752  dc.b	$BE
009753  dc.b	0
009754  dc.b	0
009755  dc.b	0
009756  add.w	d3,d3
009758  and.w	#$1F,d3
00975C  move.w	d3,($FFFFB02A).w
009760  moveq	#$28,d0
009762  moveq	#1,d1
009764  move.w	#$7FF,d2
009768  jsr	sub_1197E
00976E  tst.b	(a4)
009770  bmi.w	locret_A9D4
009774  subq.w	#1,($FFFFB02A).w
009778  move.w	#1,($FFFFB028).w
00977E  move.w	a4,d0
009780  sub.w	#$C017,d0
009784  moveq	#2,d1
009786  move.w	#$E000,($FFFFB02C).w
00978C  jsr	sub_11D3A
009792  jsr	sub_11BA4
009798  clr.w	d0
00979A  move.b	(a4),d0
00979C  jsr	sub_18B26
0097A2  addq.w	#1,($FFFFB028).w
0097A6  move.w	#$8000,($FFFFB02C).w
0097AC  jsr	sub_11BA4
0097B2  move.w	#$11,($FFFFB028).w
0097B8  tst.w	($FFFFD5AC).w
0097BC  bmi.w	loc_97FC
0097C0  clr.w	d5
0097C2  clr.w	d0
0097C4  move.b	(a4),d0
0097C6  move.w	d5,d1
0097C8  bsr.w	loc_9872
0097CC  move.w	d2,d0
0097CE  moveq	#4,d1
0097D0  jsr	sub_11D3A
0097D6  move.w	#$8000,($FFFFB02C).w
0097DC  cmp.w	($FFFFD5AC).w,d5
0097E0  bne.w	loc_97EA
0097E4  move.w	#$C000,($FFFFB02C).w
0097EA  jsr	sub_11BA4
0097F0  addq.w	#1,d5
0097F2  cmpnw	 5,d5
0097F6  bne.s	loc_97C2
0097F8  bra.w	locret_9870
0097FC  clr.w	d0
0097FE  move.b	(a4),d0
009800  moveq	#3,d1
009802  bsr.w	sub_988E
009806  clr.w	d0
009808  move.b	(a4),d0
00980A  moveq	#0,d1
00980C  move.w	d2,-(sp)
00980E  bsr.w	sub_988E
...
```

## `$009F40` -> `ai_CountRatingNibbles`  (confidence 0.5, 10 insns)

**Evidence.** a2 = player record, $1E(a2) = pointer to the player's data block; adds the word at +$A, takes the word there and counts how many left shifts by 4 it survives before becoming zero (1..4), returned in d0; used by loc_9872 (attribute lookup for PrintPlayerStatRow) as an upper bound and by sub_9F5C which adds it to a nibble of the next field

**Callers.** loc_8BA6, loc_961A, loc_9872, sub_1867E, sub_9F5C, sub_F9FC0
**Callees.** none

```
009F40  movem.l	d1/a0,-(sp)
009F44  move.l	$1E(a2),a0
009F48  add.w	$A(a0),a0
009F4C  move.w	(a0),d1
009F4E  clr.w	d0
009F50  addq.w	#1,d0
009F52  asl.w	#4,d1
009F54  bne.s	loc_9F50
009F56  movem.l	(sp)+,d1/a0
009F5A  rts
```

## `$00C656` -> `ai_SetPlayerBE78Bits`  (confidence 0.4, 12 insns)

**Evidence.** writes the 2-bit value $52(a3) of player object a3 into the packed word $BE78 at bit position 2*(d4+2) (d4 = player index, -2 for the goalie slot); $52(a3) is set to $F by asspenalty and compared against $F and $C in the puck-handling code, so it is a per-player state code; callers asspenalty, doinput, updateplayers

**Callers.** asspenalty, doinput, updateplayers
**Callees.** none

```
00C656  movem.l	d0-d1,-(sp)
00C65A  moveq	#2,d0
00C65C  add.w	d4,d0
00C65E  add.w	d0,d0
00C660  move.w	#$FFF0,d1
00C664  rol.w	d0,d1
00C666  and.w	d1,($FFFFBE78).w
00C66A  move.w	$52(a3),d1
00C66E  asl.w	d0,d1
00C670  or.w	d1,($FFFFBE78).w
00C674  movem.l	(sp)+,d0-d1
00C678  rts
```

## `$0FA014` -> `ai_BuildUserNameString`  (confidence 0.6, 29 insns)

**Evidence.** when d2 != 0 copies the 12-byte user-name entry $D45A + d2*12 into the string at a1 (length word $E, zero bytes shown as spaces) and, if $C2F8 bit 7 is set, trims trailing spaces with sub_FAF66; when d2 == 0 copies the empty default string word_FA07C instead; callers are the user-records screens sub_F9AE4, sub_F9B2A, sub_FA75C, sub_FC136

**Callers.** sub_F9AE4, sub_F9B2A, sub_FA75C, sub_FC136
**Callees.** ai_CopyLenString, ai_TrimTrailingSpaces, loc_FA076

```
0FA014  movem.l	d0-d3/a0-a3,-(sp)
0FA018  move.l	a1,a2
0FA01A  tst.w	d2
0FA01C  beq.w	loc_FA060
0FA020  move.w	#$B,d0
0FA024  clr.w	d3
0FA026  move.l	#$FFFFD45A,a0
0FA02C  mulu.w	#$C,d2
0FA030  add.l	d2,a0
0FA032  move.b	(a0,d3.w),d1
0FA036  bne.w	loc_FA03E
0FA03A  move.b	#$20,d1
0FA03E  move.b	d1,2(a1)
0FA042  tst.b	(a1)+
0FA044  addq.w	#1,d3
0FA046  dbf	d0,loc_FA032
0FA04A  move.w	#$E,(a2)
0FA04E  btst	#7,($FFFFC2F8).w
0FA054  beq.w	loc_FA05C
0FA058  bsr.w	sub_FAF66
0FA05C  bra.w	loc_FA076
0FA060  move.l	a1,a3
0FA062  move.l	a3,-(sp)
0FA064  move.l	#word_FA07C,a1
0FA06A  jsr	sub_F997A
0FA070  move.l	(sp)+,a2
0FA072  bsr.w	sub_FAF66
0FA076  movem.l	(sp)+,d0-d3/a0-a3
0FA07A  rts
```

## `$0FAF66` -> `ai_TrimTrailingSpaces`  (confidence 0.8, 13 insns)

**Evidence.** walks back from the end of the length-prefixed string at a2, replacing trailing $20 bytes with 0 and decrementing the length word, then rounds the length up to even; only called from BuildUserNameString

**Callers.** ai_BuildUserNameString
**Callees.** loc_FAF6E

```
0FAF66  movem.l	a3,-(sp)
0FAF6A  move.l	a2,a3
0FAF6C  add.w	(a2),a3
0FAF6E  move.b	-(a3),d0
0FAF70  cmpnb	 $20,d0
0FAF74  bne.w	loc_FAF80
0FAF78  move.b	#0,(a3)
0FAF7C  subq.w	#1,(a2)
0FAF7E  bra.s	loc_FAF6E
0FAF80  addq.w	#1,(a2)
0FAF82  and.w	#$FE,(a2)
0FAF86  movem.l	(sp)+,a3
0FAF8A  rts
```

## `$0FE98A` -> `ai_Unpack3BitRatings`  (confidence 0.5, 58 insns)

**Evidence.** reads a count word from (a2) into $DA1E, then for count*8 records takes 3 packed bytes, splits them into eight 3-bit fields and stores each as a nibble equal to field+5 in a longword written after the count at $DA1E; $DEA0 is scratch; callers loc_F8868, loc_FAEBC, sub_FD14A (SRAM/records screens), so this looks like the decoder for compactly stored custom ratings

**Callers.** loc_F8868, loc_FAEBC, sub_FD14A
**Callees.** none

```
0FE98A  movem.l	d0-a6,-(sp)
0FE98E  move.l	#$FFFFDA1E,a0
0FE994  move.l	#$FFFFDEA0,a1
0FE99A  move.w	(a2)+,d0
0FE99C  move.w	d0,(a0)+
0FE99E  asl.w	#3,d0
0FE9A0  subq.w	#1,d0
0FE9A2  clr.l	(a0)
0FE9A4  clr.l	(a1)
0FE9A6  move.b	(a2)+,(a1)
0FE9A8  move.b	(a2)+,1(a1)
0FE9AC  move.b	(a2)+,2(a1)
0FE9B0  move.l	#0,-(sp)
0FE9B6  move.l	(a1),d2
0FE9B8  and.l	#$E0000000,d2
0FE9BE  lsr.l	#1,d2
0FE9C0  add.l	#$50000000,d2
0FE9C6  or.l	d2,(sp)
0FE9C8  move.l	(a1),d2
0FE9CA  and.l	#$1C000000,d2
0FE9D0  lsr.l	#2,d2
0FE9D2  add.l	#$5000000,d2
0FE9D8  or.l	d2,(sp)
0FE9DA  move.l	(a1),d2
0FE9DC  and.l	#$3800000,d2
0FE9E2  lsr.l	#3,d2
0FE9E4  add.l	#$500000,d2
0FE9EA  or.l	d2,(sp)
0FE9EC  move.l	(a1),d2
0FE9EE  and.l	#$700000,d2
0FE9F4  lsr.l	#4,d2
0FE9F6  add.l	#unk_50000,d2
0FE9FC  or.l	d2,(sp)
0FE9FE  move.l	(a1),d2
0FEA00  and.l	#unk_E0000,d2
0FEA06  lsr.l	#5,d2
0FEA08  add.l	#$5000,d2
0FEA0E  or.l	d2,(sp)
0FEA10  move.l	(a1),d2
0FEA12  and.l	#unk_1C000,d2
0FEA18  lsr.l	#6,d2
0FEA1A  add.l	#$500,d2
0FEA20  or.l	d2,(sp)
0FEA22  move.l	(a1),d2
0FEA24  and.l	#$3800,d2
0FEA2A  lsr.l	#7,d2
0FEA2C  add.l	#$50,d2
0FEA32  or.l	d2,(sp)
0FEA34  move.l	(a1),d2
0FEA36  and.l	#$700,d2
0FEA3C  move.w	#8,d5
0FEA40  lsr.l	d5,d2
0FEA42  addq.l	#5,d2
0FEA44  or.l	d2,(sp)
0FEA46  move.l	(sp)+,(a0)+
0FEA48  dbf	d0,loc_FE9A2
0FEA4C  movem.l	(sp)+,d0-a6
0FEA50  rts
```

