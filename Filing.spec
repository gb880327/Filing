# -*- mode: python -*-
APP_NAME='Filing'
block_cipher = None


a = Analysis(['app.py'],
             pathex=['/Users/rookie/Workspace/python/organizeFile'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='Filing',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='/Users/rookie/Workspace/python/organizeFile/icon/favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Filing')
app = BUNDLE(coll,
             name='Filing.app',
             icon='/Users/rookie/Workspace/python/organizeFile/icon/favicon.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleName': APP_NAME,
                'CFBundleDisplayName': APP_NAME,
                'CFBundleGetInfoString': "Making Filing",
                'CFBundleIdentifier': "rookie.filing",
                'CFBundleVersion': "0.1.0",
                'CFBundleShortVersionString': "0.1.0",
                'NSHumanReadableCopyright': "Copyright © 2018, Rookie, All Rights Reserved",
                'NSHighResolutionCapable': 'True',
                })
