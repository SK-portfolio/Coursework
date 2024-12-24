#ifndef SKYBOX_H
#define SKYBOX_H

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <vector>
#include <string>

#include "shader.h"

class Skybox {
public:
    Skybox(const std::vector<std::string>& faces);
    ~Skybox();

    void Draw(const Shader& shader, const glm::mat4& view, const glm::mat4& projection);

private:
    unsigned int cubemapTexture;
    unsigned int VAO, VBO;

    unsigned int loadCubemap(const std::vector<std::string>& faces);
    void setupSkybox();
};

#endif