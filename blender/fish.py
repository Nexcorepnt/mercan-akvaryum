"""Mercan Akvaryum - Blender ile 2.5D balık sprite üretici.
Her tür: prosedürel 3D gövde + yüzgeçler + gözler, PIL ile desen dokusu,
yüzme döngüsü kareleri (Cycles) -> WebP sprite sheet + meta JSON.
Kullanım: python fish.py <tur_id|all> [kare_sayisi] [genislik] [samples]
"""
import bpy, math, sys, json, os, time, random
import numpy as np
from mathutils import Vector, Matrix
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'build', 'frames')      # ara kareler (git'e girmez)
SPR = os.path.join(ROOT, 'assets', 'sprites')    # sprite sheet + meta
TEX = os.path.join(ROOT, 'build', 'tex')
os.makedirs(OUT, exist_ok=True); os.makedirs(SPR, exist_ok=True); os.makedirs(TEX, exist_ok=True)

SPECIES = [
 dict(id='neon',  len=44, hb=.21, ped=.16, tail='fork',  dors=7,  anal=7,  c1='#c9d4de', c2='#5d6c7c', c3='#f3f6f9', fin=(225,235,245,.35), pat='neon',  wk=.085, amp=.11, eyeK=.075, eye='#c8dcff'),
 dict(id='gold',  len=64, hb=.33, ped=.16, tail='veil',  dors=15, anal=9,  c1='#ff8c1a', c2='#d9480f', c3='#ffe0b2', fin=(255,140,40,.62), pat='gold', wk=.17, amp=.09),
 dict(id='clown', len=60, hb=.31, ped=.20, tail='round', dors=11, anal=9,  c1='#ff7a00', c2='#e05200', c3='#ffb04d', fin=(255,110,0,.92), finEdge=(17,17,17), pat='clown', wk=.14, amp=.1),
 dict(id='angel', len=60, hb=.56, ped=.14, tail='fork',  dors=42, anal=42, dorsBack=.62, c1='#e2e6ea', c2='#9aa3ad', c3='#f8f9fb', fin=(205,212,222,.6), pat='angel', wk=.06, amp=.07),
 dict(id='tang',  len=74, hb=.38, ped=.17, tail='lunate',dors=10, anal=9,  c1='#2b6fe8', c2='#123d9e', c3='#5c9cff', fin=(30,70,200,.92), finEdge=(10,20,48), tailCol=(255,210,31), pecCol=(255,214,40,.9), pat='tang', wk=.1, amp=.09),
 dict(id='betta', len=54, hb=.27, ped=.20, tail='betta', dors=24, anal=26, dorsBack=.55, c1='#c2185b', c2='#5c0c33', c3='#ef5d8f', fin=(150,15,75,.8), pat='betta', wk=.1, amp=.07, film=520),
 dict(id='discus',len=68, hb=.70, ped=.12, tail='round', dors=10, anal=10, c1='#e8743b', c2='#a8441a', c3='#ffb07a', fin=(220,110,50,.6), pat='discus', wk=.075, amp=.06),
 dict(id='koi',   len=104,hb=.25, ped=.16, tail='fork',  dors=10, anal=7,  c1='#fafafa', c2='#d4d4d4', c3='#ffffff', fin=(255,255,255,.55), pat='koi', wk=.15, amp=.12, barbel=True),
 dict(id='lion',  len=80, hb=.33, ped=.17, tail='round', dors=0,  anal=10, c1='#f3e3cf', c2='#a2442b', c3='#fff4e6', fin=(240,220,200,.5), pat='lion', wk=.13, amp=.06, spiky=True),
 dict(id='puffer',len=60, hb=.42, ped=.17, tail='round', dors=7,  anal=7,  c1='#d9c27a', c2='#8a7333', c3='#fbf7ea', fin=(220,200,130,.6), pat='puffer', wk=.36, amp=.05, eyeK=.085),
 dict(id='shark', len=100,hb=.2,  ped=.09, tail='shark', dors=0,  anal=4,  c1='#8796a5', c2='#55636f', c3='#f2f5f7', fin=(115,130,145,.97), pat='shark', wk=.11, amp=.1, dshape='shark', pec='wing', eyeK=.034, eye='#1e2328'),
 dict(id='seahorse', kind='seahorse', len=70, hb=.45, c1='#f2b134', c2='#b4650f', c3='#ffe39a', fin=(255,220,120,.55), amp=.02, eyeK=.03),
 dict(id='pleco', len=58, hb=.22, ped=.15, tail='lunate', dors=15, anal=0, dorsBack=.34, c1='#5b4b33', c2='#2c2318', c3='#9a8a68', fin=(88,72,50,.9), pat='pleco', wk=.25, amp=.07, flat=.55, pec='wing', eyeK=.034, eye='#c9b98a', bristle=True, patA=(238,228,196)),
 dict(id='ray', kind='ray', len=120, hb=.3, c1='#c9a35c', c2='#8a6a32', c3='#f2e6cc', amp=.06),
 dict(id='jelly', kind='jelly', len=60, hb=.6, c1='#ffb3d9', c2='#ff5fa2', c3='#fff0f7', amp=.02),
]
VARIANTS = {
 'neon':  dict(c1='#f3e7c4', c2='#b39554', c3='#fffaf0', patA=(255,205,60), patB=(255,120,40)),
 'gold':  dict(c1='#fff6ec', c2='#e3d3c0', c3='#ffffff', fin=(255,250,245,.55), pat='tancho'),
 'clown': dict(c1='#26262d', c2='#0d0d11', c3='#45454f', fin=(40,40,48,.95), finEdge=(235,235,235)),
 'angel': dict(c1='#34343c', c2='#121216', c3='#58585f', fin=(45,45,52,.8)),
 'tang':  dict(c1='#ffd21f', c2='#d9a400', c3='#fff27d', fin=(255,205,20,.95), finEdge=(200,150,0), tailCol=(255,238,160), pecCol=(255,240,160,.9), pat='none'),
 'betta': dict(c1='#2457e0', c2='#0b1f6b', c3='#6aa8ff', fin=(30,70,220,.8), film=380),
 'discus':dict(c1='#2a8fd8', c2='#145a9c', c3='#86d0ff', fin=(40,140,220,.6), patA=(255,150,60)),
 'koi':   dict(c1='#f4c84a', c2='#cf9e1f', c3='#ffeaa6', fin=(255,225,140,.55), patA=(28,28,28)),
 'lion':  dict(c1='#efe8de', c2='#2a2a2a', c3='#ffffff', patA=(22,22,22), finBand=(25,25,25)),
 'puffer':dict(c1='#a6d45f', c2='#4f7a22', c3='#f7fbe9', fin=(170,210,110,.6), patA=(40,70,20)),
 'shark': dict(c1='#f3eee8', c2='#d8cec2', c3='#ffffff', fin=(240,232,224,.97), eye='#ff4d6d'),
 'seahorse': dict(c1='#ff8fb6', c2='#c2416b', c3='#ffd6e6', fin=(255,170,200,.55)),
 'jelly': dict(c1='#8fd8ff', c2='#2a7fd8', c3='#e6f8ff'),
 'pleco': dict(c1='#f0d79c', c2='#c9a868', c3='#fff3d6', fin=(250,232,190,.85), patA=(255,252,240), eye='#e0404a'),
 'ray': dict(c1='#4a3524', c2='#2a1d12', c3='#efe2c8', ray='motoro'),
}
LEGEND = {
 'koi':     dict(c1='#ffd34d', c2='#c98a10', c3='#fff1b8', fin=(255, 205, 90, .6), patA=(205, 28, 18), metal=.55, film=300),
 'neon':    dict(c1='#eef6ff', c2='#a9bcdc', c3='#ffffff', patA=(255, 70, 210), patB=(70, 255, 190), film=650),
 'jelly':   dict(c1='#d2dcff', c2='#6a5cff', c3='#ffffff'),
 'angel':   dict(c1='#6a3fb8', c2='#2a1458', c3='#ffd86a', fin=(130, 80, 210, .72), metal=.3, film=420),
 'discus':  dict(c1='#a6f2ff', c2='#2aa8c8', c3='#f2ffff', fin=(160, 232, 255, .5), patA=(255, 255, 255), film=520),
 'shark':   dict(c1='#e2ecff', c2='#a2b8dc', c3='#ffffff', fin=(225, 236, 255, .8), eye='#6af0ff', film=300),
 'seahorse': dict(c1='#ffd34d', c2='#b07a10', c3='#fff3c0', fin=(255, 222, 120, .6)),
}
def get_species(tag):
    base = tag[:-2] if tag[-2:] in ('_r', '_l') else tag
    sp = dict(next(x for x in SPECIES if x['id'] == base))
    if tag.endswith('_r'):
        sp.update(VARIANTS[base]); sp['id'] = tag
    elif tag.endswith('_l'):
        sp.update(LEGEND[base]); sp['id'] = tag
    return sp

