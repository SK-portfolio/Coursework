#define STB_IMAGE_IMPLEMENTATION
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <stb/stb_image.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>

#include "camera.h"
#include "shader.h"
#include "skybox.h"
#include "ground.h"
#include "model.h"

//######################################################################################################
// Window dimensions
bool isFullscreen = false;
GLFWwindow* window = nullptr;
/*
//for screen recording (screen recording while in fullscreen mode freezes playback-don't know why)
const unsigned int SCR_WIDTH = 1920;
const unsigned int SCR_HEIGHT = 1080;
*/

const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;

int windowedWidth = 800, windowedHeight = 600;  //  "default" dimensions (for fullscreen)
int windowPosX = 100, windowPosY = 100;         //  "default" position   (for fullscreen)

//######################################################################################################

//######################################################################################################
// Camera setup
Camera camera(glm::vec3(0.0f, 0.5f, 3.0f), glm::vec3(0.0f, 1.0f, 0.0f), -90.0f, 0.0f);
float timeDiff = 0.0f;
float prevFrame = 0.0f;
//######################################################################################################

//######################################################################################################
// Mouse input setup
float prevX = SCR_WIDTH / 2.0f;
float prevY = SCR_HEIGHT / 2.0f;
bool firstMouse = true;
//######################################################################################################

//######################################################################################################
// Function prototypes
void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void processInput(GLFWwindow* window);
void mouse_callback(GLFWwindow* window, double xpos, double ypos);
//######################################################################################################

//######################################################################################################
// car position along round path
glm::vec3 roundPath(float X, float Y, float Z, float time) {
    float x = sin(time) * X;                    // sin wave -> (left/right) oscillation in X-axis
    float y = Y + sin(time * 0.5f) * 5.0f;      //             (up/down) oscillation in Y-axis (height) v.small (to make car not look stiff)
    float z = cos(time) * Z;                    // cos wave -> (for/back) oscillation in Z-axis
    return glm::vec3(x, y, z);
}

// car position along straight path (x axis)
glm::vec3 straightPathX(float xMin, float xMax, float y, float z, float speed, float time) {
    float x = fmod(speed * time, (xMax - xMin)) + xMin; // get current x pos
    return glm::vec3(x, y, z);                          // y & z don't change
}

//  car position along straight path (z axis)
glm::vec3 straightPathZ(float x, float y, float zMin, float zMax, float speed, float time) {
    float z = fmod(speed * time, (zMax - zMin)) + zMin; // get current z pos
    return glm::vec3(x, y, z);                          // x & y don't change
}
//######################################################################################################

