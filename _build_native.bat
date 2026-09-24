@echo off
REM _build_native.bat — configure + build the NHL94Recomp native runner.
REM
REM Engine selection (highest priority first):
REM   1. GENESIS_RECOMP_ROOT environment variable, if set.
REM   2. A sibling ..\segagenesisrecomp checkout (development override).
REM   3. The pinned segagenesisrecomp\ submodule.
setlocal
set "HERE=%~dp0"
set "CMAKE_EXE=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
if not exist "%CMAKE_EXE%" (
    echo [build] VS-bundled cmake not found at "%CMAKE_EXE%"; falling back to PATH cmake.
    set "CMAKE_EXE=cmake"
)

set "ENGINE_ARG="
if defined GENESIS_RECOMP_ROOT (
    set "ENGINE_ARG=-DGENESIS_RECOMP_ROOT=%GENESIS_RECOMP_ROOT%"
) else if exist "%HERE%..\segagenesisrecomp\recompiler\CMakeLists.txt" (
    for %%I in ("%HERE%..\segagenesisrecomp") do set "ENGINE_ARG=-DGENESIS_RECOMP_ROOT=%%~fI"
)
if defined ENGINE_ARG (
    echo [build] engine: %ENGINE_ARG%
) else (
    echo [build] engine: pinned submodule segagenesisrecomp\
)

"%CMAKE_EXE%" -S "%HERE%." -B "%HERE%build" -G "Visual Studio 17 2022" -A x64 %ENGINE_ARG% %*
if errorlevel 1 exit /b 1
"%CMAKE_EXE%" --build "%HERE%build" --config Release --target NHL94Recomp
if errorlevel 1 exit /b 1
echo [build] OK: %HERE%build\Release\NHL94Recomp.exe
