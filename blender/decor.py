"""Mercan Akvaryum - Blender ile 2.5D süs sprite üretici.
Birim: 1 Blender birimi = oyunda 100 dünya birimi. Taban merkezi (0,0,0) = kum yüzeyi.
Kullanım: python decor.py <id|all> [samples] [ppu]
"""
import bpy, bmesh, math, sys, os, json, random, time
import numpy as np
from mathutils import Vector, Matrix
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F

ROOT = F.ROOT; SPR = F.SPR; OUT = F.OUT
hx = F.hx

def lin(h):
    r, g, b = hx(h); return ((r/255)**2.2, (g/255)**2.2, (b/255)**2.2, 1)

def active(): return bpy.context.active_object

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
    return o

def bake(o):
    M = Matrix.LocRotScale(o.location, o.rotation_euler, o.scale)
    o.data.transform(M); o.location = (0, 0, 0); o.rotation_euler = (0, 0, 0); o.scale = (1, 1, 1); return o

def add_mods(o, bevel=0, sub=0):
    if bevel:
        m = o.modifiers.new('bv', 'BEVEL'); m.width = bevel; m.segments = 3
    if sub:
        m = o.modifiers.new('ss', 'SUBSURF'); m.levels = sub; m.render_levels = sub
    return o

def mat_proc(name, ca, cb, scale=5, rough=.6, metal=0., bump=.3, moss=None, stretch=(1, 1, 1), tex='noise',
             distort=0., emit=None, emit_thr=.6, sss=0., coat=0., detail=4, pos=(0, 1), wave_dir='Z', rot=(0, 0, 0)):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links
    bs = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch; mp.inputs['Rotation'].default_value = rot
    L.new(tc.outputs['Object'], mp.inputs['Vector'])
    if tex == 'noise':
        t = N.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value = scale; t.inputs['Detail'].default_value = detail
        t.inputs['Distortion'].default_value = distort
    elif tex in ('wave', 'rings', 'brain'):
        t = N.new('ShaderNodeTexWave'); t.wave_type = 'RINGS' if tex == 'rings' else 'BANDS'
        if tex != 'rings': t.bands_direction = wave_dir
        t.inputs['Scale'].default_value = scale; t.inputs['Distortion'].default_value = distort
        t.inputs['Detail'].default_value = detail
    elif tex == 'brick':
        t = N.new('ShaderNodeTexBrick'); t.inputs['Scale'].default_value = scale; t.inputs['Mortar Size'].default_value = .025
        t.inputs['Color1'].default_value = (1, 1, 1, 1); t.inputs['Color2'].default_value = (.7, .7, .7, 1); t.inputs['Mortar'].default_value = (0, 0, 0, 1)
    elif tex == 'voronoi':
        t = N.new('ShaderNodeTexVoronoi'); t.inputs['Scale'].default_value = scale
    L.new(mp.outputs['Vector'], t.inputs['Vector'])
    fac = t.outputs['Fac'] if 'Fac' in t.outputs else t.outputs['Distance']
    if tex == 'brick':
        sepc = N.new('ShaderNodeSeparateColor'); L.new(t.outputs['Color'], sepc.inputs['Color']); fac = sepc.outputs[0]
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = lin(ca); ramp.color_ramp.elements[1].color = lin(cb)
    ramp.color_ramp.elements[0].position = pos[0]; ramp.color_ramp.elements[1].position = pos[1]
    L.new(fac, ramp.inputs['Fac']); col = ramp.outputs['Color']
    if moss:
        geo = N.new('ShaderNodeNewGeometry'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sep.inputs['Vector'])
        r2 = N.new('ShaderNodeValToRGB'); r2.color_ramp.elements[0].position = .55; r2.color_ramp.elements[1].position = .85
        L.new(sep.outputs['Z'], r2.inputs['Fac'])
        mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'
        L.new(r2.outputs['Color'], mix.inputs[0]); L.new(col, mix.inputs[6]); mix.inputs[7].default_value = lin(moss); col = mix.outputs[2]
    L.new(col, bs.inputs['Base Color'])
    if emit:
        r3 = N.new('ShaderNodeValToRGB'); r3.color_ramp.elements[0].position = emit_thr; r3.color_ramp.elements[0].color = (0, 0, 0, 1)
        r3.color_ramp.elements[1].position = min(.999, emit_thr+.04); r3.color_ramp.elements[1].color = lin(emit)
        L.new(fac, r3.inputs['Fac']); L.new(r3.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = 4
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = .02
        L.new(fac, bp.inputs['Height']); L.new(bp.outputs['Normal'], bs.inputs['Normal'])
    bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
    if sss and 'Subsurface Weight' in bs.inputs: bs.inputs['Subsurface Weight'].default_value = sss
    if coat and 'Coat Weight' in bs.inputs: bs.inputs['Coat Weight'].default_value = coat
    return m

def mat_c(name, h, rough=.4, metal=0., coat=0., emit=0., alpha=1.):
    m = bpy.data.materials.new(name); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = lin(h); bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
    if coat: bs.inputs['Coat Weight'].default_value = coat
    if emit: bs.inputs['Emission Color'].default_value = lin(h); bs.inputs['Emission Strength'].default_value = emit
    if alpha < 1: bs.inputs['Alpha'].default_value = alpha
    return m

def give(o, m): o.data.materials.clear(); o.data.materials.append(m); return o

def cube(loc, size, m, bevel=.01, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = active(); o.scale = size
    bake(o); give(o, m); add_mods(o, bevel=bevel); return o

def cyl(loc, r, depth, m, rot=(0, 0, 0), verts=32, bevel=0, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot); o = active()
    o.scale = scale; bake(o); give(o, m); smooth(o)
    for p in o.data.polygons:
        if len(p.vertices) > 4: p.use_smooth = False
    add_mods(o, bevel=bevel); return o

def sphere(loc, r, m, scale=(1, 1, 1), seg=32, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=r, location=loc); o = active()
    o.scale = scale; bake(o); give(o, m); return smooth(o)

def ico(loc, r, m, scale=(1, 1, 1), sub=4):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=loc); o = active()
    o.scale = scale; bake(o); give(o, m); return smooth(o)

def torus(loc, R_, r, m, rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R_, minor_radius=r, location=loc, rotation=rot); o = active()
    o.scale = scale; bake(o); give(o, m); return smooth(o)

def displace(o, strength, size=.5, kind='CLOUDS', seed=0):
    tex = bpy.data.textures.new(f'tx{seed}{random.random()}', kind); tex.noise_scale = size
    md = o.modifiers.new('dp', 'DISPLACE'); md.texture = tex; md.strength = strength; md.texture_coords = 'GLOBAL'
    md.mid_level = .5
    return o

def cut_below(o, z=0.0):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, 0, z), plane_no=(0, 0, 1), clear_inner=True)
    bm.to_mesh(o.data); bm.free(); return o

def xform(objs, M):
    for o in objs:
        bake(o); o.data.transform(M)

