shader_type spatial;
render_mode unshaded, cull_disabled, blend_add, depth_draw_never, fog_disabled;
#include "res://shaders/common.gdshaderinc"
// Su yüzeyi: alttan bakınca parıldayan dalgalar
varying vec3 wpos;
void vertex() { wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	float c = caust(wpos.xz * 0.12, TIME * 0.4);
	ALBEDO = vec3(0.45, 0.75, 0.85) * (0.08 + c * 0.32);
}
