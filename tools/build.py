"""Sprite'ları şablona gömer ve oynanabilir tek dosyalık index.html üretir.
Kullanım: python3 tools/build.py
"""
import json, base64, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'src', 'index.template.html'), encoding='utf-8').read()
data = {}
for m in sorted(glob.glob(os.path.join(ROOT, 'assets', 'sprites', '*_meta.json'))):
    meta = json.load(open(m)); sid = os.path.basename(m)[:-len('_meta.json')]; meta['id'] = sid
    raw = open(os.path.join(ROOT, 'assets', 'sprites', f'{sid}_sheet.webp'), 'rb').read()
    meta['src'] = 'data:image/webp;base64,' + base64.b64encode(raw).decode()
    for k, n in (('ppu', 3), ('ox', 2), ('oy', 2)): meta[k] = round(meta[k], n)
    data[sid] = meta
assert src.count('/*SPRITES*/{}') == 1
LAT = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
LATX = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'
fonts = ''
for fn, rng in (('fredoka-latin-ext-wght-normal.woff2', LATX), ('fredoka-latin-wght-normal.woff2', LAT)):
    fp = os.path.join(ROOT, 'assets', 'fonts', fn)
    if os.path.exists(fp):
        b64 = base64.b64encode(open(fp, 'rb').read()).decode()
        fonts += "@font-face{font-family:'Fredoka';font-style:normal;font-display:swap;font-weight:300 700;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s}\n" % (b64, rng)
src = src.replace('/*FONTS*/', fonts)
sp_ = os.path.join(ROOT, 'assets', 'ui', 'sand.webp')
if os.path.exists(sp_):
    src = src.replace('/*SAND*/', 'data:image/webp;base64,' + base64.b64encode(open(sp_, 'rb').read()).decode())
lp = os.path.join(ROOT, 'assets', 'ui', 'logo.webp')
if os.path.exists(lp):
    src = src.replace('/*LOGO*/', 'data:image/webp;base64,' + base64.b64encode(open(lp, 'rb').read()).decode())
out = src.replace('/*SPRITES*/{}', json.dumps(data, separators=(',', ':')))
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)
print(f'index.html: {len(out)//1024} KB, {len(data)} balık sprite')
