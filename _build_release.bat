@echo off
REM _build_release.bat - configure + build the SHIPPING NHL94Recomp runner.
REM
REM Differs from _build_native.bat in exactly two ways:
REM   * GEN_ENABLE_TRACE=OFF: no TCP command server, no history rings, no
REM     [DMA-STALL]-style dev prints, no debug.ini copied next to the exe.
REM   * Separate build tree (build-release\) so the dev build stays intact.
REM
REM Always builds against the PINNED submodule, never a sibling engine
REM checkout, so a release reflects a committed engine revision. Override with
REM GENESIS_RECOMP_ROOT only if you know why.
REM
REM Package the result with _package_release.bat (never zip the folder: CMake
REM copies the ROM next to the exe).
setlocal
set "HERE=%~dp0"
set "CMAKE_EXE=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
if not exist "%CMAKE_EXE%" (
    echo [release] VS-bundled cmake not found at "%CMAKE_EXE%"; falling back to PATH cmake.
    set "CMAKE_EXE=cmake"
)

set "ENGINE_ARG="
if defined GENESIS_RECOMP_ROOT (
    echo [release] WARNING: building against GENESIS_RECOMP_ROOT=%GENESIS_RECOMP_ROOT%, not the pinned submodule.
    set "ENGINE_ARG=-DGENESIS_RECOMP_ROOT=%GENESIS_RECOMP_ROOT%"
) else (
    echo [release] engine: pinned submodule segagenesisrecomp\
)

"%CMAKE_EXE%" -S "%HERE%." -B "%HERE%build-release" -G "Visual Studio 17 2022" -A x64 ^
    -DGEN_ENABLE_TRACE=OFF -DGENESIS_REVERSE_DEBUG=OFF %ENGINE_ARG% %*
if errorlevel 1 exit /b 1
"%CMAKE_EXE%" --build "%HERE%build-release" --config Release --target NHL94Recomp
if errorlevel 1 exit /b 1
echo [release] OK: %HERE%build-release\Release\NHL94Recomp.exe
