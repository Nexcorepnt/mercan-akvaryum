extends Camera3D
## Akvaryum kamerası: parmakla/fareyle döndür, iki parmakla/tekerlekle yakınlaş. Boşta kendiliğinden hafifçe süzülür.

var center := Vector3(0, 1.9, 0)
var yaw := 0.0
var pitch := 0.08
var dist := 9.6
var idle_t := 10.0
var touches := {}
var last_pinch := 0.0

func _ready() -> void:
	_apply()

func _unhandled_input(e: InputEvent) -> void:
	if e is InputEventScreenTouch:
		if e.pressed: touches[e.index] = e.position
		else: touches.erase(e.index)
		last_pinch = 0.0
	elif e is InputEventScreenDrag:
		touches[e.index] = e.position
		if touches.size() >= 2:
			var k := touches.keys()
			var d: float = (touches[k[0]] - touches[k[1]]).length()
			if last_pinch > 0.0: dist = clampf(dist * last_pinch / d, 5.0, 13.0)
			last_pinch = d
		else:
			_rotate(e.relative)
	elif e is InputEventMouseMotion and (e.button_mask & MOUSE_BUTTON_MASK_LEFT):
		_rotate(e.relative)
	elif e is InputEventMouseButton and e.pressed:
		if e.button_index == MOUSE_BUTTON_WHEEL_UP: dist = maxf(5.0, dist * 0.92); idle_t = 0.0
		elif e.button_index == MOUSE_BUTTON_WHEEL_DOWN: dist = minf(13.0, dist * 1.08); idle_t = 0.0

func _rotate(r: Vector2) -> void:
	yaw = clampf(yaw - r.x * 0.004, -0.75, 0.75)
	pitch = clampf(pitch + r.y * 0.003, -0.12, 0.45)
	idle_t = 0.0

func _process(dt: float) -> void:
	idle_t += dt
	if idle_t > 4.0:
		# boşta: yavaş, nefes alır gibi bir süzülme (3D derinliği hissettirir)
		var t := Time.get_ticks_msec() / 1000.0
		yaw = lerpf(yaw, sin(t * 0.13) * 0.42, dt * 0.4)
		pitch = lerpf(pitch, 0.1 + sin(t * 0.09) * 0.06, dt * 0.4)
	_apply()

func _apply() -> void:
	var off := Vector3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch)) * dist
	position = center + off
	look_at(center, Vector3.UP)
