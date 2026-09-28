# NHL 94 data structures

What the code tells us about the game's in-memory and in-ROM records. Every
field below is backed by a use in the disassembly: either an IDA comment on
the instruction that touches it (marked *IDA*), or a routine named during the
naming pass (`docs/names/`), whose evidence comment gives the exact
instruction. Fields marked **?** are inferred from a single use and have not
been confirmed; treat them as leads, not facts.

Addresses are 68000 addresses; WRAM lives at `$FF0000`, so `$B04A` means
`$FFB04A`. Offsets are hexadecimal.

Sources: IDA symbol table and comments in `game/nhl94.xml`; the 2016 asm68k
listing; `game/names-batch-NN.toml` (batch numbers cited as *bNN*); ROM dumps
taken while writing this page.

---

## 1. On-ice object ("SCstruct"), `$80` bytes each

Fifteen objects from `$B04A` (IDA: `SortCords`). Index = the object's
`SCnum` (+`$52`).

| SCnum | address | object |
|---|---|---|
| 0..5 | `$B04A` + n*`$80` | home team: five skaters and the goalie, in position-slot order |
| 6..11 | `$B34A` + (n-6)*`$80` | away team |
| 12, 13 | `$B64A`, `$B6CA` | the two nets (y = centre +-268) |
| 14 | `$B74A` | the puck |

