#version 330 core

layout (location = 0) in vec3 aPos;      // Position attribute
layout (location = 1) in vec3 aNormal;   // Normal attribute
layout (location = 2) in vec2 aTexCoords; // Texture coordinates

out vec3 FragPos;       // Position of the fragment
out vec4 FragPosLightSpace;
out vec3 Normal;        // Normal for lighting calculations
out vec2 TexCoords;     // Texture coordinates passed to fragment shader

uniform mat4 model;
uniform mat4 lightSpaceMatrix;
uniform mat4 view;
uniform mat4 projection;

void main() {
    FragPos = vec3(model * vec4(aPos, 1.0)); // Calculate world position
    Normal = mat3(transpose(inverse(model))) * aNormal; // Transform normal to world space
    TexCoords = aTexCoords; // Pass through texture coordinates

    gl_Position = projection * view * vec4(FragPos, 1.0); // Transform to clip space
    FragPosLightSpace = lightSpaceMatrix * model * vec4(aPos, 1.0);
}
