# main.spec
block_cipher = None

a = Analysis(
    ['main.py'],  # your Flask entrypoint
    pathex=[],
    binaries=[],
    datas=[
        ('data/papers.json', 'data'),
        ('data/index.idx', 'data'),
        ('data/embeddings.npy', 'data'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='research_recommender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,   # change to False if you don’t want a terminal window
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='research_recommender'
)
