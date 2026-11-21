"""Mercan Akvaryum 3D logo + mağaza görselleri için yüksek çözünürlüklü balık renderları.
Kullanım: python logo.py [samples]
Çıktı: build/hires/logo.png, build/hires/<tür>_00.png
"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F

HI = os.path.join(F.ROOT, 'build', 'hires'); os.makedirs(HI, exist_ok=True)
FONT = os.path.join(F.ROOT, 'build', 'fredoka-bold.ttf')

def lin(h):
    r, g, b = F.hx(h); return ((r/255)**2.2, (g/255)**2.2, (b/255)**2.2, 1)

def mat(name, h, rough=.25, coat=1., emit=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = lin(h); bs.inputs['Roughness'].default_value = rough
    bs.inputs['Coat Weight'].default_value = coat; bs.inputs['Coat Roughness'].default_value = .05
    if emit: bs.inputs['Emission Color'].default_value = lin(h); bs.inputs['Emission Strength'].default_value = emit
    return m

def text(body, size, loc, m, font, extrude=.06, bevel=.022, offset=0., rot=0.):
    cu = bpy.data.curves.new(body, 'FONT'); cu.body = body; cu.font = font; cu.size = size
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.extrude = extrude; cu.bevel_depth = bevel; cu.bevel_resolution = 4; cu.offset = offset
    ob = bpy.data.objects.new(body, cu); bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = (math.pi/2, 0, 0); ob.rotation_euler.y = rot
    ob.data.materials.append(m); return ob

def logo(samples):
    F.SAMPLES = samples
    sc, cam = F.setup_scene(1400)
    az, el = math.radians(0), math.radians(6)
    dv = Vector((math.sin(az)*math.cos(el), -math.cos(az)*math.cos(el), math.sin(el)))
    cam.location = dv*10; cam.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler()
    font = bpy.data.fonts.load(FONT)
    coral = mat('coral', '#ff3f73'); cyan = mat('cyan', '#5ee6e0'); navy = mat('navy', '#071a33', rough=.6, coat=.1)
    gold = mat('gold', '#ffc94a', rough=.2)
    # çizgiler: koyu dış hat (arkada) + renkli üst
    text('Mercan', 1.0, (0, -.04, .42), coral, font)
    text('Akvaryum', .62, (0, -.04, -.33), cyan, font)
    # kabarcıklar
    m_b = bpy.data.materials.new('bub'); m_b.use_nodes = True; bs = m_b.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = (.85, .97, 1, 1); bs.inputs['Transmission Weight'].default_value = 1; bs.inputs['Roughness'].default_value = .02
    bs.inputs['Alpha'].default_value = .55; bs.inputs['Coat Weight'].default_value = 1
    for (x, z, r) in [(1.72, .95, .09), (1.9, .7, .055), (1.62, .62, .04), (-1.75, -.55, .06), (-1.92, -.32, .04)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=(x, -.1, z))
        o = bpy.context.active_object; o.data.materials.append(m_b)
        for p in o.data.polygons: p.use_smooth = True
    # yıldız parıltısı
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for o in sc.objects:
        if o.type not in ('MESH', 'FONT'): continue
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        a = np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co', a)
        pts.append((np.array(o.matrix_world) @ np.c_[a.reshape(-1, 3), np.ones(len(me.vertices))].T).T[:, :3]); ev.to_mesh_clear()
    F.fit_pts(sc, cam, np.concatenate(pts), res_max=1400, pad=.04)
    sc.render.filepath = os.path.join(HI, 'logo.png'); bpy.ops.render.render(write_still=True)
    print('logo ok', sc.render.resolution_x, sc.render.resolution_y)

def hires_fish(tags, res, samples):
    F.SAMPLES = samples; F.OUT = HI; F.SPR = HI
    for t in tags:
        F.render_species(F.get_species(t), 1, res)

if __name__ == '__main__':
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    logo(s)
    hires_fish(['clown', 'koi', 'tang', 'angel', 'jelly', 'gold_r', 'betta', 'seahorse'], 900, s)
