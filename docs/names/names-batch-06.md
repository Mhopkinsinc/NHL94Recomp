# Name review: names-batch-06.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0FE660` -> `ai_LoadPlayoffPassword`  (confidence 0.7, 10 insns)

**Evidence.** ReadSRAM of $100 bytes from SRAM offset $1EF6 into $D076 (the buffer whose $D088 part ai_ApplyPlayoffPassword decodes), then the same lastsfx/recbpr resets as ai_SavePlayoffPassword, of which it is the read twin; callers Begin and GameSetUp

**Callers.** Begin, GameSetUp
**Callees.** ReadSRAM
**RAM.** lastsfx, recbpr, sflags

```
0FE660  movem.l	d0-d1/a0,-(sp)
0FE664  move.l	#$100,d1
0FE66A  move.l	#$1EF6,d0
0FE670  move.l	#$FFFFD076,a0
0FE676  jsr	sub_1A244
0FE67C  bclr	#4,($FFFFC2EC).w
0FE682  move.w	#$FFFF,($FFFFC016).w
0FE688  move.l	#$FFFF0000,($FFFFB036).w
0FE690  movem.l	(sp)+,d0-d1/a0
0FE694  rts
```

## `$0F9C68` -> `ai_ReadUserNames`  (confidence 0.7, 12 insns)

**Evidence.** clears $C2F8 bit 6 (the SRAM write flag) and transfers $80 bytes between SRAM offset $DA0 and the user-name table $D45A; because the flag was just cleared the test picks ReadSRAM, the WriteSRAM path exists for a twin that sets the flag and jumps past the bclr (the bset at $F9C5E/$F9C56); callers GameSetUp and loc_FCC76

**Callers.** GameSetUp, loc_FCC76
**Callees.** ReadSRAM, WriteSRAM, loc_F9C9E

```
0F9C68  bclr	#6,($FFFFC2F8).w
0F9C6E  movem.l	d0-a6,-(sp)
0F9C72  move.l	#$80,d1
0F9C78  move.l	#$DA0,d0
0F9C7E  move.l	#$FFFFD45A,a0
0F9C84  btst	#6,($FFFFC2F8).w
0F9C8A  beq.w	loc_F9C98
0F9C8E  jsr	sub_1A1E4
0F9C94  bra.w	loc_F9C9E
0F9C98  jsr	sub_1A244
0F9C9E  movem.l	(sp)+,d0-a6
0F9CA2  rts
```

## `$0FE172` -> `ai_GetTeamOverallRating`  (confidence 0.8, 8 insns)

**Evidence.** returns d0 = byte unk_FE18E[$28(a2)] where +$28 is the team id in the team record; the table starts $33, $4C, $49, $4B, $4E, $43 (51, 76, 73, 75, 78, 67), the overall team ratings printed as a number by sub_FABDC ('Team Rating') and by sub_FCFB8 on the ratings screen

**Callers.** ai_PrintTeamRatingBox, sub_FCFB8
**Callees.** none

```
0FE172  movem.l	d1-a6,-(sp)
0FE176  move.w	$28(a2),d0
0FE17A  move.l	#unk_FE18E,a0
0FE180  clr.w	d1
0FE182  move.b	(a0,d0.w),d1
0FE186  move.w	d1,d0
0FE188  movem.l	(sp)+,d1-a6
0FE18C  rts
```

## `$0FABDC` -> `ai_PrintTeamRatingBox`  (confidence 0.7, 19 insns)

**Evidence.** at (d0,d1) prints 'Team' and 'Rating' then the overall rating of the home or away team (ai_GetRecordsTeam logic on $D4F6) from ai_GetTeamOverallRating as a 2-digit number; caller loc_FA550 (records screen)

**Callers.** loc_FA550
**Callees.** DeterStrLength?, ai_GetTeamOverallRating, print2, printz2
**Strings.** Team | Rating
**RAM.** printx, printy

```
0FABDC  movem.l	d0-a6,-(sp)
0FABE0  move.w	d0,($FFFFB028).w
0FABE4  move.w	d1,($FFFFB02A).w
0FABE8  move.w	d0,-(sp)
0FABEA  jsr	sub_11A36
0FABF0  dc.w	6
0FABF2  aTeam:		dc.b	'Team'
0FABF6  move.w	(sp)+,($FFFFB028).w
0FABFA  addq.w	#1,($FFFFB02A).w
0FABFE  jsr	sub_11A36
0FAC04  dc.w	$A
0FAC06  aRating_1:	dc.b	'Rating  '
0FAC0E  move.l	#$FFFFC6CE,a0
0FAC14  tst.w	($FFFFD4F6).w
0FAC18  beq.w	loc_FAC22
0FAC1C  move.l	#$FFFFCA32,a0
0FAC22  move.l	a0,a2
0FAC24  bsr.w	sub_FE172
0FAC28  move.w	#2,d1
0FAC2C  jsr	sub_11D3A
0FAC32  jsr	sub_11A48
0FAC38  movem.l	(sp)+,d0-a6
0FAC3C  rts
```

