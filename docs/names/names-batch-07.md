# Name review: names-batch-07.toml

For each routine: the proposed `ai_` name, confidence, the evidence the
proposal rests on, who calls it and what it calls, and its assembly.
Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the
XML (or the proposals file and re-apply).

## `$0F87EA` -> `ai_TickSetupPhotoRotation`  (confidence 0.6, 25 insns)

**Evidence.** per-frame: counts $D440 down and, once it has expired and $D42E bit 0 is set, counts the photo timer $D43C down (with the $52/$50 wrap when bit 5 is set); at $52 it clears bits 2/3, flips the home/away side bit 1 and sets $D42A/$D42C, and when the timer goes negative it falls into ai_ShowNextSetupPhoto; caller GameSetUp_2

**Callers.** GameSetUp_2
**Callees.** ai_ResetPhotoRotateTimer, ai_ShowNextSetupPhoto

```
0F87EA  subq.w	#1,($FFFFD440).w
0F87EE  bpl.w	locret_F8860
0F87F2  move.w	#$FFFF,($FFFFD440).w
0F87F8  bset	#0,($FFFFD42E).w
0F87FE  btst	#0,($FFFFD42E).w
0F8804  beq.w	locret_F8860
0F8808  btst	#5,($FFFFD42E).w
0F880E  beq.w	loc_F8822
0F8812  cmp.w	#$52,($FFFFD43C).w
0F8818  bge.w	loc_F8822
0F881C  sub.w	#$50,($FFFFD43C).w
0F8822  subq.w	#1,($FFFFD43C).w
0F8826  bmi.w	loc_F8862
0F882A  cmp.w	#$52,($FFFFD43C).w
0F8830  bne.w	locret_F8860
0F8834  bclr	#2,($FFFFD42E).w
0F883A  bclr	#3,($FFFFD42E).w
0F8840  bchg	#1,($FFFFD42E).w
0F8846  st	($FFFFD42A).w
0F884A  st	($FFFFD42C).w
0F884E  bclr	#6,($FFFFD42E).w
0F8854  bclr	#7,($FFFFD42E).w
0F885A  jsr	loc_F8868
0F8860  rts
0F8862  jmp	sub_F87D2
```

## `$0F8868` -> `ai_ShowNextSetupPhoto`  (confidence 0.6, 74 insns)

**Evidence.** erases the two 8x8 photo panels and the 25x8 caption area (side chosen by $D42E bit 1), sets the panel through ai_SetHomePhotoPanel or ai_SetAwayPhotoPanel, advances the photo index $D43E (wrapping at 6), then takes entry $D43E of the team's photo list off_F92F4[HomeTeam or VisTeam] (player index into $D434), falls back to the generic image off_C63F8 when the entry has none, and decodes it with ai_UnpackPhotoTiles; reached from ai_TickSetupPhotoRotation

**Callers.** ai_TickSetupPhotoRotation
**Callees.** ai_SetAwayPhotoPanel, ai_SetHomePhotoPanel, ai_UnpackPhotoTiles, dobitmap, eraser, loc_F88FA, loc_F8982, printz
**RAM.** HomeTeam, VisTeam, printx, printy, vcount

```
0F8868  movem.l	d0-a6,-(sp)
0F886C  jsr	sub_11B92
0F8872  dc.w	6
0F8874  dc.b	$FF
0F8875  dc.b	0
0F8876  dc.b	0
0F8877  dc.b	0
0F8878  move.w	#$1C,($FFFFB028).w
0F887E  btst	#1,($FFFFD42E).w
0F8884  bne.w	loc_F888E
0F8888  move.w	#3,($FFFFB028).w
0F888E  move.w	#5,($FFFFB02A).w
0F8894  move.w	#8,d0
0F8898  move.w	#8,d1
0F889C  move.w	#$7FF,d2
0F88A0  jsr	sub_1197E
0F88A6  jsr	sub_11B92
0F88AC  dc.w	6
0F88AE  dc.b	$FF
0F88AF  dc.b	0
0F88B0  dc.b	0
0F88B1  dc.b	0
0F88B2  move.w	#3,($FFFFB028).w
0F88B8  btst	#1,($FFFFD42E).w
0F88BE  bne.w	loc_F88C8
0F88C2  move.w	#$B,($FFFFB028).w
0F88C8  move.w	#5,($FFFFB02A).w
0F88CE  move.w	#$19,d0
0F88D2  move.w	#8,d1
0F88D6  move.w	#$7FF,d2
0F88DA  jsr	sub_1197E
0F88E0  btst	#1,($FFFFD42E).w
0F88E6  bne.w	loc_F88F2
0F88EA  bsr.w	sub_F8762
0F88EE  bra.w	loc_F88FA
0F88F2  bsr.w	sub_F877E
0F88F6  addq.w	#1,($FFFFD43E).w
0F88FA  jsr	sub_11B92
0F8900  dc.w	6
0F8902  dc.b	$FF
0F8903  dc.b	0
0F8904  dc.b	0
0F8905  dc.b	0
0F8906  cmp.w	#6,($FFFFD43E).l
0F890E  blt.w	loc_F8916
0F8912  clr.w	($FFFFD43E).w
0F8916  move.w	($FFFFC330).w,d0
0F891A  move.w	#$1D,($FFFFB028).w
0F8920  btst	#1,($FFFFD42E).w
0F8926  beq.w	loc_F8934
0F892A  move.w	($FFFFC332).w,d0
0F892E  move.w	#4,($FFFFB028).w
0F8934  move.w	#6,($FFFFB02A).w
0F893A  move.w	($FFFFD430).w,d4
0F893E  move.w	($FFFFD43E).w,d3
0F8942  mulu.w	#6,d3
0F8946  asl.w	#2,d0
0F8948  move.l	#off_F92F4,a0
0F894E  move.l	(a0,d0.w),a0
0F8952  move.w	4(a0,d3.w),($FFFFD434).w
...
```

