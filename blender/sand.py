"""İnce taneli, yatayda kesintisiz döşenebilen kum şeridi (v8).
Yaklaşık yarım milyon minik kum tanesi geometri düğümleriyle örneklenir (instance),
araya seyrek iri çakıl ve kabuk kırıntıları serpilir.
Kullanım: python sand.py [samples] [genislik_px]
Çıktı: assets/ui/sand.webp
"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F, decor as D

W, DEP = 4.0, 1.7
EL = math.radians(24)
K1, K2 = 2*math.pi*9/W, 2*math.pi*3/W
def h(x, y): return .016*np.sin(x*K1+np.sin(y*5)*1.5)+.007*np.sin(y*13+x*K2)+.003*np.sin(x*K1*2+y*7)

def grain_template(name, sub):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1); o = bpy.context.active_object; o.name = name
    for p in o.data.polygons: p.use_smooth = sub > 1
    o.hide_render = True; o.location = (0, 0, -50)
    return o

def point_cloud(name, P, sz, rid):
    me = bpy.data.meshes.new(name); me.vertices.add(len(P)); me.vertices.foreach_set('co', P.ravel())
    a = me.attributes.new('sz', 'FLOAT_VECTOR', 'POINT'); a.data.foreach_set('vector', sz.ravel())
    b = me.attributes.new('rid', 'FLOAT', 'POINT'); b.data.foreach_set('value', rid)
    me.update(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob

def instancer(ob, tmpl):
    ng = bpy.data.node_groups.new('inst_'+ob.name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes; L = ng.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    iop = N.new('GeometryNodeInstanceOnPoints')
    oi = N.new('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = tmpl
    na = N.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT_VECTOR'; na.inputs['Name'].default_value = 'sz'
    rv = N.new('FunctionNodeRandomValue'); rv.data_type = 'FLOAT_VECTOR'
    rv.inputs['Max'].default_value = (6.3, 6.3, 6.3)
    L.new(gi.outputs[0], iop.inputs['Points']); L.new(oi.outputs['Geometry'], iop.inputs['Instance'])
    L.new(na.outputs['Attribute'], iop.inputs['Scale'])
    try:
        e2r = N.new('FunctionNodeEulerToRotation'); L.new(rv.outputs['Value'], e2r.inputs[0]); L.new(e2r.outputs[0], iop.inputs['Rotation'])
    except Exception:
        L.new(rv.outputs['Value'], iop.inputs['Rotation'])
    # rengi taneden taneye taşı
    sa = N.new('GeometryNodeStoreNamedAttribute'); sa.data_type = 'FLOAT'; sa.domain = 'INSTANCE'; sa.inputs['Name'].default_value = 'rid'
    nr = N.new('GeometryNodeInputNamedAttribute'); nr.data_type = 'FLOAT'; nr.inputs['Name'].default_value = 'rid'
    L.new(iop.outputs['Instances'], sa.inputs['Geometry']); L.new(nr.outputs['Attribute'], sa.inputs['Value'])
    L.new(sa.outputs['Geometry'], go.inputs[0])
    md = ob.modifiers.new('inst', 'NODES'); md.node_group = ng

def grain_mat(name, pal, wts, rough=.6, coat=.15):
    """rid (0-1) -> paletten renk + parlaklık oynaması"""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; bs = N['Principled BSDF']
    at = N.new('ShaderNodeAttribute'); at.attribute_type = 'INSTANCER'; at.attribute_name = 'rid'
    cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'
    cum = np.cumsum(wts)/np.sum(wts); els = cr.color_ramp.elements
    while len(els) < len(pal): els.new(0)
    for i, (c, p0) in enumerate(zip(pal, np.r_[0, cum[:-1]])):
        els[i].position = float(p0); els[i].color = (*[(int(c[k:k+2], 16)/255)**2.2 for k in (1, 3, 5)], 1)
    # aynı renkteki tanelere hafif parlaklık farkı
    mth = N.new('ShaderNodeMath'); mth.operation = 'FRACT'; mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 37.0
    L.new(at.outputs['Fac'], mul.inputs[0]); L.new(mul.outputs[0], mth.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = .78; mr.inputs['To Max'].default_value = 1.15; L.new(mth.outputs[0], mr.inputs['Value'])
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = 1
    cmb = N.new('ShaderNodeCombineColor'); [L.new(mr.outputs[0], cmb.inputs[k]) for k in range(3)]
    L.new(at.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], mix.inputs[6]); L.new(cmb.outputs[0], mix.inputs[7])
    L.new(mix.outputs[2], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = rough; bs.inputs['Coat Weight'].default_value = coat
    return m

def wrap(r, x, y, *arrs, pad=.03):
    m1 = x < -W/2+pad; m2 = x > W/2-pad
    out = [np.r_[x, x[m1]+W, x[m2]-W], np.r_[y, y[m1], y[m2]]]
    for a in arrs: out.append(np.r_[a, a[m1], a[m2]])
    return out

def build(samples, px):
    F.SAMPLES = samples
    sc, cam = F.setup_scene(px)
    sc.render.threads_mode = 'AUTO'
    dv = Vector((0, -math.cos(EL), math.sin(EL))); cam.location = dv*10; cam.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler()
    for o in list(sc.objects):
        if o.type == 'LIGHT': bpy.data.objects.remove(o)
    sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.0; sd.angle = math.radians(6); sd.color = (1, .97, .9)
    so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(18))
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .75
    sc.view_settings.exposure = -.05
    # taban: ince tane dokulu yüzey
    nx, ny = 400, 150; xs = np.linspace(-W/2-.3, W/2+.3, nx); ys = np.linspace(-DEP/2-.3, DEP/2+.3, ny)
    X, Y = np.meshgrid(xs, ys); Z = h(X, Y)
    verts = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    faces = [(j*nx+i, j*nx+i+1, (j+1)*nx+i+1, (j+1)*nx+i) for j in range(ny-1) for i in range(nx-1)]
    base = F.mk_obj('base', [tuple(v) for v in verts], faces, None, D.mat_proc('sandbase', '#b08e58', '#e2c690', scale=420, bump=.5, detail=3), subsurf=0)
    D.smooth(base)
    r = np.random.default_rng(11)
    # 1) ince taneler
    N1 = 560000
    x = r.uniform(-W/2, W/2, N1); y = r.uniform(-DEP/2, DEP/2, N1)
    s = np.clip(r.lognormal(np.log(.0021), .32, N1), .0011, .0042)
    x, y, s = wrap(r, x, y, s)
    n = len(x); sz = np.c_[s*r.uniform(.8, 1.2, n), s*r.uniform(.8, 1.2, n), s*r.uniform(.55, .9, n)]
    P = np.c_[x, y, h(x, y)+sz[:, 2]*r.uniform(.1, .7, n)]
    fine = point_cloud('fine', P, sz, r.uniform(0, 1, n))
    t1 = grain_template('g1', 1); instancer(fine, t1)
    t1.data.materials.append(grain_mat('fine', ['#f6e4bd', '#e8cc96', '#d6b077', '#c29a60', '#fbf0d8', '#a7845a', '#e2c4a2', '#efd2ae', '#5f5a55', '#d4b896'],
                                         np.array([12, 12, 9, 6, 6, 3, 4, 4, .8, 3])))
    # 2) iri kum + seyrek çakıl
    N2 = 5200
    x = r.uniform(-W/2, W/2, N2); y = r.uniform(-DEP/2, DEP/2, N2)
    s = np.where(r.uniform(0, 1, N2) < .12, r.uniform(.007, .013, N2), r.uniform(.0038, .0065, N2))
    x, y, s = wrap(r, x, y, s, pad=.05)
    n = len(x); sz = np.c_[s*r.uniform(.85, 1.3, n), s*r.uniform(.8, 1.2, n), s*r.uniform(.45, .75, n)]
    P = np.c_[x, y, h(x, y)+sz[:, 2]*.35]
    coarse = point_cloud('coarse', P, sz, r.uniform(0, 1, n))
    t2 = grain_template('g2', 2); instancer(coarse, t2)
    t2.data.materials.append(grain_mat('coarse', ['#e8dcc4', '#b8a383', '#8d7d68', '#d9c6a6', '#6d6660', '#f2ece0', '#a59a8c', '#c7a27e'],
                                           np.array([8, 7, 4, 7, 2, 4, 4, 3]), rough=.45, coat=.35))
    # 3) kabuk kırıntıları (yassı, açık renk)
    N3 = 420
    x = r.uniform(-W/2, W/2, N3); y = r.uniform(-DEP/2, DEP/2, N3); s = r.uniform(.004, .009, N3)
    x, y, s = wrap(r, x, y, s, pad=.05)
    n = len(x); sz = np.c_[s*r.uniform(1, 1.6, n), s*r.uniform(.7, 1.1, n), s*.22]
    P = np.c_[x, y, h(x, y)+sz[:, 2]]
    shell = point_cloud('shell', P, sz, r.uniform(0, 1, n))
    t3 = grain_template('g3', 2); instancer(shell, t3)
    t3.data.materials.append(grain_mat('shell', ['#fff6ea', '#f6d9cf', '#efe6f2', '#f3e2bf'], np.array([5, 3, 2, 3]), rough=.25, coat=.8))
    # kadraj
    hgt = DEP*.86*math.sin(EL)+.02
    sc.render.resolution_x = px; sc.render.resolution_y = int(round(px*hgt/W)); sc.render.resolution_percentage = 100
    cam.data.ortho_scale = W; cam.data.shift_x = 0; cam.data.shift_y = 0
    sc.render.film_transparent = False
    out = os.path.join(F.ROOT, 'build', 'hires', 'sand.png'); sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    im = Image.open(out).convert('RGB'); os.makedirs(os.path.join(F.ROOT, 'assets', 'ui'), exist_ok=True)
    im.save(os.path.join(F.ROOT, 'assets', 'ui', 'sand.webp'), 'WEBP', quality=82, method=6)
    print('sand ok', im.size, N1, N2, N3, flush=True)

if __name__ == '__main__':
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 48, int(sys.argv[2]) if len(sys.argv) > 2 else 3072)
