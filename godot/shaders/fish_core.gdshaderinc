#include "res://shaders/common.gdshaderinc"
uniform sampler2D albedo_tex : source_color, filter_linear_mipmap;
uniform vec4 albedo_col : source_color = vec4(1.0);
uniform bool has_tex = true;
uniform float roughness = 0.35;
uniform float metallic = 0.0;
uniform float wave_amp = 0.06;
uniform float wave_speed = 6.0;
uniform float wave_t = 0.0;      // betik tarafından ilerletilen faz (hıza bağlı)
uniform float caustic_k = 0.55;
varying vec3 wpos;
varying vec3 wnrm;

void vertex() {
	// Gövde dalgası: baş (+x) sabit, kuyruğa (-x) doğru artar; yanal eksen z
	float x = VERTEX.x;
	float tail = smoothstep(0.2, -0.55, x);
	VERTEX.z += sin(wave_t - x * 5.5) * wave_amp * (0.12 + tail * 1.1);
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	wnrm = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	vec4 c = has_tex ? texture(albedo_tex, UV) * albedo_col : albedo_col;
	ALBEDO = c.rgb;
	ROUGHNESS = roughness;
	METALLIC = metallic;
	SPECULAR = 0.6;
	float up = clamp(wnrm.y * 0.6 + 0.4, 0.0, 1.0);
	EMISSION = c.rgb * caust(wpos.xz * 0.16, TIME * 0.55) * caustic_k * up;
	float fr = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0);
	EMISSION += vec3(0.25, 0.6, 0.8) * fr * 0.12;
#ifdef FIN
	ALPHA = c.a;
#endif
}