def lathe(name, prof, m, NS=40, rfun=None, sub=1):
    verts = []; faces = []; uvs = []
    for i, (r, z) in enumerate(prof):
        for j in range(NS):
            a = j/NS*2*math.pi; rr = r*(rfun(a, i, z) if rfun else 1)
            verts.append((rr*math.cos(a), rr*math.sin(a), z)); uvs.append((j/NS, i/(len(prof)-1)))
    for i in range(len(prof)-1):
        for j in range(NS):
            a = i*NS+j; b = i*NS+(j+1) % NS; faces.append((a, b, b+NS, a+NS))
    return F.mk_obj(name, verts, faces, uvs, m, subsurf=sub)

class Acc:
    def __init__(s): s.v = []; s.f = []; s.uv = []
    def tube(s, pts, radii, seg=8, cap=True):
        pts = [Vector(p) for p in pts]; n = len(pts); base = len(s.v)
        for i, p in enumerate(pts):
            T = (pts[min(n-1, i+1)]-pts[max(0, i-1)]).normalized()
            ref = Vector((0, 0, 1)) if abs(T.z) < .9 else Vector((1, 0, 0))
            Nn = T.cross(ref).normalized(); B = T.cross(Nn)
            for j in range(seg):
                a = j/seg*2*math.pi; s.v.append(tuple(p+(Nn*math.cos(a)+B*math.sin(a))*radii[i])); s.uv.append((j/seg, i/(n-1)))
        for i in range(n-1):
            for j in range(seg):
                a = base+i*seg+j; b = base+i*seg+(j+1) % seg; s.f.append((a, b, b+seg, a+seg))
        if cap:
            c = len(s.v); s.v.append(tuple(pts[-1])); s.uv.append((.5, 1)); last = base+(n-1)*seg
            for j in range(seg): s.f.append((last+j, last+(j+1) % seg, c))
    def obj(s, name, m, sub=0): return F.mk_obj(name, s.v, s.f, s.uv, m, subsurf=sub)

# ================= SÜS MODELLERİ =================
def d_rock(fr=0):
    m = mat_proc('rock', '#33383e', '#8a9097', scale=3.5, bump=.6, moss='#4a7330', detail=6)
    for i, (x, y, z, sx, sy, sz) in enumerate([(0, .08, .22, .32, .28, .3), (-.3, -.02, .16, .33, .27, .24), (.26, 0, .15, .3, .25, .22), (-.52, -.08, .07, .17, .15, .12), (.52, -.06, .06, .15, .13, .1)]):
        o = ico((x, y, z), 1, m, (sx, sy, sz)); displace(o, .09, .35, seed=i)

def d_bubbler(fr=0):
    m = mat_proc('stone', '#5b6068', '#c9cdd2', scale=6, bump=.4)
    o = cyl((0, 0, .03), .17, .07, m, scale=(1, .62, 1), bevel=.025)
    md = mat_c('hole', '#151515', rough=.8)
    for i in range(-2, 3): cyl((i*.05, 0, .068), .011, .006, md, verts=12)

def d_star(fr=0):
    m = mat_proc('star', '#e0521c', '#ffb36b', scale=40, tex='voronoi', bump=-.8, rough=.55, pos=(.0, .6))
    NR, NS = 10, 120; verts = [(0, 0, .055)]; faces = []
    for i in range(1, NR+1):
        k = i/NR
        for j in range(NS):
            a = j/NS*2*math.pi+.3; r = (.07+.2*(.5+.5*math.cos(5*(a-.3)))**2.2)*k
            verts.append((r*math.cos(a), r*math.sin(a), .055*(1-k**2.2)+.004))
    for j in range(NS): faces.append((0, 1+j, 1+(j+1) % NS))
    for i in range(NR-1):
        for j in range(NS):
            a = 1+i*NS+j; b = 1+i*NS+(j+1) % NS; faces.append((a, b, b+NS, a+NS))
    F.mk_obj('star', verts, faces, None, m, subsurf=1)

def d_pebble(fr=0):
    cols = ['#ff6b6b', '#4dabf7', '#ffd43b', '#69db7c', '#da77f2', '#f1f3f5', '#ff922b']
    pos = [(-.14, .1, .07), (.04, .11, .08), (.18, .1, .06), (-.22, -.02, .09), (-.06, -.04, .1), (.12, -.03, .09), (.26, -.05, .07)]
    for i, (x, y, r) in enumerate(pos):
        sphere((x, y, r*.6), r, mat_c(f'p{i}', cols[i], rough=.15, coat=.8), scale=(1, .9, .62))

def d_urchin(fr=0):
    md = mat_c('urch', '#3b1a4f', rough=.3, coat=.4)
    sphere((0, 0, .1), .13, mat_proc('urb', '#2a1038', '#7a3a9a', scale=30, tex='voronoi', bump=.4), scale=(1, 1, .85))
    acc = Acc(); n = 220; rnd = random.Random(3)
    for i in range(n):
        z = 1-2*(i+.5)/n; r = math.sqrt(1-z*z); a = i*2.39996
        d = Vector((r*math.cos(a), r*math.sin(a), z))
        if d.z < -.35: continue
        L = rnd.uniform(.16, .26); p0 = Vector((0, 0, .1))+d*.11
        acc.tube([p0, p0+d*L], [.007, .0012], seg=5)
    acc.obj('spines', md)

def d_log(fr=0):
    bark = mat_proc('bark', '#2e1d0e', '#7a5636', scale=6, stretch=(1, 7, 7), bump=.7, moss='#4a7330', detail=8)
    rings = mat_proc('rings', '#8a6338', '#c9a273', tex='rings', scale=9, distort=2, bump=.2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=.17, depth=1.25, location=(0, 0, .15), rotation=(0, math.pi/2, .06))
    o = active(); bake(o); o.data.materials.append(bark); o.data.materials.append(rings)
    for p in o.data.polygons:
        if abs(p.normal.x) > .9: p.material_index = 1
        else: p.use_smooth = True
    sub = o.modifiers.new('sb', 'SUBSURF'); sub.levels = sub.render_levels = 1
    me = o.data; bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if abs((e.verts[0].co-e.verts[1].co).x) > .5], cuts=10)
    bm.to_mesh(me); bm.free()
    displace(o, .05, .25, seed=1)
    br = cyl((-.12, -.02, .36), .045, .32, bark, rot=(0, -.55, 0)); displace(br, .02, .2, seed=2)

def d_brain(fr=0):
    m = mat_proc('brain', '#7d5422', '#f2d38f', tex='brain', scale=5, distort=22, detail=3, bump=1.0, rough=.7, pos=(.25, .7), wave_dir='X')
    o = ico((0, 0, 0), 1, m, (.47, .42, .48), sub=5); cut_below(o, .0); displace(o, .015, .1, seed=4)

