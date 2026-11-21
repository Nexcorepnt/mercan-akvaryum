shader_type spatial;
render_mode cull_disabled;
#include "res://shaders/common.gdshaderinc"
uniform sampler2D albedo_tex : source_color, filter_linear_mipmap;
uniform vec4 albedo_col : source_color = vec4(1.0);
uniform bool has_tex = true;
uniform float roughness = 0.6;
uniform float sway = 0.0;      // bitkiler için dalgalanma genliği
uniform float height = 1.5;
uniform float phase = 0.0;
uniform float caustic_k = 0.7;
uniform vec3 glow = vec3(0.0);
varying vec3 wpos;
varying vec3 wnrm;

void vertex() {
	if (sway > 0.0) {
		float h = clamp(VERTEX.y / height, 0.0, 1.0);
		float hh = h * h;
		VERTEX.x += sin(TIME * 1.25 + VERTEX.y * 1.6 + phase) * sway * hh;
		VERTEX.z += cos(TIME * 1.05 + VERTEX.y * 1.2 + phase * 1.3) * sway * 0.6 * hh;
	}
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	wnrm = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	vec4 c = has_tex ? texture(albedo_tex, UV) * albedo_col : albedo_col;
	ALBEDO = c.rgb;
	ROUGHNESS = roughness;
	float up = clamp(wnrm.y, 0.0, 1.0);
	EMISSION = c.rgb * caust(wpos.xz * 0.16, TIME * 0.55) * caustic_k * (0.15 + up) + glow;
}
