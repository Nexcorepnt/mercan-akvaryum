extends Node3D
## Mercan Akvaryum 3D - deneme sahnesi: kum, süsler, balıklar, kabarcıklar, su ışığı.

const FISH_SH := preload("res://shaders/fish.gdshader")
const FIN_SH := preload("res://shaders/fish_fin.gdshader")
const DECOR_SH := preload("res://shaders/decor.gdshader")
const SAND_SH := preload("res://shaders/sand.gdshader")
const FishScript := preload("res://scripts/fish.gd")

# tür: [model, uzunluk (birim), hız, yükseklik tercihi]
const SPECIES := {
	"koi": ["koi", 1.05, 0.75, Vector2(1.2, 3.8)],
	"clown": ["clown", 0.6, 0.85, Vector2(0.6, 2.2)],
	"tang": ["tang", 0.75, 1.0, Vector2(1.0, 3.6)],
	"neon": ["neon", 0.42, 1.25, Vector2(1.5, 4.0)],
	"angel": ["angel", 0.62, 0.6, Vector2(1.6, 3.8)],
	"gold": ["gold", 0.64, 0.7, Vector2(1.0, 3.5)],
	"betta": ["betta", 0.55, 0.55, Vector2(2.0, 4.0)],
	"discus": ["discus", 0.68, 0.55, Vector2(1.2, 3.2)],
}
# süs: [model, x, z, dönüş (derece), ölçek, dalgalanma, boy]
const DECOR := [
	["kelp", -5.4, -1.6, 10.0, 1.05, 0.10, 2.6],
	["weed", -4.6, -0.9, 0.0, 1.0, 0.09, 1.7],
	["rock", -3.4, -1.4, 25.0, 1.25, 0.0, 1.0],
	["anem", -2.2, -0.2, 0.0, 1.0, 0.03, 0.4],
	["castle", -0.4, -1.9, -10.0, 1.15, 0.0, 1.0],
	["coral", 1.6, -1.0, 30.0, 1.1, 0.0, 1.0],
	["fan", 2.7, -2.1, -15.0, 1.2, 0.04, 1.2],
	["brain", 3.0, 0.2, 0.0, 1.0, 0.0, 1.0],
	["crystal", 4.2, -0.8, 20.0, 1.0, 0.0, 1.0],
	["chest", 0.9, 0.7, -25.0, 0.95, 0.0, 1.0],
	["shell", -1.0, 1.0, 40.0, 0.9, 0.0, 1.0],
	["redweed", 5.3, -1.3, 0.0, 1.0, 0.08, 1.0],
	["kelp", 5.9, -2.2, 60.0, 0.9, 0.10, 2.3],
	["weed", -2.8, -2.3, 30.0, 0.9, 0.09, 1.6],
]
const SCHOOL := [["neon", 6], ["clown", 2], ["koi", 2], ["tang", 2], ["angel", 1], ["gold", 2], ["betta", 1], ["discus", 1]]

var anem_pos := Vector3.INF

func _ready() -> void:
	randomize()
	_environment()
	_tank()
	for d in DECOR: _add_decor(d)
	for s in SCHOOL:
		for i in s[1]: _add_fish(s[0])
	_bubbles(Vector3(-0.4, 1.6, -1.9))
	_bubbles(Vector3(4.6, 0.2, -1.2))
	var cam := Camera3D.new()
	cam.set_script(preload("res://scripts/cam.gd"))
	cam.fov = 42.0
	add_child(cam)
	cam.current = true
	_ui()

func _environment() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.03, 0.16, 0.26)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.45, 0.6, 0.68)
	env.ambient_light_energy = 0.62
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.tonemap_exposure = 0.92
	env.fog_enabled = true
	env.fog_light_color = Color(0.07, 0.33, 0.47)
	env.fog_density = 0.02
	env.glow_enabled = true
	env.glow_intensity = 0.45
	env.glow_bloom = 0.08
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-62, 25, 0)
	sun.light_color = Color(0.85, 0.96, 1.0)
	sun.light_energy = 1.15
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 30.0
	add_child(sun)
	var fill := OmniLight3D.new()
	fill.position = Vector3(0, 3.5, 4.5); fill.omni_range = 14.0
	fill.light_color = Color(0.7, 0.85, 0.95); fill.light_energy = 0.45
	add_child(fill)

func _tank() -> void:
	# kum zemini
	var sand := MeshInstance3D.new()
	var pm := PlaneMesh.new(); pm.size = Vector2(18, 9); pm.subdivide_width = 160; pm.subdivide_depth = 80
	sand.mesh = pm
	var sm := ShaderMaterial.new(); sm.shader = SAND_SH
	sm.set_shader_parameter("sand_tex", load("res://assets/tex/sand_albedo.webp"))
	sand.material_override = sm
	add_child(sand)
	# arka plan
	var bd := MeshInstance3D.new(); var q := QuadMesh.new(); q.size = Vector2(34, 14); bd.mesh = q
	var bm := ShaderMaterial.new(); bm.shader = load("res://shaders/backdrop.gdshader"); bd.material_override = bm
	bd.position = Vector3(0, 5.5, -4.6); add_child(bd)
	# su yüzeyi
	var sf := MeshInstance3D.new(); var sp := PlaneMesh.new(); sp.size = Vector2(22, 10); sf.mesh = sp
	var sfm := ShaderMaterial.new(); sfm.shader = load("res://shaders/surface.gdshader"); sf.material_override = sfm
	sf.position = Vector3(0, 5.3, 0); add_child(sf)
	# ışık huzmeleri
	for i in 6:
		var r := MeshInstance3D.new(); var rq := QuadMesh.new(); rq.size = Vector2(randf_range(0.8, 1.6), 6.5); r.mesh = rq
		var rm := ShaderMaterial.new(); rm.shader = load("res://shaders/ray.gdshader")
		rm.set_shader_parameter("phase", randf() * TAU); rm.set_shader_parameter("strength", randf_range(0.12, 0.24))
		r.material_override = rm
		r.position = Vector3(-6.0 + i * 2.4 + randf_range(-0.5, 0.5), 2.0, randf_range(-2.5, 0.5))
		r.rotation_degrees = Vector3(0, 0, randf_range(-14, -6))
		add_child(r)

