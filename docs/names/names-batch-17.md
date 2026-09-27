# Name review: names-batch-17.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$008250` -> `ai_PrintTeamNameAndNumber`  (confidence 0.6, 11 insns)

**Evidence.** prints team d0's name (team table $30E, name at +4) at column 6 and the 2-digit value d1 at column $18 on the same row; caller sub_81F2 (edit-lines team header)

**Callers.** ai_PrintSeriesMatchup
**Callees.** NumberToPaddedText, print
**RAM.** printx

```
008250  move.w	#$30E,a1
008254  asl.w	#2,d0
008256  move.l	(a1,d0.w),a1
00825A  add.w	4(a1),a1
00825E  move.w	#6,($FFFFB028).w
008264  jsr	sub_11BA4
00826A  move.w	#$18,($FFFFB028).w
008270  move.w	d1,d0
008272  moveq	#2,d1
008274  jsr	sub_11D3A
00827A  jmp	sub_11BA4
```

## `$012DA6` -> `ai_PrintPenaltyBoxes`  (confidence 0.7, 11 insns)

**Evidence.** SetHor: sets $BF78 bit 3, refreshes the scoreboard (PrintScores1) and prints the home penalty list at column $14 row 8 and the away list at column 5 row 8 with ai_PrintPenaltyList; caller SetHor

**Callers.** SetHor
**Callees.** PrintScores1, ai_PrintPenaltyList, printz
**RAM.** disflags

```
012DA6  movem.l	d0-a3,-(sp)
012DAA  bset	#3,($FFFFBF78).w
012DB0  bsr.w	loc_12C04
012DB4  bsr.w	sub_11B92
012DB8  dc.w	6
012DBA  dc.b	$BE
012DBB  dc.b	$14
012DBC  dc.b	8
012DBD  dc.b	0
012DBE  move.w	#$C6CE,a2
012DC2  bsr.w	sub_12DDE
012DC6  bsr.w	sub_11B92
012DCA  dc.w	6
012DCC  dc.b	$BE
012DCD  dc.b	5
012DCE  dc.b	8
012DCF  dc.b	0
012DD0  move.w	#$CA32,a2
012DD4  bsr.w	sub_12DDE
012DD8  movem.l	(sp)+,d0-a3
012DDC  rts
```

## `$017190` -> `ai_InitBothTeamRecords`  (confidence 0.7, 11 insns)

**Evidence.** initialises the home record ($C6CE, objects from $B04A) for HomeTeam and the away record ($CA32, objects from $B34A) for VisTeam through ai_InitTeamRecord; caller ai_RefreshSetupTeamLogos

**Callers.** ai_RefreshSetupTeamLogos
**Callees.** ai_InitTeamRecord
**RAM.** HomeTeam, VisTeam

```
017190  movem.l	d0/a0-a2,-(sp)
017194  move.w	#$C6CE,a2
017198  move.w	($FFFFC330).w,d0
01719C  move.w	#$B04A,$22(a2)
0171A2  bsr.w	sub_171BE
0171A6  move.w	#$CA32,a2
0171AA  move.w	($FFFFC332).w,d0
0171AE  move.w	#$B34A,$22(a2)
0171B4  bsr.w	sub_171BE
0171B8  movem.l	(sp)+,d0/a0-a2
0171BC  rts
```

## `$017B78` -> `ai_DrawSetupLogoBitmap`  (confidence 0.6, 11 insns)

**Evidence.** draws logo d1 of the asset off_AFE12 (row = 2*d1 in its second block) as a 2-row bitmap at column 0 with dobitmap, tile base d4; caller ai_RefreshSetupTeamLogos (once per team)

**Callers.** ai_RefreshSetupTeamLogos
**Callees.** dobitmap

```
017B78  clr.w	d0
017B7A  asl.w	#1,d1
017B7C  move.l	#off_AFE12,a0
017B82  move.l	a0,a1
017B84  add.l	(a0),a0
017B86  add.l	4(a1),a1
017B8A  move.w	#$30A,a2
017B8E  move.w	(a1),d2
017B90  moveq	#2,d3
017B92  moveq	#0,d5
017B94  bra.w	sub_1169A
```

## `$018CDC` -> `ai_LongToHexText`  (confidence 0.8, 11 insns)

**Evidence.** writes the 8 hexadecimal digits of d0 (most significant first, 'A'..'F' via the +7 adjustment) to a0; caller DivBy0, the exception screen that prints register values

**Callers.** DivBy0
**Callees.** none
**Strings.** Period Over | Game Over | Icing | Off-side | Face Off | Face Off

