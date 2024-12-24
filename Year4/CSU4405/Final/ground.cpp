//NOT NEEDED ANYMORE - USING MODEL FOR GROUND
#include "ground.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <GLFW/glfw3.h>

Ground::Ground() {
    setupGround();
}

Ground::~Ground() {
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
}

void Ground::setupGround() {
    // define vertices for ground (quad plane)
    float groundVertices[] = {
        //positions          //texture coords
         50.0f,  0.0f,  50.0f,  1.0f, 1.0f, // top-right
         50.0f,  0.0f, -50.0f,  1.0f, 0.0f, // bottom-right
        -50.0f,  0.0f, -50.0f,  0.0f, 0.0f, // bottom-left
        -50.0f,  0.0f,  50.0f,  0.0f, 1.0f  // top-left
    };
    unsigned int groundIndices[] = {
        0, 1, 3, //1st triangle
        1, 2, 3  //2nd triangle
    };

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    //VBO setup
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(groundVertices), groundVertices, GL_STATIC_DRAW);

    //EBO setup
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(groundIndices), groundIndices, GL_STATIC_DRAW);

    //position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    //texture coordinate attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    //unbind VAO (EBO stays bound to VAO)
    glBindVertexArray(0);
}

void Ground::Draw(const Shader& shader, const glm::mat4& view, const glm::mat4& projection) {
    shader.use();
    shader.setMat4("view", view);
    shader.setMat4("projection", projection);

    glm::mat4 model = glm::mat4(1.0f); //identity matrix
    shader.setMat4("model", model);

    //set colour
    shader.setVec3("objectColour", glm::vec3(0.0f, 0.75f, 0.25f)); //green

    //render ground
    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
    glBindVertexArray(0);

    GLenum err;
    while ((err = glGetError()) != GL_NO_ERROR) {
        std::cerr << "OpenGL error: " << err << std::endl;
    }
}

