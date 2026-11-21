"""Mercan Akvaryum - nadir misafirler (v9): kaplumbağa, ahtapot, keşiş yengeci, deniz salyangozu, fener balığı.
fish.py'nin sahne/kamera/sprite hattını kullanır. Kullanım: python visitors.py <id|all> [kare] [genislik] [samples]
Çıktı: assets/sprites/v_<id>_sheet.webp + meta
"""
import bpy, math, sys, os, random
import numpy as np
from mathutils import Vector, Matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F
import decor as D

def node_mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; build(nt, nt.nodes, nt.links, nt.nodes['Principled BSDF']); return m

def lin(h): return D.lin(h)

def rot_about(co, piv, axis, ang):
    R = np.array(Matrix.Rotation(ang, 3, axis)); return (co-piv) @ R.T+piv

# ---------------- kaplumbağa ----------------
def build_turtle(sp):
    def carapace(nt, N, L, bs):
        tc = N.new('ShaderNodeTexCoord'); vo = N.new('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = 5.5
        mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 1.3, 1); L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], vo.inputs['Vector'])
        vc = N.new('ShaderNodeTexVoronoi'); vc.inputs['Scale'].default_value = 5.5; L.new(mp.outputs['Vector'], vc.inputs['Vector'])
        rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = lin('#3a2812'); rp.color_ramp.elements[1].position = .07; rp.color_ramp.elements[1].color = lin('#ffffff')
        L.new(vo.outputs['Distance'], rp.inputs['Fac'])
        cell = N.new('ShaderNodeValToRGB'); cell.color_ramp.elements[0].color = lin('#8a6a2e'); cell.color_ramp.elements[1].color = lin('#d6a650')
        sep = N.new('ShaderNodeSeparateColor'); L.new(vc.outputs['Color'], sep.inputs['Color']); L.new(sep.outputs[0], cell.inputs['Fac'])
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
        L.new(cell.outputs['Color'], mx.inputs[6]); L.new(rp.outputs['Color'], mx.inputs[7])
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 40; L.new(tc.outputs['Object'], nz.inputs['Vector'])
        mx2 = N.new('ShaderNodeMix'); mx2.data_type = 'RGBA'; mx2.blend_type = 'OVERLAY'; mx2.inputs['Factor'].default_value = .25
        L.new(mx.outputs[2], mx2.inputs[6]); L.new(nz.outputs['Color'], mx2.inputs[7]); L.new(mx2.outputs[2], bs.inputs['Base Color'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .5; L.new(vo.outputs['Distance'], bp.inputs['Height']); L.new(bp.outputs['Normal'], bs.inputs['Normal'])
        bs.inputs['Roughness'].default_value = .45; bs.inputs['Coat Weight'].default_value = .15
    def skin(nt, N, L, bs):
        tc = N.new('ShaderNodeTexCoord'); vo = N.new('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = 26
        L.new(tc.outputs['Object'], vo.inputs['Vector'])
        rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = lin('#3c4a36'); rp.color_ramp.elements[1].position = .12; rp.color_ramp.elements[1].color = lin('#8fa070')
        L.new(vo.outputs['Distance'], rp.inputs['Fac']); L.new(rp.outputs['Color'], bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = .5
    m_car = node_mat('car', carapace); m_skin = node_mat('tskin', skin)
    m_pl = F.mat_plain('plast', (226, 205, 150), rough=.5); m_eye = F.mat_plain('teye', (12, 10, 8), rough=.05, coat=1)
    parts = []
    o = D.sphere((0, 0, .02), 1, m_car, scale=(.4, .31, .17), seg=48, rings=24)
    co = np.array([v.co[:] for v in o.data.vertices]); co[:, 2] = np.where(co[:, 2] < .02, .02+(co[:, 2]-.02)*.35, co[:, 2])
    o.data.vertices.foreach_set('co', co.ravel()); o.data.update(); o.name = 'shell'; parts.append(o)
    o = D.sphere((0, 0, -.005), 1, m_pl, scale=(.36, .27, .045)); o.name = 'plast'; parts.append(o)
    o = D.sphere((.44, 0, .02), 1, m_skin, scale=(.12, .08, .075)); o.name = 'head'; parts.append(o)
    a = F.Acc() if hasattr(F, 'Acc') else D.Acc(); a = D.Acc(); a.tube([(.28, 0, .015), (.34, 0, .02), (.4, 0, .022)], [.065, .06, .055], seg=12); o = a.obj('neck', m_skin); parts.append(o)
    for sg in (-1, 1):
        o = D.sphere((.5, sg*.062, .045), .016, m_eye); o.name = f'eye{sg}'; parts.append(o)
    flips = []
    for (x, y, sx, sy, yaw, nm) in [(.2, .2, .3, .08, 1.75, 'ff'), (-.26, .16, .13, .06, 2.45, 'rf')]:
        for sg in (-1, 1):
            o = D.sphere((0, 0, 0), 1, m_skin, scale=(sx, sy, .018))
            co = np.array([v.co[:] for v in o.data.vertices]); co[:, 0] += sx*.9   # kök başta
            M = np.array(Matrix.Rotation(sg*yaw, 3, 'Z')); co = co @ M.T+np.array([x, sg*y, 0])
            o.data.vertices.foreach_set('co', co.ravel()); o.data.update(); o.name = f'{nm}{sg}'
            o['piv'] = [x, sg*y, 0]; o['sg'] = sg; o['kind'] = nm; parts.append(o); flips.append(o)
    a = D.Acc(); a.tube([(-.36, 0, .01), (-.44, 0, 0)], [.03, .004], seg=8); parts.append(a.obj('tail', m_skin))
    def fn(parts, rest, phi):
        for ob in parts:
            co = rest[ob.name].copy()
            if 'kind' in ob.keys():
                piv = np.array(ob['piv']); sg = ob['sg']; big = ob['kind'] == 'ff'
                co = rot_about(co, piv, 'X', sg*(.6 if big else .25)*math.sin(phi))
                co = rot_about(co, piv, 'Z', sg*(.35 if big else .15)*math.sin(phi+1.1))
            co[:, 2] += .012*math.sin(2*phi+.5)
            co = co @ np.array(Matrix.Rotation(math.radians(24), 3, 'X')).T
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

# ---------------- ahtapot ----------------
def build_octo(sp):
    def skin(nt, N, L, bs):
        tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 14; nz.inputs['Detail'].default_value = 6
        L.new(tc.outputs['Object'], nz.inputs['Vector'])
        rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = lin('#8a2412'); rp.color_ramp.elements[1].color = lin('#f07a4a'); L.new(nz.outputs['Fac'], rp.inputs['Fac'])
        vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 30; L.new(tc.outputs['Object'], vo.inputs['Vector'])
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = .35
        L.new(rp.outputs['Color'], mx.inputs[6]); L.new(vo.outputs['Color'], mx.inputs[7]); L.new(mx.outputs[2], bs.inputs['Base Color'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .35; L.new(vo.outputs['Distance'], bp.inputs['Height']); L.new(bp.outputs['Normal'], bs.inputs['Normal'])
        bs.inputs['Roughness'].default_value = .4; bs.inputs['Subsurface Weight'].default_value = .2; bs.inputs['Coat Weight'].default_value = .4
    m = node_mat('oskin', skin)
    arm_m = D.mat_grad('oarm', '#c9452a', '#ffc2a2', rough=.4, trans=0, sss=.2, coat=.4)
    m_eye = F.mat_plain('oeye', (235, 200, 90), rough=.2, coat=1); m_pup = F.mat_plain('opup', (8, 8, 8), rough=.05, coat=1)
    parts = []
    o = D.sphere((0, 0, 0), 1, m, scale=(.2, .17, .23)); co = np.array([v.co[:] for v in o.data.vertices])
    co = co @ np.array(Matrix.Rotation(math.radians(-50), 3, 'Y')).T+np.array([-.14, 0, .17]); o.data.vertices.foreach_set('co', co.ravel()); o.data.update(); o.name = 'mantle'; parts.append(o)
    o = D.sphere((.02, 0, .04), 1, m, scale=(.13, .14, .1)); o.name = 'headb'; parts.append(o)
    for sg in (-1, 1):
        o = D.sphere((.07, sg*.11, .09), .042, m_eye); o.name = f'oe{sg}'; parts.append(o)
        o = D.sphere((.085, sg*.15, .092), 1, m_pup, scale=(.018, .008, .008)); o.name = f'op{sg}'; parts.append(o)
    rnd = random.Random(5)
    for k in range(8):
        a = (k+.5)/8*2*math.pi; d = Vector((math.cos(a), math.sin(a)*.8, 0))
        a_ = D.Acc(); pts = []; L_ = rnd.uniform(.42, .55)
        for q in np.linspace(0, 1, 26):
            curl = q**2.2*2.6; dd = Matrix.Rotation(curl*(1 if k % 2 else -1)*.5, 3, 'Z') @ d
            p = Vector((.03, 0, .0))+dd*L_*q+Vector((0, 0, -.06*math.sin(q*math.pi)-.02*q))+Vector((.12*q, 0, 0))
            pts.append(p)
        a_.tube(pts, [.05*(1-q)**1.1+.005 for q in np.linspace(0, 1, 26)], seg=10)
        o = a_.obj(f'arm{k}', arm_m, sub=1); o['k'] = k; parts.append(o)
    def fn(parts, rest, phi):
        for ob in parts:
            co = rest[ob.name].copy()
            if ob.name.startswith('arm'):
                k = ob['k']; r = np.linalg.norm(co[:, :2]-np.array([.03, 0]), axis=1); t = np.clip(r/.55, 0, 1)
                co[:, 2] += .05*t**1.4*np.sin(phi+k*.8-t*3)
                co[:, 1] += .035*t**1.6*np.cos(phi+k*1.1-t*2.5)
            else:
                s_ = 1+.04*math.sin(phi); c0 = co.mean(0); co = c0+(co-c0)*s_
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

# ---------------- keşiş yengeci ----------------
def build_crab(sp):
    shell_m = D.mat_proc('cshell', '#7a4a2a', '#f2d9a8', scale=9, tex='wave', wave_dir='X', bump=.4, rough=.4, coat=.4)
    body_m = F.mat_plain('cbody', (214, 70, 40), rough=.45, coat=.3); leg_m = D.mat_grad('cleg', '#b8361c', '#ffb07a', rough=.45, trans=0)
    m_eye = F.mat_plain('ceye', (8, 8, 8), rough=.05, coat=1)
    parts = []
    a = D.Acc(); pts = []; rad = []
    for t in np.linspace(0, 1, 60):
        th = t*3.2*2*math.pi; R = .015+.13*t**1.2; z = .36*(1-t)**1.3
        pts.append((-.12+R*math.cos(th)*.9, R*math.sin(th), .1+z*.55+R*.2)); rad.append(.008+.12*t**1.15)
    a.tube(pts, rad, seg=18, cap=False); o = a.obj('shell', shell_m, sub=1); parts.append(o)
    o = D.sphere((.12, 0, .07), 1, body_m, scale=(.1, .09, .07)); o.name = 'cbody'; parts.append(o)
    for sg in (-1, 1):
        a = D.Acc(); a.tube([(.16, sg*.03, .1), (.19, sg*.04, .2)], [.008, .006], seg=6); o = a.obj(f'stalk{sg}', body_m); parts.append(o)
        o = D.sphere((.19, sg*.04, .21), .018, m_eye); o.name = f'ce{sg}'; parts.append(o)
    legs = []
    for i in range(3):
        for sg in (-1, 1):
            x0 = .1-i*.05; a = D.Acc()
            pts = [(x0, sg*.07, .06), (x0+.05-i*.03, sg*.2, .12), (x0+.1-i*.07, sg*.28, -.05)]
            a.tube(F.catmull(pts, 6), [.018-.01*q for q in np.linspace(0, 1, len(F.catmull(pts, 6)))], seg=7)
            o = a.obj(f'leg{i}_{sg}', leg_m); o['piv'] = [x0, sg*.07, .06]; o['ph'] = i*2.1+(0 if sg > 0 else math.pi); parts.append(o); legs.append(o)
    for sg, big in ((1, 1.0), (-1, .65)):
        a = D.Acc(); a.tube([(.16, sg*.06, .06), (.24, sg*.13, .08), (.3, sg*.12, .06)], [.024*big, .022*big, .02*big], seg=8); parts.append(a.obj(f'arm{sg}', body_m))
        o = D.sphere((.36, sg*.12, .07), 1, body_m, scale=(.07*big, .045*big, .04*big)); o.name = f'claw{sg}'; o['cl'] = 1; parts.append(o)
        o = D.sphere((.4, sg*.12, .045), 1, body_m, scale=(.05*big, .025*big, .02*big)); o.name = f'pinc{sg}'; o['pv'] = [.36, sg*.12, .05]; parts.append(o)
    def fn(parts, rest, phi):
        for ob in parts:
            co = rest[ob.name].copy()
            if ob.name.startswith('leg'):
                piv = np.array(ob['piv']); ph = ob['ph']
                co = rot_about(co, piv, 'Z', .22*math.sin(phi+ph))
                lift = max(0, math.sin(phi+ph+1.57))*.04; w = np.clip((co[:, 2]-.06)*-1/.11, 0, 1); co[:, 2] += lift*w
            elif ob.name.startswith('pinc'):
                co = rot_about(co, np.array(ob['pv']), 'Y', -.25*max(0, math.sin(phi*2)))
            if not ob.name.startswith('leg'): co[:, 2] += .006*math.sin(phi*2)
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

# ---------------- deniz salyangozu (nudibranş) ----------------
def build_nudi(sp):
    body_m = D.mat_grad('nbody', '#7a3fd0', '#c9a2ff', rough=.3, trans=.2, sss=.4, coat=.6)
    cer_m = D.mat_grad('ncer', '#ff8a2a', '#ffe0a0', rough=.3, trans=.2, sss=.3, coat=.5, emit=.1)
    rh_m = F.mat_plain('nrh', (255, 120, 60), rough=.3, coat=.4)
    parts = []
    prof = []
    for t in np.linspace(0, 1, 40):
        x = .45-t*.95; r = .09*math.sin(math.pi*min(1, t*1.15))**.6*(1-.6*t) + .004
        prof.append((x, r))
    a = D.Acc(); a.tube([(x, 0, .05) for x, r in prof], [r for x, r in prof], seg=20); o = a.obj('nb', body_m, sub=1)
    co = np.array([v.co[:] for v in o.data.vertices]); co[:, 2] = np.where(co[:, 2] < .03, .03-(.03-co[:, 2])*.35, co[:, 2]); o.data.vertices.foreach_set('co', co.ravel()); o.data.update(); parts.append(o)
    rnd = random.Random(9)
    for i in range(46):
        x = rnd.uniform(-.38, .3); r = .09*(1-.6*(.45-x)/.95)
        a0 = rnd.uniform(-1.2, 1.2); base = Vector((x, math.sin(a0)*r*.8, .05+math.cos(a0)*r*.7))
        d = Vector((rnd.uniform(-.3, .1), math.sin(a0)*.7, 1)).normalized(); L = rnd.uniform(.07, .13)
        a = D.Acc(); a.tube([base, base+d*L*.5, base+d*L], [.016, .012, .004], seg=7); o = a.obj(f'cer{i}', cer_m); o['b'] = list(base); parts.append(o)
    for sg in (-1, 1):
        a = D.Acc(); a.tube([(.4, sg*.03, .1), (.46, sg*.05, .2)], [.012, .005], seg=6); parts.append(a.obj(f'rh{sg}', rh_m))
        a = D.Acc(); a.tube([(.44, sg*.04, .04), (.54, sg*.08, .03)], [.01, .003], seg=6); parts.append(a.obj(f'ot{sg}', rh_m))
    def fn(parts, rest, phi):
        for ob in parts:
            co = rest[ob.name].copy()
            co[:, 1] += .02*np.sin(phi-co[:, 0]*6)
            if ob.name.startswith('cer'):
                b = np.array(ob['b']); h = np.clip((co[:, 2]-b[2])/.12, 0, 1); co[:, 0] += .015*h*math.sin(phi*2+b[0]*9)
            ob.data.vertices.foreach_set('co', co.ravel()); ob.data.update()
    return parts, fn

# ---------------- fener balığı ----------------
def build_angler(sp):
    fsp = dict(id='v_angler', len=80, hb=.5, ped=.12, tail='round', dors=6, anal=6, c1='#3a3f4a', c2='#16181e', c3='#545a66', fin=(40, 44, 52, .85),
               pat='none', wk=.3, amp=.05, eyeK=.034, eye='#d8e070')
    parts, pecs = F.build_fish(fsp)
    lure = F.mat_plain('stalk', (40, 44, 52), rough=.5)
    glow = bpy.data.materials.new('bulb'); glow.use_nodes = True; bs = glow.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = (.5, 1, .8, 1); bs.inputs['Emission Color'].default_value = (.45, 1, .75, 1); bs.inputs['Emission Strength'].default_value = 9
    pts = [Vector((.3, 0, .2)), Vector((.42, 0, .38)), Vector((.6, 0, .4)), Vector((.68, 0, .3))]
    parts.append(F.poly_tube('illi', [tuple(p) for p in F.catmull(pts, 8)], [.012-.007*q for q in np.linspace(0, 1, len(F.catmull(pts, 8)))], lure, seg=6))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=.04, location=(.68, 0, .27)); b = bpy.context.active_object; b.data.materials.append(glow); b.name = 'bulb'; parts.append(b)
    tooth = F.mat_plain('tooth', (240, 236, 220), rough=.2, coat=.6)
    for i in range(9):
        x = .38+i*.014
        for (z, dz) in ((-.035, .05), (.0, -.045)):
            bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=.009, radius2=0, depth=abs(dz), location=(x, (-1)**i*.012, z+dz/2))
            c = bpy.context.active_object
            if dz < 0: c.rotation_euler = (math.pi, 0, 0)
            c.data.materials.append(tooth); c.name = f'tooth{i}{"u" if dz < 0 else "d"}'; parts.append(c)
    return parts, (lambda parts, rest, phi: F.apply_frame(parts, rest, phi, fsp['amp'], pecs))

F.BUILDERS.update(turtle=build_turtle, octo=build_octo, crab=build_crab, nudi=build_nudi, angler=build_angler)
VIS = {'turtle': dict(id='v_turtle', kind='turtle'), 'octo': dict(id='v_octo', kind='octo'), 'crab': dict(id='v_crab', kind='crab'),
       'nudi': dict(id='v_nudi', kind='nudi'), 'angler': dict(id='v_angler', kind='angler')}

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    frames = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    res = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    F.SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    for k in (VIS if which == 'all' else which.split(',')):
        F.render_species(dict(VIS[k]), frames, res)