//######################################################################################################
int main() {
    // init GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // create window - title now loading screen - before new title
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Loading...", NULL, NULL);
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    // make window's context current
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    glfwSetCursorPosCallback(window, mouse_callback);
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED); // hide + capture mouse
    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);  // init OpGL loader

    // load OpGL function pointers
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }
    glEnable(GL_DEPTH_TEST);

    // cheat infinite scene with looping camera behaviour
    camera.LoopBounds = glm::vec3(55.0f, 150.0f, 55.0f); // boundary slightly wider than ground


    // shader programs
    Shader shader("vertex_shader.glsl", "fragment_shader.glsl");
    Shader groundShader("ground_vertex.glsl", "ground_fragment.glsl");
    Shader skyboxShader("skybox_vertex.glsl", "skybox_fragment.glsl");
    Shader modelShader("model_vertex.glsl", "model_fragment.glsl");

    // ground plane (MODEL - easier to add road, pavement, etc. all at once)
    Model ground("models/groundbutcooler.obj");

    //init models
    Model BuildingModelA("models/buildingA.obj");
    Model BuildingModelB("models/buildingB.obj");
    Model BuildingModelC("models/buildingC.obj");

    Model Car("models/car.obj");
    Model Monument("models/goodtimes.obj");

    Model Spire("models/spire.obj");

    //skybox
    std::vector<std::string> faces = {
        "skybox/right.png",
        "skybox/left.png",
        "skybox/top.png",
        "skybox/bottom.png",
        "skybox/front.png",
        "skybox/back.png"
    };
    Skybox skybox(faces);

    unsigned int counter = 0;   //to track #frames in timeDiff (for FPS)
    glfwSwapInterval(1);        //set to 0 -> VSync off -> FPS > 60


    // RENDER LOOP                                                      ',',',',',',',',',',',',',',',',',',',',','
    while (!glfwWindowShouldClose(window)) {
        float currFrame = static_cast<float>(glfwGetTime());                 
        timeDiff = currFrame - prevFrame;                           // Calculate delta time
        counter++;
        if (timeDiff >= 1.0 / 30.0)
        {
            //get FPS(framesPerSec) & ms(millisecs)
            float FPS = ((counter / timeDiff));         // #frames / timetaken
            float  ms = ((counter * 1000)/FPS);         // (#frames x 1000) / FPS
            //round to 2d.p. -> convert to stringstream -> combine
            std::stringstream ss;   // to convert back to float later if necsry
            ss.precision(2);
            ss << std::fixed;
            ss << FPS << " FPS / " << ms << " ms";
            // create new window title including FPS/ms
            std::string newTitle = "Final Project - Toward a Futuristic Emerald Isle     " + ss.str();
            glfwSetWindowTitle(window, newTitle.c_str());

            // reset times and counter
            prevFrame = currFrame;
            counter = 0;
        }

        // check keyboard input
        processInput(window);

        // render
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // activate shader programs
        //shader.use(); // not nedded anymore  
        groundShader.use();
        skyboxShader.use();
        modelShader.use();

        // view and projection matrices
        glm::mat4 view = camera.GetViewMatrix();
        glm::mat4 projection = glm::perspective(glm::radians(45.0f), (float)SCR_WIDTH / (float)SCR_HEIGHT, 0.1f, 150.0f);
        glm::mat4 lightProjection, lightView, lightSpaceMatrix;     // light frustum for dynamic lighting

        //ortho proj for directional light (for shadow maps)
        float nearPlane = 1.0f, farPlane = 100.0f;
        float orthoSize = 120.0f;
        lightProjection = glm::ortho(-orthoSize, orthoSize, -orthoSize, orthoSize, nearPlane, farPlane);
        
        modelShader.setMat4("view", view);
        modelShader.setMat4("projection", projection);

        // light position and view position
        glm::vec3 lightPos = glm::vec3(sin(currFrame) * 100.0f, 100.0f, cos(currFrame) * 100.0f);   //path light travels
        glm::vec3 lightTarget = glm::vec3(0.0f, 0.0f, 0.0f);                                        //point light is looking at
        glm::vec3 lightUp = glm::vec3(0.0f, 1.0f, 0.0f);                                            //up orientation of light
        lightView = glm::lookAt(lightPos, glm::vec3(0.0f), glm::vec3(0.0f, 1.0f, 0.0f));            //get view matrix for light
        // combine ortho and viw mtrx => light-space transform
        lightSpaceMatrix = lightProjection * lightView;
        shader.setMat4("lightSpaceMatrix", lightSpaceMatrix);


        modelShader.setVec3("lightPos", lightPos);
        modelShader.setVec3("viewPos", camera.Position);

        //render ground model
        glm::mat4 floor = glm::mat4(1.0f);
        floor = glm::translate(floor, glm::vec3(0.0f, -0.45f, 0.0f));
        modelShader.setMat4("model", floor);
        ground.Draw(modelShader);

        //render straightPathZ cars
        glm::mat4 flycarA = glm::mat4(1.0f);
        glm::vec3 carPositionA = straightPathZ(15.0f, 80.0f, -175, 175, 125, currFrame);
        flycarA = glm::translate(flycarA, carPositionA); // car's z position wrt time(/frames)
        flycarA = glm::rotate(flycarA, glm::radians(-90.0f), glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarA);
        Car.Draw(modelShader);

        glm::mat4 flycarB = glm::mat4(1.0f);
        glm::vec3 carPositionB = straightPathZ(-20.0f, 55.0f, 175, -175, -120, currFrame);
        flycarB = glm::translate(flycarB, carPositionB);
        flycarB = glm::rotate(flycarB, glm::radians(90.0f), glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarB);
        Car.Draw(modelShader);

        //render straightPathX cars
        glm::mat4 flycarC = glm::mat4(1.0f);
        glm::vec3 carPositionC = straightPathX(-175, 175, 70, -25, 95, currFrame);
        flycarC = glm::translate(flycarC, carPositionC); // car's x position wrt time(/frames)
        flycarC = glm::rotate(flycarC, glm::radians(0.0f), glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarC);
        Car.Draw(modelShader);

        glm::mat4 flycarD = glm::mat4(1.0f);
        glm::vec3 carPositionD = straightPathX(175, -175, 95, 30, -95, currFrame);
        flycarD = glm::translate(flycarD, carPositionD);
        flycarD = glm::rotate(flycarD, glm::radians(180.0f), glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarD);
        Car.Draw(modelShader);

        //render roundPath cars
        glm::mat4 flycarE = glm::mat4(1.0f);
        glm::vec3 carPositionE = roundPath(10.0f, 60.0f, 85.0f, currFrame);
        flycarE = glm::translate(flycarE, carPositionE);                        // car's x & z  (also y->no stiffness) position wrt time(/frames)
        flycarE = glm::rotate(flycarE, currFrame, glm::vec3(0.0f, 0.1f, 0.0f)); // & degree of car rotation wrt time (/frames) 
        modelShader.setMat4("model", flycarE);
        Car.Draw(modelShader);

        glm::mat4 flycarF = glm::mat4(1.0f);
        glm::vec3 carPositionF = roundPath(85.0f, 65.0f, 85.0f, currFrame);
        flycarF = glm::translate(flycarF, carPositionF);
        flycarF = glm::rotate(flycarF, currFrame, glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarF);
        Car.Draw(modelShader);

        glm::mat4 flycarG = glm::mat4(1.0f);
        glm::vec3 carPositionG = roundPath(85.0f, 75.0f, -85.0f, currFrame);
        flycarG = glm::translate(flycarG, carPositionG);
        flycarG = glm::rotate(flycarG, -currFrame, glm::vec3(0.0f, 0.1f, 0.0f));
        modelShader.setMat4("model", flycarG);
        Car.Draw(modelShader);

        // Render BuildingA models (medium)                         (  <-X->  ,  Y(0)  ,  /\ Z \/  )
        glm::vec3 buildingAPos[] = {
         //------------------QUAD (50,0,50) /(X,Z)------------------
            glm::vec3(15.0f, 0.0f, 40.0f),      
            glm::vec3(15.0f, 0.0f, 15.0f),      
            glm::vec3(45.0f, 0.0f, 20.0f),      
         //------------------QUAD (50,0,-50) /(X,-Z)------------------
            glm::vec3(40.0f, 0.0f, -20.0f),     
            glm::vec3(20.0f, 0.0f, -30.0f),
         //------------------QUAD (-50,0,-50) /(-X,-Z)------------------
            glm::vec3(-20.0f, 0.0f, -35.0f),    
            glm::vec3(-40.0f, 0.0f, -40.0f),    
         //------------------QUAD (-50,0,50) /(-X,Z)------------------
            glm::vec3(-15.0f, 0.0f, -15.0f),    
            glm::vec3(-20.0f, 0.0f, 20.0f),     
            glm::vec3(-40.0f, 0.0f, 40.0f)
        };

        for (const glm::vec3& pos : buildingAPos) {
            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, pos);
            modelShader.setMat4("model", model);
            BuildingModelA.Draw(modelShader);
        }

        // Render the BuildingB models (small)                    (  <-X->  ,  Y(0)  ,  /\ Z \/   )
        glm::vec3 buildingBPos[] = {
          //------------------QUAD (50,0,50) /(X,Z)------------------
            glm::vec3(10.0f, 0.0f, 45.0f),      glm::vec3(10.0f, 0.0f, 35.0f),      glm::vec3(10.0f, 0.0f, 25.0f),
            glm::vec3(10.0f, 0.0f, 15.0f),      glm::vec3(10.0f, 0.0f, 10.0f),      glm::vec3(15.0f, 0.0f, 10.0f),
            glm::vec3(25.0f, 0.0f, 10.0f),      glm::vec3(35.0f, 0.0f, 10.0f),      glm::vec3(45.0f, 0.0f, 10.0f),
          //------------------QUAD (50,0,-50) /(X,-Z)------------------
            glm::vec3(45.0f, 0.0f, -10.0f),     glm::vec3(35.0f, 0.0f, -10.0f),     glm::vec3(25.0f, 0.0f, -10.0f),
            glm::vec3(15.0f, 0.0f, -10.0f),     glm::vec3(10.0f, 0.0f, -10.0f),     glm::vec3(10.0f, 0.0f, -15.0f),
            glm::vec3(10.0f, 0.0f, -25.0f),
          //------------------QUAD (-50,0,-50) /(-X,-Z)------------------
            glm::vec3(-10.0f, 0.0f, -25.0f),    glm::vec3(-10.0f, 0.0f, -15.0f),    glm::vec3(-10.0f, 0.0f, -10.0f),
            glm::vec3(-15.0f, 0.0f, -10.0f),    glm::vec3(-25.0f, 0.0f, -10.0f),    glm::vec3(-35.0f, 0.0f, -10.0f),
            glm::vec3(-45.0f, 0.0f, -10.0f),
          //------------------QUAD (-50,0,50) /(-X,Z)------------------
            glm::vec3(-45.0f, 0.0f, 10.0f),     glm::vec3(-35.0f, 0.0f, 10.0f),     glm::vec3(-25.0f, 0.0f, 10.0f),
            glm::vec3(-15.0f, 0.0f, 10.0f),     glm::vec3(-10.0f, 0.0f, 10.0f),     glm::vec3(-10.0f, 0.0f, 15.0f),
            glm::vec3(-10.0f, 0.0f, 25.0f),     glm::vec3(-10.0f, 0.0f, 35.0f),     glm::vec3(-10.0f, 0.0f, 45.0f)  
        };

        glm::vec3 buildingBRotat[] = {
          //------------------QUAD (50,0,50) /(X,Z)------------------
            glm::vec3(0.0f, 180.0f, 0.0f),      glm::vec3(0.0f, 180.0f, 0.0f),      glm::vec3(0.0f, 180.0f, 0.0f),
            glm::vec3(0.0f, 180.0f, 0.0f),      glm::vec3(0.0f, 135.0f, 0.0f),      glm::vec3(0.0f, 90.0f, 0.0f),
            glm::vec3(0.0f, 90.0f, 0.0f),       glm::vec3(0.0f, 90.0f, 0.0f),       glm::vec3(0.0f, 90.0f, 0.0f),
          //------------------QUAD (50,0,-50) /(X,-Z)------------------
            glm::vec3(0.0f, 270.0f, 0.0f),      glm::vec3(0.0f, 270.0f, 0.0f),      glm::vec3(0.0f, 270.0f, 0.0f),
            glm::vec3(0.0f, 270.0f, 0.0f),      glm::vec3(0.0f, 225.0f, 0.0f),      glm::vec3(0.0f, 180.0f, 0.0f),
            glm::vec3(0.0f, 180.0f, 0.0f),
          //------------------QUAD (-50,0,-50) /(-X,-Z)------------------
            glm::vec3(0.0f, 0.0f, 0.0f),        glm::vec3(0.0f, 0.0f, 0.0f),        glm::vec3(0.0f, 315.0f, 0.0f),
            glm::vec3(0.0f, 270.0f, 0.0f),      glm::vec3(0.0f, 270.0f, 0.0f),      glm::vec3(0.0f, 270.0f, 0.0f),
            glm::vec3(0.0f, 270.0f, 0.0f),
          //------------------QUAD (-50,0,50) /(-X,Z)------------------            
            glm::vec3(0.0f, 90.0f, 0.0f),       glm::vec3(0.0f, 90.0f, 0.0f),       glm::vec3(0.0f, 90.0f, 0.0f),
            glm::vec3(0.0f, 90.0f, 0.0f),       glm::vec3(0.0f, 45.0f, 0.0f),       glm::vec3(0.0f, 0.0f, 0.0f),
            glm::vec3(0.0f, 0.0f, 0.0f),        glm::vec3(0.0f, 0.0f, 0.0f),        glm::vec3(0.0f, 0.0f, 0.0f)
        };

        for (int i = 0; i < sizeof(buildingBPos) / sizeof(buildingBPos[0]); i++) {
            glm::mat4 modelB = glm::mat4(1.0f);
            modelB = glm::translate(modelB, buildingBPos[i]);
            modelB = glm::rotate(modelB, glm::radians(buildingBRotat[i].y), glm::vec3(0.0f, 1.0f, 0.0f));
            modelShader.setMat4("model", modelB);
            BuildingModelB.Draw(modelShader);
        }

        // Render the BuildingC models (Big)                                (  <-X->  ,  Y(0)  ,  /\ Z \/   )
        glm::vec3 buildingCPos[] = {
         //------------------QUAD (50,0,50) /(X,Z)------------------
            glm::vec3(45.0f, 0.0f, 45.0f),
            glm::vec3(30.0f, 0.0f, 25.0f),
         //------------------QUAD (50,0,-50) /(X,-Z)------------------
            glm::vec3(40.0f, 0.0f, -40.0f),
         //------------------QUAD (-50,0,-50) /(-X,-Z)------------------
            glm::vec3(-40.0f, 0.0f, -20.0f),
         //------------------QUAD (-50,0,50) /(-X,Z)------------------
            glm::vec3(-40.0f, 0.0f, 20.0f), 
            glm::vec3(-20.0f, 0.0f, 40.0f)
        };

        for (int i = 0; i < sizeof(buildingCPos) / sizeof(buildingCPos[0]); i++) {
            glm::mat4 modelC = glm::mat4(1.0f);
            modelC = glm::translate(modelC, buildingCPos[i]);
            modelShader.setMat4("model", modelC);
            BuildingModelC.Draw(modelShader);
        }

        // Render the spire (Tallest model)
        glm::mat4 modelspr = glm::mat4(1.0f);
        modelspr = glm::translate(modelspr, glm::vec3(0.0f, 7.5f, -40.0f));
        modelShader.setMat4("model", modelspr);
        Spire.Draw(modelShader);

        glm::mat4 stone = glm::mat4(1.0f);
        stone = glm::translate(stone, glm::vec3(0.0f, 11.5f, -49.0f));
        stone = glm::rotate(stone, glm::radians(90.0f), glm::vec3(0.0f, 1.0f, 0.0f));
        modelShader.setMat4("model", stone);
        Monument.Draw(modelShader);

        // draw skybox
        skybox.Draw(skyboxShader, view, projection);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Cleanup
    glfwTerminate();
    return 0;
}
//######################################################################################################

