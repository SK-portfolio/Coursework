#ifndef SHADER_H
#define SHADER_H

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <string>

class Shader {
public:
    unsigned int ID;

    Shader(const char* vertexPath, const char* fragmentPath);
    void use() const;
    void setMat4(const std::string& name, const glm::mat4& value) const;
    void setVec3(const std::string& name, const glm::vec3& value) const;
    void setInt(const std::string& name, int value) const; // Add this for shadow map
    void setFloat(const std::string& name, float value) const; // Optional for flexibility

private:
    void checkCompileErrors(unsigned int shader, std::string type);
};

#endif