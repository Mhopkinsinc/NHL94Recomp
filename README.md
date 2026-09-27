# NHL94Recomp

Static recompilation of *NHL Hockey '94* (Sega Genesis / Mega Drive, 1993) to
native C, built on the shared [segagenesisrecomp](https://github.com/mstan/segagenesisrecomp)
engine. This repository owns everything game-specific: the ROM configuration
(`game/game.toml`), the runtime adapter (`game/nhl94_spec.c`), disassembly-derived
discovery inputs, tools, tests and release packaging. The engine is consumed as
a pinned submodule and contains no game knowledge.

**Status: playable.** Boots, menus, attract mode and human games run fully
native (interpreter floor off by default, empty miss manifests). Timing against
hardware is unverified. See `docs/BRINGUP.md` for the chronological log.

## Requirements

- Windows: Visual Studio 2022 (Community is fine) with the C++ workload. The
  build scripts use the CMake bundled with Visual Studio.
- A dump of the USA/EU *NHL Hockey '94* ROM: 1,048,576 bytes, CRC32 `9438F5DD`,
  serial `GM T-50656 -00`. Copy it to `game/NHL94.bin`. The ROM is never
  committed and is not distributed with this project.
- Python 3.12+ for the discovery and probe tooling.
- Optional: an IDA Pro XML export of the ROM database at `game/nhl94.xml`
  supplies human function names for the generated C (see `docs/DISASSEMBLY.md`).

## Build

```bat
git clone --recursive <this repo>
copy <your dump> game\NHL94.bin
_build_native.bat
build\Release\NHL94Recomp.exe build\Release\nhl94.bin
```

`_build_native.bat` regenerates the C from the ROM and config on every build.
Generated files live only under `build/` and must never be edited by hand.

If you are developing the engine at the same time, a sibling
`..\segagenesisrecomp` checkout is used automatically; set the
`GENESIS_RECOMP_ROOT` environment variable to point anywhere else.

## Release build

Dev builds (`_build_native.bat`) compile the TCP command server, history rings
and rare-event prints such as `[DMA-STALL]`. A shipping build turns all of that
off and is packaged by an allowlist tool that refuses to include a ROM, save,
dump or log. Follow `segagenesisrecomp/RELEASING.md`; the mechanics are:

```bat
_build_release.bat                 REM build-release\Release\NHL94Recomp.exe, GEN_ENABLE_TRACE=OFF
_package_release.bat 0.1.0         REM NHL94Recomp-v0.1.0-win64.zip
```

The release script builds against the **pinned** `segagenesisrecomp` submodule,
so commit the engine and bump the submodule before cutting a release. It warns
if `GENESIS_RECOMP_ROOT` redirects it to a development checkout. The zip holds
exactly `NHL94Recomp.exe`, `SDL2.dll`, `README.txt`, `LICENSE` (PolyForm
Noncommercial 1.0.0) and `THIRD-PARTY-LICENSES.md`. Never ship
`GenesisRecomp.exe` (build tool) and never zip a build folder by hand: CMake
copies the ROM next to the executable.

## Layout

```
CMakeLists.txt            game target: generated C + shared runner + adapter
_build_native.bat         configure + build with the VS-bundled CMake
game/game.toml            ROM identity, RAM layout, discovery seeds
game/nhl94_spec.c         GameSpec: entry / VBlank / HBlank dispatchers
game/NHL94.bin            (your ROM; ignored by git)
tools/debug.ini           copied next to the exe in dev builds to arm the TCP server
docs/                     bring-up notes and disassembly provenance
segagenesisrecomp/        pinned shared engine (submodule)
```

## Rules

The engine's `PRINCIPLES.md`, `CLAUDE.md` and `DEBUG.md` apply here. In
particular: the disassembly is ground truth for function discovery, generated
C is never edited, and `dispatch_misses.toml` next to the executable is checked
after every run.

## License

Project code is released under PolyForm Noncommercial 1.0.0, matching the
engine. Third-party notices are in the engine's `THIRD-PARTY-LICENSES.md`.
Release builds contain no ROM data.