def d_amph(fr=0):
    m = mat_proc('terra', '#6e2e14', '#c97a42', scale=4, bump=.25, moss='#4f7a35')
    prof = [(0.001, 0), (.05, .01), (.12, .08), (.26, .28), (.29, .42), (.26, .56), (.17, .68), (.09, .74), (.075, .82), (.085, .86), (.1, .9), (.085, .925), (.07, .91), (.06, .88)]
    body = lathe('amph', prof, m, NS=48)
    band = mat_c('band', '#2a120a', rough=.6)
    t1 = torus((0, 0, .54), .285, .008, band); t2 = torus((0, 0, .6), .272, .008, band)
    h1 = torus((.16, 0, .77), .07, .018, m, rot=(math.pi/2, 0, 0), scale=(1, 1, 1.4)); h2 = torus((-.16, 0, .77), .07, .018, m, rot=(math.pi/2, 0, 0), scale=(1, 1, 1.4))
    bar = mat_c('barn', '#ddd5c4', rough=.6); rnd = random.Random(2); bs = []
    for i in range(9):
        a = rnd.uniform(-1.9, -.6); z = rnd.uniform(.12, .5); r = .27*math.sin(min(math.pi, (z+.05)*3.2))*.95+.02
        bs.append(sphere((r*math.cos(a), r*math.sin(a), z), .018, bar, scale=(1, 1, .7)))
    objs = [body, t1, t2, h1, h2]+bs
    M = Matrix.Translation((0, 0, .02)) @ Matrix.Rotation(.2, 4, 'Y') @ Matrix.Rotation(.12, 4, 'X')
    xform(objs, M)
    for o in objs: cut_below(o, 0)

def d_column(fr=0):
    m = mat_proc('marble', '#8d887c', '#e9e4d8', tex='wave', scale=3, distort=9, detail=6, bump=.15, rough=.35, wave_dir='DIAGONAL')
    cube((0, 0, .04), (.62, .62, .08), m, bevel=.01); cube((0, 0, .115), (.52, .52, .07), m, bevel=.01)
    rnd = random.Random(7); NS = 60; prof = []
    rows = 24; tops = [1.0+.22*rnd.random() for _ in range(NS)]
    verts = []; faces = []
    for i in range(rows+1):
        k = i/rows
        for j in range(NS):
            a = j/NS*2*math.pi; r = .2*(1-.06*abs(math.sin(10*a)))
            z = .15+k*(tops[j]-.15) if i == rows else .15+k*(1.0-.15)
            if i == rows: z = tops[j]
            verts.append((r*math.cos(a), r*math.sin(a), z))
    for i in range(rows):
        for j in range(NS):
            a = i*NS+j; b = i*NS+(j+1) % NS; faces.append((a, b, b+NS, a+NS))
    c = len(verts); verts.append((0, 0, 1.08))
    for j in range(NS): faces.append((rows*NS+j, rows*NS+(j+1) % NS, c))
    o = F.mk_obj('col', verts, faces, None, m); smooth(o)
    dr = cyl((.52, .12, .19), .19, .38, m, rot=(0, math.pi/2, .3), verts=40)

def d_volcano(fr=0):
    rock = mat_proc('vrock', '#1d1614', '#6b5750', scale=5, bump=.8, stretch=(6, 6, 1), emit='#ff7a1a', emit_thr=.72, detail=6)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=.66, radius2=.1, depth=1.0, location=(0, 0, .5)); o = active(); bake(o); give(o, rock); smooth(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    top = [f for f in bm.faces if f.normal.z > .95 and f.calc_center_median().z > .9]
    bmesh.ops.delete(bm, geom=top, context='FACES')
    bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if abs(e.verts[0].co.z-e.verts[1].co.z) > .5], cuts=14)
    bm.to_mesh(o.data); bm.free()
    displace(o, .07, .25, seed=6); add_mods(o, sub=1)
    lava = mat_c('lava', '#ffb030', rough=.4, emit=6)
    cyl((0, 0, .965), .095, .02, lava, verts=32)

def d_shell(fr=0):
    opn = [0, .33, .66, 1.0][fr]
    shell = mat_proc('shell', '#8e6fa8', '#efe2f7', scale=3, bump=.2, rough=.35, coat=.5)
    inner = mat_c('mantle', '#c96a92', rough=.3, coat=.6)
    pearl = mat_c('pearl', '#f7f9ff', rough=.08, coat=1)
    def half(name, up):
        NR, NS = 16, 72; verts = []; faces = []
        for i in range(NR+1):
            k = i/NR
            for j in range(NS+1):
                a = j/NS*math.pi
                x = .46*math.cos(a)*k; y = .34*(1-math.sin(a)*k*1.0)-.34*0+(-.34*math.sin(a)*k)+.0
                y = .3-.62*math.sin(a)*k
                rib = 1+.09*abs(math.cos(9*a))**.6*k
                z = .16*math.sqrt(max(0, 1-k*k))*rib*up+(.004*up)
                verts.append((x, y, z))
        for i in range(NR):
            for j in range(NS):
                a = i*(NS+1)+j; faces.append((a, a+1, a+NS+2, a+NS+1) if up > 0 else (a, a+NS+1, a+NS+2, a+1))
        return smooth(F.mk_obj(name, verts, faces, None, shell, subsurf=1))
    lo = half('lo', -1); hi = half('hi', 1)
    for o in (lo, hi): o.location.z += .16
    bake(lo); bake(hi)
    ang = -math.radians(55)*opn
    hi.data.transform(Matrix.Translation((0, .3, .16)) @ Matrix.Rotation(ang, 4, 'X') @ Matrix.Translation((0, -.3, -.16)))
    sphere((0, -.02, .16), .36, inner, scale=(1.05, .78, .12))
    if opn > .1: sphere((0, -.05, .2), .065, pearl)

def d_chest(fr=0):
    wood = mat_proc('wood', '#3f230e', '#8e5829', tex='wave', scale=12, distort=4, bump=.3, wave_dir='Z', rough=.65)
    gold = mat_c('gold', '#e8b84a', rough=.25, metal=.95)
    coin = mat_c('coin', '#ffd15c', rough=.18, metal=1, emit=.25)
    cube((0, 0, .2), (.84, .48, .4), wood, bevel=.02)
    for x in (-.3, .3): cube((x, 0, .2), (.06, .5, .41), gold, bevel=.006)
    cube((0, 0, .4), (.86, .5, .03), gold, bevel=.006)
    cube((0, -.245, .3), (.1, .02, .12), gold, bevel=.004)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.24, depth=.84, location=(0, 0, 0), rotation=(0, math.pi/2, 0))
    lid = active(); bake(lid)
    bm = bmesh.new(); bm.from_mesh(lid.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -.001], context='VERTS'); bm.to_mesh(lid.data); bm.free()
    give(lid, wood); smooth(lid); sd = lid.modifiers.new('s', 'SOLIDIFY'); sd.thickness = .03
    ang = -105*fr/7   # 8 kare: kapalı -> açık
    lid.data.transform(Matrix.Translation((0, .24, .41)) @ Matrix.Rotation(math.radians(ang), 4, 'X') @ Matrix.Translation((0, -.24, 0)))
    sphere((0, 0, .4), .36, coin, scale=(1.1, .6, .25))
    rnd = random.Random(4)
    for i in range(40):
        a = rnd.uniform(0, 2*math.pi); r = rnd.uniform(0, .34)
        cyl((math.cos(a)*r, math.sin(a)*r*.55, .42+.07*(1-r/.34)+rnd.uniform(0, .02)), .035, .008, coin, rot=(rnd.uniform(-.6, .6), rnd.uniform(-.6, .6), 0), verts=16)

