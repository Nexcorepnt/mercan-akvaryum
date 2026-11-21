"""Logo son hali (dış hat + gölge), oyun içi logo (webp), Google Play ikon (512) ve tanıtım görseli (1024x500).
Kullanım: python tools/store_assets.py   (Pillow + numpy gerekli)
"""
import os, json, math, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageChops, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HI = os.path.join(ROOT, 'build', 'hires'); SPR = os.path.join(ROOT, 'assets', 'sprites')
UI = os.path.join(ROOT, 'assets', 'ui'); ST = os.path.join(ROOT, 'store')
os.makedirs(UI, exist_ok=True); os.makedirs(ST, exist_ok=True)

def outline(im, r, col):
    a = im.split()[3]
    big = a.filter(ImageFilter.MaxFilter(r*2+1)).filter(ImageFilter.GaussianBlur(1.2))
    base = Image.new('RGBA', im.size, col); base.putalpha(big)
    return base

def hires(name):
    im = Image.open(os.path.join(HI, name)).convert('RGBA'); a = np.asarray(im).copy()
    a[..., 3] = np.where(a[..., 3] < 10, 0, a[..., 3]); im = Image.fromarray(a, 'RGBA'); return im.crop(im.getbbox())

def logo_final():
    im = hires('logo.png'); al = im.split()[3]
    im = ImageEnhance.Contrast(ImageEnhance.Color(im.convert('RGB')).enhance(1.45)).enhance(1.08).convert('RGBA'); im.putalpha(al)
    pad = 40; W, H = im.width+pad*2, im.height+pad*2
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); src = Image.new('RGBA', (W, H), (0, 0, 0, 0)); src.paste(im, (pad, pad), im)
    sh = outline(src, 16, (2, 14, 32, 140)).filter(ImageFilter.GaussianBlur(10)); canvas.alpha_composite(sh, (0, 10))
    canvas.alpha_composite(outline(src, 13, (7, 26, 51, 255)))
    canvas.alpha_composite(outline(src, 5, (255, 255, 255, 255)))
    canvas.alpha_composite(src)
    bb = canvas.getbbox(); canvas = canvas.crop(bb)
    canvas.save(os.path.join(ST, 'logo.png'))
    small = canvas.copy(); small.thumbnail((900, 900), Image.LANCZOS)
    small.save(os.path.join(UI, 'logo.webp'), 'WEBP', quality=88, method=6)
    return canvas

def water_bg(w, h, top=(70, 205, 240), mid=(22, 120, 180), bot=(6, 44, 82), seed=1):
    y = np.linspace(0, 1, h)[:, None]
    def lerp(a, b, t): return np.array(a)*(1-t)+np.array(b)*t
    col = np.where(y[..., None] < .45, lerp(top, mid, y[..., None]/.45), lerp(mid, bot, (y[..., None]-.45)/.55))
    arr = np.repeat(col, w, 1).astype('uint8')
    img = Image.fromarray(arr, 'RGB').convert('RGBA')
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); r = random.Random(seed)
    for i in range(6):
        x = r.uniform(.05, .95)*w; ww = r.uniform(.04, .09)*w; sk = r.uniform(-.1, .2)*w
        d.polygon([(x-ww/2, 0), (x+ww/2, 0), (x+ww*1.6+sk, h), (x-ww*1.2+sk, h)], fill=(220, 250, 255, 26))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(w*.01)))
    return img

def bubbles(img, n, seed=3, rmax=10):
    d = ImageDraw.Draw(img, 'RGBA'); r = random.Random(seed); w, h = img.size
    for _ in range(n):
        x, y, rr = r.uniform(0, w), r.uniform(0, h*.85), r.uniform(2, rmax)
        d.ellipse([x-rr, y-rr, x+rr, y+rr], outline=(230, 250, 255, 170), width=max(1, int(rr/4)), fill=(255, 255, 255, 25))
        d.ellipse([x-rr*.55, y-rr*.6, x-rr*.15, y-rr*.2], fill=(255, 255, 255, 200))

