"""Godot için üstten görünüşlü, iki yönde kesintisiz kum dokusu (renk + yükseklik).
sand.py'nin tane örnekleme yardımcılarını kullanır. Çıktı: godot/assets/tex/sand_albedo.png, sand_height.png"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F, decor as D, sand as SA

W = 1.6
def wrap2(x, y, *arrs, pad=.03):
    X = [x]; Y = [y]; A = [[a] for a in arrs]
    for dx in (-W, 0, W):
        for dy in (-W, 0, W):
            if dx == 0 and dy == 0: continue
            m = (np.abs(x+dx) < W/2+pad) & (np.abs(y+dy) < W/2+pad)
            X.append(x[m]+dx); Y.append(y[m]+dy)
            for i, a in enumerate(arrs): A[i].append(a[m])
    return [np.concatenate(X), np.concatenate(Y)]+[np.concatenate(a) for a in A]

def build(px=2048, samples=32):
    F.SAMPLES = samples
    sc, cam = F.setup_scene(px); sc.render.threads_mode = 'AUTO'
    cam.location = (0, 0, 10); cam.rotation_euler = (0, 0, 0); cam.data.ortho_scale = W
    sc.render.resolution_x = px; sc.render.resolution_y = px; sc.render.film_transparent = False
    for o in list(sc.objects):
        if o.type == 'LIGHT': bpy.data.objects.remove(o)
    sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 2.4; sd.angle = math.radians(12)
    so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(28), 0, math.radians(30))
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
    bp = F.mk_obj('base', [(-1.5, -1.5, 0), (1.5, -1.5, 0), (1.5, 1.5, 0), (-1.5, 1.5, 0)], [(0, 1, 2, 3)], None,
                  D.mat_proc('sandbase', '#b08e58', '#e2c690', scale=420, bump=.5, detail=3), subsurf=0)
    r = np.random.default_rng(5)
    N1 = int(560000*(W*W)/(4*1.7))*1
    x = r.uniform(-W/2, W/2, N1); y = r.uniform(-W/2, W/2, N1); s = np.clip(r.lognormal(np.log(.0021), .32, N1), .0011, .0042)
    x, y, s = wrap2(x, y, s); n = len(x)
    sz = np.c_[s*r.uniform(.8, 1.2, n), s*r.uniform(.8, 1.2, n), s*r.uniform(.55, .9, n)]
    P = np.c_[x, y, sz[:, 2]*r.uniform(.1, .7, n)]
    fine = SA.point_cloud('fine', P, sz, r.uniform(0, 1, n)); t1 = SA.grain_template('g1', 1); SA.instancer(fine, t1)
    t1.data.materials.append(SA.grain_mat('fine', ['#f6e4bd', '#e8cc96', '#d6b077', '#c29a60', '#fbf0d8', '#a7845a', '#e2c4a2', '#efd2ae', '#5f5a55', '#d4b896'],
                                          np.array([12, 12, 9, 6, 6, 3, 4, 4, .8, 3])))
    N2 = int(5200*(W*W)/(4*1.7))
    x = r.uniform(-W/2, W/2, N2); y = r.uniform(-W/2, W/2, N2)
    s = np.where(r.uniform(0, 1, N2) < .12, r.uniform(.007, .013, N2), r.uniform(.0038, .0065, N2))
    x, y, s = wrap2(x, y, s, pad=.05); n = len(x)
    sz = np.c_[s*r.uniform(.85, 1.3, n), s*r.uniform(.8, 1.2, n), s*r.uniform(.45, .75, n)]
    coarse = SA.point_cloud('coarse', np.c_[x, y, sz[:, 2]*.35], sz, r.uniform(0, 1, n)); t2 = SA.grain_template('g2', 2); SA.instancer(coarse, t2)
    t2.data.materials.append(SA.grain_mat('coarse', ['#e8dcc4', '#b8a383', '#8d7d68', '#d9c6a6', '#6d6660', '#f2ece0', '#a59a8c', '#c7a27e'],
                                          np.array([8, 7, 4, 7, 2, 4, 4, 3]), rough=.45, coat=.35))
    out = os.path.join(F.ROOT, 'godot', 'assets', 'tex'); os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(F.ROOT, 'build', 'hires', 'sand_top.png'); bpy.ops.render.render(write_still=True)
    Image.open(sc.render.filepath).convert('RGB').save(os.path.join(out, 'sand_albedo.webp'), 'WEBP', quality=86)
    print('sand_top ok', flush=True)

if __name__ == '__main__':
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 2048, int(sys.argv[2]) if len(sys.argv) > 2 else 32)
