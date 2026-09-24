/*
 * nhl94_spec.c — GameSpec for NHL Hockey '94 (Electronic Arts, 1993), USA/EU.
 *
 * ROM layout: flat 1 MB at $000000-$0FFFFF, identity-mapped. Battery SRAM is
 * declared in the cartridge header ("RA" $F8 $20, odd bytes $200001-$203FFF),
 * so the runner maps it from the header and sram_start/sram_end stay 0.
 *
 * Boot/dispatch (from the 68K vector table — see game.toml):
 *   Reset SSP    = $00FFFFF6
 *   EntryPoint   = $00000200  (SetupGame)
 *   VInt  (IRQ6) = $000076B2  (VBlankInt: jumps through the pointer at $FFB03A)
 *   HInt  (IRQ4) = $00015E6C  (ExpReturn: bare RTE)
 *
 * Minimal bring-up spec: the three mandatory entry/interrupt dispatchers plus
 * ROM identity. No fill_frame_record and no per-game TCP commands yet — the
 * WRAM layout is only partially named in the disassembly, and inventing
 * addresses would put unverified per-game literals in shared code
 * (PRINCIPLES #21). Dispatchers route through recomp_call_addr(), which uses
 * the generated dispatch table and falls back to the Tier-3 floor.
 */
#include "game_spec.h"
#include "genesis_runtime.h"

#include <stddef.h>
#include <stdint.h>

/* ---- Entry-point / interrupt dispatchers (canonical org-0 addresses) ---- */
static void nhl94_call_entry_point(void) { recomp_call_addr(0x000200u); }
static void nhl94_call_vblank(void)      { recomp_call_addr(0x0076B2u); }
static void nhl94_call_hblank(void)      { recomp_call_addr(0x015E6Cu); }

const GameSpec g_game_spec = {
    .display_name           = "NHL Hockey '94",
    .short_name             = "NHL94",

    /* USA/EU cartridge dump: 1 MB, CRC32 9438F5DD, serial GM T-50656 -00. */
    .expected_rom_crc32     = 0x9438F5DDu,
    .expected_rom_size      = 0x100000u,

    /* Native by default (2026-09-23): discovery is disassembly-driven and
     * human games plus the attract loop run with an empty floor manifest,
     * so a dispatch miss is now a loud regression, as for the Sonic titles.
     * Set GENESIS_FLOOR=1 in the environment to re-enable the Tier-3 miss
     * fallback while diagnosing one (it feeds floor_coverage.toml). */
    .tier3_floor_default    = 0,

    /* NHL 94's V-blank routines drive the Z80 sound driver through a
     * request/acknowledge handshake in Z80 RAM ($A00096/97) and busy-wait
     * for the reply. Delivered atomically the scheduler cannot step the Z80
     * during the handler, so the wait never ends (instruction watchdog).
     * Interleaved delivery runs the handler on the game fiber and lets its
     * bus accesses yield to the scheduler, as on hardware. */
    .vint_interleave_default = 1,

    /* Header-declared SRAM; sram_start/end intentionally 0 (see file header). */

    .call_entry_point       = nhl94_call_entry_point,
    .call_vblank            = nhl94_call_vblank,
    .call_hblank            = nhl94_call_hblank,
    .resume_main_loop_pc    = 0u,
    .save_resume_pc         = NULL,
    .dispatch_main_loop_pc  = 0u,
    .call_periodic          = NULL,

    .on_post_reset          = NULL,
    .on_frame_pre           = NULL,
    .on_frame_post          = NULL,
    .on_hblank              = NULL,

    .handle_arg             = NULL,
    .arg_usage              = NULL,
    .dispatch_override      = NULL,

    .fill_frame_record      = NULL,
    .frame_record_version   = 0u,

    .commands               = NULL,
    .command_count          = 0,
};
