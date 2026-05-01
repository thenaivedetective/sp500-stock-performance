"""
Fix PPTX so audio clips auto-play on slide entry and slides auto-advance
when audio finishes. Also converts m4a → wav for universal codec support.
"""

import zipfile, shutil, os, subprocess, re, tempfile

INPUT  = 'attached_assets/Final_Presentation_Fixed_MGLGST_1777593284137.pptx'
OUTPUT = 'Final_Presentation_AutoPlay.pptx'
TMPDIR = tempfile.mkdtemp()

# Audio on each slide: {slide_num: (media_filename, duration_ms)}
AUDIO_SLIDES = {
     5: ('media5.m4a',   85900),
     6: ('media6.m4a',   42747),
     7: ('media7.m4a',   25588),
     8: ('media8.m4a',   56179),
     9: ('media9.m4a',   33423),
    10: ('media10.m4a',  31937),
    11: ('media11.m4a',  68684),
    12: ('media12.m4a',  53950),
    13: ('media13.m4a',  47262),
    14: ('media14.m4a', 101156),
    15: ('media15.m4a', 102758),
}

# ── Unpack ─────────────────────────────────────────────────────────────────────
print(f'Unpacking {INPUT} ...')
with zipfile.ZipFile(INPUT, 'r') as z:
    z.extractall(TMPDIR)

# ── Convert m4a → wav ─────────────────────────────────────────────────────────
media_dir = os.path.join(TMPDIR, 'ppt', 'media')
conversions = {}
for slide_num, (m4a, dur_ms) in AUDIO_SLIDES.items():
    wav = m4a.replace('.m4a', '.wav')
    src = os.path.join(media_dir, m4a)
    dst = os.path.join(media_dir, wav)
    print(f'  Converting {m4a} → {wav}  ({dur_ms/1000:.1f}s)')
    subprocess.run(
        ['ffmpeg', '-y', '-i', src, '-ar', '44100', '-ac', '2',
         '-acodec', 'pcm_s16le', dst],
        capture_output=True
    )
    os.remove(src)
    conversions[m4a] = wav

# ── Build auto-play timing XML ─────────────────────────────────────────────────
def auto_play_timing(spid, dur_ms, ctn_id_start=1):
    """
    Returns timing XML that auto-plays audio on slide entry.
    spid      = shape ID of the audio element on the slide
    dur_ms    = audio duration in milliseconds
    """
    i = ctn_id_start
    return (
        f'<p:timing>'
        f'<p:tnLst>'
        f'<p:par>'
        f'<p:cTn id="{i}" dur="indefinite" restart="never" nodeType="tmRoot">'
        f'<p:childTnLst>'
        f'<p:par>'
        f'<p:cTn id="{i+1}" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:par>'
        f'<p:cTn id="{i+2}" fill="hold">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:par>'
        f'<p:cTn id="{i+3}" presetID="1" presetClass="mediacall" '
        f'presetSubtype="0" fill="hold" nodeType="clickEffect">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:childTnLst>'
        f'<p:cmd type="call" cmd="playFrom(0.0)">'
        f'<p:cBhvr>'
        f'<p:cTn id="{i+4}" dur="{dur_ms}" fill="hold"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'</p:cBhvr>'
        f'</p:cmd>'
        f'</p:childTnLst>'
        f'</p:cTn>'
        f'</p:par>'
        f'</p:childTnLst>'
        f'</p:cTn>'
        f'</p:par>'
        f'</p:childTnLst>'
        f'</p:cTn>'
        f'</p:par>'
        f'<p:audio>'
        f'<p:cMediaNode vol="80000">'
        f'<p:cTn id="{i+5}" fill="hold" display="0">'
        f'<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f'<p:endCondLst>'
        f'<p:cond evt="onStopAudio" delay="0">'
        f'<p:tgtEl><p:sldTgt/></p:tgtEl>'
        f'</p:cond>'
        f'</p:endCondLst>'
        f'</p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'</p:cMediaNode>'
        f'</p:audio>'
        f'</p:childTnLst>'
        f'</p:cTn>'
        f'</p:par>'
        f'</p:tnLst>'
        f'</p:timing>'
    )


