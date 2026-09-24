cmake_minimum_required(VERSION 3.16)
project(NHL94Recomp C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# ---------------------------------------------------------------------------
# Engine location.
#
# The pinned engine lives in the segagenesisrecomp/ submodule. For local
# engine development, point GENESIS_RECOMP_ROOT at a sibling checkout instead
# (the _build_native.bat wrapper does this automatically when one exists).
# ---------------------------------------------------------------------------
set(GENESIS_RECOMP_ROOT "" CACHE PATH
    "Override: absolute path to a segagenesisrecomp checkout (default: submodule)")
if(GENESIS_RECOMP_ROOT)
    get_filename_component(RECOMP_ROOT "${GENESIS_RECOMP_ROOT}" ABSOLUTE)
else()
    set(RECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/segagenesisrecomp")
endif()
if(NOT EXISTS "${RECOMP_ROOT}/recompiler/CMakeLists.txt")
    message(FATAL_ERROR
        "segagenesisrecomp engine not found at:\n    ${RECOMP_ROOT}\n"
        "Run `git submodule update --init --recursive`, or configure with "
        "-DGENESIS_RECOMP_ROOT=<path to a segagenesisrecomp checkout>.")
endif()
if(NOT EXISTS "${RECOMP_ROOT}/external/m68k-recomp-core/cmake/M68kRecompCore.cmake")
    message(FATAL_ERROR
        "The engine's external/m68k-recomp-core submodule is not checked out under\n"
        "    ${RECOMP_ROOT}\nRun `git submodule update --init --recursive` there.")
endif()
message(STATUS "NHL94Recomp: engine root = ${RECOMP_ROOT}")

set(RUNNER_ROOT "${RECOMP_ROOT}/runner")
set(GAME_DIR    "${CMAKE_CURRENT_SOURCE_DIR}/game")

# ---------------------------------------------------------------------------
# Build options.
# ---------------------------------------------------------------------------
option(GEN_ENABLE_TRACE
    "Compile the TCP command server + history rings (dev builds). OFF = shipping build." ON)
option(GENESIS_REVERSE_DEBUG
    "Emit reverse-debug instrumentation into the generated C" OFF)
set(GENESIS_DEBUG_PORT 4380 CACHE STRING "Compile-time default TCP debug port")

# ---------------------------------------------------------------------------
# Generated 68K -> C translation. Regenerated from game/NHL94.bin + game/game.toml
# by the engine's recompiler whenever any input changes. Never edit the output.
# ---------------------------------------------------------------------------
include("${RECOMP_ROOT}/cmake/GenesisRecompGenerated.cmake")
genesisrecomp_add_generated_sources(NHL94_GEN nhl94 "${GAME_DIR}" NHL94.bin
    REVERSE_DEBUG ${GENESIS_REVERSE_DEBUG})

# ---------------------------------------------------------------------------
# Shared clean-room runner (engine-owned). One backend: ours.
# ---------------------------------------------------------------------------
set(RUNNER_SOURCES
    "${RUNNER_ROOT}/main.c"
    "${RUNNER_ROOT}/glue.c"
    "${RUNNER_ROOT}/app_config.c"
    "${RUNNER_ROOT}/audio.c"
    "${RUNNER_ROOT}/chip_trace.c"
    "${RUNNER_ROOT}/crash_report.c"
    "${RUNNER_ROOT}/fiber_compat.c"
    "${RUNNER_ROOT}/frame_snapshots.c"
    "${RUNNER_ROOT}/game_cycles.c"
    "${RUNNER_ROOT}/gamepad.c"
    "${RUNNER_ROOT}/input_map.c"
    "${RUNNER_ROOT}/input_script.c"
    "${RUNNER_ROOT}/m68k_interp.c"
    "${RUNNER_ROOT}/reverse_debug.c"
    # State hashing is used by the always-on benchmark/state paths in main.c;
    # the lockstep cosim server (cosim.c, cosim_visible.c) is GENESIS_COSIM-only.
    "${RUNNER_ROOT}/cosim_state.c"
    # z80_recomp.c is the opt-in Z80 static-recomp experiment (GENESIS_Z80_RECOMP);
    # the default build runs the superzazu Z80 interpreter.
    "${RUNNER_ROOT}/video/genesis_bus.c"
    "${RUNNER_ROOT}/video/genesis_machine.c"
    "${RUNNER_ROOT}/video/genesis_vdp.c"
    "${RUNNER_ROOT}/video/color_lut.c"
    "${RUNNER_ROOT}/audio/mixer.c"
    "${RUNNER_ROOT}/audio/event_queue.c"
    "${RUNNER_ROOT}/audio/observability.c"
    "${RUNNER_ROOT}/audio/sn76489.c"
    "${RUNNER_ROOT}/audio/ym2612_ymfm.cpp"
    "${RUNNER_ROOT}/audio/audio_shadow.c"
    "${RUNNER_ROOT}/audio/fm_shadow.cpp"
    # Vendored third-party (see THIRD-PARTY-LICENSES.md in the engine).
    "${RUNNER_ROOT}/external/superzazu/z80.c"
    "${RUNNER_ROOT}/external/ymfm/src/ymfm_opn.cpp"
    "${RUNNER_ROOT}/external/ymfm/src/ymfm_ssg.cpp"
    "${RUNNER_ROOT}/external/ymfm/src/ymfm_adpcm.cpp"
    # The Tier-3 interpreter decodes with the same clean-room decoder the
    # recompiler uses; the ROM view comes from the recompiler's parser.
    "${RECOMP_ROOT}/external/m68k-recomp-core/common/m68k_decoder.c"
    "${RECOMP_ROOT}/recompiler/src/rom_parser.c"
)
if(GEN_ENABLE_TRACE)
    list(APPEND RUNNER_SOURCES "${RUNNER_ROOT}/cmd_server.c")
    # Rare-event dev prints ([DMA-STALL], [VINT-MASK], [IRQ-DEBT]) and the
    # chip/sound trace commands. Off in shipping builds.
    add_compile_definitions(GEN_DEV_TRACE=1)
else()
    list(APPEND RUNNER_SOURCES "${RUNNER_ROOT}/cmd_server_stub.c")
endif()

add_executable(NHL94Recomp
    ${RUNNER_SOURCES}
    ${NHL94_GEN}
    "${NHL94_GEN_CYCLES}"
    "${GAME_DIR}/nhl94_spec.c"
)
add_dependencies(NHL94Recomp ${NHL94_GEN_TARGET})

target_include_directories(NHL94Recomp PRIVATE
    "${GAME_DIR}"
    "${NHL94_GEN_DIR}"
    "${RUNNER_ROOT}"
    "${RUNNER_ROOT}/include"
    "${RUNNER_ROOT}/video"
    "${RUNNER_ROOT}/audio"
    "${RUNNER_ROOT}/external"
    "${RUNNER_ROOT}/external/clowncommon"
    "${RUNNER_ROOT}/external/superzazu"
    "${RUNNER_ROOT}/external/ymfm/src"
    "${RECOMP_ROOT}/recompiler/src"
    "${RECOMP_ROOT}/external/m68k-recomp-core/common"
    "${RECOMP_ROOT}/external/m68k-recomp-core/profiles/genesis"
)

target_compile_definitions(NHL94Recomp PRIVATE
    DEFAULT_DEBUG_PORT=${GENESIS_DEBUG_PORT}
    GENESIS_GAME_VERSION="dev"
)

# ---------------------------------------------------------------------------
# SDL2 — bundled with the engine on Windows; system package elsewhere.
# ---------------------------------------------------------------------------
if(WIN32)
    set(SDL2_BUNDLED "${RUNNER_ROOT}/external/SDL2/SDL2-2.28.5")
    target_include_directories(NHL94Recomp PRIVATE "${SDL2_BUNDLED}/include")
    target_link_libraries(NHL94Recomp PRIVATE
        "${SDL2_BUNDLED}/lib/x64/SDL2.lib"
        "${SDL2_BUNDLED}/lib/x64/SDL2main.lib"
        ws2_32)
    add_custom_command(TARGET NHL94Recomp POST_BUILD
        COMMAND "${CMAKE_COMMAND}" -E copy_if_different
            "${SDL2_BUNDLED}/lib/x64/SDL2.dll" "$<TARGET_FILE_DIR:NHL94Recomp>"
        COMMAND "${CMAKE_COMMAND}" -E copy_if_different
            "${GAME_DIR}/NHL94.bin" "$<TARGET_FILE_DIR:NHL94Recomp>/nhl94.bin"
        VERBATIM)
    if(GEN_ENABLE_TRACE)
        # The TCP debug server only arms when debug.ini sits next to the exe.
        add_custom_command(TARGET NHL94Recomp POST_BUILD
            COMMAND "${CMAKE_COMMAND}" -E copy_if_different
                "${CMAKE_CURRENT_SOURCE_DIR}/tools/debug.ini" "$<TARGET_FILE_DIR:NHL94Recomp>"
            VERBATIM)
    endif()
else()
    find_package(SDL2 REQUIRED)
    target_include_directories(NHL94Recomp PRIVATE ${SDL2_INCLUDE_DIRS})
    target_link_libraries(NHL94Recomp PRIVATE ${SDL2_LIBRARIES} m pthread)
endif()

if(MSVC)
    target_compile_options(NHL94Recomp PRIVATE /W3 /WX- /utf-8)
    target_compile_definitions(NHL94Recomp PRIVATE _CRT_SECURE_NO_WARNINGS)
    # 32 generated shards can be large; MSVC needs /bigobj for some of them.
    target_compile_options(NHL94Recomp PRIVATE /bigobj)
endif()