```
018CDC  moveq	#7,d2
018CDE  rol.l	#4,d0
018CE0  move.w	d0,d1
018CE2  and.w	#$F,d1
018CE6  add.w	#$30,d1
018CEA  cmpnw	 $39,d1
018CEE  ble.w	loc_18CF4
018CF2  addq.w	#7,d1
018CF4  move.b	d1,(a0)+
018CF6  dbf	d2,loc_18CDE
018CFA  rts
```

## `$0F7144` -> `ai_NextHomeBestPlayer`  (confidence 0.5, 11 insns)

**Evidence.** ticker helper: returns d1 = entry $BF56 of the home best-first list $BF5E and a1 = the home record, advancing the cursor $BF56 while it is negative; one of four near-identical accessors (with ai_NextAwayBestPlayer, ai_NextHomeWorstPlayer, ai_NextAwayWorstPlayer) over the lists built by ai_BuildRatingsStartingSix; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none

```
0F7144  movem.l	d0/a0,-(sp)
0F7148  move.l	#$FFFFBF5E,a0
0F714E  move.w	($FFFFBF56).w,d0
0F7152  add.w	d0,d0
0F7154  move.w	(a0,d0.w),d1
0F7158  cmp.w	#0,($FFFFBF56).w
0F715E  bge.w	loc_F7166
0F7162  addq.w	#1,($FFFFBF56).w
0F7166  movem.l	(sp)+,d0/a0
0F716A  move.l	#$FFFFC6CE,a1
0F7170  rts
```

## `$0F7172` -> `ai_NextAwayBestPlayer`  (confidence 0.5, 11 insns)

**Evidence.** ticker helper: entry $BF54 of the away best-first list $BF5C with a1 = the away record; see ai_NextHomeBestPlayer; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none

```
0F7172  movem.l	d0/a0,-(sp)
0F7176  move.l	#$FFFFBF5C,a0
0F717C  move.w	($FFFFBF54).w,d0
0F7180  add.w	d0,d0
0F7182  move.w	(a0,d0.w),d1
0F7186  cmp.w	#0,($FFFFBF54).w
0F718C  bge.w	loc_F7194
0F7190  addq.w	#1,($FFFFBF54).w
0F7194  movem.l	(sp)+,d0/a0
0F7198  move.l	#$FFFFCA32,a1
0F719E  rts
```

## `$0F727C` -> `ai_NextHomeWorstPlayer`  (confidence 0.5, 11 insns)

**Evidence.** ticker helper: entry $BF5A of the home worst-first list $BF62 with a1 = the home record; see ai_NextHomeBestPlayer; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none

```
0F727C  movem.l	d0/a0,-(sp)
0F7280  move.l	#$FFFFBF62,a0
0F7286  move.w	($FFFFBF5A).w,d0
0F728A  add.w	d0,d0
0F728C  move.w	(a0,d0.w),d1
0F7290  cmp.w	#0,($FFFFBF5A).w
0F7296  bge.w	loc_F729E
0F729A  addq.w	#1,($FFFFBF5A).w
0F729E  movem.l	(sp)+,d0/a0
0F72A2  move.l	#$FFFFC6CE,a1
0F72A8  rts
```

## `$0F72AA` -> `ai_NextAwayWorstPlayer`  (confidence 0.5, 11 insns)

**Evidence.** ticker helper: entry $BF58 of the away worst-first list $BF60 with a1 = the away record; see ai_NextHomeBestPlayer; caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** none

```
0F72AA  movem.l	d0/a0,-(sp)
0F72AE  move.l	#$FFFFBF60,a0
0F72B4  move.w	($FFFFBF58).w,d0
0F72B8  add.w	d0,d0
0F72BA  move.w	(a0,d0.w),d1
0F72BE  cmp.w	#0,($FFFFBF58).w
0F72C4  bge.w	loc_F72CC
0F72C8  addq.w	#1,($FFFFBF58).w
0F72CC  movem.l	(sp)+,d0/a0
0F72D0  move.l	#$FFFFCA32,a1
0F72D6  rts
```

## `$0FA708` -> `ai_PrintSaveRecordLine`  (confidence 0.6, 11 insns)

**Evidence.** goalie twin of ai_PrintGoalRecordLine: chooses ' Saves ' / ' Save ' (word_FA734) or ' Saves by' / ' Save by' (word_FA746) by d3 and d2, stores the label pointer in $BF18 and joins the shared record-line printer at loc_FA7B0; caller ai_PrintRecordsScreen

**Callers.** ai_PrintRecordsScreen
**Callees.** loc_FA7B0
**Strings.** Saves | Save | Saves by | Save by
**RAM.** TempMaxSpd

