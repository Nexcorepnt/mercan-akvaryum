"""Mercan Akvaryum -> Godot: Blender modellerini .glb olarak dışa aktarır.
Balıklar: resim dokulu malzemeler doğrudan aktarılır (yüzme dalgası Godot'da shader ile).
Süsler: kodla üretilen malzemeler tek bir dokuya pişirilir (Cycles bake), sonra aktarılır.
Kullanım: python export_godot.py fish koi,clown,...   |   python export_godot.py decor rock,coral,...
Çıktı: godot/assets/models/<ad>.glb
"""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fish as F
import decor as D

F.SAMPLES = 16
OUTDIR = os.path.join(F.ROOT, 'godot', 'assets', 'models'); os.makedirs(OUTDIR, exist_ok=True)
BAKEDIR = os.path.join(F.ROOT, 'build', 'bake'); os.makedirs(BAKEDIR, exist_ok=True)

def meshes(): return [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.hide_render]

def apply_all(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.convert(target='MESH')

def export(name, objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    path = os.path.join(OUTDIR, name+'.glb')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True,
                              export_yup=True, export_image_format='WEBP', export_image_quality=88, export_animations=False)
    print('[glb]', name, os.path.getsize(path)//1024, 'KB', flush=True)

def has_image_base(m):
    if not m or not m.use_nodes: return False
    bs = m.node_tree.nodes.get('Principled BSDF')
    if not bs: return True   # özel shader (ör. emisyon): dokuya pişirilsin
    l = bs.inputs['Base Color'].links
    return (not l) or l[0].from_node.type == 'TEX_IMAGE'

def bake_object(o, size=1024):
    """Objenin bütün malzemelerini tek bir renk dokusuna pişirir ve basit malzemeyle değiştirir."""
    mats = [s.material for s in o.material_slots]
    if all(has_image_base(m) for m in mats if m): return
    me = o.data
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    if not me.uv_layers or o.get('reuv', True):
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=.006)
        bpy.ops.object.mode_set(mode='OBJECT')
    img = bpy.data.images.new(f'bake_{o.name}', size, size, alpha=False)
    rough = []
    for i, s in enumerate(o.material_slots):
        m = s.material.copy() if s.material else bpy.data.materials.new('x'); s.material = m; m.use_nodes = True
        bs = m.node_tree.nodes.get('Principled BSDF')
        rough.append(bs.inputs['Roughness'].default_value if bs else .5)
        n = m.node_tree.nodes.new('ShaderNodeTexImage'); n.image = img
        for x in m.node_tree.nodes: x.select = False
        n.select = True; m.node_tree.nodes.active = n
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 16
    sc.render.bake.use_pass_direct = False; sc.render.bake.use_pass_indirect = False; sc.render.bake.use_pass_color = True
    sc.render.bake.margin = 6
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
    p = os.path.join(BAKEDIR, f'{o.name}.png'); img.filepath_raw = p; img.file_format = 'PNG'; img.save()
    nm = bpy.data.materials.new(f'b_{o.name}'); nm.use_nodes = True; bs = nm.node_tree.nodes['Principled BSDF']
    t = nm.node_tree.nodes.new('ShaderNodeTexImage'); t.image = img; nm.node_tree.links.new(t.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = sum(rough)/max(1, len(rough))
    me.materials.clear(); me.materials.append(nm)

def fish_export(tag):
    F.setup_scene(256)
    sp = F.get_species(tag)
    kind = sp.get('kind', 'fish')
    if kind == 'fish':
        parts, pecs = F.build_fish(sp)
    else:
        parts, fn = F.BUILDERS[kind](sp)
    bpy.context.view_layer.update()
    objs = [o for o in meshes()]
    apply_all(objs)
    objs = meshes()
    for o in objs:
        # emisyon/plain malzemeler aynen kalır; prosedürel olanlar pişirilir
        if any(s.material and not has_image_base(s.material) for s in o.material_slots): bake_object(o, 512)
    export(tag, objs)

def decor_export(tag):
    F.setup_scene(256)
    fn, nfr = D.DECOR[tag]
    fn(0) if nfr > 1 else fn()
    bpy.context.view_layer.update()
    objs = meshes()
    for o in list(objs):
        if o.name.lower().startswith(('shadow', 'catch', 'plane')): bpy.data.objects.remove(o)
    objs = meshes(); apply_all(objs); objs = meshes()
    # çok parçalı süsleri tek objede birleştir (pişirme ve çizim için daha verimli)
    if len(objs) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); objs = meshes()
    for o in objs: o.name = tag; bake_object(o, 1024)
    export('d_'+tag, objs)

if __name__ == '__main__':
    what = sys.argv[1]; tags = sys.argv[2].split(',')
    for t in tags:
        (fish_export if what == 'fish' else decor_export)(t)
