#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec2 textCoord;

out vec2 outTexCoord;

uniform mat4 transform;
uniform mat4 projection;
uniform mat4 view;


void main()
{
    gl_Position = projection * view * transform * vec4(position.x, position.y, position.z, 1.0);
    outTexCoord = vec2(textCoord.x, 1.0 - textCoord.y);
}