def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ---------------- 2D yol örnekleme (JS çizimleriyle aynı koordinatlar: x sağ, y aşağı, L=1) -------------
class P2:
    def __init__(s): s.pts = []; s.cur = (0, 0)
    def M(s, x, y): s.cur = (x, y); s.pts.append((x, y)); return s
    def L(s, x, y): return s.M(x, y)
    def Q(s, cx, cy, x, y, n=18):
        x0, y0 = s.cur
        for i in range(1, n+1):
            t = i/n; a = (1-t)**2; b = 2*(1-t)*t; c = t*t
            s.pts.append((a*x0+b*cx+c*x, a*y0+b*cy+c*y))
        s.cur = (x, y); return s
    def C(s, ax, ay, bx, by, x, y, n=24):
        x0, y0 = s.cur
        for i in range(1, n+1):
            t = i/n; m = 1-t
            s.pts.append((m**3*x0+3*m*m*t*ax+3*m*t*t*bx+t**3*x, m**3*y0+3*m*m*t*ay+3*m*t*t*by+t**3*y))
        s.cur = (x, y); return s

def body_profile(H, P):
    top = P2().M(.5, 0).C(.49, -H*.62, .28, -H, .02, -H, 200).C(-.24, -H, -.4, -P*2.2, -.5, -P, 200).pts
    bot = P2().M(-.5, P).C(-.4, P*2.2, -.24, H*.92, .02, H*.92, 200).C(.28, H*.92, .49, H*.55, .5, 0, 200).pts
    tx = np.array([p[0] for p in top]); ty = np.array([-p[1] for p in top])
    bx = np.array([p[0] for p in bot]); by = np.array([-p[1] for p in bot])
    ot = np.argsort(tx); ob = np.argsort(bx)
    ztop = lambda x: np.interp(x, tx[ot], ty[ot])
    zbot = lambda x: np.interp(x, bx[ob], by[ob])
    return ztop, zbot

def tail_outline(sp, H, P):
    w = 0.0; e = .04
    t = sp['tail']; p = P2()
    if t == 'fork':
        tl = .34; p.M(e, -P).Q(-tl*.45, -tl*.25, -tl, -tl*.62).Q(-tl*.5, 0, -tl, tl*.62).Q(-tl*.45, tl*.25, e, P)
    elif t == 'lunate':
        tl = .3; p.M(e, -P).Q(-tl*.5, -tl*.3, -tl*.95, -tl*.85).Q(-tl*.45, 0, -tl*.95, tl*.85).Q(-tl*.5, tl*.3, e, P)
    elif t == 'round':
        tl = .3; p.M(e, -P).C(-tl*.3, -tl*.75, -tl*1.05, -tl*.72, -tl*1.05, 0).C(-tl*1.05, tl*.72, -tl*.3, tl*.75, e, P)
    elif t == 'veil':
        tl = .52; v = 0
        p.M(e, -P).C(-tl*.3, -tl*.5, -tl*.8, -tl*.78, -tl*1.15, -tl*.58).C(-tl*.85, -tl*.18, -tl*.95, 0, -tl*.68, 0)
        p.C(-tl*.95, 0, -tl*.85, tl*.2, -tl*1.15, tl*.58).C(-tl*.8, tl*.78, -tl*.3, tl*.5, e, P)
    elif t == 'shark':
        p.M(e, -P).Q(-.15, -.13, -.44, -.37).Q(-.26, -.12, -.22, 0).Q(-.27, .07, -.3, .17).Q(-.12, .08, e, P)
    elif t == 'betta':
        tl = .78
        p.M(e, -P).C(-tl*.15, -tl*.75, -tl*.85, -tl*.85, -tl*1.0, -tl*.25).Q(-tl*1.08, 0, -tl*1.0, tl*.25).C(-tl*.85, tl*.85, -tl*.15, tl*.75, e, P)
    return [(x-.48, y) for x, y in p.pts], (-.45, 0)

def dorsal_outline(sp, H):
    D = sp['dors']/sp['len']; bk = sp.get('dorsBack', .4)
    p = P2().M(.15, -H*.9).Q(.04-bk*.2, -H-D*1.3, -bk, -H*.5-D*.62).Q(-(bk-.04), -H*.45, -.38, -H*.35)
    a, b = p.pts[0], p.pts[-1]
    return p.pts, ((a[0]+b[0])/2, (a[1]+b[1])/2+H*.12)

def anal_outline(sp, H):
    A = sp['anal']/sp['len']; bk = sp.get('dorsBack', .4)
    p = P2().M(-.02, H*.85).Q(-.12, H+A*1.15, -bk, H*.45+A*.6).Q(-(bk-.04), H*.4, -.38, H*.3)
    a, b = p.pts[0], p.pts[-1]
    return p.pts, ((a[0]+b[0])/2, (a[1]+b[1])/2-H*.12)

# ---------------- dokular ----------------
TW, TH = 1024, 512

def grad_rows(c2, c1, c3, H, zr):
    ys = (np.arange(TH)+.5)/TH*2-1          # -1 üst ... +1 alt  => y(2D) = ys*zr
    t = np.clip((ys*zr/H+1)/2, 0, 1)
    c2, c1, c3 = [np.array(hx(c), float) for c in (c2, c1, c3)]
    out = np.zeros((TH, 3))
    for i, tt in enumerate(t):
        if tt < .42: k = tt/.42; col = c2*(1-k)+c1*k
        elif tt < .85: k = (tt-.42)/.43; col = c1*(1-k)+c3*k
        else: col = c3
        out[i] = col
    return np.repeat(out[:, None, :], TW, 1)

