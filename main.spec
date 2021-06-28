# -*- mode: python ; coding: utf-8 -*-

import eel
import os
import platform

block_cipher = None

if platform.system() == "Windows":
    driver_extension = ".exe"
else:
    driver_extension = ""

a = Analysis(['main.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[(eel.__file__.replace("__init__.py", "eel.js"), 'eel'), ('web', 'web'), ('lib/chromedriver'+driver_extension, 'lib')],
             hiddenimports=['bottle_websocket'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='Downloader.app',
             icon=None,
             bundle_identifier=None)
