@echo off
REM _package_release.bat <version> - build the compliance-checked release zip.
REM
REM   _package_release.bat 0.1.0   ->  NHL94Recomp-v0.1.0-win64.zip
REM
REM Uses the engine's allowlist packager, which REFUSES if a ROM, save, dump,
REM log or build junk would land in the zip. Requires a prior
REM _build_release.bat (GEN_ENABLE_TRACE=OFF build in build-release\).
REM See segagenesisrecomp\RELEASING.md for the full checklist.
setlocal
set "HERE=%~dp0"
if "%~1"=="" (
    echo usage: _package_release.bat ^<version^>   e.g. 0.1.0
    exit /b 2
)
set "VER=%~1"
set "EXE=%HERE%build-release\Release\NHL94Recomp.exe"
if not exist "%EXE%" (
    echo [package] %EXE% not found. Run _build_release.bat first.
    exit /b 1
)
set "ENGINE=%HERE%segagenesisrecomp"
if defined GENESIS_RECOMP_ROOT set "ENGINE=%GENESIS_RECOMP_ROOT%"

python "%ENGINE%\tools\package_release.py" ^
    --exe     "%EXE%" ^
    --extra   "%HERE%build-release\Release\SDL2.dll" "%HERE%release\settings.ini" ^
    --license "%HERE%LICENSE" ^
    --notices "%ENGINE%\THIRD-PARTY-LICENSES.md" ^
    --readme  "%HERE%release\README.txt" ^
    --out     "%HERE%NHL94Recomp-v%VER%-win64.zip"
if errorlevel 1 exit /b 1
echo [package] OK: %HERE%NHL94Recomp-v%VER%-win64.zip
