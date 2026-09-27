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

## IDA Pro export (function names)

`game/nhl94.xml` is an IDA Pro 7.7 XML export (File > Produce file > XML) of
the owner's working database for this ROM. It is the source of the function
names that appear as comments above the generated C functions: 320-odd
human-named functions against the 45 named labels the 2016 listing carries,
plus the end-of-line comment at each entry as the annotation's notes column.
`tools/nhl94_disassembly.py` reads it (`--ida-xml`, default `game/nhl94.xml`)
when regenerating `annotations_from_disasm.csv`, taking the XML name where
one exists and the listing name otherwise. Only names at addresses the
listing proves to be instruction starts are accepted; the rest are reported.

The XML is used for names only. Discovery (the code-address oracle, entry and
seed labels, jump tables) still comes from the reassembled listing, which is
byte-verified and marks every instruction start; the XML's code blocks cover
fewer instruction starts and its function list adds no real entries beyond
the listing's (its four extras are IDA artefacts inside inline printer data
or mid-function labels). Its 213 named RAM variables and 4500 comments are
not consumed yet; emitting them into the generated C would need an engine
addition to the annotation table.

After every new export: copy it over `game/nhl94.xml`, rerun the tool with
`--reuse`, rebuild.

## Naming the unnamed routines (`tools/nhl94_names.py`)

`game/nhl94.xml` is the source of truth for names, and it is edited in place
rather than round-tripping through IDA. Provenance is visible in the name
itself: human names from IDA are plain (`getpde`); machine-derived names carry
the `ai_` prefix (`ai_LoadAsset`) and an `[AI <confidence>] <evidence>`
function comment in the XML. The prefix follows the name everywhere, into the
annotations CSV and the generated C, so a guess is never mistaken for a fact.

Workflow:

```
python tools/nhl94_names.py status                 # human / ai / unnamed counts
python tools/nhl94_names.py dossier                # evidence per unnamed routine -> game/nhl94.dossier.md
python tools/nhl94_names.py review game/names-batch-NN.toml   # reviewer doc -> docs/names/names-batch-NN.md
python tools/nhl94_names.py apply game/names-batch-NN.toml    # write ai_ names into nhl94.xml
python tools/nhl94_names.py accept 0x11738 ...     # drop the prefix once a human agrees
python tools/nhl94_names.py export-idc             # optional: IDC to push ai_ names into IDA
python tools/nhl94_disassembly.py --rom game/NHL94.bin --reuse   # regenerate the CSV
```

The dossier lists, per routine in priority order (distinct callers, then
size): callers and callees by name, inline printer strings, named RAM
variables touched, and hardware ports touched. Proposals are TOML tables
(`addr`, `name`, `confidence`, `evidence`); `apply` refuses to overwrite a
human name. The XML edits are minimal text changes (a `NAME` attribute and a
`REGULAR_CMT` child), so the diff stays reviewable and IDA's XML import still
reads the file. Batches live in `game/names-batch-NN.toml`, each with a
reviewer document in `docs/names/`; the dossier is regenerated and committed
with every batch so the remaining work is visible in the repository.