def d_castle(fr=0):
    stone = mat_proc('cstone', '#2f2c27', '#8c867a', tex='brick', scale=9, bump=.5, moss='#4a7330', rough=.8, rot=(math.pi/2, 0, 0))
    dark = mat_c('win', '#0c1620', rough=.9); glow = mat_c('door', '#4fd1ff', rough=.5, emit=1.5)
    def tower(x, r, h):
        cyl((x, 0, h/2), r, h, stone, verts=40)
        for i in range(12):
            a = i/12*2*math.pi
            if i % 2 == 0: cube((x+math.cos(a)*r*.9, math.sin(a)*r*.9, h+.04), (.06, .06, .08), stone, bevel=.004, rot=(0, 0, a))
        cyl((x, 0, h+.005), r*.92, .02, stone, verts=40)
        cube((x, -r-.003, h*.75), (.055, .02, .09), dark, bevel=0)
    cube((0, .05, .6), (.36, .3, 1.2), stone, bevel=.01)
    for i in range(4): cube((-.135+i*.09, -.1, 1.24), (.05, .05, .08), stone, bevel=.004)
    cube((0, -.103, 1.0), (.06, .02, .1), dark, bevel=0)
    cube((0, 0, .35), (1.0, .28, .7), stone, bevel=.01)
    for i in range(10): cube((-.45+i*.1, -.12, .74), (.055, .05, .08), stone, bevel=.004)
    cube((0, -.142, .2), (.22, .02, .4), dark, bevel=0); cyl((0, -.142, .4), .11, .02, dark, rot=(math.pi/2, 0, 0))
    cube((0, -.13, .17), (.16, .02, .3), glow, bevel=0)
    tower(-.55, .19, 1.35); tower(.55, .17, 1.15)

def d_diver(fr=0):
    brass = mat_c('brass', '#d9a43c', rough=.28, metal=.9)
    suit = mat_proc('suit', '#3a4652', '#7f91a3', scale=5, bump=.15, rough=.85, pos=(.3, .75))
    dark = mat_c('boot', '#222222', rough=.6); glass = mat_c('glass', '#0b2a44', rough=.05, coat=1, emit=.3)
    for x in (-.085, .085): cube((x, -.02, .05), (.13, .2, .1), dark, bevel=.03)
    for x in (-.085, .085): o = cyl((x, 0, .3), .068, .42, suit, verts=24); add_mods(o, bevel=.03)
    o = cube((0, 0, .66), (.38, .27, .4), suit, bevel=.08); add_mods(o, sub=2)
    cube((0, 0, .49), (.4, .29, .05), dark, bevel=.01); cube((0, -.15, .49), (.07, .02, .05), brass, bevel=.005)
    cyl((0, 0, .87), .22, .07, brass, scale=(1, .75, 1), bevel=.02)
    hel = sphere((0, 0, 1.05), .2, brass, seg=48, rings=24)
    bm = bmesh.new(); bm.from_mesh(hel.data); cen = Vector((0, 0, 1.05))
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f.calc_center_median()-cen).normalized().dot(Vector((0, -1, 0))) > math.cos(math.radians(31))], context='FACES')
    bm.to_mesh(hel.data); bm.free()
    sd = hel.modifiers.new('s', 'SOLIDIFY'); sd.thickness = .012
    inn = sphere((0, 0, 1.05), .188, mat_c('inner', '#2a2018', rough=.9))
    bm = bmesh.new(); bm.from_mesh(inn.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f.calc_center_median()-cen).normalized().dot(Vector((0, -1, 0))) > math.cos(math.radians(55))], context='FACES')
    bm.to_mesh(inn.data); bm.free()
    skin = mat_c('skin', '#f2c29b', rough=.55); eye = mat_c('eye', '#121212', rough=.1, coat=1); cheek = mat_c('cheek', '#f28e8e', rough=.6)
    sphere((0, -.07, 1.045), .112, skin)
    for sx in (-1, 1):
        sphere((sx*.042, -.171, 1.07), .017, eye); sphere((sx*.042+.006, -.186, 1.077), .005, mat_c('glint', '#ffffff', rough=0, emit=1))
        sphere((sx*.068, -.158, 1.027), .02, cheek, scale=(1, .5, .7))
    sphere((0, -.18, 1.045), .02, skin)
    torus((0, -.165, 1.012), .03, .006, mat_c('mouth', '#7a2a1a', rough=.6), rot=(math.pi/2, 0, 0), scale=(1, 1, .55))
    vis = []
    vis.append(torus((0, -.2, 1.05), .1, .024, brass, rot=(math.pi/2, 0, 0))); vis.append(cyl((0, -.204, 1.05), .088, .012, glass, rot=(math.pi/2, 0, 0)))
    for sx in (-1, 1): torus((sx*.18, -.04, 1.05), .055, .016, brass, rot=(0, math.pi/2, 0)); cyl((sx*.185, -.04, 1.05), .045, .01, glass, rot=(0, math.pi/2, 0))
    for i in range(8):
        a = i/8*2*math.pi; vis.append(sphere((math.cos(a)*.128, -.214, 1.05+math.sin(a)*.128), .012, brass))
    vis.append(cyl((.122, -.2, 1.05), .014, .07, brass, verts=12))   # menteşe
    hx_, hy_ = .122, -.2; th = math.radians(115*fr/7)   # 8 kare: kask camı kapalı -> açık
    M = Matrix.Translation((hx_, hy_, 0)) @ Matrix.Rotation(th, 4, 'Z') @ Matrix.Translation((-hx_, -hy_, 0))
    for o in vis[:-1]: o.data.transform(M)
    acc = Acc(); acc.tube([(-.22, 0, .8), (-.28, -.02, .62), (-.3, -.04, .5)], [.06, .058, .056], seg=16); acc.obj('armL', suit, sub=1)
    acc = Acc(); acc.tube([(.22, 0, .8), (.32, -.03, .92), (.38, -.06, 1.1)], [.06, .058, .056], seg=16); acc.obj('armR', suit, sub=1)
    sphere((-.3, -.05, .46), .06, dark); sphere((.39, -.07, 1.15), .06, dark)
    pts = [(-.12, .14, 1.12)]; P0, P1, P2, P3 = Vector((-.12, .14, 1.12)), Vector((-.35, .25, 1.15)), Vector((-.3, .3, 1.45)), Vector((-.45, .32, 1.62))
    pts = [tuple((1-t)**3*P0+3*(1-t)**2*t*P1+3*(1-t)*t*t*P2+t**3*P3) for t in np.linspace(0, 1, 24)]
    acc = Acc(); acc.tube(pts, [.026]*24, seg=12); acc.obj('hose', dark, sub=1)

