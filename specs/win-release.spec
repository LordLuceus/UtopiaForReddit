# -*- mode: python -*-

import os, importlib.util

spec = importlib.util.spec_from_file_location("common", os.path.join(os.getcwd(), "specs", "common.py"))
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

block_cipher = None


a = Analysis(['../src\\UtopiaForReddit.py'],
             pathex=['../src/'],
             binaries=[],
             datas=common.datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=common.excludes,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='win')
