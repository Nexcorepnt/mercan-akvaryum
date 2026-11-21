shader_type spatial;
render_mode unshaded, cull_disabled, blend_add, depth_draw_never, fog_disabled;
// Yukarıdan inen ışık huzmesi kartı
uniform float phase = 0.0;
uniform float strength = 0.22;
void vertex() {
	// Y eksenli billboard
	MODELVIEW_MATRIX = VIEW_MATRIX * mat4(INV_VIEW_MATRIX[0], MODEL_MATRIX[1], vec4(normalize(cross(INV_VIEW_MATRIX[0].xyz, MODEL_MATRIX[1].xyz)), 0.0), MODEL_MATRIX[3]);
}
void fragment() {
	float edge = smoothstep(0.0, 0.35, UV.x) * smoothstep(1.0, 0.65, UV.x);
	float fade = pow(1.0 - UV.y, 1.6);
	float flick = 0.6 + 0.4 * sin(TIME * 0.7 + phase);
	ALBEDO = vec3(0.55, 0.85, 1.0) * edge * fade * flick * strength;
}
