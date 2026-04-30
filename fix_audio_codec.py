"""
Fix audio playback on projectors by converting embedded .m4a files to .wav
inside Final_Presentation_Fixed.pptx, producing Final_Presentation_Projector.pptx
"""

import zipfile, shutil, os, subprocess, re, tempfile

INPUT  = 'Final_Presentation_Fixed.pptx'
OUTPUT = 'Final_Presentation_Projector.pptx'
TMPDIR = tempfile.mkdtemp()

print(f'Unpacking {INPUT} ...')
with zipfile.ZipFile(INPUT, 'r') as z:
    z.extractall(TMPDIR)

# ── Find all .m4a files ────────────────────────────────────────────────────────
media_dir = os.path.join(TMPDIR, 'ppt', 'media')
m4a_files = [f for f in os.listdir(media_dir) if f.endswith('.m4a')]
print(f'Found {len(m4a_files)} .m4a files: {m4a_files}')

conversions = {}   # old_name -> new_name

for m4a in m4a_files:
    wav_name = m4a.replace('.m4a', '.wav')
    src = os.path.join(media_dir, m4a)
    dst = os.path.join(media_dir, wav_name)
    print(f'  Converting {m4a} → {wav_name} ...')
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', src, '-ar', '44100', '-ac', '2',
         '-acodec', 'pcm_s16le', dst],
        capture_output=True
    )
    if result.returncode != 0:
        print(f'  ERROR: {result.stderr.decode()[-300:]}')
    else:
        size_mb = os.path.getsize(dst) / 1024 / 1024
        print(f'  Done  → {wav_name}  ({size_mb:.1f} MB)')
        os.remove(src)          # remove original m4a
        conversions[m4a] = wav_name

print(f'\nConverted {len(conversions)} files.')

# ── Patch all XML files that reference old filenames ─────────────────────────
def patch_file(path, conversions):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    changed = False
    for old, new in conversions.items():
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed

patched = 0
for root, dirs, files in os.walk(TMPDIR):
    for fname in files:
        if fname.endswith('.xml') or fname.endswith('.rels'):
            fpath = os.path.join(root, fname)
            if patch_file(fpath, conversions):
                patched += 1
                print(f'  Patched: {os.path.relpath(fpath, TMPDIR)}')

# ── Update [Content_Types].xml ───────────────────────────────────────────────
ct_path = os.path.join(TMPDIR, '[Content_Types].xml')
with open(ct_path, 'r', encoding='utf-8') as f:
    ct = f.read()

# Remove m4a entry, add wav entry if not present
ct = re.sub(r'<Default[^>]*Extension="m4a"[^/]*/>', '', ct)
if 'Extension="wav"' not in ct:
    wav_ct = '<Default Extension="wav" ContentType="audio/wav"/>'
    ct = ct.replace('</Types>', f'  {wav_ct}\n</Types>')
with open(ct_path, 'w', encoding='utf-8') as f:
    f.write(ct)
print(f'\nUpdated [Content_Types].xml  (m4a → wav)')

# ── Repack into new PPTX ──────────────────────────────────────────────────────
print(f'\nRepacking into {OUTPUT} ...')
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

with zipfile.ZipFile(OUTPUT, 'w', compression=zipfile.ZIP_DEFLATED,
                     compresslevel=6) as zout:
    for root, dirs, files in os.walk(TMPDIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            arcname = os.path.relpath(fpath, TMPDIR)
            zout.write(fpath, arcname)

shutil.rmtree(TMPDIR)

size_mb = os.path.getsize(OUTPUT) / 1024 / 1024
print(f'\nDone!  {OUTPUT}  ({size_mb:.1f} MB)')
print('WAV audio is codec-free — will play on any Windows projector.')