def body_texture(sp, H, zr, path):
    S2 = 2
    base = grad_rows(sp['c2'], sp['c1'], sp['c3'], H, zr)
    img = Image.fromarray(base.astype('uint8'), 'RGB').resize((TW*S2, TH*S2)).convert('RGBA')
    d = ImageDraw.Draw(img, 'RGBA')
    W2, H2 = TW*S2, TH*S2
    P = lambda x, y: ((x+.5)*W2, (y/zr+1)/2*H2)
    poly = lambda pts, col: d.polygon([P(*q) for q in pts], fill=col)
    def ell(cx, cy, rx, ry, ang, col, outline=None, ow=0):
        pts = [(cx+math.cos(a)*rx*math.cos(ang)-math.sin(a)*ry*math.sin(ang), cy+math.cos(a)*rx*math.sin(ang)+math.sin(a)*ry*math.cos(ang)) for a in np.linspace(0, 2*math.pi, 90)]
        d.polygon([P(*q) for q in pts], fill=col, outline=outline, width=ow)
    def stroke(pts, col, w):
        d.line([P(*q) for q in pts], fill=col, width=int(w), joint='curve')
    pat = sp['pat']
    if pat == 'neon':
        pa = sp.get('patA'); pb = sp.get('patB', (255, 40, 64))
        poly(P2().M(.36, -H*.2).Q(0, -H*.48, -.5, -H*.12).L(-.5, H*.08).Q(0, -H*.06, .36, H*.02).pts, (*(pa or (40, 215, 255)), 255))
        poly(P2().M(.3, -H*.08).Q(0, -H*.3, -.5, -H*.02).L(-.5, H*.08).Q(0, -H*.06, .3, H*.02).pts, (*(pa or (30, 90, 255)), 200))
        poly(P2().M(.06, H*.12).Q(-.2, H*.04, -.5, H*.1).L(-.5, H*.95).Q(-.2, H*.98, .06, H*.65).pts, (*pb, 255))
    elif pat == 'gold':
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        cx, cy = P(.1, -H*.25); r = .5*W2
        for i in range(30, 0, -1):
            a = int(140*(1-i/30)); od.ellipse([cx-r*i/30, cy-r*i/30*.6, cx+r*i/30, cy+r*i/30*.6], fill=(255, 235, 130, a//6))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img, 'RGBA')
    elif pat == 'clown':
        for x, w in [(.27, .075), (0, .09), (-.37, .05)]:
            ell(x, 0, w+.012, H*1.4, 0, (17, 17, 17, 255))
            ell(x, 0, w, H*1.4, 0, (255, 255, 255, 255))
    elif pat == 'angel':
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for i in range(TH*S2//2):
            a = int(90*(1-i/(TH*S2/2))); od.line([(0, i), (W2, i)], fill=(240, 200, 90, a))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img, 'RGBA')
        for x in (.33, .06, -.24): ell(x, 0, .035, H*1.4, .12, (25, 25, 32, 230))
    elif pat == 'tang':
        stroke(P2().M(.3, -H*.32).C(0, -H*.85, -.3, -H*.62, -.5, -H*.12).pts, (10, 20, 48, 255), H*.3/zr*H2/2*1.0)
        stroke(P2().M(-.05, -H*.5).Q(-.22, H*.08, .12, H*.06).pts, (10, 20, 48, 255), H*.2/zr*H2/2)
    elif pat == 'betta':
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for i in range(W2):
            k = i/W2; od.line([(i, 0), (i, H2)], fill=(90, 60, 255, int(110*(1-k))))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img, 'RGBA')
    elif pat == 'discus':
        for i in range(-4, 5):
            pts = [(x, i*H*.22+math.sin(x*14+i)*H*.04) for x in np.linspace(.5, -.55, 60)]
            stroke(pts, (*sp.get('patA', (60, 210, 205)), 230), H*.075/zr*H2/2)
    elif pat == 'koi':
        import random; r = random.Random(7)
        for (x, y, rx, ry, a) in [(.18, -.35, .14, .55, .3), (-.12, -.15, .12, .7, -.4), (-.36, -.4, .08, .4, .2), (.36, -.5, .07, .35, 0)]:
            ell(x, y*H, rx, ry*H, a, (*sp.get('patA', (232, 64, 28)), 255))
        for (x, y) in [(-.02, -.55), (-.25, -.3), (.08, -.1)]:
            ell(x, y*H, .025, .13*H, .5, (28, 28, 28, 255))
    elif pat == 'lion':
        for i in range(15):
            x = .52-i*.075
            poly([(x, -H*1.3), (x+.035, -H*1.3), (x+.01, H*1.3), (x-.025, H*1.3)], (*sp.get('patA', (140, 40, 22)), 225))
    elif pat == 'puffer':
        import random; r = random.Random(3)
        for _ in range(40):
            x = r.uniform(-.5, .5); y = -r.uniform(-.05, .95)*H; rr = r.uniform(.01, .028)
            ell(x, y, rr, rr, 0, (*sp.get('patA', (62, 47, 18)), 255))
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        y0 = P(0, 0)[1]
        for yy in range(int(y0), H2):
            k = min(1, (yy-y0)/(H2*.12)); od.line([(0, yy), (W2, yy)], fill=(255, 255, 248, int(240*k)))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img, 'RGBA')
    elif pat == 'pleco':
        import random as _rd; rr_ = _rd.Random(11); pa = sp.get('patA', (238, 228, 196))
        pts_ = []
        for _ in range(900):
            x = rr_.uniform(-.52, .52); y = rr_.uniform(-1.25, .45)*H
            if all((x-a)**2+((y-b)/H*.1)**2 > .0012 for a, b in pts_): pts_.append((x, y))
        for x, y in pts_:
            r = rr_.uniform(.006, .011); ell(x, y, r, r*1.1, 0, (*pa, 230))
        for i in range(9):
            x = .3-i*.085; stroke([(x+.01*math.sin(t*3), -H*1.2+H*1.5*t) for t in np.linspace(0, 1, 10)], (0, 0, 0, 40), 4)
    elif pat == 'tancho':
        ell(.3, -H*.5, .09, H*.38, 0, (225, 35, 30, 255))
    elif pat == 'shark':
        poly([(.56, H*.06)] + [(x, H*.14+H*.05*math.sin(x*22)) for x in np.linspace(.5, -.56, 50)] + [(-.56, H*1.5), (.56, H*1.5)], (*hx(sp['c3']), 255))
        for i in range(5):
            gx = .23-i*.035; stroke([(gx+.012*math.sin(t*math.pi), -H*.35+H*.6*t) for t in np.linspace(0, 1, 12)], (30, 40, 50, 110), 5)
    # solungaç kapağı + ağız
    gr = min(H*.7, .2)
    stroke([(.4+math.cos(a)*gr, math.sin(a)*gr) for a in np.linspace(math.pi-.75, math.pi+.75, 30)], (0, 0, 0, 60), 5)
    stroke([(.5, H*.04), (.46, H*.1), (.43, H*.08)], (60, 20, 10, 140), 4)
    img = img.filter(ImageFilter.GaussianBlur(1.2)).resize((TW, TH), Image.LANCZOS)
    img.convert('RGB').save(path)

def fin_texture(path, base, tip, a0, a1, rays=14, edge=None, bands=None):
    w, h = 256, 128
    v = np.linspace(0, 1, h)[:, None, None]; u = np.linspace(0, 1, w)[None, :, None]
    base = np.array(base, float)[None, None, :]; tip = np.array(tip, float)[None, None, :]
    col = base*(1-v)+tip*v
    alpha = (a0*(1-v)+a1*v)[..., 0]*np.ones((1, w))
    if bands:
        st = (np.floor(v[..., 0]*bands[0]) % 2 == 0)*np.ones((1, w))
        bc = np.array(bands[1], float); col = np.where(st[..., None], bc, col)
        alpha = np.where(st, np.maximum(alpha, .8), alpha)
    if rays:
        r = .5+.5*np.cos(u[..., 0]*2*math.pi*rays)
        ray = (r > .82)*np.ones((h, 1))
        col = col*(1-.18*ray[..., None]); alpha = np.clip(alpha+.12*ray*(1-v[..., 0]*.3), 0, 1)
    if edge:
        e = (v[..., 0] > .9)*np.ones((1, w))
        col = np.where(e[..., None], np.array(edge, float), col); alpha = np.where(e, 1., alpha)
    arr = np.concatenate([np.clip(col, 0, 255), (alpha*255)[..., None]], 2).astype('uint8')
    Image.fromarray(np.flipud(arr), 'RGBA').save(path)

