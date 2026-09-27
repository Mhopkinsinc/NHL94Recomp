# Name review: names-batch-19.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$01A3B2` -> `ai_ReadFourWayPad1`  (confidence 0.7, 8 insns)

**Evidence.** EA 4-Way Play read of pad 1: requests the Z80 bus (reset retry via Z80_ResetAndRequestBus), writes the select value $0C to port 2 ($A10005) and joins the shared pad reader at loc_1A456 (ai_ReadPad1Hardware's body reading port 1); caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** ai_Z80_ResetAndRequestBus, loc_1A456
**Hardware.** Z80 busreq, pad2

```
01A3B2  move.w	#$100,($A11100).l
01A3BA  move.w	#$64,d0
01A3BE  btst	#0,($A11100).l
01A3C6  beq.s	loc_1A3D0
01A3C8  dbf	d0,loc_1A3BE
01A3CC  bsr.w	sub_1A4EE
01A3D0  move.b	#$C,($A10005).l
01A3D8  bra.w	loc_1A456
```

## `$01A3DC` -> `ai_ReadFourWayPad2`  (confidence 0.7, 8 insns)

**Evidence.** EA 4-Way Play read of pad 2: same as ai_ReadFourWayPad1 with select value $1C; caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** ai_Z80_ResetAndRequestBus, loc_1A456
**Hardware.** Z80 busreq, pad2

```
01A3DC  move.w	#$100,($A11100).l
01A3E4  move.w	#$64,d0
01A3E8  btst	#0,($A11100).l
01A3F0  beq.s	loc_1A3FA
01A3F2  dbf	d0,loc_1A3E8
01A3F6  bsr.w	sub_1A4EE
01A3FA  move.b	#$1C,($A10005).l
01A402  bra.w	loc_1A456
```

## `$01A406` -> `ai_ReadFourWayPad3`  (confidence 0.7, 8 insns)

**Evidence.** EA 4-Way Play read of pad 3: same as ai_ReadFourWayPad1 with select value $2C; caller ReadJoyData

**Callers.** ReadJoyData
**Callees.** ai_Z80_ResetAndRequestBus, loc_1A456
**Hardware.** Z80 busreq, pad2

```
01A406  move.w	#$100,($A11100).l
01A40E  move.w	#$64,d0
01A412  btst	#0,($A11100).l
01A41A  beq.s	loc_1A424
01A41C  dbf	d0,loc_1A412
01A420  bsr.w	sub_1A4EE
01A424  move.b	#$2C,($A10005).l
01A42C  bra.w	loc_1A456
```

## `$0FD5F4` -> `ai_GetTeamNameString3`  (confidence 0.4, 9 insns)

**Evidence.** ticker helper: returns a1 = the third length-prefixed string of team a2's name block (data +$1E, block offset +4, skipping two strings); the first string is the full name used elsewhere, so this is one of the short forms; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none

```
0FD5F4  movem.l	d0/a0/a2,-(sp)
0FD5F8  move.l	a2,a1
0FD5FA  move.l	$1E(a1),a1
0FD5FE  add.w	4(a1),a1
0FD602  add.w	(a1),a1
0FD604  add.w	(a1),a1
0FD606  add.w	(a1),a1
0FD608  movem.l	(sp)+,d0/a0/a2
0FD60C  rts
```

## `$008B84` -> `ai_ShowEditLinesPage`  (confidence 0.6, 6 insns)

**Evidence.** sets the edit-lines page $D5B2 from the high word of d0 and draws it with ai_DrawEditLinesHeader; caller sub_8B1C

**Callers.** sub_8B1C
**Callees.** ai_DrawEditLinesHeader

```
008B84  move.l	d0,-(sp)
008B86  swap	d0
008B88  move.w	d0,($FFFFD5B2).w
008B8C  bsr.w	loc_8BA6
008B90  move.l	(sp)+,d0
008B92  rts
```

## `$008B94` -> `ai_ShowEditLinesPageNext`  (confidence 0.6, 7 insns)

**Evidence.** sets the edit-lines page $D5B2 to the high word of d0 plus one and draws it with ai_DrawEditLinesHeader; caller sub_8B1C

**Callers.** sub_8B1C
**Callees.** ai_DrawEditLinesHeader

```
008B94  move.l	d0,-(sp)
008B96  swap	d0
008B98  addq.w	#1,d0
008B9A  move.w	d0,($FFFFD5B2).w
008B9E  bsr.w	loc_8BA6
008BA2  move.l	(sp)+,d0
008BA4  rts
```

## `$013848` -> `ai_SnapshotGameState`  (confidence 0.6, 7 insns)

**Evidence.** copies $5BE words of game state from $C2EA into the unused low RAM at $FF0000 followed by ScoreSumbytes, so the state can be restored after the highlight replay; caller ai_PlayHighlightFromGame

**Callers.** ai_PlayHighlightFromGame
**Callees.** none
**RAM.** ScoreSumbytes

```
013848  move.w	#$5BD,d0
01384C  move.w	#$C2EA,a1
013850  move.l	#$FFFF0000,a2
013856  move.w	(a1)+,(a2)+
013858  dbf	d0,loc_13856
01385C  move.w	($FFFFC472).w,(a2)+
013860  rts
```

## `$014A94` -> `ai_ElapsedGameTime`  (confidence 0.6, 7 insns)

**Evidence.** returns d0 = (period gsp << 14 | PerTimeTotal) - gameclock, the elapsed time code stored with goals; caller checkgoal

**Callers.** checkgoal
**Callees.** none
**RAM.** PerTimeTotal, gameclock, gsp

```
014A94  move.w	($FFFFC466).w,d0
014A98  swap	d0
014A9A  clr.w	d0
014A9C  lsr.l	#2,d0
014A9E  or.w	($FFFFC46C).w,d0
014AA2  sub.w	($FFFFC468).w,d0
014AA6  rts
```

## `$015EA4` -> `ai_WritePlaneScroll`  (confidence 0.7, 7 insns)

**Evidence.** writes Hscroll ($BD1E) to the horizontal scroll table (VSCRLPM + 2) and Vscroll ($BD20) to VSRAM entry 1 (command $40020010); caller sub_15E6E (the attract-mode V-blank routine)

**Callers.** sub_15E6E
**Callees.** Vmaddr
**RAM.** Hscroll, VSCRLPM, Vscroll

```
015EA4  move.w	($FFFFB000).w,d0
015EA8  addq.w	#2,d0
015EAA  bsr.w	VDP_SetAddress
015EAE  move.w	($FFFFBD1E).w,(a0)
015EB2  move.l	#$40020010,4(a0)
015EBA  move.w	($FFFFBD20).w,(a0)
015EBE  rts
```

## `$0FAC78` -> `ai_PrintCentredAtColumn20`  (confidence 0.6, 7 insns)

**Evidence.** prints the length-prefixed string a0 centred on column $14 (printx = $14 - (length - 2) / 2); caller ai_PrintRecordsTeamName

**Callers.** ai_PrintRecordsTeamName
**Callees.** print2
**RAM.** printx

```
0FAC78  move.w	#$14,($FFFFB028).w
0FAC7E  move.w	(a0),d0
0FAC80  subq.w	#2,d0
0FAC82  lsr.w	#1,d0
0FAC84  sub.w	d0,($FFFFB028).w
0FAC88  move.l	a0,a1
0FAC8A  jmp	sub_11A48
```

## `$009112` -> `ai_PrintSummaryPlayerName`  (confidence 0.7, 6 insns)

**Evidence.** scoring/penalty summary: when the player index d0 is not negative prints 'I. Surname' (ai_FormatPlayerInitialSurname) and moves to the next row; caller ai_PrintScoringSummaryRow (three times per row)

**Callers.** ai_PrintScoringSummaryRow
**Callees.** ai_FormatPlayerInitialSurname, print
**Strings.** SH2 | PP2 | Penalty  Summary | ^Per^^Time^^Tm^^Player/Penalty^^^^min^^^ù
**RAM.** printy

```
009112  ext.w	d0
009114  bmi.w	loc_9124
009118  jsr	sub_18AE8
00911E  jsr	sub_11BA4
009124  addq.w	#1,($FFFFB02A).w
009128  rts
```

## `$0098CE` -> `ai_SumPlayoffStatColumn`  (confidence 0.5, 6 insns)

**Evidence.** playoff stats: looks up column d1 in the pointer table at $98E6 and, when set, adds the entry for player d0 to d2; caller ai_GetPlayerStatValue

**Callers.** ai_GetPlayerStatValue
**Callees.** none
**Strings.** Saves Shots Save % | G | A | Pts | SOG | PIM

```
0098CE  move.l	#$98E6,a1
0098D4  tst.w	(a1,d1.w)
0098D8  beq.w	locret_A9D4
0098DC  move.w	(a1,d1.w),a1
0098E0  add.w	(a1,d0.w),d2
0098E4  rts
```

## `$017718` -> `ai_ResetTickerState`  (confidence 0.7, 6 insns)

**Evidence.** resets the ticker: row counter $D5AE = -1, PlayerScrollCtr = -1, line index $D5B2 and delay $D5B4 = 0, returns a0 = the line offset table $D5B8; caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** none
**RAM.** PlayerScrollCtr, VertLineScrolling

```
017718  move.w	#$FFFF,($FFFFD5AE).w
01771E  st	($FFFFD5B0).w
017722  clr.w	($FFFFD5B2).w
017726  clr.w	($FFFFD5B4).w
01772A  move.w	#$D5B8,a0
01772E  rts
```

## `$0077E4` -> `ai_ClearPlayoffStatsBlock`  (confidence 0.6, 5 insns)

**Evidence.** StartGame: zeroes the $E4-word packed playoff stats block at $D092 (the one ai_UnpackPlayoffStats reads); caller StartGame

**Callers.** StartGame
**Callees.** none

```
0077E4  move.w	#$E3,d0
0077E8  move.w	#$D092,a0
0077EC  clr.w	(a0)+
0077EE  dbf	d0,loc_77EC
0077F2  rts
```

