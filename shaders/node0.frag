#version 330 core

uniform sampler2D diffuse_map;
in vec2 TexCoord;
in vec3 color_frag;

out vec4 out_color;

void main() {
    out_color = texture(diffuse_map, TexCoord);
    //out_color = vec4(color_frag, 1);
}