# ---------------- blender yardımcıları ----------------
def mat_image(name, path, alpha=False, rough=.35, coat=.35, metal=0., bump=True, film=0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bs = N['Principled BSDF']
    tx = N.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(path); tx.interpolation = 'Linear'
    tx.extension = 'EXTEND'
    Lk.new(tx.outputs['Color'], bs.inputs['Base Color'])
    if alpha: Lk.new(tx.outputs['Alpha'], bs.inputs['Alpha'])
    def si(k, v):
        if k in bs.inputs: bs.inputs[k].default_value = v
    si('Roughness', rough); si('Coat Weight', coat); si('Coat Roughness', .08); si('Metallic', metal); si('Specular IOR Level', .6)
    if film: si('Thin Film Thickness', film); si('Thin Film IOR', 1.4)
    if bump:
        vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 55
        tc = N.new('ShaderNodeTexCoord'); Lk.new(tc.outputs['Object'], vo.inputs['Vector'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .18; bp.inputs['Distance'].default_value = .004
        Lk.new(vo.outputs['Distance'], bp.inputs['Height']); Lk.new(bp.outputs['Normal'], bs.inputs['Normal'])
    return m

def mat_plain(name, rgb, rough=.2, metal=0., coat=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = (*[(c/255)**2.2 for c in rgb], 1)
    bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
    if 'Coat Weight' in bs.inputs: bs.inputs['Coat Weight'].default_value = coat
    return m

def mk_obj(name, verts, faces, uvs=None, mat=None, subsurf=0, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if uvs is not None:
        uvl = me.uv_layers.new(name='UV')
        for poly in me.polygons:
            for li in poly.loop_indices:
                vi = me.loops[li].vertex_index; uvl.data[li].uv = uvs[vi]
    if smooth:
        for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    if mat: me.materials.append(mat)
    if subsurf:
        md = ob.modifiers.new('ss', 'SUBSURF'); md.levels = subsurf; md.render_levels = subsurf
    return ob

def fin_mesh(name, outline2d, center2d, mat, plane_fn, rings=5, closed=False):
    """outline2d: (x,y-aşağı) noktalar; plane_fn((x,y))->Vector 3D"""
    n = len(outline2d); cx, cy = center2d
    verts = [plane_fn((cx, cy))]; uvs = [(.5, 0)]
    for j in range(1, rings+1):
        k = j/rings
        for i, (x, y) in enumerate(outline2d):
            verts.append(plane_fn((cx+(x-cx)*k, cy+(y-cy)*k))); uvs.append((i/(n-1), k))
    faces = []
    rng = range(n) if closed else range(n-1)
    for i in rng:
        i2 = (i+1) % n
        faces.append((0, 1+i, 1+i2))
    for j in range(1, rings):
        a = 1+(j-1)*n; b = 1+j*n
        for i in rng:
            i2 = (i+1) % n
            faces.append((a+i, b+i, b+i2, a+i2))
    return mk_obj(name, [tuple(v) for v in verts], faces, uvs, mat, subsurf=1)

def tube(name, p0, p1, r0, r1, mat, seg=6, nl=8):
    p0 = Vector(p0); p1 = Vector(p1); ax = (p1-p0); L = ax.length; ax.normalize()
    t = ax.orthogonal().normalized(); b = ax.cross(t)
    verts = []; uvs = []; faces = []
    for j in range(nl+1):
        k = j/nl; c = p0+ax*L*k; r = r0*(1-k)+r1*k
        for i in range(seg):
            a = i/seg*2*math.pi; verts.append(tuple(c+(t*math.cos(a)+b*math.sin(a))*r)); uvs.append((i/seg, k))
    for j in range(nl):
        for i in range(seg):
            a = j*seg+i; b2 = j*seg+(i+1) % seg
            faces.append((a, b2, b2+seg, a+seg))
    return mk_obj(name, verts, faces, uvs, mat)

# ---------------- sahne ----------------
def setup_scene(res_w):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = .02
    sc.cycles.transparent_max_bounces = 12; sc.cycles.max_bounces = 6
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.view_settings.exposure = .15
    sc.render.threads_mode = 'FIXED'; sc.render.threads = 2
    w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (.12, .3, .42, 1); bg.inputs['Strength'].default_value = 1.1
    def area(name, loc, energy, size, col=(1, 1, 1)):
        ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
        ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob); ob.location = loc
        d = Vector((0, 0, 0))-Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    area('key', (1.2, -2.2, 4.5), 520, 3.5, (1, .98, .94))
    area('rim', (-1.5, 3.2, 1.8), 330, 2.5, (.7, .9, 1))
    area('fill', (0, -5, -.5), 110, 4, (.75, .9, 1))
    cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'; cd.sensor_fit = 'HORIZONTAL'
    cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
    az, el = math.radians(22), math.radians(14)
    dirv = Vector((math.cos(el)*math.sin(az), -math.cos(el)*math.cos(az), math.sin(el)))
    cam.location = dirv*8; cam.rotation_euler = (-dirv).to_track_quat('-Z', 'Y').to_euler()
    return sc, cam

def build_fish(sp):
    H = sp['hb']; P = sp['ped']*sp['hb']
    ztop, zbot = body_profile(H, P)
    if sp.get('flat'):
        _zb = zbot; zbot = lambda x, _zb=_zb, k=sp['flat']: _zb(x)*k
    xs = np.linspace(-.5, .5, 400); zr = max(ztop(xs).max(), -zbot(xs).min())*1.04
    tag = sp['id']
    body_texture(sp, H, zr, f'{TEX}/{tag}_body.png')
    fc = sp['fin']; c1 = hx(sp['c1'])
    edge = sp.get('finEdge')
    if sp.get('spiky'):
        fb = sp.get('finBand', (150, 50, 28))
        fin_texture(f'{TEX}/{tag}_fin.png', (250, 238, 222), (245, 228, 210), .85, .7, rays=18, bands=(7, fb))
        fin_texture(f'{TEX}/{tag}_tail.png', (250, 238, 222), (245, 228, 210), .9, .75, rays=12, bands=(6, fb))
    else:
        fin_texture(f'{TEX}/{tag}_fin.png', c1, fc[:3], .96, max(.5, fc[3]), edge=edge)
        tc = sp.get('tailCol')
        fin_texture(f'{TEX}/{tag}_tail.png', tc or c1, tc or fc[:3], .96, (.95 if tc else max(.5, fc[3])), edge=edge if not tc else None)
    if sp.get('pecCol'):
        pc = sp['pecCol']; fin_texture(f'{TEX}/{tag}_pec.png', pc[:3], pc[:3], .95, pc[3])
    m_body = mat_image('body', f'{TEX}/{tag}_body.png', metal=sp.get('metal', .25 if tag == 'gold' else 0), film=sp.get('film', 0))
    m_fin = mat_image('fin', f'{TEX}/{tag}_fin.png', alpha=True, rough=.3, coat=.2, bump=False)
    m_tail = mat_image('tail', f'{TEX}/{tag}_tail.png', alpha=True, rough=.3, coat=.2, bump=False)
    m_pec = mat_image('pec', f'{TEX}/{tag}_pec.png', alpha=True, rough=.3, coat=.2, bump=False) if sp.get('pecCol') else m_fin
    # ---- gövde
    wmax = sp['wk']; hmax = H
    def W(x):
        hh = (ztop(x)-zbot(x))/2
        k = (hh/hmax)**.75
        head = 1+.18*max(0, min(1, (x-.0)/.3))*(1-max(0, (x-.42)/.08))
        return max(.012, wmax*k*head)
    NR, NS = 46, 40
    ts = np.linspace(0, 1, NR)
    rx = [-.5+.995*(1-(1-t)**1.7) for t in ts]
    verts = []; uvs = []
    for x in rx:
        zt, zb = float(ztop(x)), float(zbot(x)); zc = (zt+zb)/2; hh = (zt-zb)/2; ww = W(x)
        for i in range(NS):
            a = i/NS*2*math.pi
            y = ww*math.sin(a); z = zc+hh*math.cos(a)
            verts.append((x, y, z)); uvs.append((x+.5, (z/zr+1)/2))
    nose = len(verts); verts.append((.5, 0, float(ztop(.5)+zbot(.5))/2)); uvs.append((1, .5))
    tailc = len(verts); xt = rx[0]; verts.append((xt-.005, 0, float(ztop(xt)+zbot(xt))/2)); uvs.append((0, .5))
    faces = []
    for j in range(NR-1):
        for i in range(NS):
            a = j*NS+i; b = j*NS+(i+1) % NS
            faces.append((a, b, b+NS, a+NS))
    last = (NR-1)*NS
    for i in range(NS):
        faces.append((last+i, last+(i+1) % NS, nose))
        faces.append(((i+1) % NS, i, tailc))
    body = mk_obj('body', verts, faces, uvs, m_body, subsurf=2)
    parts = [body]
    side = lambda q: Vector((q[0], 0, -q[1]))
    # ---- kuyruk / sırt / anal
    to, tcn = tail_outline(sp, H, P)
    parts.append(fin_mesh('tail', to, tcn, m_tail, side))
    if sp.get('spiky'):
        m_sp = bpy.data.materials.new('spine'); m_sp.use_nodes = True
        nt = m_sp.node_tree; bs = nt.nodes['Principled BSDF']
        tc_ = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 7, 1)
        nt.links.new(tc_.outputs['UV'], mp.inputs['Vector'])
        sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(mp.outputs['Vector'], sep.inputs['Vector'])
        mth = nt.nodes.new('ShaderNodeMath'); mth.operation = 'PINGPONG'; mth.inputs[1].default_value = .5
        nt.links.new(sep.outputs['Y'], mth.inputs[0])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
        ramp.color_ramp.elements[0].color = (.97, .9, .82, 1); ramp.color_ramp.elements[1].position = .25; ramp.color_ramp.elements[1].color = (.33, .04, .02, 1)
        nt.links.new(mth.outputs[0], ramp.inputs[0]); nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
        bs.inputs['Roughness'].default_value = .4
        tips = []
        for i in range(12):
            k = i/11; bx = .24-.6*k; bz = float(ztop(bx))-.02; L = .46-.26*k; a = .3+.35*k
            tip = (bx-math.sin(a)*L, 0, bz+math.cos(a)*L); tips.append(tip)
            parts.append(tube(f'sp{i}', (bx, 0, bz-.03), tip, .012, .003, m_sp))
        outl = []
        for i, t in enumerate(tips):
            outl.append((t[0], -t[2]))
            if i < len(tips)-1:
                n2 = tips[i+1]; bx = (t[0]+n2[0])/2; bz = float(ztop(bx))
                outl.append((bx-.01, -(bz+(t[2]-bz)*.55)))
        cz = float(ztop(-.05))-.04
        parts.append(fin_mesh('dorsal', outl, (-.05, -cz), m_fin, side))
    elif sp.get('dshape') == 'shark':
        o = P2().M(.1, -H*.85).Q(.02, -H-.1, -.06, -H-.21).Q(-.07, -H-.06, -.17, -H*.7).pts
        parts.append(fin_mesh('dorsal', o, (-.03, -H*.6), m_fin, side))
        o = P2().M(-.33, -H*.45).Q(-.37, -H*.75, -.41, -H*.88).Q(-.4, -H*.55, -.44, -H*.4).pts
        parts.append(fin_mesh('dorsal2', o, (-.38, -H*.32), m_fin, side))
    elif sp['dors']:
        o, c = dorsal_outline(sp, H); parts.append(fin_mesh('dorsal', o, c, m_fin, side))
    if sp['anal']:
        o, c = anal_outline(sp, H); parts.append(fin_mesh('anal', o, c, m_fin, side))
    # ---- göğüs yüzgeçleri (iki yan)
    pecs = []
    for sgn in (-1, 1):
        px = .2; zt, zb = float(ztop(px)), float(zbot(px)); zc = (zt+zb)/2; hh = (zt-zb)/2
        pz = zc-hh*.35; py = sgn*W(px)*.9
        piv = Vector((px, py, pz))
        if sp.get('spiky'):
            outl = []
            for i in range(10):
                b = math.radians(-95+i*10.5); L = .62-i*.03
                outl.append((L*math.cos(b), L*math.sin(b)))
                if i < 9:
                    b2 = math.radians(-95+(i+.5)*10.5); outl.append((L*.72*math.cos(b2), L*.72*math.sin(b2)))
            cen = (0, 0); yaw0 = math.radians(30)
        elif sp.get('pec') == 'wing':
            outl = [(-.02, 0), (.09, -.05), (.22, -.11), (.35, -.17), (.29, -.11), (.18, -.05), (.08, -.005)]
            cen = (.04, -.02); yaw0 = math.radians(52); pz = zc-hh*.5; piv = Vector((px, py, pz))
        else:
            ry = max(.05, H*.17)
            outl = [(.1+.1*math.cos(a), ry*math.sin(a)) for a in np.linspace(math.pi*.95, -math.pi*.95, 40)]
            cen = (0.005, 0); yaw0 = math.radians(38)
        tilt = math.radians(-18)
        def plane(q, piv=piv, sgn=sgn, yaw0=yaw0, tilt=tilt):
            a, b = q  # a: geri yön, b: yukarı
            v = Vector((-a, 0, b))
            v = Matrix.Rotation(tilt, 3, 'Y') @ v
            v = Matrix.Rotation(sgn*-yaw0, 3, 'Z') @ v
            return piv+v
        ob = fin_mesh(f'pec{sgn}', outl, cen, m_pec, plane, closed=not sp.get('spiky'))
        ob['pivot'] = list(piv); ob['sgn'] = sgn
        pecs.append(ob); parts.append(ob)
    # ---- gözler
    er = sp.get('eyeK', .055); ex = .34
    zt, zb = float(ztop(ex)), float(zbot(ex)); zc = (zt+zb)/2; hh = (zt-zb)/2
    ez = min(H*.2, .07); ww = W(ex)*math.sqrt(max(0, 1-((ez-zc)/hh)**2))
    m_iris = mat_plain('iris', hx(sp.get('eye', '#e8c46a')), rough=.25, metal=.4)
    m_pup = mat_plain('pupil', (5, 5, 6), rough=.03, coat=1)
    m_white = mat_plain('glint', (255, 255, 255), rough=.0, coat=1)
    for sgn in (-1, 1):
        base_y = ww-er*.15
        for (r, yo, xo, sy, m) in ((er, 0, 0, .55, m_iris), (er*.6, er*.32, er*.12, .5, m_pup)):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=(ex+xo, sgn*(base_y+yo), ez))
            o = bpy.context.active_object; o.data.materials.append(m)
            o.scale = (1, sy, 1)
            for p in o.data.polygons: p.use_smooth = True
            parts.append(o)
    if sp.get('bristle'):
        m_br = mat_plain('bristle', tuple(min(255, int(c*1.25)) for c in hx(sp['c1'])), rough=.5)
        rr_ = random.Random(4)
        for i in range(9):
            bx = .4+.09*rr_.random(); sg = rr_.choice((-1, 1)); by = sg*rr_.uniform(.005, .05)
            bz = float(ztop(bx))-.012; L = rr_.uniform(.035, .07)
            parts.append(tube(f'br{i}', (bx, by, bz), (bx+L*.55, by*1.25, bz+L*.85), .007, .003, m_br, seg=5, nl=3))
        m_mo = mat_plain('mouth', tuple(int(c*.8) for c in hx(sp['c3'])), rough=.55)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=.055, location=(.44, 0, float(zbot(.44))+.012))
        o = bpy.context.active_object; o.data.materials.append(m_mo); o.scale = (1, 1.15, .28)
        for p_ in o.data.polygons: p_.use_smooth = True
        parts.append(o)
    if sp.get('barbel'):
        m_b = mat_plain('barb', (235, 205, 185), rough=.5)
        for sgn in (-1, 1):
            parts.append(tube(f'barb{sgn}', (.48, sgn*.02, -.02), (.5, sgn*.05, -.11), .008, .003, m_b))
    return parts, pecs

def apply_frame(parts, rest, phi, amp, pecs):
    def disp(x):
        s = max(0., (.2-x)/.7)
        g = s*s if s < 1 else 1+(s-1)*1.3
        return amp*g*math.sin(phi-2.2*s)
    for ob in parts:
        me = ob.data; r = rest[ob.name]
        co = r.copy()
        if ob in pecs:
            piv = np.array(ob['pivot']); sgn = ob['sgn']
            ang = sgn*.38*math.sin(phi+1.2)
            c, s = math.cos(ang), math.sin(ang)
            d = co-piv
            co = piv+np.stack([d[:, 0]*c-d[:, 1]*s, d[:, 0]*s+d[:, 1]*c, d[:, 2]], 1)
        dy = np.array([disp(x) for x in co[:, 0]])
        co[:, 1] += dy
        me.vertices.foreach_set('co', co.ravel()); me.update()

def fit_camera(sc, cam, parts, rest, amp, res_max):
    M = cam.matrix_world.inverted()
    pts = []
    for ob in parts:
        r = rest[ob.name]
        for sy in (-1, 1):
            q = r.copy(); s = np.clip((.2-q[:, 0])/.7, 0, None); g = np.where(s < 1, s*s, 1+(s-1)*1.3)
            q[:, 1] += sy*amp*g
            pts.append(q)
    pts = np.concatenate(pts)
    hom = np.c_[pts, np.ones(len(pts))] @ np.array(M).T
    x, y = hom[:, 0], hom[:, 1]
    pad = .05
    x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
    w, h = (x1-x0)*(1+pad*2), (y1-y0)*(1+pad*2)
    if w >= h: rw = res_max; rh = int(round(res_max*h/w))
    else: rh = res_max; rw = int(round(res_max*w/h))
    rw += rw % 2; rh += rh % 2
    sc.render.resolution_x = rw; sc.render.resolution_y = rh; sc.render.resolution_percentage = 100
    cam.data.ortho_scale = max(w, h*rw/rh)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    cam.data.shift_x = cx/cam.data.ortho_scale; cam.data.shift_y = cy/cam.data.ortho_scale
    ppu = rw/cam.data.ortho_scale
    ox = rw/2+(0-cx)*ppu; oy = rh/2-(0-cy)*ppu   # gövde merkezi (orijin) piksel konumu
    # orijin kamera uzayında (0,0) değil; dünya orijinini projekte et
    o = np.array(M) @ np.array([0, 0, 0, 1.])
    ox = rw/2+(o[0]-cx)*ppu; oy = rh/2-(o[1]-cy)*ppu
    return rw, rh, ppu, ox, oy

def bake_world(parts):
    rest = {}
    for ob in parts:
        if ob.matrix_world != Matrix.Identity(4):
            ob.data.transform(ob.matrix_world); ob.matrix_world = Matrix.Identity(4)
        a = np.zeros(len(ob.data.vertices)*3); ob.data.vertices.foreach_get('co', a)
        rest[ob.name] = a.reshape(-1, 3)
    return rest

def fit_pts(sc, cam, pts, res_max=None, ppu=None, pad=.05):
    M = np.array(cam.matrix_world.inverted())
    hom = np.c_[pts, np.ones(len(pts))] @ M.T
    x, y = hom[:, 0], hom[:, 1]
    x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
    w, h = (x1-x0)*(1+2*pad), (y1-y0)*(1+2*pad)
    if ppu is None:
        if w >= h: rw = res_max; rh = int(round(res_max*h/w))
        else: rh = res_max; rw = int(round(res_max*w/h))
    else:
        rw = int(math.ceil(w*ppu)); rh = int(math.ceil(h*ppu))
    rw += rw % 2; rh += rh % 2
    sc.render.resolution_x = rw; sc.render.resolution_y = rh; sc.render.resolution_percentage = 100
    cam.data.ortho_scale = max(w, h*rw/rh) if ppu is None else rw/ppu
    cx, cy = (x0+x1)/2, (y0+y1)/2
    cam.data.shift_x = cx/cam.data.ortho_scale; cam.data.shift_y = cy/cam.data.ortho_scale
    pp = rw/cam.data.ortho_scale
    o = M @ np.array([0, 0, 0, 1.])
    return rw, rh, pp, rw/2+(o[0]-cx)*pp, rh/2-(o[1]-cy)*pp

def poly_tube(name, pts, radii, mat, seg=8, subsurf=0):
    pts = [Vector(p) for p in pts]; n = len(pts); verts = []; uvs = []; faces = []
    for i, p in enumerate(pts):
        T = (pts[min(n-1, i+1)]-pts[max(0, i-1)]).normalized()
        ref = Vector((0, 0, 1)) if abs(T.z) < .9 else Vector((1, 0, 0))
        Nn = T.cross(ref).normalized(); B = T.cross(Nn)
        for j in range(seg):
            a = j/seg*2*math.pi
            verts.append(tuple(p+(Nn*math.cos(a)+B*math.sin(a))*radii[i])); uvs.append((j/seg, i/(n-1)))
    for i in range(n-1):
        for j in range(seg):
            a = i*seg+j; b = i*seg+(j+1) % seg; faces.append((a, b, b+seg, a+seg))
    c = len(verts); verts.append(tuple(pts[-1])); uvs.append((.5, 1)); last = (n-1)*seg
    for j in range(seg): faces.append((last+j, last+(j+1) % seg, c))
    return mk_obj(name, verts, faces, uvs, mat, subsurf=subsurf)

def catmull(points, n):
    P = [np.array(p, float) for p in points]; P = [P[0]]+P+[P[-1]]; out = []
    for i in range(1, len(P)-2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for k in range(n):
            t = k/n; t2 = t*t; t3 = t2*t
            out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(P[-2]); return np.array(out)

def build_seahorse(sp):
    tag = sp['id']; c1, c2, c3 = [np.array(hx(sp[k]), float) for k in ('c1', 'c2', 'c3')]
    # gövde dokusu: u = omurga boyunca, v = çevre
    w, h = 1024, 256
    v = np.linspace(0, 1, h)[:, None, None]; k = (np.cos(v*2*math.pi)+1)/2
    base = c2*(1-k)+c1*k
    base = np.where(k > .78, c1*(1-(k-.78)*2.5)+c3*((k-.78)*2.5), base)
    col = np.repeat(base, w, 1)
    u = np.linspace(0, 1, w)[None, :, None]
    col = col*(1-.38*np.cos(u*2*math.pi*38)**8)
    img = Image.fromarray(np.clip(col, 0, 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(img)
    rr_ = random.Random(5)
    for _ in range(260):
        x = rr_.uniform(0, w); y = rr_.uniform(0, h); r = rr_.uniform(1.5, 3.5); d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 248, 220))
    img.filter(ImageFilter.GaussianBlur(.8)).save(f'{TEX}/{tag}_body.png')
    m_body = mat_image('sh_body', f'{TEX}/{tag}_body.png', rough=.45, coat=.25)
    m_head = mat_plain('sh_head', tuple(int(x) for x in c1*.85+c2*.15), rough=.45, coat=.25)
    m_dark = mat_plain('sh_dark', tuple(int(x) for x in c2*.8), rough=.5)
    fc = sp['fin']; fin_texture(f'{TEX}/{tag}_fin.png', fc[:3], fc[:3], .85, fc[3], rays=16)
    m_fin = mat_image('sh_fin', f'{TEX}/{tag}_fin.png', alpha=True, rough=.3, coat=.2, bump=False)
    ctrl = [(0.03, 0.40), (0.07, 0.30), (0.11, 0.17), (0.10, 0.03), (0.03, -0.10), (-0.03, -0.20), (-0.03, -0.30),
            (0.03, -0.37), (0.10, -0.34), (0.11, -0.27), (0.07, -0.24), (0.04, -0.27)]
    sp2 = catmull(ctrl, 14); N = len(sp2)
    spine = np.c_[sp2[:, 0], np.zeros(N), sp2[:, 1]]
    t = np.linspace(0, 1, N)
    rad = np.interp(t, [0, .06, .14, .32, .45, .6, .8, 1], [.05, .05, .044, .095, .08, .045, .024, .01])
    rad = rad*(1+.07*np.cos(t*2*math.pi*38)**8)
    NS = 24; verts = []; uvs = []; faces = []; Ns = []
    for i in range(N):
        a = spine[max(0, i-1)]; b = spine[min(N-1, i+1)]; T = (b-a); T /= np.linalg.norm(T)
        Nn = np.array([-T[2], 0, T[0]]); Nn /= np.linalg.norm(Nn); Ns.append(Nn)
        for j in range(NS):
            ang = j/NS*2*math.pi
            p = spine[i]+Nn*rad[i]*math.cos(ang)+np.array([0, 1., 0])*rad[i]*.85*math.sin(ang)
            verts.append(tuple(p)); uvs.append((t[i], j/NS))
    for i in range(N-1):
        for j in range(NS):
            a = i*NS+j; b = i*NS+(j+1) % NS; faces.append((a, b, b+NS, a+NS))
    c0 = len(verts); verts.append(tuple(spine[0])); uvs.append((0, .5))
    c1i = len(verts); verts.append(tuple(spine[-1])); uvs.append((1, .5)); last = (N-1)*NS
    for j in range(NS):
        faces.append(((j+1) % NS, j, c0)); faces.append((last+j, last+(j+1) % NS, c1i))
    parts = [mk_obj('sh_body', verts, faces, uvs, m_body, subsurf=1)]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=.068, location=(.055, 0, .405))
    o = bpy.context.active_object; o.scale = (1.15, .8, .95); o.data.materials.append(m_head)
    for p in o.data.polygons: p.use_smooth = True
    parts.append(o)
    parts.append(tube('snout', (.09, 0, .388), (.235, 0, .345), .03, .021, m_head))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=.024, location=(.237, 0, .345))
    o = bpy.context.active_object; o.scale = (.7, 1, 1); o.data.materials.append(m_dark); parts.append(o)
    for i, (x, z, dx) in enumerate([(.03, .465, -.01), (.0, .455, -.02), (.065, .462, .01)]):
        parts.append(tube(f'crown{i}', (x, 0, z-.02), (x+dx, 0, z+.035), .014, .003, m_head))
    # sırt yüzgeci (sırtta, -N yönünde)
    i0, i1 = int(N*.36), int(N*.56); outl = []
    for kk in range(21):
        ii = int(i0+(i1-i0)*kk/20); off = rad[ii]+.085*math.sin(math.pi*kk/20)
        p = spine[ii]-Ns[ii]*off; outl.append((p[0], -p[2]))
    im = (i0+i1)//2; cc = spine[im]-Ns[im]*rad[im]*.5
    fin = fin_mesh('sdors', outl, (cc[0], -cc[2]), m_fin, lambda q: Vector((q[0], 0, -q[1])))
    fin['c'] = list(cc); parts.append(fin)
    # göğüs yüzgeçleri
    for sgn in (-1, 1):
        piv = Vector((.035, sgn*.045, .335))
        outl = [(.035+.035*math.cos(a), .025*math.sin(a)) for a in np.linspace(math.pi*.95, -math.pi*.95, 24)]
        def plane(q, piv=piv, sgn=sgn):
            v = Vector((-q[0], 0, q[1])); v = Matrix.Rotation(sgn*-math.radians(40), 3, 'Z') @ v; return piv+v
        ob = fin_mesh(f'spec{sgn}', outl, (.003, 0), m_fin, plane, closed=True); ob['pivot'] = list(piv); ob['sgn'] = sgn
        parts.append(ob)
    # gözler
    er = sp.get('eyeK', .03)
    m_iris = mat_plain('iris', hx(sp.get('eye', '#e8c46a')), rough=.25, metal=.4); m_pup = mat_plain('pupil', (5, 5, 6), rough=.03, coat=1)
    for sgn in (-1, 1):
        for (r, yo, xo, sy, m) in ((er, 0, 0, .55, m_iris), (er*.6, er*.32, er*.12, .5, m_pup)):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=r, location=(.08+xo, sgn*(.052+yo), .41))
            o = bpy.context.active_object; o.data.materials.append(m); o.scale = (1, sy, 1)
            for p in o.data.polygons: p.use_smooth = True
            parts.append(o)
    def fn(parts, rest, phi):
        sw = .06*math.sin(phi); cs, sn = math.cos(sw), math.sin(sw)
        for ob in parts:
            co = rest[ob.name].copy()
            if ob.name.startswith('sdors'):
                c = np.array(ob['c']); dist = np.clip(np.linalg.norm(co-c, axis=1)/.09, 0, 1)
                co[:, 1] += .035*np.sin(2*phi+co[:, 2]*45)*dist
            elif ob.name.startswith('spec'):
                piv = np.array(ob['pivot']); ang = ob['sgn']*.5*math.sin(2*phi); c_, s_ = math.cos(ang), math.sin(ang); d_ = co-piv
                co = piv+np.stack([d_[:, 0]*c_-d_[:, 1]*s_, d_[:, 0]*s_+d_[:, 1]*c_, d_[:, 2]], 1)
            x, y = co[:, 0].copy(), co[:, 1].copy(); co[:, 0] = x*cs-y*sn; co[:, 1] = x*sn+y*cs
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