The puck reuses the layout: `puckx` = `$B74A`+0, `pucky` = +`$14`, `puckz` =
+`$18`, `puckvx/vy/vz` = +`$28`/`$2A`/`$2C`, `puckx_nopuck` = +`$5E`, `puckc`
(the carrier's SCnum) = +`$60`, `puck_pflags2` = +`$63`.

Team records point at their first object through +`$22` (`tmsort`).

| offset | size | name | meaning | source |
|---|---|---|---|---|
| +0 | w | Xpos | x position, rink units | IDA |
| +2 | l | sprite data pointer | address of the current sprite-frame table | IDA "move long address at a3+2" |
| +4 | w | attribute | sprite attribute word; bit 3 = X flip, bit 0 of +5 | IDA |
| +6 | w | frame | current animation frame | IDA |
| +8 | w | old frame / lock flag | previous frame; nets get 1 here at reinit (b21 ReinitRinkAndReplay); IDA notes "objects tied to screen scrolling" | IDA, b21 |
| +`$12` | w | VRChar | tile base added to the object's sprite tiles | IDA |
| +`$14` | w | Ypos | y position | IDA |
| +`$18` | w | Zpos | height above the ice | IDA |
| +`$1C`, +`$20`, +`$24` | w | oldXpos, oldYpos, oldZpos | previous positions | IDA |
| +`$28`, +`$2A`, +`$2C` | w | Xvel, Yvel, Zvel | velocity | IDA |
| +`$2E` | w | impactp | SCnum of the last object this one collided with | IDA |
| +`$30` | w | limpact | last impact value | IDA |
| +`$32` | w | impact | current impact value, decays each frame | IDA |
| +`$34` | w | position | position slot: 0 goalie, 1..5 skaters (2 = LD? 3 = RD, 5 = RW per IDA); negative = off the ice / in the box; 2 and 4 are also used as celebration and penalty-shot roles (b9, b12) | IDA, b9, b12 |
| +`$36` | w | assnum | current AI assignment index (0..7) | IDA |
| +`$38` | 8 b | assignment queue | assignment codes, indexed by assnum (`assinsert`/`assreplace`) | IDA |
| +`$40` | w | temp1 | AI scratch (timers) | IDA |
| +`$42` | w | temp2 | AI scratch; shot power for CompShoot (b9) | IDA, b9 |
| +`$44` | w | temp3 | AI scratch (skate-to x) | IDA |
| +`$46` | w | temp4 | AI scratch (skate-to y) | IDA |
| +`$48` | w | temp5 | AI scratch (old zone number) | IDA |
| +`$4A`, +`$4C` | w | wall collision radius x, y | | IDA |
| +`$4E`, +`$50` | w | wallcos, wallsin | angle of the last wall collision | IDA |
| +`$52` | w | SCnum | object index (0..11 players, 12/13 nets, 14 puck); +`$53` is used as SCnum+1 | IDA |
| +`$54` | w | facedir | facing direction 0..7 (0 = up, 4 = down) | IDA |
| +`$58` | w | SPA | animation id (set through `SetSPA`) | IDA |
| +`$5A` | w | SPAnum | index into the animation | IDA |
| +`$5C` | w | SPAcnt | frames left in the current animation frame; -1 restarts | IDA |
| +`$5E` | w | nopuck | frames until the object may touch the puck again (+`$5F` low byte) | IDA |
| +`$60` | b | newpos | requested next position slot (`$FF` = none) | IDA |
| +`$61` | b | newpnum | requested roster index for a substitution (`$FF` = none) | IDA |
| +`$62` | b | pflags | bit 7 which goal the player shoots at (also used as the side flip for relative coordinates), bit 6 away team, bit 5 one-timer pending (b5), bit 3 animation lock, bit 1 new assignment, `pfjoycon` human-controlled, `pfdoff` deceleration | IDA, b5 |
| +`$63` | b | pflags2 | bit 1 one-timer (b5), bit 2 unavailable / benched (`pf2unav`), bit 3 line-change menu open (b9) and "animation in progress" per IDA, bit 6 cleared by `setplayer`, `pf2fight` fighting, `pf2npc` no collision | IDA, b5, b9 |
| +`$64` | b | pflags3 | breakaway, fall-down, offside and wall-collision bits; bit 3 one-timer (b5) | IDA, b5 |
| +`$65` | b | glitch | minimum frames between sprite frame switches | IDA |
| +`$66` | b | pnum | roster index of the player in this object | IDA |
| +`$67` | b | Wgt | weight (roster byte 1 high nibble * 8) | IDA, `$15BA6` |
| +`$68` | b | Agl | agility (roster byte 1 low nibble, bonus applied) | `$15BB8` |
| +`$69` | b | legspd | speed (roster byte 2 high nibble, capped at `$1E`) | `$15BD0` |
| +`$6A` | b | OfA / aioff | offensive awareness, folded with the team/period bonuses | `$15BE6` |
| +`$6B` | b | DfA / aidef | defensive awareness | `$15C1E` |
| +`$6C` | b | ShP | shot power (roster byte 3 low nibble) | `$15C48` |
| +`$6D` | b | ShA | shot accuracy | IDA |
| +`$6E` | b | Pas | passing | IDA |
| +`$6F` | b | jersey | jersey number, BCD (roster byte 0) | `$15BA6` |
| +`$70` | b | PS bias | penalty-shot / period bias | IDA |
| +`$71` | b | Stk | stick handling | IDA |
| +`$72` | b | End | endurance | IDA |
| +`$73` | b | Agr | aggression (goalies: glove left) | IDA |
| +`$74` | b | Fgt | fighting (from the Chk/Hnd byte with bit 0 masked) | IDA |
| +`$75` | b | Chk | checking (roster byte 4 high nibble) | `$15C68` |
| +`$76` | b | Hnd | handedness, bit 0 (roster byte 4 bit 0, inverted); also sets attribute bit 3 | `$15C8C` |

The roster-to-object copy is the routine at `$15BA4`..`$15CA8` (inside
`setplayer`'s family); it applies the power-play, home and period bonuses
(`sub_F70E4`, `sub_15D84`) while copying.

---

## 2. Team record, `$364` bytes: home `$C6CE`, away `$CA32`

Away = home + `$364`; code that handles "the other team" adds or subtracts
`$364`. The current team ids are `HomeTeam` `$C330` and `VisTeam` `$C332`.

| offset | size | name | meaning | source |
|---|---|---|---|---|
| +0 | w | shots (`HmShots` = `$C6CE`) | team shots on goal | IDA symbol |
| +2 | w | power-play goals **?** | incremented on a goal that ends a penalty | b11 EndPenaltyOnGoal |
| +`$C` | w | tmscore (`HmGoals` = `$C6DA`) | goals | IDA |
| +`$E` | w | faceoffs won | | IDA |
| +`$10` | w | team checks | | IDA |
| +`$12` | w | pass attempts | | IDA |
| +`$14` | w | passes completed | | IDA |
| +`$16` | w | tmline | line currently on the ice | IDA |
| +`$18` | w | last player to touch the puck | pnum | IDA |
| +`$1A` | w | assist 1 | pnum, -1 none | IDA |
| +`$1C` | w | assist 2 | pnum, -1 none | IDA |
| +`$1E` | l | team data pointer | ROM address of the team block (section 3) | IDA |
| +`$22` | w | tmsort | address of the team's first object (`$B04A` / `$B34A`) | IDA |
| +`$24` | w | tmap (`$C6F2`) | active skaters on the ice (4..6) | IDA |
| +`$26` | w | tmgoalie | goalie selector; -1 = no goalie (pulled) | IDA |
| +`$28` | w | team id | index into the team table | b11 InitTeamRecord |
| +`$2E` | w | pending line | line requested by a line change | b2 PrintLineChangeMenu |
| +`$30` | w | team flags (`$C6FE`) | bit 1 line change pending, bit 4 in the attacking zone (offside tracking) | IDA, b14 |
| +`$32` | 26 w | energy | per roster slot, `$1000` = full | b6 ResetLineEnergy |
| +`$66` | 26 w | status | per roster slot: positive = penalty time remaining (& `$7FF`) with bit 6 major, bit 4/5 flags; -1 / -2 available; -3 demoted to -2 on reset; -4 out (injured) | b6, b11, b24 |
| +`$9A` | bytes | penalized list (`$C768`) | pnums in the box, -1 terminated | IDA, b11 |
| +`$B4` | 26 b | goals per player | | b11 |
| +`$CE` | 26 b | assists per player | | b11 |
| +`$E8` | 26 b | shots per player | | b8, b9 |
| +`$102` | 26 b | **?** | fourth per-player column, unused by the named code | layout |
| +`$11C` | 26 b | checks per player | | IDA |
| +`$136` | 26 b | per-player rating/bonus word used by the stars scorer **?** | b8 ScorePlayerForStars |
| +`$16A` | 8 b/line | line table | player indexes per line, 8 bytes each (goalie entry first); copied from the ROM block by InitTeamRecord | b3, b11 |
| +`$1A2` | 16 b/player | hot/cold rating table | per-player attribute rows summed by RateStartingSix | IDA, b4 |
| +`$342` | words | period stats (view 1) | printed by PrintPeriodStatColumns | b27 |
| +`$34A` | words | period shots (view 2) | | IDA, b27 |
| +`$352` | w | power-play total | | IDA |
| +`$354` | w | power-play shots | | IDA |
| +`$358` | w | breakaway attempts | | IDA |
| +`$35A` | w | breakaway goals | | IDA |
| +`$35C` | w | one-timer attempts | | IDA |
| +`$362` | w | short-handed goals | | IDA |

---

## 3. Team data block (ROM)

The team table is at `$30A`; entry for team id *t* is the longword at
`$30A + (t+1)*4` (so `$30E` is team 0). Each points at a block whose header
holds byte offsets from the block start:

| header | points at | notes |
|---|---|---|
| +0 | player list | length-prefixed records, see below |
| +2 | palette block | 32-byte CRAM lines; home palette at +`$0C`, road at +`$2C` in the team-colour routines; `LoadTeamPaletteLine` copies one line into `$BD68` |
| +4 | name strings | three length-prefixed strings: city (`Anaheim`), abbreviation (`ANH`), nickname (`Mighty Ducks`) |
| +6 | lineup | six starting player indexes (used by RateStartingSix and the shootout), then the line table (8 bytes per line) that InitTeamRecord copies to record +`$16A` |
| +8 | roster info block | six bytes before the lineup; the code reads byte 3's high nibble as a count (`GetGoalieCount`, unverified) |
| +`$A` | attribute-count word | the word whose nibble count `CountRatingNibbles` returns |

Dump for Anaheim (`$5330`): header `0092 000C 0222 0052 004C 0050 0EE8 ...`.

**Roster record** (`player list` entries, terminated by a record whose length
word is 2):

```
word  length of the name part (includes this word)
      name, zero padded to the length
byte 0  jersey number, BCD                         -> object +$6F
byte 1  weight (high nibble) | agility (low)       -> +$67 (x8), +$68
byte 2  speed | offensive awareness               -> +$69, +$6A
byte 3  defensive awareness | shot power          -> +$6B, +$6C
byte 4  checking | handedness (bit 0)             -> +$75, +$76; also +$74 Fgt = byte & $E
byte 5  stick handling | shot accuracy            -> +$71, +$6D
byte 6  endurance | penalty-shot bias             -> +$72, +$70
byte 7  passing | aggression                      -> +$6E, +$73 (low nibble)
```

All eight mappings are the copy routine at `$15BA4`..`$15D00`.

Goalies carry zeros in bytes 4 and 5; `PickBestAvailableSkater` treats a
shot-accuracy nibble of 0 or 1 as "goalie". Example: `Guy Hebert` =
`29 62 33 32 00 00 22 22`, `Adam Oates` = `12 75 46 53 31 54 50 61`.

Rosters in the record are indexed 0..25 (`pnum`); the code assumes at most
26 players per team (`MaxRos`).

---

## 4. Player photos, logos and other assets

**Photo table** `off_F92F4[team]`: a list of 6-byte entries (longword photo
address, word player index) terminated by a zero longword. Players without
an entry get one of four generic images (`unk_C6F02`, `unk_C726C`,
`unk_C6B98`, `unk_C682E`), chosen by bit 0 of the record's byte +4 and by
goalie/skater (b4 GetPlayerPhoto). Anaheim's table only lists generic images;
Boston has seven real photos (players 0, 18, 17, 6, 11, 2, 19).

**Photo asset**: two longwords (the second is the offset of a private palette,
or 0 to use the shared palette block `off_C63F8`), then a tile count word
(`$24` = 36 tiles = 6x6) and the pixels packed 3 bits each, 8 pixels per
3 bytes. `UnpackPhotoTiles` (b2) expands each pixel to nibble+5, so photos
use palette entries 5..12 of their line. The shared block `off_C63F8` holds
two palette lines at +`$36A` and +`$3EA`.

**Team logos** `off_F86F2[team]`: an asset with two longword offsets (tiles,
name-table map) drawn as 6x6 with the template `unk_FF462 + team*8` (b4
DrawTeamLogo6x6). Setup-screen logo palettes: `word_F8BF4 + team*64`
(+2 home, +`$26` away).

**Centre-ice logos** `long[$FEA74 + team*4]`: 8 zero bytes, then a count
word (`$18` = 24 tiles) and raw 4bpp tiles (b3 LoadHomeCenterIceLogo).

**Generic asset** (`LoadAsset` / `LoadTilesCore`, b13): a sequence of blocks,
each a count word followed by tiles; count 0 ends, a negative count marks a
compressed block for `DecompressTiles`. `LoadAssetInline` callers put an
8-byte nibble remap table right after the `jsr`.

---

## 5. Playoff series record ("gsstruct"), `$10` bytes x 8 at `$CE66`

`gamenum` `$CEE6` = index of the current series (-1 outside the playoffs).
Series *i* is at `$CE66 + i*$10`.

| offset | meaning | source |
|---|---|---|
| +0 / +2 | the two teams; the id byte sits at +1 and +3 | b15 SeedPlayoffBracket, SetSeriesTeams |
| +4 / +6 | wins for each side (`gspobwins` / `gspotwins`); a side with 4 has won | IDA, b4 |
| +8 | game number in the series, 0..6, or 7 when not best-of-seven | IDA |
| +`$A` / +`$C` | scores of the last game | b4 AdvancePlayoffSeries |
| +`$E` | flags: bit 0 teams flipped / home advantage (`gsftf`), bit 1 highlight pending, bit 2 series finished | IDA, b16 |

The password (b2/b4) encodes the eight +4/+6 win counts in base 5 together
with the option values; `pojoy` `$CEF0` is the round, `potreeteam` `$CEEE`
the user's team slot, `bosgames` `$CEEA` the series length option.

---

## 6. Scoring and penalty summaries

**ScoreSum** `$C474`, 6 bytes per goal; `ScoreSumbytes` `$C472` = bytes used,
`ChkCnt` `$C46E` = index of the last entry (b8, b11):

```
word  time code: period in the top 2 bits, elapsed time in the low 14
      (ElapsedGameTime = (gsp << 14 | PerTimeTotal) - gameclock)
byte  bit 7 = away team; low bits = goal type index (SH2, SH, PP, PP2)
byte  scorer pnum
byte  assist 1 pnum (-1 none)
byte  assist 2 pnum (-1 none)
```

**Penalty summary** `$C5DE`, 4 bytes per penalty: time word, a byte with
bit 7 = away and the penalty type in the low 7 bits (index into the string
table `word_18E0C`, whose entries carry the minutes), and the player (b27
PrintPenaltySummaryRow).

---

## 7. Sound driver tables

| table | layout | source |
|---|---|---|
| `$D3D4` active sounds, 8 x 6 bytes | +0 longword pointer to the sound's data (-1 = free), +4 wait counter, +5 byte from the sound header | b2 StopSound30, b12 RunMusicTrack, b5 InitSoundChannels |
| `$D3A4` channels, 6 x 8 bytes | +3 note/type byte (`$60` and above = PSG), +4 hardware channel (0,1,2,4,5,6; FM channel 3 unused), +6 flags with bit 0 = active | b5, b22 SetChannelVolume, b21 SetChannelFrequency |
| `$D182` | update masks (pending bits per channel) copied into Z80 RAM `$98` by `Z80_WriteVolume` | b3 |
| `$D187` + channel | volume bytes | b22 |
| `$D18E` + 2*channel | FM frequency words | b21 |

Sound list `off_2C648` (4 bytes per id); ids `$30` and above are music and
ambient tracks (StopSound30 runs before any of them starts).

---

## 8. SRAM layout

All accesses go through `ReadSRAM` / `WriteSRAM` with a byte offset and
length; the routines that set `$C2F8` bit 6 select the write path.

| offset | size | contents | source |
|---|---|---|---|
| `$0000` | `$2D8` x 4 | record fields, addressed as `field*4 + word_F9CA4[category]*4` (`ReadRecordField`, `WriteRecordField`); each 4 bytes = value, user id, opponent team, user id | b1, b9 |
| `$0B60` | 28 x 16 | team records: bytes 0..3 most goals in a game, 4..7 best margin, 8..`$B` loudest crowd; each group = value + user/team ids | b8 UpdateTeamRecords |
| `$0D20` | 8 x 16 | user records: 0..3 best goals, 4..7 best margin, 8/9 wins, `$A`/`$B` games played, `$C`/`$D` ties | b8 UpdateUserWinLoss, b21 RankUsersByRecord |
| `$0DA0` | `$80` | user names, 12 bytes each (RAM mirror `$D45A`) | b6 ReadUserNames |
| `$1EF6` | `$100` | playoff state and password (RAM mirror `$D076`; the five-word password at `$D088`) | b4 SavePlayoffPassword |

`$CF36` is the 16-byte scratch record most SRAM readers fill. The SRAM
signature and checksum live in `sub_1A14E` (see the boot cheats in
`docs/DISASSEMBLY.md`).

---

## 9. Smaller records

- **Indicator records** `$BDB4`, 6 x `$1C` bytes: the controlled-player
  markers; +`$12` x, +`$18` flag; sprite output slots at `$BE88` + n*`$14`
  (b8 PlaceOffscreenIndicator, b21 InitRinkScreen).
- **Replay ring** `$FF0000`..`$AF54`, `$62` bytes per frame; write pointer
  `recbpr` `$B036` (b20/b21/b24). The same low RAM holds the game-state
  snapshot taken before a highlight replay (`$5BE` words from `$C2EA`).
- **Sprite list** `$C018`, 8 bytes per hardware sprite, count in `$C2E8`.
- **Print state**: `printx` `$B028`, `printy` `$B02A`, `printa` `$B02C`
  (palette/priority attribute), `printm` `$B02E` (plane descriptor offset
  into `$B004`); strings are length-prefixed (the length word counts itself)
  and inline print strings carry `$F8`..`$FF` control codes handled by the
  `PrintCtl_*` routines (b26).
- **Camera**: `Hpos` `$BD1C`, `Vpos` `$BD18`, clamped to -`$3C`..`$3C` and
  -`$C8`..`$100` (b13 ClampCamera).
- **Pad bytes** (`$BEEE`.. per controller): bit 0 Up, 1 Down, 2 Left,
  3 Right, 4 B, 5 C, 6 A, 7 Start; `sub_11340` returns d3 = held, d2 =
  previous, d1 = new presses.