## `$0F8762` -> `ai_SetHomePhotoPanel`  (confidence 0.5, 3 insns)

**Evidence.** loads d4 = tile base $D436 and printx = $1C, then joins the shared photo-panel drawing at loc_F8796; called by ai_ShowNextSetupPhoto for the home side

**Callers.** ai_ShowNextSetupPhoto
**Callees.** loc_F8796
**RAM.** printx

```
0F8762  move.w	($FFFFD436).w,d4
0F8766  move.w	#$1C,($FFFFB028).w
0F876C  bra.w	loc_F8796
```

## `$0F877E` -> `ai_SetAwayPhotoPanel`  (confidence 0.5, 3 insns)

**Evidence.** loads d4 = tile base $D438 and printx = 3, then joins the shared photo-panel drawing at loc_F8796; called by ai_ShowNextSetupPhoto for the away side

**Callers.** ai_ShowNextSetupPhoto
**Callees.** loc_F8796
**RAM.** printx

```
0F877E  move.w	($FFFFD438).w,d4
0F8782  move.w	#3,($FFFFB028).w
0F8788  bra.w	loc_F8796
```

## `$0F76D4` -> `ai_MoveSetupCursor`  (confidence 0.6, 82 insns)

**Evidence.** GameSetUp cursor handling: d7 = cursor row, d0 = signed step; scrolls the menu offset $D422 (0..3, previous value in $D424, $C2F6 bit 2 flags a scroll) so the cursor stays within 5 rows of the window, skips row 6 outside playoff mode ($D048), then redraws the menu window from off_BEFB8 with dobitmap, positions via loc_F7864 and draws the cursor box with sub_119B8 in palette $6000; caller GameSetUp

**Callers.** GameSetUp
**Callees.** Framer, dobitmap, loc_F7766, loc_F780C, loc_F7864
**RAM.** OptPlayMode, printa, printx, printy

```
0F76D4  move.w	d7,d3
0F76D6  bclr	#2,($FFFFC2F6).w
0F76DC  tst.w	d0
0F76DE  bpl.w	loc_F770A
0F76E2  move.w	d0,-(sp)
0F76E4  move.w	d7,d0
0F76E6  asr.w	#1,d0
0F76E8  cmp.w	($FFFFD422).w,d0
0F76EC  bne.w	loc_F7708
0F76F0  move.w	($FFFFD422).w,($FFFFD424).w
0F76F6  bset	#2,($FFFFC2F6).w
0F76FC  subq.w	#1,($FFFFD422).w
0F7700  bpl.w	loc_F7708
0F7704  clr.w	($FFFFD422).w
0F7708  move.w	(sp)+,d0
0F770A  move.w	d7,($FFFFBF12).w
0F770E  add.w	d0,d7
0F7710  bpl.w	loc_F7716
0F7714  clr.w	d7
0F7716  tst.w	d0
0F7718  bmi.w	loc_F7768
0F771C  move.w	d0,-(sp)
0F771E  move.w	d7,d0
0F7720  asr.w	#1,d0
0F7722  sub.w	($FFFFD422).w,d0
0F7726  cmpnw	 5,d0
0F772A  bgt.w	loc_F7732
0F772E  bra.w	loc_F7766
0F7732  move.w	($FFFFD422).w,($FFFFD424).w
0F7738  bset	#2,($FFFFC2F6).w
0F773E  addq.w	#1,($FFFFD422).w
0F7742  move.w	d7,d0
0F7744  asr.w	#1,d0
0F7746  sub.w	($FFFFD422).w,d0
0F774A  cmpnw	 5,d0
0F774E  ble.w	loc_F7756
0F7752  addq.w	#1,($FFFFD422).w
0F7756  cmp.w	#3,($FFFFD422).w
0F775C  ble.w	loc_F7766
0F7760  move.w	#3,($FFFFD422).w
0F7766  move.w	(sp)+,d0
0F7768  btst	#2,($FFFFC2F6).w
0F776E  bne.w	loc_F7778
0F7772  move.w	($FFFFD422).w,($FFFFD424).w
0F7778  cmpnw	 $12,d7
0F777C  blt.w	loc_F7782
0F7780  sub.w	d0,d7
0F7782  cmp.w	#1,($FFFFD048).w
0F7788  bne.w	loc_F779A
0F778C  tst.w	d7
0F778E  beq.w	loc_F779A
0F7792  cmpnw	 6,d7
0F7796  bls.w	loc_F76D6
0F779A  cmp.w	#2,($FFFFD048).w
0F77A0  blt.w	loc_F77B6
0F77A4  cmp.w	#4,($FFFFD048).w
0F77AA  beq.w	loc_F77B6
0F77AE  cmpnw	 6,d7
0F77B2  beq.w	loc_F76D6
0F77B6  bsr.w	loc_F780C
...
```