def build_jelly(sp):
    c1, c2, c3 = hx(sp['c1']), hx(sp['c2']), hx(sp['c3'])
    def jmat(name, c, alpha, emis, trans=.6):
        m = bpy.data.materials.new(name); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']
        lc = (*[(x/255)**2.2 for x in c], 1)
        bs.inputs['Base Color'].default_value = lc; bs.inputs['Alpha'].default_value = alpha; bs.inputs['Roughness'].default_value = .12
        for kk, vv in (('Transmission Weight', trans), ('Coat Weight', .5), ('Emission Strength', emis)):
            if kk in bs.inputs: bs.inputs[kk].default_value = vv
        if 'Emission Color' in bs.inputs: bs.inputs['Emission Color'].default_value = lc
        return m
    m_bell = jmat('bell', c1, .62, .9); m_in = jmat('gonad', c2, .9, 1.6, .2); m_arm = jmat('arm', c3, .6, .8); m_ten = jmat('ten', c1, .75, 1.0, .3)
    NR, NS = 22, 64; verts = [(0, 0, .26)]; uvs = [(.5, 0)]
    for i in range(1, NR+1):
        t = i/NR; r = .34*math.sin(t*math.pi/2)**.85; z = .26*math.cos(t*math.pi/2)**1.15-.035*t**4
        for j in range(NS):
            a = j/NS*2*math.pi; rr = r*(1+.04*math.cos(16*a)*t**6)
            verts.append((rr*math.cos(a), rr*math.sin(a), z)); uvs.append((j/NS, t))
    faces = [(0, 1+(j+1) % NS, 1+j) for j in range(NS)]
    for i in range(NR-1):
        for j in range(NS):
            a = 1+i*NS+j; b = 1+i*NS+(j+1) % NS; faces.append((a, b, b+NS, a+NS))
    bell = mk_obj('bell', verts, faces, uvs, m_bell, subsurf=1)
    sd = bell.modifiers.new('sol', 'SOLIDIFY'); sd.thickness = .018
    parts = [bell]
    for kk in range(4):
        a = kk*math.pi/2+math.pi/4
        bpy.ops.mesh.primitive_torus_add(major_radius=.055, minor_radius=.014, location=(math.cos(a)*.085, math.sin(a)*.085, .15))
        o = bpy.context.active_object; o.data.materials.append(m_in)
        for p in o.data.polygons: p.use_smooth = True
        parts.append(o)
    for kk in range(4):
        a = kk*math.pi/2; dv = np.array([math.cos(a), math.sin(a)]); pp = np.array([-dv[1], dv[0]])
        n = 36; L = .55; verts = []; uvs = []; faces = []
        for i in range(n+1):
            t = i/n; z = .04-L*t; cxy = dv*(.035+.03*t)+pp*.025*math.sin(t*9+kk)
            w = .05*(1-.45*t); fr = .015*math.sin(t*40+kk*2)
            for sg in (-1, 1):
                q = cxy+pp*w*sg; verts.append((q[0]+dv[0]*fr*sg, q[1]+dv[1]*fr*sg, z)); uvs.append(((sg+1)/2, t))
        for i in range(n): faces.append((2*i, 2*i+1, 2*i+3, 2*i+2))
        parts.append(mk_obj(f'arm{kk}', verts, faces, uvs, m_arm, subsurf=1))
    for kk in range(18):
        a = kk/18*2*math.pi+.1; L = .7+.25*((kk*7) % 5)/4; pts = []; rad = []
        for i in range(25):
            t = i/24; rr = .30*(1+.15*t)
            pts.append((rr*math.cos(a)+.03*math.sin(t*8+kk), rr*math.sin(a)+.03*math.cos(t*7+kk), -.02-L*t)); rad.append(.006*(1-t)+.0015)
        parts.append(poly_tube(f'ten{kk}', pts, rad, m_ten, seg=6))
    def fn(parts, rest, phi):
        pulse = .5+.5*math.sin(phi); sr = 1-.12*pulse; sz = 1+.09*pulse
        for ob in parts:
            co = rest[ob.name].copy(); nm = ob.name
            if nm.startswith('bell') or nm.startswith('Torus'):
                co[:, 0] *= sr; co[:, 1] *= sr; co[:, 2] *= sz
            else:
                depth = np.clip(-co[:, 2]/.9, 0, 1); kf = sr+(1-sr)*np.clip(depth*2, 0, 1)
                co[:, 0] *= kf; co[:, 1] *= kf
                co[:, 0] += .045*depth*np.sin(phi-depth*5); co[:, 1] += .03*depth*np.cos(phi-depth*4)
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

