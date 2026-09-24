# NHL 94 bring-up log

## Plan

1. **Consumer repo + build wiring** (this commit). `game/game.toml`,
   `game/nhl94_spec.c`, CMake target linking the shared runner, engine pinned
   as a submodule.
2. **Disassembly-driven discovery.** Adapt the engine's `tests/tools/gen_disasm_*`
   pipeline (which parses Macroassembler AS `.lst` files) to the asm68k listing
   the NHL 94 disassembly produces, then populate `discovery_files`,
   `code_addrs_file` and `annotations` in `game.toml`. See `DISASSEMBLY.md`.
3. **Push-then-RTS dispatch.** `VBlankInt` ($0076B2) is
   `move.l ($FFFFB03A).w,-(sp); rts`, an indirect jump through a RAM-held
   routine pointer. The recompiler emits `rts` as a plain C return, so the
   per-frame routine never runs. Needs an engine-generic codegen pattern.
4. **First boot + dispatch-miss loop.** Boot to the EA logo, then iterate
   `dispatch_misses.toml` against the disassembly until empty.

## ROM facts (verified 2026-09-22)

| Item | Value |
|---|---|
| Size / CRC32 | 0x100000 / 9438F5DD |
| Reset SSP / entry | $00FFFFF6 / $000200 (`SetupGame`) |
| V-int (IRQ6) | $0076B2 `VBlankInt` |
| H-int (IRQ4) | $015E6C `ExpReturn` (bare `rte`) |
| SRAM | header-declared, odd bytes $200001-$203FFF |
| V-blank routine pointer | $FFB03A; values seen: sub_15E4C, sub_15D9A, sub_17692, sub_1A148 |
| Frame counter | $FFB03E (word, incremented by sub_15E4C) |
| Code footprint | ~29.8k instructions; 630 `sub_` + 39 named + 2794 `loc_` labels |
| Dispatch idioms | 0 PC-indexed jump tables, 2 `jmp (aN)`, 9 `jsr (aN)`, 1 push-then-rts |

`WaitVBlank` ($10F86) is not the 4-instruction yield idiom the recompiler
auto-detects: it saves the routine pointer, installs sub_15E4C, spins on
`tst.w ($FFFFBD26).w / bpl.s`, then restores. `vblank_yield_addr` cannot
replace it (side effects). Generated code yields through per-instruction
cycle accounting, so the spin is expected to work; confirm on first boot.

## Milestone 2026-09-23: attract-mode gameplay runs natively

Run 21 (9000 turbo frames): EA logo, title screens, game setup menu and the
attract-mode game (LA vs MTL, clock running, players skating) all render, with
an empty `dispatch_misses.toml`, empty `floor_coverage.toml`, no interior-label
misses and no floor declines. Owner confirmed the front end visually. Fixes
since the earlier status below:

6. Call sites check the top-of-stack VALUE first: our own return address means
   resume even if a callee moved it (word-argument strip via
   `move.l (sp)+,(sp); rts`), a foreign value above the slot means unwind, a
   value at or below the slot is a guest-pushed continuation to run.
7. `intr_stack = 0` in game.toml: handlers push on the live A7 (hardware
   behaviour) instead of a relocated stack with RAM save/restore.
8. Finder: a return-capturing callee's continuation is the next instruction
   start after the inline text (code oracle), not the data return address;
   the scanner stops decoding there.
9. `tools/nhl94_disassembly.py` matches dispatch tables whose indirect call
   is a few instructions after the table load (ObjListMaybe, 36 object
   handlers).

Owner verified keyboard input, sound and a human-played game (2026-09-23).
Not yet verified: timing against hardware, Sonic baselines after the engine changes.

## Fix 2026-09-24: player energy drained immediately (HV counter)

Owner report: with line changes on, every skater's energy bar emptied within
seconds. The drain lives at `$10D26`: it reads the VDP HV counter
(`move.w ($C00008).l,d0`), masks `and.w #$7F`, and only subtracts `$21` from
the player's energy word (`$32(a2,d1.w)` in the team struct at `$C6CE` /
`$CA32`, read and written via `sub_1575A` / `sub_1577A`) when the low seven
bits are zero: a one-in-128 gate per call. The runner's `gvdp_read_hv_counter`
returned a constant H byte (`$00` or `$80`), so the gate passed on every
call. NHL 94 reads the HV counter as an entropy source in about twenty
places (`and.w #3`, `#1`, `#2`, `#$7F`), so more than fatigue was affected.

