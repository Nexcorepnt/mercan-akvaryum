"""fish.py'ye v3 eklemeleri: köpekbalığı, deniz atı, denizanası, nadir varyantlar, kare tabanlı kadraj."""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blender', 'fish.py')
s = open(P, encoding='utf-8').read()

def R(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

R("import bpy, math, sys, json, os, time", "import bpy, math, sys, json, os, time, random")

# ---- yeni türler + varyantlar
R(" dict(id='puffer',len=60, hb=.42, ped=.17, tail='round', dors=7,  anal=7,  c1='#d9c27a', c2='#8a7333', c3='#fbf7ea', fin=(220,200,130,.6), pat='puffer', wk=.36, amp=.05, eyeK=.085),\n]",
""" dict(id='puffer',len=60, hb=.42, ped=.17, tail='round', dors=7,  anal=7,  c1='#d9c27a', c2='#8a7333', c3='#fbf7ea', fin=(220,200,130,.6), pat='puffer', wk=.36, amp=.05, eyeK=.085),
 dict(id='shark', len=100,hb=.2,  ped=.09, tail='shark', dors=0,  anal=4,  c1='#8796a5', c2='#55636f', c3='#f2f5f7', fin=(115,130,145,.97), pat='shark', wk=.11, amp=.1, dshape='shark', pec='wing', eyeK=.034, eye='#1e2328'),
 dict(id='seahorse', kind='seahorse', len=70, hb=.45, c1='#f2b134', c2='#b4650f', c3='#ffe39a', fin=(255,220,120,.55), amp=.02, eyeK=.03),
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
}
def get_species(tag):
    base = tag[:-2] if tag.endswith('_r') else tag
    sp = dict(next(x for x in SPECIES if x['id'] == base))
    if tag.endswith('_r'):
        sp.update(VARIANTS[base]); sp['id'] = tag
    return sp""")

# ---- desen renk parametreleri
R("        poly(P2().M(.36, -H*.2).Q(0, -H*.48, -.5, -H*.12).L(-.5, H*.08).Q(0, -H*.06, .36, H*.02).pts, (40, 215, 255, 255))\n        poly(P2().M(.3, -H*.08).Q(0, -H*.3, -.5, -H*.02).L(-.5, H*.08).Q(0, -H*.06, .3, H*.02).pts, (30, 90, 255, 200))\n        poly(P2().M(.06, H*.12).Q(-.2, H*.04, -.5, H*.1).L(-.5, H*.95).Q(-.2, H*.98, .06, H*.65).pts, (255, 40, 64, 255))",
  "        pa = sp.get('patA'); pb = sp.get('patB', (255, 40, 64))\n"
  "        poly(P2().M(.36, -H*.2).Q(0, -H*.48, -.5, -H*.12).L(-.5, H*.08).Q(0, -H*.06, .36, H*.02).pts, (*(pa or (40, 215, 255)), 255))\n"
  "        poly(P2().M(.3, -H*.08).Q(0, -H*.3, -.5, -H*.02).L(-.5, H*.08).Q(0, -H*.06, .3, H*.02).pts, (*(pa or (30, 90, 255)), 200))\n"
  "        poly(P2().M(.06, H*.12).Q(-.2, H*.04, -.5, H*.1).L(-.5, H*.95).Q(-.2, H*.98, .06, H*.65).pts, (*pb, 255))")
R("            stroke(pts, (60, 210, 205, 230), H*.075/zr*H2/2)", "            stroke(pts, (*sp.get('patA', (60, 210, 205)), 230), H*.075/zr*H2/2)")
R("            ell(x, y*H, rx, ry*H, a, (232, 64, 28, 255))", "            ell(x, y*H, rx, ry*H, a, (*sp.get('patA', (232, 64, 28)), 255))")
R("            poly([(x, -H*1.3), (x+.035, -H*1.3), (x+.01, H*1.3), (x-.025, H*1.3)], (140, 40, 22, 225))", "            poly([(x, -H*1.3), (x+.035, -H*1.3), (x+.01, H*1.3), (x-.025, H*1.3)], (*sp.get('patA', (140, 40, 22)), 225))")
R("            ell(x, y, rr, rr, 0, (62, 47, 18, 255))", "            ell(x, y, rr, rr, 0, (*sp.get('patA', (62, 47, 18)), 255))")
R("    # solungaç kapağı + ağız",
  "    elif pat == 'tancho':\n"
  "        ell(.3, -H*.5, .09, H*.38, 0, (225, 35, 30, 255))\n"
  "    elif pat == 'shark':\n"
  "        poly([(.56, H*.06)] + [(x, H*.14+H*.05*math.sin(x*22)) for x in np.linspace(.5, -.56, 50)] + [(-.56, H*1.5), (.56, H*1.5)], (*hx(sp['c3']), 255))\n"
  "        for i in range(5):\n"
  "            gx = .23-i*.035; stroke([(gx+.012*math.sin(t*math.pi), -H*.35+H*.6*t) for t in np.linspace(0, 1, 12)], (30, 40, 50, 110), 5)\n"
  "    # solungaç kapağı + ağız")
R("        fin_texture(f'{TEX}/{tag}_fin.png', (250, 238, 222), (245, 228, 210), .85, .7, rays=18, bands=(7, (150, 50, 28)))\n        fin_texture(f'{TEX}/{tag}_tail.png', (250, 238, 222), (245, 228, 210), .9, .75, rays=12, bands=(6, (150, 50, 28)))",
  "        fb = sp.get('finBand', (150, 50, 28))\n"
  "        fin_texture(f'{TEX}/{tag}_fin.png', (250, 238, 222), (245, 228, 210), .85, .7, rays=18, bands=(7, fb))\n"
  "        fin_texture(f'{TEX}/{tag}_tail.png', (250, 238, 222), (245, 228, 210), .9, .75, rays=12, bands=(6, fb))")

# ---- köpekbalığı kuyruğu / sırt / kanat yüzgeç
R("    elif t == 'betta':",
  "    elif t == 'shark':\n"
  "        p.M(e, -P).Q(-.15, -.13, -.44, -.37).Q(-.26, -.12, -.22, 0).Q(-.27, .07, -.3, .17).Q(-.12, .08, e, P)\n"
  "    elif t == 'betta':")
R("    elif sp['dors']:\n        o, c = dorsal_outline(sp, H); parts.append(fin_mesh('dorsal', o, c, m_fin, side))",
  "    elif sp.get('dshape') == 'shark':\n"
  "        o = P2().M(.1, -H*.85).Q(.02, -H-.1, -.06, -H-.21).Q(-.07, -H-.06, -.17, -H*.7).pts\n"
  "        parts.append(fin_mesh('dorsal', o, (-.03, -H*.6), m_fin, side))\n"
  "        o = P2().M(-.33, -H*.45).Q(-.37, -H*.75, -.41, -H*.88).Q(-.4, -H*.55, -.44, -H*.4).pts\n"
  "        parts.append(fin_mesh('dorsal2', o, (-.38, -H*.32), m_fin, side))\n"
  "    elif sp['dors']:\n        o, c = dorsal_outline(sp, H); parts.append(fin_mesh('dorsal', o, c, m_fin, side))")
R("        else:\n            ry = max(.05, H*.17)",
  "        elif sp.get('pec') == 'wing':\n"
  "            outl = [(-.02, 0), (.08, -.06), (.2, -.16), (.31, -.25), (.27, -.18), (.17, -.08), (.08, -.01)]\n"
  "            cen = (.04, -.02); yaw0 = math.radians(52); pz = zc-hh*.5; piv = Vector((px, py, pz))\n"
  "        else:\n            ry = max(.05, H*.17)")

# ---- render: kare tabanlı kadraj + özel yapıcılar
start = s.index("def render_species(sp, frames, res_max):")
end = s.index("if __name__ == '__main__':")
NEW = r'''def bake_world(parts):
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
        piv = Vector((.0, sgn*.05, .33))
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
    m_bell = jmat('bell', c1, .55, .6); m_in = jmat('gonad', c2, .9, 1.6, .2); m_arm = jmat('arm', c3, .6, .8); m_ten = jmat('ten', c1, .75, 1.0, .3)
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

def render_species(sp, frames, res_max):
    t0 = time.time()
    sc, cam = setup_scene(res_max)
    kind = sp.get('kind', 'fish')
    if kind == 'fish':
        parts, pecs = build_fish(sp); rest = bake_world(parts)
        ff = lambda phi: apply_frame(parts, rest, phi, sp['amp'], pecs)
    else:
        parts, fn = (build_seahorse if kind == 'seahorse' else build_jelly)(sp); rest = bake_world(parts)
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

'''
s = s[:start]+NEW+s[end:]
R("""    for sp in SPECIES:
        if which == 'all' or sp['id'] in which.split(','):
            render_species(sp, frames, res)""",
"""    if which == 'all': tags = [x['id'] for x in SPECIES]+[k+'_r' for k in VARIANTS]
    elif which == 'new': tags = ['shark', 'seahorse', 'jelly']+[k+'_r' for k in VARIANTS]
    else: tags = which.split(',')
    for tg in tags:
        render_species(get_species(tg), frames, res)""")
open(P, 'w', encoding='utf-8').write(s)
print('fish.py güncellendi')
