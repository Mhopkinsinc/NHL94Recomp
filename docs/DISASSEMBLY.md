# NHL 94 disassembly provenance

A complete asm68k-syntax disassembly of the USA/EU *NHL Hockey '94* ROM exists:
"NHL Hockey 94 (16-bit) Mega Drive source", disassembled December 2016 by
MarkeyJester. It is not yet pinned in this repository; the working copy is at

```
C:\_Personal\NHL94Sandbox\GENS\GENS - NHL94 Disassembly\NHL94 Disassembly\
```

Contents: `Source.asm` (~135k lines), `Equates.asm`, `Macros.asm`,
`Unknown\*.asm` (data blobs), `_Assembly Tools\Asm68k.exe`, and an IDA
database `_0 Temp\nhl94.idb` (IDA Pro 7.7 with the Gens plugin is installed
under `C:\_Personal\IDAPRO_7.7_GENS\`).

## Verification

Reassembling `Source.asm` reproduces bytes `$000000-$0FFABF` of the target ROM
exactly. Bytes `$0FFAC0-$0FFFFF` differ because the disassembly's
`_Assemble.bat` patches a separately-assembled checksum stub into that tail
after assembly. All code labels therefore map 1:1 to ROM addresses.

## Producing a listing

Run from the disassembly directory via `cmd` (not an MSYS shell, which mangles
the `/p` switch), writing into a temp directory so the disassembly tree is never
modified:

```bat
"_Assembly Tools\Asm68k.exe" /q /p Source.asm, %TEMP%\nhl94lst\out.bin, , %TEMP%\nhl94lst\Listings.lst
```

The listing rows are `ADDR BYTES  source`. Forward-referenced operands appear as
`0000 0000` in the bytes column (pass-1 values), so tools must take bytes from
the ROM, not from the listing. The engine's `gen_disasm_*` scripts expect
Macroassembler AS rows (`NNNN/ HEXOFFS :`), so an adapter is required
(bring-up step 2).