def sand(img, y0, seed=5):
    w, h = img.size; d = ImageDraw.Draw(img, 'RGBA'); r = random.Random(seed)
    pts = [(x, y0+math.sin(x*.012)*6+math.sin(x*.031)*4) for x in range(0, w+10, 10)]
    d.polygon(pts+[(w, h), (0, h)], fill=(214, 192, 140, 255))
    cols = [(239, 224, 184), (194, 164, 110), (156, 129, 82), (220, 204, 163), (125, 106, 74), (246, 234, 208)]
    for _ in range(int(w*(h-y0)/30)):
        x = r.uniform(0, w); yy = r.uniform(y0, h); s = r.uniform(1.5, 4)
        d.ellipse([x-s, yy-s*.6, x+s, yy+s*.6], fill=cols[r.randrange(len(cols))]+(255,))
    g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for i in range(30): gd.line([(0, y0-15+i), (w, y0-15+i)], fill=(10, 50, 80, int(90*(1-i/30))))
    img.alpha_composite(g)

def sprite(name, frame=0):
    m = json.load(open(os.path.join(SPR, f'{name}_meta.json'))); im = Image.open(os.path.join(SPR, f'{name}_sheet.webp')).convert('RGBA')
    return im.crop((frame*m['fw'], 0, (frame+1)*m['fw'], m['fh']))

def paste_h(img, im, cx, by, height, flip=False):
    k = height/im.height; im = im.resize((max(1, int(im.width*k)), int(height)), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    img.alpha_composite(im, (int(cx-im.width/2), int(by-im.height)))

def paste_c(img, im, cx, cy, width, flip=False, rot=0):
    k = width/im.width; im = im.resize((int(width), max(1, int(im.height*k))), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    img.alpha_composite(im, (int(cx-im.width/2), int(cy-im.height/2)))

def icon(logo):
    S = 1024
    img = Image.new('RGBA', (S, S)); y = np.linspace(0, 1, S)
    xx, yy = np.meshgrid(np.linspace(-1, 1, S), np.linspace(-1, 1, S))
    rr = np.sqrt((xx+.15)**2+(yy+.35)**2)
    t = np.clip(rr/1.6, 0, 1)[..., None]
    col = np.array([95, 225, 245])*(1-t)+np.array([8, 60, 120])*t
    img = Image.fromarray(col.astype('uint8'), 'RGB').convert('RGBA')
    ov = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x, w in [(.22, .07), (.45, .1), (.7, .06)]:
        d.polygon([(x*S, 0), ((x+w)*S, 0), ((x+w*2.2)*S, S), ((x-w*.6)*S, S)], fill=(230, 252, 255, 40))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(18)))
    # mercan tabanı
    cor = sprite('d_coral'); paste_h(img, cor, S*.16, S*1.02, S*.42); paste_h(img, cor, S*.88, S*1.03, S*.32, flip=True)
    fish = hires('clown_00.png')
    sh = outline(fish, 3, (0, 20, 50, 70)).filter(ImageFilter.GaussianBlur(30))
    paste_c(img, sh, S*.53, S*.57, S*.78, rot=8); paste_c(img, fish, S*.5, S*.5, S*.78, rot=8)
    bubbles(img, 14, seed=9, rmax=26)
    img = img.convert('RGB').resize((512, 512), Image.LANCZOS)
    img.save(os.path.join(ST, 'icon-512.png'), optimize=True)
    print('icon', os.path.getsize(os.path.join(ST, 'icon-512.png'))//1024, 'KB')

def feature(logo):
    W, H = 1024, 500
    img = water_bg(W, H); sand(img, H*.8)
    paste_h(img, sprite('d_castle'), W*.9, H*.9, H*.5)
    paste_h(img, sprite('d_coral'), W*.07, H*.92, H*.36)
    paste_h(img, sprite('d_chest'), W*.73, H*.94, H*.2)
    paste_h(img, sprite('d_rock'), W*.2, H*.95, H*.14)
    for nm, cx, cy, wdt, fl in [('koi', .14, .27, 220, False), ('tang', .87, .22, 140, True), ('angel', .06, .6, 85, False), ('betta', .25, .74, 115, False), ('gold_r', .67, .75, 105, True), ('jelly', .6, .14, 48, False)]:
        paste_c(img, hires(f'{nm}_00.png'), W*cx, H*cy, wdt, flip=fl)
    bubbles(img, 40, seed=4, rmax=9)
    lg = logo.copy(); lg.thumbnail((int(W*.56), int(H*.48)), Image.LANCZOS)
    img.alpha_composite(lg, (int(W*.5-lg.width/2), int(H*.47-lg.height/2)))
    img.convert('RGB').save(os.path.join(ST, 'feature-1024x500.png'), optimize=True)
    print('feature ok')

if __name__ == '__main__':
    lg = logo_final(); icon(lg); feature(lg)
