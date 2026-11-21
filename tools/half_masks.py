"""Üst yüzey maskelerini yarı çözünürlüğe indirir (yumuşak oldukları için kayıp görünmez)."""
import glob, json, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for mp in glob.glob(os.path.join(ROOT, 'assets', 'sprites', 'm_*_meta.json')):
    m = json.load(open(mp)); sp = mp.replace('_meta.json', '_sheet.webp'); im = Image.open(sp)
    if m.get('half'): continue
    fw, fh = max(1, m['fw']//2), max(1, m['fh']//2)
    out = Image.new('RGBA', (fw*m['n'], fh))
    for i in range(m['n']): out.paste(im.crop((i*m['fw'], 0, (i+1)*m['fw'], m['fh'])).resize((fw, fh), Image.LANCZOS), (i*fw, 0))
    out.save(sp, 'WEBP', quality=60, method=6)
    k = fw/m['fw']; m.update(fw=fw, fh=fh, ppu=m['ppu']*k, ox=m['ox']*k, oy=m['oy']*k, half=1); json.dump(m, open(mp, 'w'))
print('ok')