//######################################################################################################
void toggleFullscreen(GLFWwindow* window) {
    static int lastWindowedWidth = windowedWidth;
    static int lastWindowedHeight = windowedHeight;
    static int lastWindowPosX = windowPosX;
    static int lastWindowPosY = windowPosY;

    GLFWmonitor* monitor = glfwGetPrimaryMonitor();
    const GLFWvidmode* mode = glfwGetVideoMode(monitor);

    if (!isFullscreen) {
        // save current window size and position
        glfwGetWindowPos(window, &lastWindowPosX, &lastWindowPosY);
        glfwGetWindowSize(window, &lastWindowedWidth, &lastWindowedHeight);

        // switch to fullscreen
        glfwSetWindowMonitor(window, monitor, 0, 0, mode->width, mode->height, mode->refreshRate);
    }
    else {
        // switch back to windowed mode
        glfwSetWindowMonitor(window, nullptr, lastWindowPosX, lastWindowPosY, lastWindowedWidth, lastWindowedHeight, 0);
    }

    isFullscreen = !isFullscreen;
}
//######################################################################################################

//######################################################################################################
void processInput(GLFWwindow* window) {
    static bool fKeyPressed = false;  // flag to track F key state
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        camera.ProcessKeyboard(GLFW_KEY_W, timeDiff);
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        camera.ProcessKeyboard(GLFW_KEY_S, timeDiff);
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        camera.ProcessKeyboard(GLFW_KEY_A, timeDiff);
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        camera.ProcessKeyboard(GLFW_KEY_D, timeDiff);

    if (glfwGetKey(window, GLFW_KEY_F) == GLFW_PRESS && !fKeyPressed) {
        fKeyPressed = true;  // prevent spamming
        toggleFullscreen(window);
    }
    if (glfwGetKey(window, GLFW_KEY_F) == GLFW_RELEASE) {
        fKeyPressed = false;  // reset state when key is released
    }
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}
//######################################################################################################

//######################################################################################################
// update camera view based on cursor movement
void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
    // first mouse movement detected
    if (firstMouse) {
        prevX = static_cast<float>(xpos);       // store current X position of the cursor as previous 
        prevY = static_cast<float>(ypos);       // store current Y position of the cursor as previous
        firstMouse = false;
    }
    // get change in cursor pos (offset) sinc prev frame.
    float xoffset = static_cast<float>(xpos - prevX);
    float yoffset = static_cast<float>(prevY - ypos);

    // update prev cursor pos to curr pos
    prevX = static_cast<float>(xpos);
    prevY = static_cast<float>(ypos);

    // pass the offsets to camera.cpp to adjust camera orientation
    camera.ProcessMouseMovement(xoffset, yoffset);
}
//######################################################################################################

//######################################################################################################
// resize framebuffer
void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
//######################################################################################################