## `$0FCC76` -> `ai_MatchupsScreen`  (confidence 0.7, 155 insns)

**Evidence.** PeriodOver's MATCHUPS screen: reads the user names, rates both starting sixes, installs sub_15E4C as the V-blank routine, prepares both team records (sub_F70A2), loads the setup tiles (unk_A9A18), font (ai_LoadFontTiles), frame tiles (unk_55B86) and prints the 'MATCHUPS' / 'ADVANTAGE:' headers before the ratings and ticker routines; caller PeriodOver

**Callers.** PeriodOver
**Callees.** Create_HotCold_Table, Framer, ai_BuildRatingsStartingSix, ai_DrawRatingsPictures, ai_LoadAsset, ai_LoadAssetInline, ai_LoadFontTiles, ai_PrintBigInline, ai_PrintTeamRatingsScreen, ai_ReadUserNames, ai_RunTickerMessage, ai_SelectRatingsPlayers, clearTeamStats, dobitmap, loc_FCF4C, printz, setvram, song, sub_17718, sub_F7318, sub_FCF86, sub_FD4C0, sub_FD4CA, waitx
**Strings.** MATCHUPS | ADVANTAGE:
**RAM.** HomeTeam, Map1col1, Map2col1, OptNOP, VisTeam, asv, disflags, framercset, palcount, vbint

```
0FCC76  jsr	sub_F9C68
0FCC7C  jsr	sub_F71A2
0FCC82  clr.w	($FFFFD5A4).w
0FCC86  move.w	#$7A,-(sp)
0FCC8A  jsr	sub_11156
0FCC90  move.l	#sub_15E4C,($FFFFB03A).w
0FCC98  jsr	sub_17102
0FCC9E  move.l	a0,-(sp)
0FCCA0  move.l	#$FFFFC6CE,a0
0FCCA6  jsr	sub_F70A2
0FCCAC  move.l	#$FFFFCA32,a0
0FCCB2  jsr	sub_F70A2
0FCCB8  move.l	(sp)+,a0
0FCCBA  jsr	sub_F71A2
0FCCC0  bclr	#1,($FFFFBF78).w
0FCCC6  move.w	#6,($FFFFB006).w
0FCCCC  move.w	#6,($FFFFB00A).w
0FCCD2  move.w	#0,d0
0FCCD6  jsr	sub_11594
0FCCDC  move.w	#2,d4
0FCCE0  move.w	d4,($FFFFD430).w
0FCCE4  add.w	#$24,d4
0FCCE8  move.w	d4,($FFFFD432).w
0FCCEC  add.w	#$24,d4
0FCCF0  move.w	d4,($FFFFB010).w
0FCCF4  move.l	#unk_A9A18,a2
0FCCFA  jsr	sub_1172C
0FCD00  dc.w	$543
0FCD02  dc.w	$1567
0FCD04  dc.w	$79AB
0FCD06  dc.w	$CDEF
0FCD08  jsr	sub_11F04
0FCD0E  move.w	d4,($FFFFB014).w
0FCD12  move.l	#unk_AAC5A,a2
0FCD18  jsr	sub_1172C
0FCD1E  dc.w	$A23
0FCD20  dc.w	$4567
0FCD22  dc.w	$89AB
0FCD24  dc.w	$CDEF
0FCD26  move.l	#unk_55B86,a2
0FCD2C  move.w	d4,($FFFFB01E).w
0FCD30  jsr	sub_1172C
0FCD36  dc.w	$542
0FCD38  dc.w	$2561
0FCD3A  dc.w	$89AB
0FCD3C  dc.w	$CDEF
0FCD3E  jsr	sub_11B92
0FCD44  dc.w	6
0FCD46  dc.b	$FE
0FCD47  dc.b	0
0FCD48  dc.b	0
0FCD49  dc.b	0
0FCD4A  move.l	#off_54E24,a0
0FCD50  move.l	a0,a1
0FCD52  move.l	a0,a2
0FCD54  add.l	(a2)+,a0
0FCD56  add.l	(a2)+,a1
0FCD58  clr.w	d0
0FCD5A  clr.w	d1
0FCD5C  moveq	#$28,d2
...
```