func _restyle(root: Node, fish: bool, extra := {}) -> Array[ShaderMaterial]:
	var out: Array[ShaderMaterial] = []
	for mi in root.find_children("*", "MeshInstance3D", true, false):
		var m: MeshInstance3D = mi
		for i in m.mesh.get_surface_count():
			var src := m.mesh.surface_get_material(i) as BaseMaterial3D
			var sm := ShaderMaterial.new()
			var transparent := src != null and src.transparency != BaseMaterial3D.TRANSPARENCY_DISABLED
			sm.shader = (FIN_SH if transparent else FISH_SH) if fish else DECOR_SH
			if src:
				sm.set_shader_parameter("albedo_col", src.albedo_color)
				sm.set_shader_parameter("has_tex", src.albedo_texture != null)
				if src.albedo_texture: sm.set_shader_parameter("albedo_tex", src.albedo_texture)
				sm.set_shader_parameter("roughness", src.roughness)
				if fish: sm.set_shader_parameter("metallic", src.metallic)
			for k in extra: sm.set_shader_parameter(k, extra[k])
			m.set_surface_override_material(i, sm)
			m.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
			out.append(sm)
	return out

func _add_decor(d: Array) -> void:
	var path := "res://assets/models/d_%s.glb" % d[0]
	if not ResourceLoader.exists(path): return
	var inst: Node3D = load(path).instantiate()
	inst.position = Vector3(d[1], 0.0, d[2])
	inst.rotation_degrees.y = d[3]
	inst.scale = Vector3.ONE * d[4]
	add_child(inst)
	var extra := {"phase": randf() * TAU}
	if d[5] > 0.0:
		extra["sway"] = d[5]; extra["height"] = d[6]
	if d[0] == "crystal": extra["glow"] = Vector3(0.05, 0.12, 0.2)
	_restyle(inst, false, extra)
	if d[0] == "anem": anem_pos = inst.position + Vector3(0, 0.35, 0)

func _add_fish(kind: String) -> void:
	var info: Array = SPECIES[kind]
	var path := "res://assets/models/%s.glb" % info[0]
	if not ResourceLoader.exists(path): return
	var f := Node3D.new(); f.set_script(FishScript)
	var model: Node3D = load(path).instantiate()
	model.scale = Vector3.ONE * info[1]
	f.add_child(model)
	f.species = kind
	f.speed = info[2] * randf_range(0.85, 1.15)
	f.depth_pref = info[3]
	f.body_len = info[1]
	if kind == "clown" and anem_pos != Vector3.INF: f.home = anem_pos
	f.position = Vector3(randf_range(-5, 5), randf_range(info[3].x, info[3].y), randf_range(-1.5, 1.5))
	add_child(f)
	f.mats = _restyle(model, true, {"wave_amp": 0.06})

func _bubbles(at: Vector3) -> void:
	var p := CPUParticles3D.new()
	p.position = at
	p.amount = 26; p.lifetime = 4.5
	var s := SphereMesh.new(); s.radius = 0.035; s.height = 0.07; s.radial_segments = 10; s.rings = 6
	var m := StandardMaterial3D.new()
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.albedo_color = Color(0.85, 0.95, 1.0, 0.35)
	m.roughness = 0.05; m.metallic_specular = 1.0
	m.rim_enabled = true; m.rim = 1.0
	m.emission_enabled = true; m.emission = Color(0.3, 0.5, 0.6)
	s.material = m
	p.mesh = s
	p.direction = Vector3.UP; p.spread = 12.0
	p.initial_velocity_min = 0.4; p.initial_velocity_max = 0.8
	p.gravity = Vector3(0, 0.35, 0)
	p.scale_amount_min = 0.5; p.scale_amount_max = 1.6
	p.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE; p.emission_sphere_radius = 0.08
	add_child(p)

func _ui() -> void:
	var cl := CanvasLayer.new(); add_child(cl)
	var lb := Label.new()
	lb.text = "Mercan Akvaryum 3D · Godot denemesi"
	lb.position = Vector2(24, 18)
	lb.add_theme_font_size_override("font_size", 22)
	lb.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
	lb.add_theme_color_override("font_shadow_color", Color(0, 0.1, 0.2, 0.7))
	cl.add_child(lb)
	var hint := Label.new()
	hint.text = "Sürükle: döndür · İki parmak / tekerlek: yakınlaş"
	hint.position = Vector2(24, 50)
	hint.add_theme_font_size_override("font_size", 15)
	hint.add_theme_color_override("font_color", Color(0.85, 0.95, 1, 0.7))
	cl.add_child(hint)
