NHL94Recomp - NHL Hockey '94 (Sega Genesis / Mega Drive) static recompilation
=============================================================================

This is a native Windows (x64) build of NHL Hockey '94 produced by statically
recompiling the game's 68000 code to C and running it on the segagenesisrecomp
engine (own VDP / bus / sound implementation; no emulator core).

BRING YOUR OWN ROM
------------------
No game data is included. You need your own dump of the USA/EU release:

    NHL Hockey '94   1,048,576 bytes   CRC32 9438F5DD   serial GM T-50656 -00

Running
-------
    NHL94Recomp.exe <path-to-your-rom>.bin

Keep SDL2.dll next to the executable. Battery-backed save data (user records,
team lines, player cards) is written to nhl94.srm next to the ROM.

Controls: keyboard (arrows, Z/X/C = A/B/C, Return = Start) and any
SDL-compatible gamepad, both active for player 1. Edit settings.ini next to
the executable to change bindings, enable player 2, or set the window size;
the file documents every value. Hotkeys: Tab or Back/Select held = turbo,
F11 = fullscreen, Esc = quit.

License
-------
The recompiled runtime and this package are licensed under the PolyForm
Noncommercial License 1.0.0 (see LICENSE). Third-party components and their
licenses are listed in THIRD-PARTY-LICENSES.md. The game itself remains the
property of its rights holders; this package contains none of it.

Source
------
Game repository:   NHL94Recomp   (game configuration, adapter, tooling)
Engine repository: segagenesisrecomp (shared recompiler and runtime)
