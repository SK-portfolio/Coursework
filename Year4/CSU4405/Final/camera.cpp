#include <GLFW/glfw3.h>
#include "Camera.h"

Camera::Camera(glm::vec3 position, glm::vec3 up, float yaw, float pitch)
    : Front(glm::vec3(0.0f, 0.0f, -1.0f)), MovementSpeed(5.5f), MouseSensitivity(0.1f) {
    Position = position;
    WorldUp = up;
    Yaw = yaw;
    Pitch = pitch;
    LoopBounds = glm::vec3(200.0f, 200.0f, 200.0f); //default loop boundaries
    updateCameraVectors();            //func to get initial camera vectors
}

glm::mat4 Camera::GetViewMatrix() {
    return glm::lookAt(Position, Position + Front, Up);
}

//process keyboard input to move camera
void Camera::ProcessKeyboard(int direction, float deltaTime) {
    float velocity = MovementSpeed * deltaTime;
    if (direction == GLFW_KEY_W)
        Position += Front * velocity;
    if (direction == GLFW_KEY_S)
        Position -= Front * velocity;
    if (direction == GLFW_KEY_A)
        Position -= Right * velocity;
    if (direction == GLFW_KEY_D)
        Position += Right * velocity;

   Loop(); //apply looping logic
}

//process mouse movement to adjust yaw and pitch
void Camera::ProcessMouseMovement(float xoffset, float yoffset, bool constrainPitch) {
    xoffset *= MouseSensitivity;    //adjust xoffset by sensitivity
    yoffset *= MouseSensitivity;    //adjust yoffset by sensitivity

    Yaw += xoffset;                 //use xoffset to update yaw
    Pitch += yoffset;               //use yoffset to update pitch

    if (constrainPitch) {           //limit pitch -> avoid camera flipping
        if (Pitch > 89.0f)
            Pitch = 89.0f;
        if (Pitch < -89.0f)
            Pitch = -89.0f;
    }

    updateCameraVectors();          //recalc camera vectors
}

// loop camera position within predefined bounds
void Camera::Loop() {
    if (Position.x > LoopBounds.x)
        Position.x = -LoopBounds.x;
    else if (Position.x < -LoopBounds.x)
        Position.x = LoopBounds.x;

    if (Position.y > LoopBounds.y)
        Position.y = -LoopBounds.y;
    else if (Position.y < -LoopBounds.y)
        Position.y = LoopBounds.y;

    if (Position.z > LoopBounds.z)
        Position.z = -LoopBounds.z;
    else if (Position.z < -LoopBounds.z)
        Position.z = LoopBounds.z;
}

//recalc camera direction vectors
void Camera::updateCameraVectors() {
    glm::vec3 front;
    front.x = cos(glm::radians(Yaw)) * cos(glm::radians(Pitch));
    front.y = sin(glm::radians(Pitch));
    front.z = sin(glm::radians(Yaw)) * cos(glm::radians(Pitch));
    Front = glm::normalize(front);

    Right = glm::normalize(glm::cross(Front, WorldUp));
    Up = glm::normalize(glm::cross(Right, Front));
}
