#version 330 core

in vec3 ourColor;    // Input from vertex shader
in vec2 TexCoords;   // Input from vertex shader

out vec4 FragColor;

uniform sampler2D texture_diffuse1; // Texture sampler

void main() {
    vec4 texColor = texture(texture_diffuse1, TexCoords); // Sample texture
    FragColor = texColor * vec4(ourColor, 1.0);           // Blend with color
}
