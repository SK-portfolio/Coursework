#ifndef MESH_H
#define MESH_H

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <string>
#include <vector>
#include "shader.h"

// Structure for vertex attributes
struct Vertex {
    glm::vec3 Position;
    glm::vec3 Normal;
    glm::vec2 TexCoords;
};

// Structure for texture information
struct Texture {
    unsigned int id;
    std::string type;
    std::string path; // File path for debugging
};

class Mesh {
public:
    // Mesh Data
    std::vector<Vertex> vertices;
    std::vector<unsigned int> indices;
    std::vector<Texture> textures;

    // Constructor
    Mesh(std::vector<Vertex> vertices, std::vector<unsigned int> indices, std::vector<Texture> textures);

    // Render the mesh
    void Draw(Shader& shader);

private:
    // Render data
    unsigned int VAO, VBO, EBO;

    // Initializes the buffer objects
    void setupMesh();
};

#endif
