shader_type spatial;
#include "res://shaders/common.gdshaderinc"
uniform sampler2D sand_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform float tile = 1.6;
uniform float ripple = 0.035;
varying vec3 wpos;

float h(vec2 p) {
	return ripple * (sin(p.x * 3.1 + sin(p.y * 1.7) * 1.4) + 0.45 * sin(p.y * 4.3 + p.x * 1.1) + 0.25 * sin(p.x * 7.0 + p.y * 2.3));
}

void vertex() {
	vec3 w = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float e = 0.02;
	float hc = h(w.xz);
	VERTEX.y += hc;
	vec3 n = normalize(vec3(-(h(w.xz + vec2(e, 0.0)) - hc) / e, 1.0, -(h(w.xz + vec2(0.0, e)) - hc) / e));
	NORMAL = n;
	wpos = w;
}

void fragment() {
	vec3 c = texture(sand_tex, wpos.xz / tile).rgb;
	// uzaktaki tekrarı kırmak için ikinci, büyük ölçekli örnek
	c = mix(c, texture(sand_tex, wpos.xz / (tile * 3.7) + 0.31).rgb, 0.35);
	c *= vec3(1.1, 1.0, 0.84);
	ALBEDO = c;
	ROUGHNESS = 0.9;
	EMISSION = c * caust(wpos.xz * 0.16, TIME * 0.55) * 0.5;
	ALBEDO *= 0.82;
}