## `$0FAF50` -> `ai_GetRecordsTeam`  (confidence 0.7, 5 insns)

**Evidence.** returns a0 = home team record $C6CE, or the away record $CA32 when the records-screen side toggle $D4F6 is non-zero; callers loc_FACF0 and sub_FAD84 (Saves / Save % printer)

**Callers.** loc_FACF0, sub_FAD84
**Callees.** none

```
0FAF50  move.l	#$FFFFC6CE,a0
0FAF56  tst.w	($FFFFD4F6).w
0FAF5A  beq.w	locret_FAF64
0FAF5E  move.l	#$FFFFCA32,a0
0FAF64  rts
```

## `$007E0E` -> `ai_GetControllingTeam`  (confidence 0.6, 9 insns)

**Evidence.** returns a2 = home team record $C6CE when the pausing controller's team selection (cont2team when sflags bit 1, else cont1team) equals 1, otherwise the away record (+$364); callers PauseMode and loc_7E88 (pause menu)

**Callers.** PauseMode, loc_7E88
**Callees.** loc_7E2C
**RAM.** cont1team, cont2team, sflags

```
007E0E  move.w	#$C6CE,a2
007E12  btst	#1,($FFFFC2EC).w
007E18  beq.w	loc_7E26
007E1C  cmp.w	#1,($FFFFC32A).w
007E22  bra.w	loc_7E2C
007E26  cmp.w	#1,($FFFFC328).w
007E2C  beq.w	locret_7E34
007E30  add.w	#$364,a2
007E34  rts
```

## `$0130BE` -> `ai_ResetLineEnergy`  (confidence 0.6, 10 insns)

**Evidence.** a2 = team record: for the 26 player slots sets the energy word at +$32+2i to $1000 (full) unless the status word at +$66+2i is -4, and demotes a -3 status to -2; callers sub_13068 (period/line reset, which then picks line 3 or 5 for $16(a3)) and sub_137FC

**Callers.** sub_13068, sub_137FC
**Callees.** none

```
0130BE  moveq	#$32,d0
0130C0  cmp.w	#$FFFC,$66(a2,d0.w)
0130C6  beq.w	loc_130E0
0130CA  move.w	#$1000,$32(a2,d0.w)
0130D0  cmp.w	#$FFFD,$66(a2,d0.w)
0130D6  bne.w	loc_130E0
0130DA  move.w	#$FFFE,$66(a2,d0.w)
0130E0  subq.w	#2,d0
0130E2  bpl.s	loc_130C0
0130E4  rts
```

## `$0FD46C` -> `ai_SelectRatingsPlayers`  (confidence 0.6, 9 insns)

**Evidence.** for the home and away records calls ai_GetLineupPlayerForPosition and stores the resulting player indexes in $D59C/$D59E, which ai_DrawRatingsPictures and ai_PrintTeamRatingsScreen use for the per-position comparison; callers loc_FCC76 and sub_FCF86

**Callers.** loc_FCC76, sub_FCF86
**Callees.** ai_GetLineupPlayerForPosition

```
0FD46C  movem.l	d0/a0-a1,-(sp)
0FD470  move.l	#$FFFFC6CE,a0
0FD476  bsr.w	sub_FD492
0FD47A  move.w	d0,($FFFFD59C).w
0FD47E  move.l	#$FFFFCA32,a0
0FD484  bsr.w	sub_FD492
0FD488  move.w	d0,($FFFFD59E).w
0FD48C  movem.l	(sp)+,d0/a0-a1
0FD490  rts
```

## `$0FD492` -> `ai_GetLineupPlayerForPosition`  (confidence 0.6, 11 insns)

**Evidence.** a0 = team record: maps the ratings-screen position $D598 through byte_FD4B8 to a lineup slot (kept in $D5AA), reads that slot from the six-player list at team data offset +6 and returns the player index minus 1; only caller ai_SelectRatingsPlayers

**Callers.** ai_SelectRatingsPlayers
**Callees.** none

```
0FD492  move.l	$1E(a0),a0
0FD496  add.w	6(a0),a0
0FD49A  move.w	($FFFFD598).w,d0
0FD49E  move.l	#byte_FD4B8,a1
0FD4A4  move.b	(a1,d0.w),d0
0FD4A8  ext.w	d0
0FD4AA  move.w	d0,($FFFFD5AA).w
0FD4AE  move.b	(a0,d0.w),d0
0FD4B2  ext.w	d0
0FD4B4  subq.w	#1,d0
0FD4B6  rts
```