def d_coral(fr=0):
    m = mat_proc('coral', '#e8507e', '#ffb3c8', scale=14, tex='voronoi', bump=.5, sss=.25, rough=.55, pos=(.0, .7))
    tip = mat_c('ctip', '#ffd6e2', rough=.4, coat=.3)
    rnd = random.Random(11); acc = Acc(); tips = []
    def br(p, d, L, r, dep):
        q = p+d*L; acc.tube([p, (p+q)/2+Vector((rnd.uniform(-.02, .02), rnd.uniform(-.02, .02), 0)), q], [r, r*.9, r*.8], seg=10, cap=False)
        if dep >= 4: tips.append((q, r*.9)); return
        n = 3 if rnd.random() < .4 else 2
        for i in range(n):
            ax = Vector((rnd.uniform(-1, 1), rnd.uniform(-.6, .6), 0)).normalized()
            nd = (Matrix.Rotation((i-(n-1)/2)*rnd.uniform(.45, .75), 3, d.cross(ax).normalized() if d.cross(ax).length > .01 else 'X') @ d).normalized()
            nd.z = max(nd.z, .2); nd.normalize()
            br(q, nd, L*rnd.uniform(.68, .82), r*.72, dep+1)
    br(Vector((0, 0, 0)), Vector((0, 0, 1)), .3, .055, 0)
    acc.obj('coral', m, sub=1)
    for (q, r) in tips: sphere(tuple(q), r*1.1, tip, seg=12, rings=8)

def d_ship(fr=0):
    wood = mat_proc('hull', '#2c1a0c', '#7a5232', tex='wave', scale=14, distort=1.5, wave_dir='Z', bump=.35, moss='#4a7330', rough=.75)
    deck = mat_proc('deck', '#4a3018', '#9a7046', tex='wave', scale=16, distort=1, wave_dir='X', bump=.3, rough=.8)
    brass = mat_c('pbrass', '#c9a24a', rough=.3, metal=.9); dark = mat_c('hole', '#070504', rough=1)
    portg = mat_c('portg', '#5ad2ff', rough=.1, emit=.6)
    sail = mat_proc('sail', '#bfb08a', '#ece2c4', scale=6, bump=.1, rough=.9)
    NX, NA = 40, 18; verts = []; faces = []
    xs = np.linspace(-1.1, 1.1, NX)
    for x in xs:
        u = x/1.1; w = .36*max(.03, (1-abs(u)**(2.6 if u > 0 else 6)))**.5; d = .55*(1-.25*u*u); top = .55+.12*u*u
        for j in range(NA+1):
            a = j/NA*math.pi; verts.append((x, w*math.cos(a), top-d*math.sin(a)))
    for i in range(NX-1):
        for j in range(NA):
            a = i*(NA+1)+j; faces.append((a, a+NA+1, a+NA+2, a+1))
    hull = smooth(F.mk_obj('hull', verts, faces, None, wood, subsurf=1)); sd = hull.modifiers.new('s', 'SOLIDIFY'); sd.thickness = .03
    dv = []; df = []
    for i, x in enumerate(xs):
        u = x/1.1; w = .36*max(.03, (1-abs(u)**(2.6 if u > 0 else 6)))**.5; top = .55+.12*u*u-.04
        dv += [(x, w*.97, top), (x, -w*.97, top)]
    for i in range(NX-1): df.append((2*i, 2*i+2, 2*i+3, 2*i+1))
    dk = F.mk_obj('deck', dv, df, None, deck)
    objs = [hull, dk]
    for i, x in enumerate(np.linspace(-.85, .75, 12)):
        u = x/1.1; w = .36*max(.03, (1-abs(u)**(2.6 if u > 0 else 6)))**.5; top = .55+.12*u*u
        objs.append(cyl((x, -w, top+.06), .012, .12, wood, verts=8))
    for x in (-.1, .25, .6):
        u = x/1.1; w = .36*(1-abs(u)**2.6)**.5
        objs.append(torus((x, -w-.005, .36), .055, .014, brass, rot=(math.pi/2, 0, 0))); objs.append(cyl((x, -w-.006, .36), .045, .01, portg, rot=(math.pi/2, 0, 0)))
    objs.append(sphere((-.55, -.33, .3), .14, dark, scale=(1.2, .2, .8)))
    mast = cyl((-.05, 0, 1.05), .045, 1.2, wood, verts=16); yard = cyl((-.05, 0, 1.35), .025, .8, wood, rot=(0, math.pi/2, 0), verts=12)
    sv = []; sf = []; rnd = random.Random(3)
    for i in range(9):
        for j in range(7):
            x = -.42+i*.105; z = 1.33-j*.08-(.06*rnd.random() if j == 6 else 0)
            sv.append((x-.05, -.06+.04*math.sin(i*.8)*(j/6), z))
    for i in range(8):
        for j in range(6):
            if (i, j) in ((2, 3), (5, 2), (6, 4), (3, 5)): continue
            a = i*7+j; sf.append((a, a+7, a+8, a+1))
    sl = F.mk_obj('sail', sv, sf, None, sail, subsurf=1)
    objs += [mast, yard, sl]
    M = Matrix.Translation((0, 0, -.18)) @ Matrix.Rotation(math.radians(14), 4, 'X') @ Matrix.Rotation(math.radians(-5), 4, 'Y')
    xform(objs, M)
    for o in objs: cut_below(o, 0)


def clean_shadow(im):
    """Gölge yakalayıcının kare kenarında bıraktığı gri dikdörtgeni temizler."""
    a = np.asarray(im.convert('RGBA')).astype(float)
    rgb, al = a[..., :3], a[..., 3]/255
    sh = (al < .985) & (rgb.max(-1) < 40)
    h, w = al.shape
    border = np.concatenate([al[:6].ravel(), al[-6:].ravel(), al[:, :6].ravel(), al[:, -6:].ravel()])
    bmask = np.concatenate([sh[:6].ravel(), sh[-6:].ravel(), sh[:, :6].ravel(), sh[:, -6:].ravel()])
    base = np.percentile(border[bmask], 75) if bmask.any() else 0
    base = min(base, .35)
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.minimum.reduce([xx, w-1-xx, yy, h-1-yy]).astype(float)
    m = np.clip(d/(.12*min(w, h)), 0, 1); m = m*m*(3-2*m)
    al2 = np.where(sh, np.clip((al-base)/(1-base), 0, 1)*m*.85, al)
    a[..., 3] = al2*255
    return Image.fromarray(a.astype('uint8'), 'RGBA')

def fix_all():
    import glob
    for m in glob.glob(f'{SPR}/d_*_meta.json'):
        meta = json.load(open(m)); f = m.replace('_meta.json', '_sheet.webp'); im = Image.open(f)
        out = Image.new('RGBA', im.size, (0, 0, 0, 0))
        for i in range(meta['n']):
            tile = im.crop((i*meta['fw'], 0, (i+1)*meta['fw'], meta['fh'])); out.paste(clean_shadow(tile), (i*meta['fw'], 0))
        out.save(f, 'WEBP', quality=84, method=6); print('fix', os.path.basename(f))