Engine fix: `gvdp_read_hv_counter_at` derives the H byte from the 68K's cycle
position within the current scanline (`glue_line_cycle_position`: chunk
budget drained so far plus instructions since the last drain, modulo 488),
mapped onto the hardware's 211 (H40) or 171 (H32) distinct values with the
`$B6 -> $E4` / `$93 -> $E9` discontinuity, and the V byte gets the `$EA ->
$E5` wrap. Measured with `--mem-write-log 0xFFC700-0xFFC717` over a
6000-frame attract run: energy-store writes fell from 619 frames to 45.

## Fix 2026-09-24: quickload corrupted the game (save states disabled)

Release test: gamepad shoulder taps (the runner's quicksave / quickload on a
3-button pad) produced a burst of interior-label misses to garbage addresses
(`$900000`, `$190000`, ...) at one frame and the game fell over. The saved
`native_save_1.bin` held sane registers, so the save was fine; the load is
the problem. `runner_load_state_file` replaces WRAM and the 68K registers and
then restarts the game fiber at `resume_main_loop_pc`. NHL 94 defines none,
so the fiber stayed parked where it was, deep inside nested screen
subroutines, while its guest stack had been replaced: the next return-slot
check read a foreign value and dispatched into it. Sonic can restart at a flat
game-mode loop; NHL 94 has no such single loop top.

Fix in `game/nhl94_spec.c`: `state_unavailable_reason` returns a message, so
both quicksave and quickload print `[SAVE]/[LOAD] unavailable: ...` and do
nothing. Proper support needs a resume trampoline that restarts the fiber at
the parked PC and re-walks the restored guest stack when the restarted
routine returns; that is an engine feature, not a game one.

## Fix 2026-09-23: Edit Lines > "Set Original lines" interior-label miss

First native-default run: selecting "Set Original lines" in Edit Lines logged
`interior-label miss: $0171CE`. The menu tables at `$19FC0` / `$1A030` store
that handler as a raw `dc.l $171CE`: IDA gave the address no label because it
starts mid-way through `sub_171BE` (after the line-table lookup, so the same
code serves as a subroutine tail and as a menu handler). The labels tool only
promoted `dc.l <label>` references, so the address stayed an interior seed.
`tools/nhl94_disassembly.py` now also resolves raw `dc.l $hex` longwords
against the code set and promotes them (synthetic name `ptr_171CE`; the only
such case in this ROM). 796 functions; headless attract run still clean.

## Fix 2026-09-23: last two floor-covered routines (`$00E12C`, `$010676`)

A `GENESIS_FLOOR=0`-style audit of several human games left `dispatch_misses`
empty but `floor_coverage.toml` listing `$00E12C` and `$010676`. `loc_E12C`
is reached only by `lea loc_E12C(pc),a0 ; bra.w sub_103C8` inside `sub_DEEE`,
and `sub_103C8` ends with `jsr (a0)`: a callback handed over in an address
register. The finder only knew pushed / memory-stored code addresses
(`pea`, `move.l #X,(mem)`), and the labels tool classed `loc_E12C` as an
interior seed, so no dispatch entry existed and the interpreter floor took the
call. `sub_10676` is a direct `bsr` callee already in the dispatch table; it is
the subtree the floor recorded while running `loc_E12C`, not a miss.

Engine fix (`function_finder.c`): when a code oracle is loaded, a static ROM
address loaded into an address register (`lea abs/pc-rel,An`, `movea.l #imm,An`)
whose target the oracle marks as an instruction start becomes a function
entry. Oracle-gated on purpose: without one, such loads are mostly art and
table pointers. NHL 94: 68 sites matched (11 distinct targets, e.g.
`locret_15464`, `sub_E594`, `loc_7DCE`, `loc_10EE0`, `loc_113D0`). A 9000-frame
headless attract run with `GENESIS_FLOOR=0` is clean (no misses, empty floor
manifest, no unsafe / interior-label logs). The `loc_E12C` path itself only
occurs in a human game and awaits owner verification.