## `$0FCFDC` -> `ai_PrintRatingsSpacer`  (confidence 0.6, 7 insns)

**Evidence.** prints the 4-byte control string word_FCFF6 with print2 while preserving printx and a1; callers ai_PrintTeamRatingsScreen and sub_FCFB8

**Callers.** ai_PrintTeamRatingsScreen, sub_FCFB8
**Callees.** print2
**Strings.** Shooting | Skating | Passing | Defense | Checking | Fighting
**RAM.** printx

```
0FCFDC  move.l	a1,-(sp)
0FCFDE  move.w	($FFFFB028).w,-(sp)
0FCFE2  move.l	#word_FCFF6,a1
0FCFE8  jsr	sub_11A48
0FCFEE  move.w	(sp)+,($FFFFB028).w
0FCFF2  move.l	(sp)+,a1
0FCFF4  rts
```

## `$009872` -> `ai_GetPlayerAttributeChecked`  (confidence 0.5, 7 insns)

**Evidence.** d0 = player, d1 = attribute column: returns d2 = 0 when the column is not below ai_CountRatingNibbles for the team, otherwise tail-calls sub_988E to fetch the value; callers ai_PrintPlayerStatRow and loc_961A

**Callers.** ai_PrintPlayerStatRow, loc_961A
**Callees.** ai_CountRatingNibbles

```
009872  move.w	d0,-(sp)
009874  bsr.w	sub_9F40
009878  move.w	d0,d2
00987A  move.w	(sp)+,d0
00987C  cmp.w	d2,d0
00987E  bge.w	sub_988E
009882  clr.w	d2
009884  dc.b	3
009885  dc.b	$3C
009886  dc.b	0
009887  dc.b	6
009888  dc.b	$67
009889  dc.b	0
00988A  dc.b	$11
00988B  dc.b	$4A
00988C  dc.b	$72
00988D  dc.b	1
```

## `$012D70` -> `ai_DrawHudPanel`  (confidence 0.5, 13 insns)

**Evidence.** unless sflags2 bit 5 is set, positions at column 1 row $19 (inline attribute string) and draws the second bitmap of asset unk_B3530 with dobitmap at tile base $B020 (the rink tile base), a2 = the team table $30A; callers PrintScores1 and updatepwrplay, i.e. the in-game scoreboard panel

**Callers.** PrintScores1, updatepwrplay
**Callees.** dobitmap, printz
**RAM.** sflags2

```
012D70  btst	#5,($FFFFC2EE).w
012D76  bne.w	locret_15464
012D7A  bsr.w	sub_11B92
012D7E  dc.w	6
012D80  dc.b	$BF
012D81  dc.b	1
012D82  dc.b	$19
012D83  dc.b	0
012D84  move.l	#unk_B3530,a1
012D8A  add.l	4(a1),a1
012D8E  move.w	#$30A,a2
012D92  clr.w	d0
012D94  clr.w	d1
012D96  move.w	(a1),d2
012D98  move.w	2(a1),d3
012D9C  move.w	($FFFFB020).w,d4
012DA0  clr.w	d5
012DA2  bra.w	sub_1169A
```

## `$0134E4` -> `ai_TickerAreaSetup`  (confidence 0.5, 7 insns)

**Evidence.** sets the print position for the intermission ticker (column 3 row $17, a second attribute string unless sflags bit 0) and returns the erase size d0 = $1A, d1 = 5 that its callers pass to eraser; callers NewTicker3pt2 and sub_134D8 (Intermission)

**Callers.** NewTicker3pt2, sub_134D8
**Callees.** printz
**RAM.** sflags

```
0134E4  bsr.w	sub_11B92
0134E8  dc.w	6
0134EA  dc.b	$BD
0134EB  dc.b	3
0134EC  dc.b	$17
0134ED  dc.b	0
0134EE  btst	#0,($FFFFC2EC).w
0134F4  bne.w	loc_13502
0134F8  bsr.w	sub_11B92
0134FC  dc.w	6
0134FE  dc.b	$BF
0134FF  dc.b	3
013500  dc.b	$17
013501  dc.b	0
013502  moveq	#$1A,d0
013504  moveq	#5,d1
013506  rts
```

## `$007E72` -> `ai_SetPauseMenuColumn`  (confidence 0.5, 5 insns)

**Evidence.** sets printx = 5, or 9 when disflags bit 1 (rink screen) is set; callers ai_PrintScrollingMenu and loc_7E46 (pause menu refresh)

**Callers.** ai_PrintScrollingMenu, loc_7E46
**Callees.** none
**RAM.** disflags, printx

```
007E72  move.w	#5,($FFFFB028).w
007E78  btst	#1,($FFFFBF78).w
007E7E  bne.w	locret_A9D4
007E82  addq.w	#4,($FFFFB028).w
007E86  rts
```

