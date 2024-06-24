#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec2 texCoord;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// color given to the fragment shader
out vec3 color_frag;
out vec2 TexCoord;

void main() {
    color_frag = color;
    TexCoord = texCoord;
    gl_Position = projection * view * model * vec4(position, 1);
}
