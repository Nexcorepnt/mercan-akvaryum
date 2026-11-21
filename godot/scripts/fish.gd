extends Node3D
## Bir balığın davranışı: akvaryum içinde gezinir, hedefe yumuşakça döner, hıza göre kuyruk sallar.

const BOUNDS_MIN := Vector3(-5.8, 0.7, -1.9)
const BOUNDS_MAX := Vector3(5.8, 4.2, 1.7)

var species := ""
var speed := 0.8          # birim/sn (gezinme hızı)
var body_len := 1.0
var vel := Vector3.ZERO
var target := Vector3.ZERO
var idle := 0.0
var wave_t := 0.0
var depth_pref := Vector2(0.7, 4.2)   # tercih edilen yükseklik aralığı
var home := Vector3.INF              # yuva (ör. palyaço için anemon)
var mats: Array[ShaderMaterial] = []

func _ready() -> void:
	wave_t = randf() * TAU
	_pick()

func _pick() -> void:
	if home != Vector3.INF and randf() < 0.6:
		target = home + Vector3(randf_range(-0.5, 0.5), randf_range(0.0, 0.4), randf_range(-0.4, 0.4))
	else:
		target = Vector3(randf_range(BOUNDS_MIN.x, BOUNDS_MAX.x), randf_range(depth_pref.x, depth_pref.y), randf_range(BOUNDS_MIN.z, BOUNDS_MAX.z))

func _process(dt: float) -> void:
	var to := target - position
	if to.length() < 0.35:
		idle = randf_range(0.6, 2.5) if randf() < 0.35 else 0.0
		_pick()
	var mult := 0.18 if idle > 0.0 else 1.0
	idle -= dt
	var want := to.normalized() * speed * mult
	vel = vel.lerp(want, clampf(dt * 1.1, 0.0, 1.0))
	position += vel * dt
	position = position.clamp(BOUNDS_MIN, BOUNDS_MAX)
	# yön: yerel +x hareket yönüne baksın, dikey eğim sınırlı
	if vel.length() > 0.04:
		var fwd := vel.normalized()
		fwd.y = clampf(fwd.y, -0.45, 0.45)
		fwd = fwd.normalized()
		var z := fwd.cross(Vector3.UP).normalized()
		var y := z.cross(fwd).normalized()
		var q := Quaternion(Basis(fwd, y, z).orthonormalized())
		quaternion = quaternion.slerp(q, clampf(dt * 2.5, 0.0, 1.0))
	# kuyruk dalgası hıza bağlı
	var s := vel.length() / maxf(speed, 0.01)
	wave_t += dt * (2.5 + s * 7.0)
	for m in mats:
		m.set_shader_parameter("wave_t", wave_t)
