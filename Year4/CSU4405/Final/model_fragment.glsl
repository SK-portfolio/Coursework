#version 330 core

in vec3 FragPos;       // Fragment position in world space
in vec3 Normal;        // Normal in world space
in vec2 TexCoords;     // Texture coordinates
in vec4 FragPosLightSpace; // Fragment position in light-space

out vec4 FragColor;

uniform sampler2D texture_diffuse1;  // Diffuse texture sampler
uniform sampler2D shadowMap;         // Shadow map sampler
uniform vec3 lightColor = vec3(1.0); // Default white light
uniform vec3 lightPos = vec3(0.0, 1.0, 0.0); // Default light position
uniform vec3 viewPos;                // Camera position

// Function to calculate shadow
float ShadowCalculation(vec4 fragPosLightSpace) {
    // Perform perspective division
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5; // Transform to [0, 1] range

    // Check if within shadow map bounds
    if (projCoords.z > 1.0 || projCoords.z < 0.0)
        return 0.0;

    // Retrieve the closest depth from the shadow map
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;

    // Shadow offset to avoid acne
    float bias = max(0.005 * (1.0 - dot(normalize(Normal), normalize(lightPos - FragPos))), 0.005);

    // Shadow calculation
    float shadow = currentDepth > closestDepth + bias ? 1.0 : 0.0;

    return shadow;
}

void main() {
    // Sample the texture color
    vec4 texColor = texture(texture_diffuse1, TexCoords);

    // Basic ambient lighting
    float ambientStrength = 0.5;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse lighting
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Shadow calculation
    float shadow = ShadowCalculation(FragPosLightSpace);

    // Combine lighting and apply shadow
    vec3 lighting = (ambient + (1.0 - shadow) * diffuse) * vec3(texColor);

    FragColor = vec4(lighting, texColor.a); // Keep alpha from texture
}
