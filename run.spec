# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=[],
             binaries=[],
             datas=[('imgs\\698_v5_b.png', 'imgs'), ('imgs\\698_v5_o.png', 'imgs'), ('imgs\\alipay.jpg', 'imgs'), ('docs\\dev_log.html', 'docs'), ('styles\\white_blue.qss', 'styles')],
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
          name='698master',
          debug=False,
          strip=False,
          upx=True,
          console=False ,
          icon='imgs\\logo.ico')