## `$017730` -> `ai_RunTickerMessage`  (confidence 0.6, 171 insns)

**Evidence.** intermission ticker: every time the $D5B4 delay expires takes the next line of the message text at aWelcomeToASoldOut_Ton ('Welcome to a sold out ^. Tonight's ...', lines separated by $D, line offsets in the $D5B8 table indexed by $D5B2), scrolls the display with ai_ScrollTickerRows and interprets the placeholder characters _ + $ { } [ ] < > | \ to insert team, player and stat text; caller ai_MatchupsScreen

**Callers.** ai_MatchupsScreen
**Callees.** ai_ScrollTickerRows, loc_1778E, loc_17890, loc_17982, loc_17986, loc_17994, loc_179B4, loc_179B8, print, printz, sub_F7144, sub_F7172, sub_F727C, sub_F72AA, sub_FCB9A, sub_FD5AE, sub_FD5F4, sub_FEEC8, sub_FEF5A
**RAM.** DispAttribCtr, PlayerScrollCtr, VertLineScrolling, asv, mesarea, printx, printy

```
017730  cmp.w	#$1000,($FFFFD5B4).w
017736  bgt.w	locret_15464
01773A  tst.w	($FFFFB044).w
01773E  bmi.w	loc_1774A
017742  subq.w	#1,($FFFFD5B4).w
017746  bpl.w	locret_15464
01774A  move.l	#aWelcomeToASoldOut_Ton,a1
017750  move.w	($FFFFD5B0).w,d0
017754  bpl.w	loc_17796
017758  clr.w	($FFFFD5AC).w
01775C  move.w	($FFFFD5B2).w,d0
017760  addq.w	#2,($FFFFD5B2).w
017764  move.w	#$D5B8,a0
017768  move.w	(a0,d0.w),d0
01776C  bpl.w	loc_1777E
017770  move.w	#$7FFF,($FFFFD5B4).w
017776  move.w	#$1E0,($FFFFD5B6).w
01777C  rts
01777E  bsr.w	sub_179D2
017782  move.l	a1,a2
017784  bra.w	loc_1778E
017788  cmp.b	#$D,(a2)+
01778C  bne.s	loc_17788
01778E  dbf	d0,loc_17788
017792  suba.l	a1,a2
017794  move.w	a2,d0
017796  lea	(a1,d0.w),a2
01779A  move.w	#$A,($FFFFD5B4).w
0177A0  move.w	($FFFFD5AC).w,d0
0177A4  cmp.b	#$5F,(a2)
0177A8  beq.w	loc_179B0
0177AC  cmp.b	#$2B,(a2)
0177B0  beq.w	loc_1799C
0177B4  cmp.b	#$24,(a2)
0177B8  beq.w	loc_17956
0177BC  cmp.b	#$7B,(a2)
0177C0  beq.w	loc_179B0
0177C4  cmp.b	#$7D,(a2)
0177C8  beq.w	loc_179A8
0177CC  cmp.b	#$5B,(a2)
0177D0  beq.w	loc_1797E
0177D4  cmp.b	#$5D,(a2)
0177D8  beq.w	loc_17976
0177DC  cmp.b	#$3C,(a2)
0177E0  beq.w	loc_1792E
0177E4  cmp.b	#$3E,(a2)
0177E8  beq.w	loc_17938
0177EC  cmp.b	#$7C,(a2)
0177F0  beq.w	loc_17942
0177F4  cmp.b	#$5C,(a2)
0177F8  beq.w	loc_1794C
0177FC  cmp.b	#$40,(a2)
017800  beq.w	loc_178C0
017804  cmp.b	#$23,(a2)
017808  beq.w	loc_178CA
01780C  cmp.b	#$25,(a2)
017810  beq.w	loc_178D4
017814  cmp.b	#$3D,(a2)
017818  beq.w	loc_178DE
01781C  cmp.b	#$2A,(a2)
...
```

## `$0179D2` -> `ai_ScrollTickerRows`  (confidence 0.6, 17 insns)

**Evidence.** clears $D5AC, advances the ticker row counter $D5AE and once it reaches 7 keeps it at 6 and shifts the eight 58-tile rows of the ticker window up by one row with ai_VDP_VramCopyDMA (plane rows $80 bytes apart starting at $B004 + $212); only caller ai_RunTickerMessage

**Callers.** ai_RunTickerMessage
**Callees.** ai_VDP_VramCopyDMA
**RAM.** DispAttribCtr, VertLineScrolling, VmMap1

```
0179D2  clr.w	($FFFFD5AC).w
0179D6  addq.w	#1,($FFFFD5AE).w
0179DA  cmp.w	#7,($FFFFD5AE).l
0179E2  blt.w	locret_15464
0179E6  subq.w	#1,($FFFFD5AE).w
0179EA  movem.l	d0-d3,-(sp)
0179EE  move.l	#7,d3
0179F4  move.w	($FFFFB004).w,d1
0179F8  add.w	#$212,d1
0179FC  move.l	#$3A,d0
017A02  move.w	d1,d2
017A04  add.w	#$80,d2
017A08  bsr.w	sub_114B8
017A0C  move.w	d2,d1
017A0E  dbf	d3,loc_179FC
017A12  movem.l	(sp)+,d0-d3
017A16  rts
```

## `$012828` -> `ai_ClearMessageLine`  (confidence 0.7, 2 insns)

**Evidence.** prints 22 spaces at column 5, row $B with attribute $BF, i.e. blanks the in-game message line; callers UpdatePA and prefmes

**Callers.** UpdatePA, prefmes
**Callees.** printz
**Strings.** 

```
012828  bsr.w	sub_11B92
01282C  dc.w	$1C
01282E  dc.b	$BF
01282F  dc.b	5
012830  dc.b	$B
012831  dc.b	'                      ',0
012848  rts
```

## `$00961A` -> `ai_PrintPlayerStatsList`  (confidence 0.6, 81 insns)

**Evidence.** stats screen body: prints the 'Player' header and the five column titles from word_990E (Saves Shots Save %, G, A, Pts, SOG, PIM, highlighting column DispAttribCtr in palette $C000), the category banner from word_9942 ('[ Goals ]' etc.), then walks the roster (ai_CountRosterPlayers) repeatedly picking the player with the highest remaining value of the selected column (ai_GetPlayerAttributeChecked, ties broken by the roster byte) to print the rows sorted; caller loc_945C

**Callers.** loc_945C
**Callees.** Framer, ai_CountRatingNibbles, ai_CountRosterPlayers, ai_GetPlayerAttributeChecked, ai_PrintNextString, ai_PrintPlayerStatRow, loc_95DC, loc_96FC, print2, printz, printz2
**Strings.** Player
**RAM.** DispAttribCtr, VertLineScrolling, printa

```
00961A  jsr	sub_11A36
009620  dc.w	$12
009622  dc.b	$F8
009623  dc.b	6
009624  dc.b	3
009625  dc.b	4
009626  dc.b	$B
009627  dc.b	$F9
009628  dc.b	1
009629  aPlayer:	dc.b	'Player'
00962F  dc.b	$FB
009630  dc.b	7
009631  dc.b	0
009632  lea	word_990E(pc),a1
009636  moveq	#5,d3
009638  tst.w	($FFFFD5AC).w
00963C  bmi.w	loc_9644
009640  add.w	(a1),a1
009642  clr.w	d3
009644  move.w	#$8000,($FFFFB02C).w
00964A  cmp.w	($FFFFD5AC).w,d3
00964E  bne.w	loc_9658
009652  move.w	#$C000,($FFFFB02C).w
009658  jsr	sub_11A48
00965E  addq.w	#1,d3
009660  cmpnw	 5,d3
009664  blt.s	loc_9644
009666  jsr	sub_11A36
00966C  dc.w	8
00966E  dc.b	$F8
00966F  dc.b	4
009670  dc.b	3
009671  dc.b	9
009672  dc.b	7
009673  dc.b	0
009674  moveq	#$16,d0
009676  moveq	#3,d1
009678  jsr	sub_119B8
00967E  jsr	sub_11B92
009684  dc.w	6
009686  dc.b	$8D
009687  dc.b	$A
009688  dc.b	8
009689  dc.b	0
00968A  lea	word_9942(pc),a1
00968E  moveq	#1,d0
009690  add.w	($FFFFD5AC).w,d0
009694  jsr	sub_13508
00969A  clr.w	($FFFFB030).w
00969E  move.w	#$C018,a3
0096A2  clr.l	d6
0096A4  tst.w	($FFFFD5AC).w
0096A8  bpl.w	loc_96B6
0096AC  bsr.w	sub_9F40
0096B0  bset	d0,d6
0096B2  subq.w	#1,d6
0096B4  not.l	d6
0096B6  moveq	#$FFFFFFFF,d4
0096B8  st	d5
0096BA  bsr.w	sub_9F9A
...
```

## `$0FE548` -> `ai_StopTileAnimation`  (confidence 0.8, 3 insns)

**Evidence.** sets the animation id $D6B4 to -1 and clears $C2FC bit 0; callers ai_TileAnimationStep (script end marker -2) and puckfaceoff2

**Callers.** ai_TileAnimationStep, puckfaceoff2
**Callees.** none

```
0FE548  move.w	#$FFFF,($FFFFD6B4).w
0FE54E  bclr	#0,($FFFFC2FC).w
0FE554  rts
```

## `$0FD78A` -> `ai_EmitAnimationSprites`  (confidence 0.6, 80 insns)

**Evidence.** setvideo hook: when a tile animation is active ($D6B4 >= 0 with an asset in $D6BA) and no menu/pause/replay flag is set ($C2F4 bit 4, $C2EE bit 3, $C2EC bit 7), takes the sprite list of the current frame $D6AE from the asset's second block and appends the sprites inside the camera window (Hpos/Vpos) to the sprite table, using the same window and record layout as ai_EmitCrowdSprites; caller setvideo

**Callers.** setvideo
**Callees.** loc_FD7EA, loc_FD7F0
**RAM.** Hpos, Vpos, sflags, sflags2

```
0FD78A  tst.w	($FFFFD6B4).w
0FD78E  bmi.w	locret_FD898
0FD792  tst.l	($FFFFD6BA).w
0FD796  beq.w	locret_FD898
0FD79A  btst	#4,($FFFFC2F4).w
0FD7A0  bne.w	locret_FD898
0FD7A4  btst	#3,($FFFFC2EE).w
0FD7AA  bne.w	locret_FD898
0FD7AE  btst	#7,($FFFFC2EC).w
0FD7B4  bne.w	locret_FD898
0FD7B8  move.l	($FFFFD6BA).w,a1
0FD7BC  add.l	4(a1),a1
0FD7C0  move.w	($FFFFBD1C).w,d4
0FD7C4  move.w	($FFFFBD18).w,d5
0FD7C8  move.w	($FFFFD6AE).w,d0
0FD7CC  bra.w	loc_FD7F0
0FD7D0  and.w	#$F,d2
0FD7D4  cmpnw	 3,d2
0FD7D8  bls.w	loc_FD7DE
0FD7DC  moveq	#3,d2
0FD7DE  bra.w	loc_FD7EA
0FD7E2  move.w	d3,d0
0FD7E4  add.w	d2,d0
0FD7E6  bsr.w	loc_FD7F0
0FD7EA  dbf	d2,loc_FD7E2
0FD7EE  rts
0FD7F0  ext.w	d0
0FD7F2  beq.w	locret_FD898
0FD7F6  cmpnw	 $40,d6
0FD7FA  bge.w	locret_FD898
0FD7FE  movem.l	d0-d5,-(sp)
0FD802  add.w	d0,d0
0FD804  move.l	a1,a0
0FD806  move.w	2(a0,d0.w),d1
0FD80A  sub.w	(a0,d0.w),d1
0FD80E  lsr.w	#3,d1
0FD810  subq.w	#1,d1
0FD812  move.w	d1,-(sp)
0FD814  add.w	(a0,d0.w),a0
0FD818  move.w	d4,d0
0FD81A  add.w	#$C0,d0
0FD81E  move.w	d0,d1
0FD820  sub.w	#$90,d0
0FD824  add.w	#$80,d1
0FD828  move.w	#$170,d2
0FD82C  sub.w	d5,d2
0FD82E  move.w	d2,d3
0FD830  sub.w	#$80,d2
0FD834  add.w	#$70,d3
0FD838  move.w	(sp)+,d4
0FD83A  cmp.w	2(a0),d2
0FD83E  bgt.w	loc_FD88E
0FD842  cmp.w	2(a0),d3
0FD846  blt.w	loc_FD88E
0FD84A  cmp.w	(a0),d0
0FD84C  bgt.w	loc_FD88E
0FD850  cmp.w	(a0),d1
0FD852  blt.w	loc_FD88E
0FD856  move.w	2(a0),d5
0FD85A  add.w	#$70,d5
...
```

## `$011F12` -> `ai_LoadFrameTiles`  (confidence 0.6, 3 insns)

**Evidence.** stores d4 in $B01E and loads asset unk_55B86 there; $B01E is the tile base that the box drawer sub_119B8 (asset unk_55B7E, same family) and eraser add to their tiles, so unk_55B86 holds the menu frame/blank tiles; callers loc_9CDC and setupice (ai_MatchupsScreen loads the same asset inline)

**Callers.** loc_9CDC, setupice
**Callees.** ai_LoadAsset
**RAM.** framercset

```
011F12  move.l	#unk_55B86,a2
011F18  move.w	d4,($FFFFB01E).w
011F1C  bra.w	sub_11738
```

## `$0FEB54` -> `ai_SlideToFaceoffSpot`  (confidence 0.5, 67 insns)

**Evidence.** updateplayers helper: for six specific animation states of $58(a3) ($1776, $185A, $17E8, $1A00, $18CC, $193E) eases the player's y ($14(a3)) toward $124/$116 or -$124/-$116 (chosen by whether the faceoff x $D41C is within +-$56) or the x toward +-$82/$88 by half the remaining distance each frame, i.e. the crouch/positioning animations used at faceoffs; caller updateplayers

**Callers.** updateplayers
**Callees.** locret_FEC5C
**RAM.** FallXPos

```
0FEB54  cmp.w	#$193E,$58(a3)
0FEB5A  beq.w	loc_FEC44
0FEB5E  cmp.w	#$1A00,$58(a3)
0FEB64  beq.w	loc_FEC0C
0FEB68  cmp.w	#$18CC,$58(a3)
0FEB6E  beq.w	loc_FEC28
0FEB72  cmp.w	#$17E8,$58(a3)
0FEB78  beq.w	loc_FEBF0
0FEB7C  cmp.w	#$1776,$58(a3)
0FEB82  beq.w	loc_FEB94
0FEB86  cmp.w	#$185A,$58(a3)
0FEB8C  beq.w	loc_FEBC2
0FEB90  bra.w	locret_FEC5C
0FEB94  move.w	#$124,d0
0FEB98  cmp.w	#$56,($FFFFD41C).w
0FEB9E  bgt.w	loc_FEBAC
0FEBA2  cmp.w	#$FFAA,($FFFFD41C).w
0FEBA8  bgt.w	loc_FEBB0
0FEBAC  move.w	#$116,d0
0FEBB0  sub.w	$14(a3),d0
0FEBB4  bmi.w	locret_FEC5C
0FEBB8  asr.w	#1,d0
0FEBBA  add.w	d0,$14(a3)
0FEBBE  bra.w	locret_FEC5C
0FEBC2  move.w	#$FEDC,d0
0FEBC6  cmp.w	#$56,($FFFFD41C).w
0FEBCC  bgt.w	loc_FEBDA
0FEBD0  cmp.w	#$FFAA,($FFFFD41C).w
0FEBD6  bgt.w	loc_FEBDE
0FEBDA  move.w	#$FEEA,d0
0FEBDE  sub.w	$14(a3),d0
0FEBE2  bpl.w	locret_FEC5C
0FEBE6  asr.w	#1,d0
0FEBE8  add.w	d0,$14(a3)
0FEBEC  bra.w	locret_FEC5C
0FEBF0  move.w	#$82,d0
0FEBF4  btst	#3,4(a3)
0FEBFA  beq.w	loc_FEC02
0FEBFE  move.w	#$FF7E,d0
0FEC02  sub.w	(a3),d0
0FEC04  asr.w	#1,d0
0FEC06  add.w	d0,(a3)
0FEC08  bra.w	locret_FEC5C
0FEC0C  move.w	#$88,d0
0FEC10  btst	#3,4(a3)
0FEC16  beq.w	loc_FEC1E
0FEC1A  move.w	#$FF78,d0
0FEC1E  sub.w	(a3),d0
0FEC20  asr.w	#1,d0
0FEC22  add.w	d0,(a3)
0FEC24  bra.w	locret_FEC5C
0FEC28  move.w	#$FF7E,d0
0FEC2C  btst	#3,4(a3)
0FEC32  beq.w	loc_FEC3A
0FEC36  move.w	#$82,d0
0FEC3A  sub.w	(a3),d0
0FEC3C  asr.w	#1,d0
0FEC3E  add.w	d0,(a3)
0FEC40  bra.w	locret_FEC5C
0FEC44  move.w	#$FF78,d0
...
```

## `$0F67E4` -> `ai_ComputePassTarget`  (confidence 0.6, 63 insns)

**Evidence.** passmode helper: picks a (dx, dy) pair by the passer's facing $54(a3) from unk_F691E for the goalie (slot $34 = 0), word_F68DE, or unk_F68FE when the passer is deep in the zone (y >= $58 after side flip), overriding dy with $103 for a long centre pass, flips for the side, adds random 0..9 jitter to both (sub_11086) and stores the target x in $D414; caller passmode

**Callers.** passmode
**Callees.** loc_F6830, loc_F68D4, randomd0

```
0F67E4  movem.l	d0-a6,-(sp)
0F67E8  bclr	#2,($FFFFC2F8).w
0F67EE  tst.w	$34(a3)
0F67F2  bne.w	loc_F6800
0F67F6  move.l	#unk_F691E,a0
0F67FC  bra.w	loc_F6830
0F6800  move.w	$14(a3),d0
0F6804  btst	#7,$62(a3)
0F680A  bne.w	loc_F6810
0F680E  neg.w	d0
0F6810  bset	#2,($FFFFC2F8).w
0F6816  move.l	#word_F68DE,a0
0F681C  cmpnw	 $58,d0
0F6820  blt.w	loc_F6830
0F6824  move.l	#unk_F68FE,a0
0F682A  bclr	#2,($FFFFC2F8).w
0F6830  move.w	$54(a3),d0
0F6834  btst	#7,$62(a3)
0F683A  bne.w	loc_F6844
0F683E  addq.w	#4,d0
0F6840  and.w	#7,d0
0F6844  asl.w	#2,d0
0F6846  move.w	(a0,d0.w),d1
0F684A  move.w	2(a0,d0.w),d2
0F684E  cmp.l	#unk_F68FE,a0
0F6854  bne.w	loc_F687E
0F6858  move.w	$14(a3),d0
0F685C  bpl.w	loc_F6862
0F6860  neg.w	d0
0F6862  cmpnw	 $8A,d0
0F6866  blt.w	loc_F687E
0F686A  move.w	(a3),d0
0F686C  bpl.w	loc_F6872
0F6870  neg.w	d0
0F6872  cmpnw	 $37,d0
0F6876  bgt.w	loc_F687E
0F687A  move.w	#$103,d2
0F687E  btst	#7,$62(a3)
0F6884  bne.w	loc_F688C
0F6888  neg.w	d1
0F688A  neg.w	d2
0F688C  move.w	#$A,d0
0F6890  jsr	sub_11086
0F6896  add.w	d0,d1
0F6898  move.w	#$A,d0
0F689C  jsr	sub_11086
0F68A2  add.w	d0,d2
0F68A4  move.w	d1,($FFFFD414).w
0F68A8  tst.w	$34(a3)
0F68AC  beq.w	loc_F68D4
0F68B0  sub.w	(a3),d1
0F68B2  bmi.w	loc_F68C8
0F68B6  sub.w	#$3C,d1
0F68BA  bpl.w	loc_F68D4
0F68BE  neg.w	d1
0F68C0  add.w	d1,($FFFFD414).w
0F68C4  bra.w	loc_F68D4
0F68C8  add.w	#$3C,d1
0F68CC  bmi.w	loc_F68D4
0F68D0  sub.w	d1,($FFFFD414).w
...
```

## `$0FBA76` -> `ai_PurgeUserFromRecords`  (confidence 0.7, 74 insns)

**Evidence.** user-name deletion: for the $2D8 four-byte SRAM records from offset 0 and the $1C sixteen-byte records from $B60, reads each with ReadSRAM into $CF36, clears every user-index byte (odd offsets) equal to the user being deleted ($D4EA) and writes the record back with WriteSRAM when changed; caller sub_FB9D4 (delete user name)

**Callers.** sub_FB9D4
**Callees.** MakeSRAMChecksum, ReadSRAM, WriteSRAM

```
0FBA76  movem.l	d0-a6,-(sp)
0FBA7A  move.w	#$2D7,d7
0FBA7E  moveq	#0,d0
0FBA80  moveq	#4,d1
0FBA82  move.l	#$FFFFCF36,a0
0FBA88  move.w	($FFFFD4EA).w,d6
0FBA8C  clr.w	d5
0FBA8E  jsr	sub_1A244
0FBA94  cmp.b	1(a0),d6
0FBA98  bne.w	loc_FBAA2
0FBA9C  clr.b	1(a0)
0FBAA0  st	d5
0FBAA2  cmp.b	3(a0),d6
0FBAA6  bne.w	loc_FBAB0
0FBAAA  clr.b	3(a0)
0FBAAE  st	d5
0FBAB0  tst.w	d5
0FBAB2  beq.w	loc_FBABC
0FBAB6  jsr	sub_1A1E4
0FBABC  addq.l	#4,d0
0FBABE  dbf	d7,loc_FBA8C
0FBAC2  move.w	#$1B,d7
0FBAC6  move.l	#$B60,d0
0FBACC  moveq	#$10,d1
0FBACE  move.l	#$FFFFCF36,a0
0FBAD4  move.w	($FFFFD4EA).w,d6
0FBAD8  clr.w	d5
0FBADA  jsr	sub_1A244
0FBAE0  cmp.b	1(a0),d6
0FBAE4  bne.w	loc_FBAEE
0FBAE8  clr.b	1(a0)
0FBAEC  st	d5
0FBAEE  cmp.b	3(a0),d6
0FBAF2  bne.w	loc_FBAFC
0FBAF6  clr.b	3(a0)
0FBAFA  st	d5
0FBAFC  cmp.b	5(a0),d6
0FBB00  bne.w	loc_FBB0A
0FBB04  clr.b	5(a0)
0FBB08  st	d5
0FBB0A  cmp.b	7(a0),d6
0FBB0E  bne.w	loc_FBB18
0FBB12  clr.b	7(a0)
0FBB16  st	d5
0FBB18  cmp.b	9(a0),d6
0FBB1C  bne.w	loc_FBB26
0FBB20  clr.b	9(a0)
0FBB24  st	d5
0FBB26  cmp.b	$B(a0),d6
0FBB2A  bne.w	loc_FBB34
0FBB2E  clr.b	$B(a0)
0FBB32  st	d5
0FBB34  tst.w	d5
0FBB36  beq.w	loc_FBB40
0FBB3A  jsr	sub_1A1E4
0FBB40  add.l	#$10,d0
0FBB46  dbf	d7,loc_FBAD8
0FBB4A  move.l	#$D20,d0
0FBB50  move.w	($FFFFD4EA).w,d3
0FBB54  asl.w	#4,d3
...
```

