// ground.h
#ifndef GROUND_H
#define GROUND_H

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <string>
#include <vector>
#include "shader.h" // Include the Shader class for setting up the ground's shader

class Ground {
public:
    Ground();
    ~Ground();
    void Draw(const Shader& shader, const glm::mat4& view, const glm::mat4& projection);

private:
    GLuint VAO, VBO, EBO;
    void setupGround();
};

#endif