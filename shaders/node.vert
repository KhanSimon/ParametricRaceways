#version 330 core

// input attribute variable, given per vertex
in vec3 position;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main() {
    gl_Position = projection * view * model * vec4(position, 1);
}