# ================= v8: 3D bitkiler ve yeni süsler =================
NFR_PLANT = 12

def mat_grad(name, c_base, c_tip, rough=.45, sss=.0, trans=.25, coat=.2, veins=0., emit=0.):
    """UV.y boyunca dipten uca renk geçişi; ince yapraklar için ışık geçirgenliği."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links
    bs = N['Principled BSDF']; out = N['Material Output']
    uv = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(uv.outputs['UV'], sep.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = lin(c_base); ramp.color_ramp.elements[1].color = lin(c_tip)
    L.new(sep.outputs['Y'], ramp.inputs['Fac'])
    col = ramp.outputs['Color']
    if veins:
        wv = N.new('ShaderNodeTexWave'); wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = veins; wv.inputs['Distortion'].default_value = 2
        L.new(uv.outputs['UV'], wv.inputs['Vector'])
        mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = .18
        L.new(col, mix.inputs[6]); L.new(wv.outputs['Color'], mix.inputs[7]); col = mix.outputs[2]
    L.new(col, bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = rough
    if sss: bs.inputs['Subsurface Weight'].default_value = sss
    if coat: bs.inputs['Coat Weight'].default_value = coat
    if emit:
        L.new(col, bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = emit
    if trans:
        tr = N.new('ShaderNodeBsdfTranslucent'); L.new(col, tr.inputs['Color'])
        mx = N.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = trans
        L.new(bs.outputs['BSDF'], mx.inputs[1]); L.new(tr.outputs['BSDF'], mx.inputs[2]); L.new(mx.outputs['Shader'], out.inputs['Surface'])
    return m

def ribbon(acc, path, widths, side, twist=0.):
    """path: Nx3 noktalar, widths: N, side: başlangıç yan yönü (Vector). İki yüzlü şerit."""
    n = len(path); base = len(acc.v)
    for i, p in enumerate(path):
        p = Vector(p); T = (Vector(path[min(n-1, i+1)])-Vector(path[max(0, i-1)])).normalized()
        sd = Matrix.Rotation(twist*i/(n-1), 3, T) @ side
        sd = (sd-T*sd.dot(T)).normalized()
        for k in (-1, 1):
            acc.v.append(tuple(p+sd*widths[i]*.5*k)); acc.uv.append(((k+1)/2, i/(n-1)))
    for i in range(n-1):
        a = base+2*i; acc.f.append((a, a+1, a+3, a+2))

def sway_path(bx, by, H, lean, amp, ph, fr, n=28, k=2.2, curl=0.):
    pts = []; w = 2*math.pi*fr/NFR_PLANT
    for i in range(n):
        t = i/(n-1); z = H*t*(1-.04*math.sin(w+ph)*t)
        sx = lean[0]*t*H+amp*H*t**1.6*math.sin(w+ph-t*k)
        sy = lean[1]*t*H+amp*.5*H*t**1.6*math.cos(w+ph-t*k)+curl*t*t*H
        pts.append((bx+sx, by+sy, z))
    return pts

def plant_base(r, m):
    o = ico((0, 0, -.01), r, m, scale=(1, .8, .35), sub=3); displace(o, .02, .08); return o

def d_weed(fr=0, red=False):
    rnd = random.Random(31 if not red else 47)
    if not red:
        m = mat_grad('weed', '#1e5a26', '#8fd36a', sss=.15, trans=.35, veins=30)
        n, H0, H1, W0 = 8, 1.1, 1.8, .085
    else:
        m = mat_grad('rweed', '#5a1424', '#ff6a5a', sss=.15, trans=.3)
        n, H0, H1, W0 = 0, .55, 1.05, .05
    acc = Acc()
    for i in range(n):
        bx = rnd.uniform(-.17, .17); by = rnd.uniform(-.08, .08); H = rnd.uniform(H0, H1)
        path = sway_path(bx, by, H, (bx*.35, rnd.uniform(-.05, .05)), rnd.uniform(.05, .09), rnd.uniform(0, 6.3), fr)
        ws = [W0*rnd.uniform(.8, 1.15)*(1-.85*(i_/27)**3) for i_ in range(28)]
        ribbon(acc, path, ws, Vector((math.cos(rnd.uniform(0, 3.1)), math.sin(rnd.uniform(0, 3.1)), 0)), twist=rnd.uniform(-1.2, 1.2))
    if red:
        # kızıl yosun: gövde + çift yapraklar (rotala gibi)
        stem = mat_c('rstem', '#7a1e2a', rough=.5)
        for i in range(9):
            bx = rnd.uniform(-.18, .18); by = rnd.uniform(-.08, .08); H = rnd.uniform(H0, H1)
            path = sway_path(bx, by, H, (bx*.3, 0), rnd.uniform(.05, .08), rnd.uniform(0, 6.3), fr, n=20)
            Acc_s = Acc(); Acc_s.tube(path, [.012*(1-.5*j/19) for j in range(20)], seg=6); Acc_s.obj(f'rs{i}', stem)
            for j in range(3, 20, 2):
                p = Vector(path[j]); T = (Vector(path[min(19, j+1)])-Vector(path[j-1])).normalized()
                for sg in (-1, 1):
                    a0 = (j*1.7+i)+(0 if sg > 0 else math.pi)
                    d = Vector((math.cos(a0), math.sin(a0), .35)).normalized()
                    L = .085*(1-.5*j/19); lp = [tuple(p+d*L*q+T*.015*q*q) for q in np.linspace(0, 1, 7)]
                    ribbon(acc, lp, [.045*math.sin(math.pi*q)*(1-.4*j/19)+.004 for q in np.linspace(0, 1, 7)], T.cross(d).normalized())
    o = acc.obj('weed', m, sub=1); sd = o.modifiers.new('sol', 'SOLIDIFY'); sd.thickness = .006
    plant_base(.16 if not red else .15, mat_c('wbase', '#3b4a24' if not red else '#4a2a22', rough=.8))

def d_redweed(fr=0): d_weed(fr, red=True)

def d_kelp(fr=0):
    rnd = random.Random(53)
    stip = mat_grad('stipe', '#3d2e12', '#8a7a2a', rough=.5, trans=.1)
    blade = mat_grad('kblade', '#6b5a1e', '#c9b24a', sss=.2, trans=.4, veins=18)
    blad = mat_c('bladder', '#a8902e', rough=.3, coat=.5)
    acc = Acc(); sacc = Acc()
    for s_ in range(3):
        bx = (s_-1)*.09; H = (2.55, 2.25, 1.95)[s_]
        path = sway_path(bx, rnd.uniform(-.04, .04), H, ((s_-1)*.05, 0), .07, s_*1.3, fr, n=40, k=2.6)
        sacc.tube(path, [.018*(1-.4*j/39) for j in range(40)], seg=7)
        for j in range(5, 40, 3):
            p = Vector(path[j]); T = (Vector(path[min(39, j+1)])-Vector(path[j-1])).normalized()
            a0 = j*2.4+s_; d = Vector((math.cos(a0), math.sin(a0)*.6, 0)); d = (d-T*d.dot(T)).normalized()
            L = rnd.uniform(.28, .42)*(1-.35*j/39); w = 2*math.pi*fr/NFR_PLANT
            lp = []
            for q in np.linspace(0, 1, 14):
                droop = -.35*q*q*L+.06*math.sin(w+j*.5+q*3)*q
                lp.append(tuple(p+d*L*q+T*droop))
            ribbon(acc, lp, [.11*math.sin(math.pi*min(1, q*1.15+.05))**.7*(1-.3*j/39)+.01 for q in np.linspace(0, 1, 14)], T, twist=.8)
            sphere(tuple(p+d*.02), .022, blad, seg=12, rings=8)
    sacc.obj('stipe', stip, sub=0)
    o = acc.obj('kblade', blade, sub=1); sd = o.modifiers.new('sol', 'SOLIDIFY'); sd.thickness = .005
    # yaprak kenarı dalgalı
    tex = bpy.data.textures.new('kw', 'CLOUDS'); tex.noise_scale = .06
    md = o.modifiers.new('dp', 'DISPLACE'); md.texture = tex; md.strength = .02
    plant_base(.18, mat_c('kbase', '#3a3020', rough=.85))

def d_anem(fr=0):
    rnd = random.Random(61); w = 2*math.pi*fr/NFR_PLANT
    col = mat_grad('acol', '#c86a3a', '#f0b27a', rough=.5, trans=0, sss=.25)
    ten = mat_grad('aten', '#d9c39a', '#c86cc8', rough=.35, trans=.25, sss=.3, coat=.4)
    tip = mat_c('atip', '#e9a6ff', rough=.3, coat=.6, emit=.15)
    prof = [(.16, 0), (.17, .04), (.15, .1), (.16, .15), (.22, .19), (.27, .205), (.2, .215), (0, .2)]
    lathe('acol', prof, col, NS=48, rfun=lambda a, i, z: 1+.05*math.sin(a*7))
    acc = Acc(); tips = []
    for ring_ in range(4):
        rr = .07+ring_*.065; cnt = 10+ring_*7
        for k in range(cnt):
            a = k/cnt*2*math.pi+ring_*.3; L = rnd.uniform(.17, .27)*(1.1-ring_*.08)
            base = Vector((rr*math.cos(a), rr*.85*math.sin(a), .205))
            out = Vector((math.cos(a), .85*math.sin(a), 0)); up = Vector((0, 0, 1))
            pts = []; ph = rnd.uniform(0, 6.3)
            for q in np.linspace(0, 1, 9):
                d = (up*(1-.45*q*(ring_+1)/4)+out*(.35+.55*q*(ring_+1)/4)).normalized()
                sw = Vector((math.cos(w+ph)*.05, math.sin(w+ph)*.04, 0))*q*q
                pts.append(base+d*L*q+sw)
            acc.tube(pts, [.017*(1-.35*q) for q in np.linspace(0, 1, 9)], seg=7, cap=False)
            tips.append((pts[-1], .019))
    acc.obj('aten', ten, sub=1)
    for (p, r) in tips: sphere(tuple(p), r, tip, seg=10, rings=6)

def d_fan(fr=0):
    rnd = random.Random(71); w = 2*math.pi*fr/NFR_PLANT
    m = mat_proc('fan', '#8a1f4a', '#ff7a9a', scale=60, tex='voronoi', bump=.6, rough=.55, sss=.2)
    acc = Acc()
    def P(x, z):
        k = z/1.15; return Vector((x+.04*k*k*math.sin(w), .09*(x/.55)**2+.05*k*math.sin(w+1.2), z))
    def br(x, z, ang, L, r, dep):
        x2 = x+math.sin(ang)*L; z2 = z+math.cos(ang)*L
        acc.tube([P(x, z), P((x+x2)/2+rnd.uniform(-.01, .01), (z+z2)/2), P(x2, z2)], [r, r*.92, r*.85], seg=6, cap=dep >= 6)
        if dep >= 6: return
        for s_ in (-1, 1):
            br(x2, z2, ang+s_*rnd.uniform(.25, .5), L*rnd.uniform(.72, .86), r*.78, dep+1)
    br(0, 0, 0, .27, .04, 0)
    for k in range(6):
        br(rnd.uniform(-.06, .06), .14, rnd.uniform(-.85, .85), .2, .024, 2)
    acc.obj('fan', m, sub=0)
    plant_base(.1, mat_c('fbase', '#5a3a3a', rough=.8))

def d_crystal(fr=0):
    rnd = random.Random(81)
    glass = [(c, mat_c(f'gl{i}', c, rough=.05)) for i, c in enumerate(['#3fa8e0', '#8a5ce6', '#2fbf9a'])]
    for _, m in glass:
        bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Transmission Weight'].default_value = .85; bs.inputs['IOR'].default_value = 1.5
        bs.inputs['Coat Weight'].default_value = .6; bs.inputs['Emission Color'].default_value = bs.inputs['Base Color'].default_value; bs.inputs['Emission Strength'].default_value = .12
    core = [mat_c(f'core{i}', c, emit=1.6) for i, c in enumerate(['#bdf0ff', '#e2cfff', '#c6fff0'])]
    rockm = mat_proc('crock', '#2c2f38', '#6c707a', scale=4, bump=.6)
    o = ico((0, 0, .02), .26, rockm, scale=(1.2, .9, .4), sub=3); displace(o, .05, .15)
    for (x, y, h, r, tx, ty, ci) in [(0, 0, .92, .1, 0, 0, 0), (-.2, .02, .6, .075, -.3, .05, 1), (.22, .03, .64, .07, .28, -.04, 2),
                                     (-.1, -.12, .42, .06, -.5, -.3, 2), (.12, -.13, .38, .055, .5, -.3, 1), (.05, .14, .5, .06, .1, .4, 0), (-.28, -.05, .32, .05, -.7, -.1, 0)]:
        objs = []
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=r, depth=h, location=(0, 0, h/2)); a = active(); objs.append(a)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=r, radius2=0, depth=r*2.2, location=(0, 0, h+r*1.1)); b = active(); objs.append(b)
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=r*.4, depth=h*.9, location=(0, 0, h*.5)); c = active(); objs.append(c)
        M = Matrix.Translation((x, y, -.05)) @ Matrix.Rotation(ty, 4, 'X') @ Matrix.Rotation(tx, 4, 'Y')
        for ob in objs: bake(ob); ob.data.transform(M)
        give(a, glass[ci][1]); give(b, glass[ci][1]); give(c, core[ci])

def d_arch(fr=0):
    rnd = random.Random(91)
    rockm = mat_proc('arock', '#3a302c', '#8a7462', scale=5, bump=.7, moss='#5a7a3a', detail=6)
    acc = Acc(); pts = []; rad = []
    for i in range(40):
        t = i/39; a = math.pi*(1-t)
        pts.append((.62*math.cos(a), .0, .88*math.sin(a)-.02)); rad.append(.2-.06*math.sin(math.pi*t))
    acc.tube(pts, rad, seg=16, cap=False)
    o = acc.obj('arch', rockm, sub=2); displace(o, .07, .18)
    cols = ['#ff7aa8', '#ffb347', '#b58cff', '#5fd3c4', '#ff6a5a', '#ffe066']
    for i in range(46):
        t = rnd.uniform(.05, .95); a = math.pi*(1-t); rr = .2-.06*math.sin(math.pi*t)
        n = Vector((math.cos(a), rnd.uniform(-.7, -.1), math.sin(a))).normalized()
        c = Vector((.62*math.cos(a), 0, .88*math.sin(a)-.02))+n*rr*.95
        if c.z < .05: continue
        m = mat_c(f'ac{i}', cols[i % len(cols)], rough=.5, coat=.3)
        if i % 5 == 0:
            cyl(tuple(c+n*.04), .022, .11, m, rot=(math.acos(max(-1, min(1, n.z))), 0, math.atan2(n.y, n.x)+math.pi/2))
        else:
            o2 = ico(tuple(c), rnd.uniform(.03, .06), m, scale=(1, 1, .7), sub=2); displace(o2, .012, .03)
    for x in (-.62, .62):
        o3 = ico((x, 0, .02), .24, rockm, scale=(1.1, 1, .45), sub=3); displace(o3, .05, .12)

DECOR = dict(rock=(d_rock, 1), bubbler=(d_bubbler, 1), star=(d_star, 1), pebble=(d_pebble, 1), urchin=(d_urchin, 1), log=(d_log, 1),
             brain=(d_brain, 1), amph=(d_amph, 1), column=(d_column, 1), volcano=(d_volcano, 1), shell=(d_shell, 4), chest=(d_chest, 8),
             castle=(d_castle, 1), diver=(d_diver, 8), coral=(d_coral, 1), ship=(d_ship, 1),
             weed=(d_weed, NFR_PLANT), redweed=(d_redweed, NFR_PLANT), kelp=(d_kelp, NFR_PLANT), anem=(d_anem, NFR_PLANT),
             fan=(d_fan, NFR_PLANT), crystal=(d_crystal, 1), arch=(d_arch, 1))

_MM = None
def mask_mat():
    m = bpy.data.materials.new('topmask'); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links
    for n in list(N):
        if n.type != 'OUTPUT_MATERIAL': N.remove(n)
    out = [n for n in N if n.type == 'OUTPUT_MATERIAL'][0]
    geo = N.new('ShaderNodeNewGeometry'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sep.inputs['Vector'])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -.1; mr.inputs['From Max'].default_value = .95
    mr.inputs['To Min'].default_value = .04; mr.inputs['To Max'].default_value = 1; mr.clamp = True
    L.new(sep.outputs['Z'], mr.inputs['Value'])
    pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.4; L.new(mr.outputs['Result'], pw.inputs[0])
    em = N.new('ShaderNodeEmission'); L.new(pw.outputs[0], em.inputs['Strength']); em.inputs['Color'].default_value = (1, 1, 1, 1)
    L.new(em.outputs['Emission'], out.inputs['Surface'])
    return m

def render_decor(tag, ppu):
    t0 = time.time(); fn, nfr = DECOR[tag]
    files = []; mfiles = []; meta = None
    pts_all = []
    # kadraj tüm karelerin birleşimine göre: önce her kareyi kur, noktaları topla
    for fr in range(nfr):
        sc, cam = F.setup_scene(300)
        fn(fr)
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        for o in bpy.context.scene.objects:
            if o.type != 'MESH': continue
            ev = o.evaluated_get(dg); me = ev.to_mesh()
            a = np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co', a); pts_all.append((np.array(o.matrix_world) @ np.c_[a.reshape(-1, 3), np.ones(len(me.vertices))].T).T[:, :3])
            ev.to_mesh_clear()
    pts = np.concatenate(pts_all)
    sh = pts.copy(); sh[:, 1] += .25*pts[:, 2]; sh[:, 2] = 0     # gölge payı (arkaya düşer)
    pts = np.concatenate([pts, sh])
    for fr in range(nfr):
        sc, cam = F.setup_scene(300)
        az, el = math.radians(14), math.radians(24)
        dv = Vector((math.cos(el)*math.sin(az), -math.cos(el)*math.cos(az), math.sin(el)))
        cam.location = dv*10; cam.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler()
        fn(fr)
        bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0)); pl = active(); pl.is_shadow_catcher = True
        bpy.context.view_layer.update()
        rw, rh, pp, ox, oy = F.fit_pts(sc, cam, pts, ppu=ppu, pad=.04)
        f = f'{OUT}/d_{tag}_{fr:02d}.png'; sc.render.filepath = f; bpy.ops.render.render(write_still=True); files.append(f)
        # üst yüzey maskesi: yukarı bakan yüzeyler beyaz (oyunda su ışığı ve toz için)
        pl.hide_render = True; vl = bpy.context.view_layer; vl.material_override = mask_mat(); smp = sc.cycles.samples; sc.cycles.samples = 8
        mf = f'{OUT}/m_{tag}_{fr:02d}.png'; sc.render.filepath = mf; bpy.ops.render.render(write_still=True); mfiles.append(mf)
        vl.material_override = None; sc.cycles.samples = smp
        meta = dict(id=tag, fw=rw, fh=rh, n=nfr, ppu=pp, ox=ox, oy=oy)
    sheet = Image.new('RGBA', (meta['fw']*nfr, meta['fh']), (0, 0, 0, 0))
    for i, f in enumerate(files): sheet.paste(clean_shadow(Image.open(f)), (i*meta['fw'], 0))
    sheet.save(f'{SPR}/d_{tag}_sheet.webp', 'WEBP', quality=84, method=6)
    json.dump(meta, open(f'{SPR}/d_{tag}_meta.json', 'w'))
    msheet = Image.new('RGBA', (meta['fw']*nfr, meta['fh']), (0, 0, 0, 0))
    for i, f in enumerate(mfiles):
        a_ = np.asarray(Image.open(f).convert('RGBA')).astype(float)
        g = a_[..., 0]/255; al = a_[..., 3]/255
        out = np.zeros_like(a_); out[..., :3] = 255; out[..., 3] = np.clip(g*al, 0, 1)*255
        msheet.paste(Image.fromarray(out.astype('uint8'), 'RGBA'), (i*meta['fw'], 0))
    msheet.save(f'{SPR}/m_{tag}_sheet.webp', 'WEBP', quality=70, method=6)
    json.dump(dict(meta, id='m_'+tag), open(f'{SPR}/m_{tag}_meta.json', 'w'))
    print(f'[d_{tag}] {meta["fw"]}x{meta["fh"]} x{nfr} {time.time()-t0:.1f}s', flush=True)

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'rock'
    F.SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    ppu = float(sys.argv[3]) if len(sys.argv) > 3 else 200
    for tag in (DECOR if which == 'all' else which.split(',')):
        render_decor(tag, ppu)
