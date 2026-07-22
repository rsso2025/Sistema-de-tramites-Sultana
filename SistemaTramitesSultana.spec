# -*- mode: python ; coding: utf-8 -*-
# PyInstaller specification for Sistema de Trámites Sultana
# Python 3.14 / PyInstaller 6.21.x - Windows onedir
# Stable production build – no UPX, no excludes, no runtime hooks.

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

# ----------------------------------------------------------------------------
# Project root detection (always run from project root via:
# python -m PyInstaller SistemaTramitesSultana.spec)
# ----------------------------------------------------------------------------
PROJECT_ROOT = Path.cwd().resolve()

# ----------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------
def add_file_if_exists(collection, source_path: Path, target_dir: str) -> None:
    """Add a single file to the datas list if it exists."""
    if source_path.exists():
        collection.append((str(source_path), target_dir))

def add_files_from_pattern(collection, source_dir: Path, pattern: str, target_dir: str) -> None:
    """Add all files matching a pattern from a directory to datas."""
    if source_dir.exists():
        for file_path in source_dir.glob(pattern):
            collection.append((str(file_path), target_dir))

# ----------------------------------------------------------------------------
# Datas collection
# ----------------------------------------------------------------------------
datas = []

# Configuration file
config_file = PROJECT_ROOT / "app" / "config" / "documentos_config.json"
add_file_if_exists(datas, config_file, "app/config")

# Word templates
templates_dir = PROJECT_ROOT / "app" / "assets" / "templates"
add_files_from_pattern(datas, templates_dir, "*.docx", "app/assets/templates")

# Third-party data files (using collect_data_files for each)
datas += collect_data_files("customtkinter")
datas += collect_data_files("tkcalendar")
datas += collect_data_files("babel")

# ----------------------------------------------------------------------------
# Hidden imports (strictly necessary)
# ----------------------------------------------------------------------------
hiddenimports = [
    "darkdetect",          # dependency of customtkinter on Windows
    "win32com",
    "win32com.client",
    "pythoncom",
    "pywintypes",
]

# ----------------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------------
a = Analysis(
    scripts=["main.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],           # No modules excluded to ensure maximum compatibility
)

# ----------------------------------------------------------------------------
# PYZ (bytecode archive)
# ----------------------------------------------------------------------------
pyz = PYZ(a.pure, a.zipped_data)

# ----------------------------------------------------------------------------
# EXE (main executable)
# ----------------------------------------------------------------------------
# Attempt to load icon if it exists, otherwise keep None.
icon_path = PROJECT_ROOT / "assets" / "icon.ico"
icon_file = str(icon_path) if icon_path.exists() else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SistemaTramitesSultana",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                     # Disabled for stability
    console=False,                 # Windowed GUI application
    disable_windowed_traceback=False,
    icon=icon_file,                # Placeholder: set to your .ico path
    version=None,                  # Placeholder: add VSVersionInfo file
    manifest=None,                 # Placeholder: add custom manifest if needed
)

# ----------------------------------------------------------------------------
# COLLECT (onedir bundle)
# ----------------------------------------------------------------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="SistemaTramitesSultana",
)

# ----------------------------------------------------------------------------
# Notes for future enhancements:
# - To add a version info file, set `version` to a VSVersionInfo object.
# - To add a custom manifest, set `manifest` to a file path.
# - The icon is automatically used if assets/icon.ico exists.
# - No runtime hooks are needed; PathManager handles resource resolution.
# ----------------------------------------------------------------------------