@echo off
echo TradeWinds - Choose Your Version
echo ================================
echo.
echo 1. Accessible Edition (TTS, large fonts, multiplayer-ready)
echo 2. Desktop Text Adventure (Windows GUI with retro terminal)  
echo 3. Pure Text Adventure (Classic command-line parser)
echo 4. Original GUI (Graphical trading interface)
echo 5. Simple CLI (Basic command-line version)
echo.

choice /c 12345 /n /m "Select version (1, 2, 3, 4, or 5): "

if %errorlevel%==1 (
    echo Starting Accessible Edition...
    python tradewinds_accessible.py
) else if %errorlevel%==2 (
    echo Starting Desktop Text Adventure...
    python tradewinds_desktop.py
) else if %errorlevel%==3 (
    echo Starting Pure Text Adventure...
    python tradewinds_adventure.py
) else if %errorlevel%==4 (
    echo Starting Original GUI...
    python tradewinds_gui.py
) else (
    echo Starting Simple CLI...
    python tradewinds.py
)

pause