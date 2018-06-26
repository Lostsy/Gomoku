# -*- mode: python -*-

block_cipher = None


a = Analysis(['fighting_random_log.py', 'gomoku_util.py', 'pisqpipe_log.py'],
             pathex=['C:\\Users\\zkdin\\Documents\\Programming\\python\\AI\\Gomoku\\Gomoku\\fighting_random'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pbrain-fighting-random-log.exe',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