`.tier3_floor_default` is now 0 in `game/nhl94_spec.c` (owner request,
2026-09-23): the build is native by default and a dispatch miss is a loud
regression. `GENESIS_FLOOR=1` re-enables the Tier-3 fallback and the
`floor_coverage.toml` feedback for diagnosis. A 9000-frame headless attract
run with no override: zero raw miss events, both manifests empty.

## Fix 2026-09-23: Player Cards menu did nothing (battery SRAM never mapped)

The handler `loc_FA07E` returns at once when `$FFD458` is negative. That flag
is set by `sub_1A14E`, the checksum of the 8 KB save image the game copies
from SRAM to `$FF0000` at boot (`sub_1A050`: copy, validate, format defaults
and write back if invalid, copy and validate again). The runner only mapped
SRAM while the `$A130F1` enable bit was set, but NHL 94 never writes that
register (zero references): on its cartridge the SRAM lies above the 1 MB
ROM and is decoded unconditionally. Every save read was open bus, both
validations failed, and no `nhl94.srm` was ever written. Runner fix in
`genesis_bus.c`: SRAM whose base is above the header's ROM end is always
active (`sram_always`); the enable bit still gates SRAM that shadows ROM
(lock-on carts). First boot after the fix flushes a 16 KB `nhl94.srm`.

## Fix 2026-09-23: disassembly mis-decodes around inline arguments

Two floor-handled misses (`$0F84F6`, `$007FC4`) traced to IDA decoding the
inline-argument bytes after `jsr sub_1172C` / `jsr sub_11B92` as
instructions, which shifted the "next instruction start" the code oracle
reported. Two engine-side answers, neither dependent on the listing:
`m68k_return_slot_fixed_skip` derives the continuation `ret + N` for callees
that end with `addq.l #N,(sp); rts`; and a `[[inline_args]]` declaration in
game.toml (`callee`, `length = "word"`) tells the scanner the word after the
call is the block's total length, so `ret + word` is the continuation. NHL 94
declares its three text-printer entry points (`$11B92 $11A36 $11DE2`). Result:
329 static continuations, zero raw miss events across a 6000-frame attract
run, no floor activity. The listing errors themselves belong upstream in the
MarkeyJester disassembly (`nullsub_3` at `$F84F8`, the `dc.b $2F,9` at `$7FC4`).

## Fix 2026-09-23: pause-menu stats screens were interpreter-floor declines

A human game left `floor_unsafe.log` entries for `$0FBC14 $0FDC5A $009A2A
$00945A $008EB0 $009142 $0082DA`, all dispatched from the `jsr (a0)` at
`$7ED6`. Each is a `loc_` label whose only reference is a `dc.l` inside a
menu table (`dc.l handler ; dc.w len ; dc.b "Game Stats"`), so the labels
tool had classed them as interior seeds. `tools/nhl94_disassembly.py` now
promotes any code label referenced by a data `dc.l` to a function entry
(32 promoted). One further miss, `$007D50`, is the return address of
`bsr sub_80BA` and appeared after the declines; re-test after this change
before treating it as a separate defect.

## Fix 2026-09-23: pause-menu scoreboard scores missing