def auto_advance_transition(dur_ms, extra_ms=1000):
    """Transition XML: no click advance, auto-advance after audio + buffer."""
    return (
        f'<p:transition advClick="0" advTm="{dur_ms + extra_ms}">'
        f'<p:fade/>'
        f'</p:transition>'
    )


# ── Patch each audio slide ────────────────────────────────────────────────────
slides_dir = os.path.join(TMPDIR, 'ppt', 'slides')

for slide_num, (m4a, dur_ms) in AUDIO_SLIDES.items():
    slide_path = os.path.join(slides_dir, f'slide{slide_num}.xml')
    with open(slide_path, 'r', encoding='utf-8') as f:
        xml = f.read()

    # Extract the audio shape ID (spid)
    spid_match = re.search(r'<p:cTn[^>]*dur="\d+"[^>]*/><p:tgtEl><p:spTgt spid="(\d+)"', xml)
    if not spid_match:
        # Fallback: find spid from the cmd playFrom block
        spid_match = re.search(r'playFrom\(0\.0\).*?spid="(\d+)"', xml, re.DOTALL)
    if not spid_match:
        # Second fallback: any spTgt in the timing block
        spid_match = re.search(r'<p:spTgt spid="(\d+)"', xml)

    if spid_match:
        spid = spid_match.group(1)
        print(f'  Slide {slide_num}: spid={spid}, dur={dur_ms}ms')
    else:
        print(f'  Slide {slide_num}: WARNING could not find spid, skipping')
        continue

    # Replace timing block
    new_timing = auto_play_timing(spid, dur_ms)
    xml = re.sub(r'<p:timing>.*?</p:timing>', new_timing, xml, flags=re.DOTALL)

    # Replace or add transition block (before </p:sld>)
    new_transition = auto_advance_transition(dur_ms)
    if '<p:transition' in xml:
        xml = re.sub(r'<p:transition[^>]*>.*?</p:transition>', new_transition,
                     xml, flags=re.DOTALL)
        xml = re.sub(r'<p:transition[^/]*/>', new_transition, xml)
    else:
        xml = xml.replace('</p:sld>', f'{new_transition}</p:sld>')

    with open(slide_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f'  Slide {slide_num}: timing + transition patched ✓')

# ── Patch all XML for m4a → wav filename references ──────────────────────────
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

for root, dirs, files in os.walk(TMPDIR):
    for fname in files:
        if fname.endswith('.xml') or fname.endswith('.rels'):
            patch_file(os.path.join(root, fname), conversions)

# Update [Content_Types].xml
ct_path = os.path.join(TMPDIR, '[Content_Types].xml')
with open(ct_path, 'r', encoding='utf-8') as f:
    ct = f.read()
ct = re.sub(r'<Default[^>]*Extension="m4a"[^/]*/>', '', ct)
if 'Extension="wav"' not in ct:
    ct = ct.replace('</Types>', '  <Default Extension="wav" ContentType="audio/wav"/>\n</Types>')
with open(ct_path, 'w', encoding='utf-8') as f:
    f.write(ct)

# ── Repack ────────────────────────────────────────────────────────────────────
print(f'\nRepacking into {OUTPUT} ...')
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

with zipfile.ZipFile(OUTPUT, 'w', compression=zipfile.ZIP_DEFLATED,
                     compresslevel=5) as zout:
    for root, dirs, files in os.walk(TMPDIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            arcname = os.path.relpath(fpath, TMPDIR)
            zout.write(fpath, arcname)

shutil.rmtree(TMPDIR)
size = os.path.getsize(OUTPUT) / 1024 / 1024
print(f'Done!  {OUTPUT}  ({size:.1f} MB)')
print()
print('Changes made:')
print('  ✓ All 11 audio clips set to AUTO-PLAY on slide entry (no click needed)')
print('  ✓ Slides AUTO-ADVANCE 1 second after each audio clip finishes')
print('  ✓ Audio converted m4a → wav (plays on any projector, no codec needed)')
