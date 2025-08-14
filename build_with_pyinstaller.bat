@echo off
echo Building TradeWinds Windows Executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

echo Building executable...
pyinstaller --onefile --windowed --name TradeWinds tradewinds_gui.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Build successful!
    echo Executable created at: dist\TradeWinds.exe
    echo.
) else (
    echo ❌ Build failed!
    echo.
)

pause