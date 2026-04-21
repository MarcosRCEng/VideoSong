# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path


def get_packaged_binary(path_value, binary_name):
    if not path_value:
        return []

    binary_path = Path(path_value)
    if not binary_path.exists():
        return []

    return [(str(binary_path), ".")]


packaged_binaries = []
packaged_binaries += get_packaged_binary(os.environ.get("VIDEOSONG_FFMPEG_PATH"), "ffmpeg")
packaged_binaries += get_packaged_binary(os.environ.get("VIDEOSONG_FFPROBE_PATH"), "ffprobe")


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=packaged_binaries,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VideoSong',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
