shader_type spatial;
render_mode unshaded, cull_disabled, fog_disabled;
// Arka plan: derinlik gradyanı + uzak kaya silüetleri + yukarıdan süzülen ışık
float hash(float n) { return fract(sin(n) * 43758.5453); }
float noise1(float x) { float i = floor(x); float f = fract(x); f = f * f * (3.0 - 2.0 * f); return mix(hash(i), hash(i + 1.0), f); }

void fragment() {
	vec2 uv = UV;
	vec3 top = vec3(0.16, 0.55, 0.72);
	vec3 bot = vec3(0.02, 0.12, 0.22);
	vec3 c = mix(top, bot, pow(uv.y, 0.8));
	float ridge = 0.58 + 0.12 * noise1(uv.x * 6.0) + 0.06 * noise1(uv.x * 17.0 + 3.0);
	float ridge2 = 0.70 + 0.10 * noise1(uv.x * 9.0 + 11.0) + 0.04 * noise1(uv.x * 31.0);
	c = mix(c, vec3(0.05, 0.22, 0.32), smoothstep(ridge - 0.004, ridge + 0.004, uv.y) * 0.75);
	c = mix(c, vec3(0.03, 0.15, 0.24), smoothstep(ridge2 - 0.004, ridge2 + 0.004, uv.y) * 0.85);
	float rays = 0.0;
	for (int i = 0; i < 4; i++) {
		float fi = float(i);
		float x = 0.15 + fi * 0.24 + 0.03 * sin(TIME * 0.2 + fi);
		rays += smoothstep(0.05, 0.0, abs(uv.x - x - (uv.y) * 0.12)) * (1.0 - uv.y) * (0.5 + 0.5 * sin(TIME * 0.6 + fi * 2.0));
	}
	c += vec3(0.25, 0.45, 0.55) * rays * 0.35;
	ALBEDO = c;
}
