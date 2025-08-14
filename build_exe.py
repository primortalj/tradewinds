"""
Build script to create TradeWinds Windows executable
Requires: pip install cx_Freeze
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning
build_options = {
    'packages': ['tkinter'],
    'excludes': ['matplotlib', 'numpy', 'PIL'],
    'include_files': []
}

# GUI applications require a different base on Windows
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('tradewinds_gui.py', 
              base=base, 
              target_name='TradeWinds.exe',
              icon=None)  # You can add an .ico file here if you have one
]

setup(
    name='TradeWinds',
    version='1.0',
    description='Space Trading Adventure Game',
    options={'build_exe': build_options},
    executables=executables
)