def build_ray(sp):
    """Vatoz: disk gövde xy düzleminde, burun +x. Kanat dalgası + kamuflaj için kameraya doğru eğilir."""
    tag = sp['id']; motoro = sp.get('ray') == 'motoro'
    c1, c2, c3 = [np.array(hx(sp[k]), float) for k in ('c1', 'c2', 'c3')]
    CX, A, B = .14, .27, .31
    X0, X1 = CX-A-.02, CX+A+.08
    # --- üst doku (UV = üstten düzlemsel)
    TS = 1024; u = np.linspace(0, 1, TS)[None, :]; v = np.linspace(0, 1, TS)[:, None]
    xx = X0+(X1-X0)*u; yy = (v*2-1)*B
    rho = np.sqrt(((xx-CX)/A)**2+(yy/B)**2)
    base = c1[None, None, :]*(1-np.clip(rho, 0, 1)[..., None]*.45)+c2[None, None, :]*(np.clip(rho, 0, 1)[..., None]*.45)
    noise = np.random.RandomState(3).rand(TS//16, TS//16); noise = np.array(Image.fromarray((noise*255).astype('uint8')).resize((TS, TS), Image.BICUBIC))/255.
    col = base*(.86+.24*noise[..., None])
    img = Image.fromarray(np.clip(col, 0, 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(img, 'RGBA')
    P = lambda x, y: ((x-X0)/(X1-X0)*TS, (y/B+1)/2*TS)
    rr_ = random.Random(21)
    placed = []; mind = .05 if motoro else .036
    for _ in range(3000):
        x = rr_.uniform(CX-A, CX+A); y = rr_.uniform(-B, B)
        if ((x-CX)/A)**2+(y/B)**2 > .86: continue
        if ((x-CX-.15)**2+(abs(y)-.062)**2) < .004: continue
        if any((x-a)**2+(y-b)**2 < mind*mind for a, b in placed): continue
        placed.append((x, y))
        if motoro:
            r = rr_.uniform(.016, .03); px, py = P(x, y); rp = r/(X1-X0)*TS
            d.ellipse([px-rp*1.35, py-rp*1.35, px+rp*1.35, py+rp*1.35], fill=(20, 12, 6, 255))
            d.ellipse([px-rp, py-rp, px+rp, py+rp], fill=(255, 150, 40, 255))
            d.ellipse([px-rp*.55, py-rp*.55, px+rp*.55, py+rp*.55], fill=(250, 205, 90, 255))
        else:
            r = rr_.uniform(.009, .02); px, py = P(x, y); rp = r/(X1-X0)*TS
            d.ellipse([px-rp*1.3, py-rp*1.3, px+rp*1.3, py+rp*1.3], fill=(18, 40, 90, 200))
            d.ellipse([px-rp, py-rp, px+rp, py+rp], fill=(40, 150, 255, 255))
            d.ellipse([px-rp*.45, py-rp*.6, px+rp*.2, py-rp*.1], fill=(170, 225, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(1.1)); img.save(f'{TEX}/{tag}_top.png')
    m_top = mat_image('ray_top', f'{TEX}/{tag}_top.png', rough=.42, coat=.45)
    m_bot = mat_plain('ray_bot', tuple(int(x) for x in c3), rough=.5)
    m_tail = mat_plain('ray_tail', tuple(int(x) for x in c1*.75+c2*.25), rough=.45, coat=.3)
    m_stripe = mat_plain('ray_stripe', (30, 120, 235) if not motoro else (255, 150, 40), rough=.3, coat=.4)
    # --- disk: üst + alt yüzey, ortak kenar halkası
    NSg, NR = 96, 26
    def R(th):
        n = 2.25; c, s_ = abs(math.cos(th)), abs(math.sin(th))
        r = 1/((c/A)**n+(s_/B)**n)**(1/n)
        if math.cos(th) > 0: r *= 1+.13*math.cos(th)**10   # sivri burun
        if math.cos(th) < -.2: r *= 1-.08*(-math.cos(th)-.2)  # arka düzleşme
        return r
    verts = [(CX+.02, 0, .085)]; uvs = []
    ring = lambda i: 1+(i-1)*NSg
    for i in range(1, NR+1):
        rh = i/NR
        for j in range(NSg):
            th = j/NSg*2*math.pi; r = R(th)*rh; x = CX+r*math.cos(th); y = r*math.sin(th)
            z = .075*(1-rh**2)**.75+.012*math.exp(-((x-CX-.12)**2+y**2)/.004)
            verts.append((x, y, z))
    bot0 = len(verts)
    for i in range(NR-1, 0, -1):
        rh = i/NR
        for j in range(NSg):
            th = j/NSg*2*math.pi; r = R(th)*rh
            verts.append((CX+r*math.cos(th), r*math.sin(th), -.032*(1-rh**2)**.8))
    botc = len(verts); verts.append((CX, 0, -.034))
    faces = []; mats = []
    for j in range(NSg):
        faces.append((0, ring(1)+j, ring(1)+(j+1) % NSg)); mats.append(0)
    for i in range(1, NR):
        for j in range(NSg):
            a_ = ring(i)+j; b_ = ring(i)+(j+1) % NSg; faces.append((a_, a_+NSg, b_+NSg, b_)); mats.append(0)
    # kenar halkası -> alt halkalar
    rows = [ring(NR)]+[bot0+k*NSg for k in range(NR-1)]
    for k in range(len(rows)-1):
        for j in range(NSg):
            a_ = rows[k]+j; b_ = rows[k]+(j+1) % NSg; c_ = rows[k+1]+(j+1) % NSg; d_ = rows[k+1]+j
            faces.append((a_, d_, c_, b_)); mats.append(1)
    last = rows[-1]
    for j in range(NSg):
        faces.append((last+j, botc, last+(j+1) % NSg)); mats.append(1)
    me = bpy.data.meshes.new('disc'); me.from_pydata(verts, [], faces); me.update()
    uvl = me.uv_layers.new(name='UV')
    for poly in me.polygons:
        poly.use_smooth = True; poly.material_index = mats[poly.index]
        for li in poly.loop_indices:
            vx, vy, vz = verts[me.loops[li].vertex_index]; uvl.data[li].uv = ((vx-X0)/(X1-X0), 1-(vy/B+1)/2)
    disc = bpy.data.objects.new('disc', me); bpy.context.collection.objects.link(disc)
    me.materials.append(m_top); me.materials.append(m_bot)
    md = disc.modifiers.new('ss', 'SUBSURF'); md.levels = 1; md.render_levels = 1
    parts = [disc]
    # --- kuyruk
    xt0 = CX-A*.62; pts = []; rad = []
    for i in range(34):
        t = i/33; pts.append((xt0-.55*t, 0, .004-.03*t)); rad.append(.022*(1-t)**1.5+.0025)
    parts.append(poly_tube('tail', pts, rad, m_tail, seg=10, subsurf=1))
    for sg in (-1, 1):
        sp_ = [(xt0-.12-.28*t, sg*(.016*(1-t)+.003), .006-.02*t) for t in np.linspace(0, 1, 16)]
        parts.append(poly_tube(f'tstripe{sg}', sp_, [.005*(1-t*.6) for t in np.linspace(0, 1, 16)], m_stripe, seg=6))
    # karın yüzgeçleri (arkada iki lob)
    for sg in (-1, 1):
        outl = [(CX-A*.7+.07*math.cos(a_), sg*(.05+.055*math.sin(a_)*.9)) for a_ in np.linspace(-math.pi*.9, math.pi*.9, 20)]
        vv = [(CX-A*.72, sg*.05, -.005)]+[(x, y, -.01) for x, y in outl]
        ff = [(0, i, i+1) if sg > 0 else (0, i+1, i) for i in range(1, len(outl))]
        parts.append(mk_obj(f'pelv{sg}', vv, ff, None, m_top if False else mat_plain(f'pv{sg}', tuple(int(x) for x in c2*.9), rough=.5), subsurf=1))
    # --- gözler (üstte, kabarık) + spirakül
    m_eye = mat_plain('reye', tuple(int(x) for x in c1*.8), rough=.35, coat=.5)
    m_pup = mat_plain('rpup', (8, 8, 10), rough=.03, coat=1)
    m_gl = mat_plain('rgl', (255, 255, 255), rough=.0, coat=1)
    for sg in (-1, 1):
        ex, ey = CX+.15, sg*.062
        for (r, dz, dx, m) in ((.03, .07, 0, m_eye), (.017, .088, .006, m_pup), (.006, .1, .012, m_gl)):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=r, location=(ex+dx, ey, dz))
            o = bpy.context.active_object; o.data.materials.append(m)
            for p_ in o.data.polygons: p_.use_smooth = True
            parts.append(o)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=.016, location=(ex-.06, sg*.07, .062))
        o = bpy.context.active_object; o.data.materials.append(m_pup); o.scale = (1.4, .8, .4); parts.append(o)
    TILT = math.radians(38)
    ct, st = math.cos(TILT), math.sin(TILT)
    def fn(parts, rest, phi):
        for ob in parts:
            co = rest[ob.name].copy(); x = co[:, 0]; y = co[:, 1]
            lat = np.clip(np.abs(y)/B, 0, 1)**1.6
            on_disc = (x > CX-A-.03).astype(float)
            co[:, 2] += sp['amp']*lat*np.sin(phi-(CX+A-x)/(2*A)*2*math.pi*.95)*on_disc
            s_ = np.clip((CX-A*.9-x)/.47, 0, 1)
            co[:, 1] += .035*s_**1.4*np.sin(phi-s_*3.5)
            co[:, 2] += .012*s_*np.sin(phi*2-s_*4)
            yy, zz = co[:, 1].copy(), co[:, 2].copy()
            co[:, 1] = yy*ct-zz*st; co[:, 2] = yy*st+zz*ct
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

BUILDERS = {'seahorse': build_seahorse, 'jelly': build_jelly, 'ray': build_ray}

def render_species(sp, frames, res_max):
    t0 = time.time()
    sc, cam = setup_scene(res_max)
    kind = sp.get('kind', 'fish')
    if kind == 'fish':
        parts, pecs = build_fish(sp); rest = bake_world(parts)
        ff = lambda phi: apply_frame(parts, rest, phi, sp['amp'], pecs)
    else:
        parts, fn = BUILDERS[kind](sp); bpy.context.view_layer.update(); rest = bake_world(parts)
        ff = lambda phi: fn(parts, rest, phi)
    bpy.context.view_layer.update()
    allp = []
    for f in range(frames):
        ff(2*math.pi*f/frames)
        for ob in parts:
            a = np.zeros(len(ob.data.vertices)*3); ob.data.vertices.foreach_get('co', a); allp.append(a.reshape(-1, 3))
    rw, rh, ppu, ox, oy = fit_pts(sc, cam, np.concatenate(allp), res_max=res_max)
    tag = sp['id']; files = []
    for f in range(frames):
        ff(2*math.pi*f/frames)
        fn_ = f'{OUT}/{tag}_{f:02d}.png'; sc.render.filepath = fn_
        bpy.ops.render.render(write_still=True); files.append(fn_)
    sheet = Image.new('RGBA', (rw*frames, rh), (0, 0, 0, 0))
    for i, fn_ in enumerate(files): sheet.paste(Image.open(fn_), (i*rw, 0))
    sheet.save(f'{SPR}/{tag}_sheet.webp', 'WEBP', quality=82, method=6)
    json.dump(dict(id=tag, fw=rw, fh=rh, n=frames, ppu=ppu, ox=ox, oy=oy), open(f'{SPR}/{tag}_meta.json', 'w'))
    print(f'[{tag}] {rw}x{rh} x{frames}  {time.time()-t0:.1f}s', flush=True)

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'gold'
    frames = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    res = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    if which == 'all': tags = [x['id'] for x in SPECIES]+[k+'_r' for k in VARIANTS]
    elif which == 'new': tags = ['shark', 'seahorse', 'jelly']+[k+'_r' for k in VARIANTS]
    else: tags = which.split(',')
    for tg in tags:
        render_species(get_species(tg), frames, res)