```
0FA708  movem.l	a1-a3,-(sp)
0FA70C  move.l	#word_FA734,a1
0FA712  tst.w	d3
0FA714  beq.w	loc_FA71E
0FA718  move.l	#word_FA746,a1
0FA71E  cmpnb	 1,d2
0FA722  bne.w	loc_FA728
0FA726  add.w	(a1),a1
0FA728  move.l	a1,($FFFFBF18).w
0FA72C  movem.l	(sp)+,a1-a3
0FA730  bra.w	loc_FA7B0
```

## `$0FCFB8` -> `ai_PrintTeamOverallRating`  (confidence 0.7, 11 insns)

**Evidence.** ratings screen: prints the spacer (ai_PrintRatingsSpacer) then team a0's overall rating (ai_GetTeamOverallRating) as a 2-digit number, returning it in d0 for the $D5A0/$D5A2 comparison; caller ai_PrintTeamRatingsScreen

**Callers.** ai_PrintTeamRatingsScreen
**Callees.** NumberToPaddedText, ai_GetTeamOverallRating, ai_PrintRatingsSpacer, print2

```
0FCFB8  bsr.w	sub_FCFDC
0FCFBC  move.l	a2,-(sp)
0FCFBE  move.l	a0,a2
0FCFC0  bsr.w	sub_FE172
0FCFC4  move.l	(sp)+,a2
0FCFC6  move.l	d0,-(sp)
0FCFC8  move.w	#2,d1
0FCFCC  jsr	sub_11D3A
0FCFD2  jsr	sub_11A48
0FCFD8  move.l	(sp)+,d0
0FCFDA  rts
```

## `$0FE1AA` -> `ai_LimitTwoPlayerSpeedBoost`  (confidence 0.4, 11 insns)

**Evidence.** doinput helper: when a second controller has a team (cont2team) and the player a3 is not the puck carrier, or in any case when cont2team is unset, caps $C31A at 2; caller doinput

**Callers.** doinput
**Callees.** none
**RAM.** cont2team, puckc

```
0FE1AA  movem.l	d0,-(sp)
0FE1AE  tst.w	($FFFFC32A).w
0FE1B2  beq.w	loc_FE1C2
0FE1B6  move.w	$52(a3),d0
0FE1BA  cmp.w	($FFFFB7AA).w,d0
0FE1BE  bne.w	loc_FE1D2
0FE1C2  cmp.w	#2,($FFFFC31A).w
0FE1C8  ble.w	loc_FE1D2
0FE1CC  move.w	#2,($FFFFC31A).w
0FE1D2  movem.l	(sp)+,d0
0FE1D6  rts
```

## `$007E46` -> `ai_RedrawPauseMenu`  (confidence 0.7, 10 insns)

**Evidence.** runs the menu's refresh handler $CF28 (installed with the item list by sub_7E36), positions via ai_SetPauseMenuColumn, draws the 22x6 box and the items with ai_PrintScrollingMenu, and starts a short palette fade ($BD26 = $18); caller ai_PauseMenuInput

**Callers.** ai_PauseMenuInput
**Callees.** Framer, ai_PrintScrollingMenu, ai_SetPauseMenuColumn, printz2
**RAM.** palcount

```
007E46  move.l	($FFFFCF28).w,a0
007E4A  jsr	(a0)
007E4C  jsr	sub_11A36
007E52  dc.w	6
007E54  dc.b	$FE
007E55  dc.b	4
007E56  dc.b	$FC
007E57  dc.b	$C
007E58  bsr.w	sub_7E72
007E5C  moveq	#$16,d0
007E5E  moveq	#6,d1
007E60  jsr	sub_119B8
007E66  bsr.w	loc_7EF2
007E6A  move.w	#$18,($FFFFBD26).w
007E70  rts
```

## `$011C72` -> `ai_PrintPeriodAndTime`  (confidence 0.7, 10 insns)

**Evidence.** d0 = packed (period << 16 | time*4): prints the period label from the table off_11C92 (entry = period), moves two columns right and prints the time (time / 4) with PushTime; caller ai_PrintScoringSummaryRow

**Callers.** ai_PrintScoringSummaryRow
**Callees.** PushTime, ai_PrintNextString, print
**RAM.** printx

```
011C72  swap	d0
011C74  clr.w	d0
011C76  rol.l	#2,d0
011C78  move.l	#off_11C92,a1
011C7E  bsr.w	sub_13508
011C82  addq.w	#2,($FFFFB028).w
011C86  swap	d0
011C88  lsr.w	#2,d0
011C8A  bsr.w	sub_11CA2
011C8E  bra.w	sub_11BA4
```

