# -*- mode: python ; coding: utf-8 -*-
"""Especificación PyInstaller para Sistema de Trámites Sultana (Windows onedir)."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

project_root = Path(__file__).resolve().parent

block_cipher = None


def _append_if_exists(collection, source_path: Path, target_dir: str) -> None:
    if source_path.exists():
        collection.append((str(source_path), target_dir))


def _collect_templates(template_dir: Path, target_dir: str, collection) -> None:
    if not template_dir.exists():
        return
    for template_file in template_dir.glob("*.docx"):
        collection.append((str(template_file), target_dir))


datas = []
_append_if_exists(datas, project_root / "app" / "config" / "documentos_config.json", "app/config")
_collect_templates(project_root / "app" / "assets" / "templates", "app/assets/templates", datas)

datas += collect_data_files("customtkinter")
datas += collect_data_files("tkcalendar")
datas += collect_data_files("babel")

hiddenimports = [
    "customtkinter",
    "darkdetect",
    "tkcalendar",
    "babel",
    "babel.dates",
    "babel.numbers",
    "babel.localedata",
    "win32com",
    "win32com.client",
    "pythoncom",
    "pywintypes",
]

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SistemaTramitesSultana",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign=None,
    icon=None,
)

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