Symptom: the two big score digits on the pause scoreboard were blank; every
other element rendered. Evidence chain (tools added on the way):
`dump_vram`/`read_cram` vs Gens showed identical palette and digit tiles and
only the eight score cells differing (blank fill vs digit tiles); the memory
write log on the printer's cursor variables (`--mem-write-log
0xFFB028-0xFFB02F`, now tagged with the recent-function ring) showed the
printer positioned at the score cells and emitting zero characters;
`tools/vdp_event_capture.py` (drains the always-on VDP event ring, events now
carry the three most recently entered functions) showed the address-set with
no data following. The number formatter `sub_11D06` builds the digit string
backwards with `clr.b -(a1)` for the pad byte; the recompiler emitted CLR
through the read-modify-write store path, which skips the `-(An)`
predecrement (no load precedes CLR), so the pad byte overwrote the digit and
the string was empty. Fixed in `code_generator.c` (CLR uses the plain store
path). Engine-wide: affects any game using `clr.x -(An)` or `clr.x (An)+`.

## Status 2026-09-23 (earlier, superseded)

Boots through checksum, shows the EA SPORTS logo (frame ~310), fades to the
256-wide title load, V-ints delivered interleaved. Zero dispatch misses and an
empty floor manifest with the disasm-driven inputs. Engine changes made for
this game, all generic (uncommitted, in the sibling engine checkout):

1. `move.l <ea>,-(sp); rts` / `pea; rts` lowered as a computed jump.
2. Call sites follow the return slot from the emulated stack: unwind when the
   callee discarded it, run guest-pushed continuations, and `goto` the
   oracle-known continuation past inline JSR arguments. RTS no longer sets
   `g_rte_pending` from a static pop count (that count was 8 for the
   decompressor end handler and unwound the whole game).
3. Scanner resumes past inline arguments when the code oracle says the bytes
   after a `jsr` to a return-slot-rewriting callee are data.
4. Finder: declared `[[jump_table]]` records are walked at seed time (the
   register-indexed `lea tbl(pc),a2; jsr (a2,d0.w)` idiom never reaches the
   PC-indexed site scan); pushed / stored ROM code addresses (`pea Cont`,
   `move.l #Routine,(mem)`) become entries.
5. Runner: `vblank_info` reports V-int delivery counters and scheduler state;
   `GameSpec.vint_interleave_default` runs handlers interleaved even when the
   game is not parked (NHL 94's V-blank routine busy-waits on the Z80).

Current blocker (run17): at frame ~451, inside an interleaved V-int handler,
a call-site continuation check reads a slot from the MAIN program's stack
(`A7=$FFFFF2`, value `$0172FA`) and dispatches to it. `intr_stack` in
game.toml is the reset SSP `$FFFFF6`, the same region the main program uses
(RunGame sets sp=$FFFE, clamped to initial_ssp), so the handler's frames sit
on top of live main-program slots. Next: give the interrupt handler its own
stack region (or run interleaved handlers on the live A7 as hardware does) and
re-run; then the dispatch-miss loop against the disassembly.

## First native run (step 1 complete, 2026-09-22)

`_build_native.bat` builds `NHL94Recomp.exe` against engine c5d40a6. A
600-frame turbo run exits cleanly with `dispatch_misses.toml` and
`floor_coverage.toml` both empty, but the `[FBHASH]` framebuffer hash is
identical at every sampled frame: nothing is drawn.

Live TCP probing (`get_registers` over ~6 s) shows the 68K parked in a loop
with unchanging registers (D0=$FFFC, A0=$0113C0, A1=$FFFFD404, A7=$FFFFC6)
and SR=$2514, so IRQ6 is enabled and the game has reached its normal
interrupt-on state. The VBlank vector does fire, but the generated
`func_0076B2` (see `build/generated/nhl94/nhl94_part00.c`) is:

```c
uint32_t _ts0076B2 = m68k_read32(0xB03A);
g_cpu.A[7] -= 4; m68k_write32(g_cpu.A[7], _ts0076B2);   /* move.l ($B03A).w,-(sp) */
...
return;                                                 /* rts */
```

The pushed routine address is never entered, so the per-frame routine
(sub_15E4C etc.) never runs, `$FFB03E` never increments, and `WaitVBlank`'s
`tst.w ($FFFFBD26).w / bpl.s` spin never completes. This is exactly the
step-3 blocker: the recompiler must treat `MOVE.L <ea>,-(SP)` immediately
followed by `RTS` as a computed jump to the pushed value.

## Heuristic-only dry run (engine c5d40a6, 2026-09-22)

Recompiling with vectors-only seeds found 433 functions, 524 after boundary
splitting, with 1 unresolved dynamic dispatch and several
`MISALIGNED_FUNC_ENTRY` / `EA_FALLBACK` warnings, which usually mean data was
admitted as code. The disassembly's code-address oracle (step 2) is the fix.
