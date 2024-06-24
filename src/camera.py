import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args

import glm
import glfw
import math


class Camera:
    """Camera object"""


    def __init__(self):
        #######The camera position is a vector in world space that points to the camera's position
        self.cameraPos = glm.vec3(0, 0, 2)
        #######The next vector required is the camera's direction e.g. at what direction it is pointing at
        self.cameraTarget = glm.vec3(0, 0, 0)
        #Subtracting the camera position vector from the target vector thus results in the direction vector we want
        self.cameraDirection = glm.normalize(self.cameraPos - self.cameraTarget)
        ########The next vector that we need is a right vector that represents the positive x-axis of the camera space. To get the right vector we use a little trick by first specifying an up vector that points upwards (in world space). Then we do a cross product on the up vector and the direction vector from step 2
        up = glm.vec3(0, 1, 0)
        self.cameraRight = glm.normalize(glm.cross(up, self.cameraDirection))
        ########Up axis Now that we have both the x-axis vector and the z-axis vector, retrieving the vector that points to the camera's positive y-axis is relatively easy: we take the cross product of the right and direction vector:
        self.cameraUp = glm.cross(self.cameraDirection, self.cameraRight)




    def update_target(self,target):
        self.cameraTarget = glm.vec3(target)
        self.cameraDirection = glm.normalize(self.cameraTarget)
        self.cameraPos = self.cameraTarget - 7 * self.cameraDirection + (0,3,0)
        #self.cameraPos = self.cameraPos * 0.3 + (self.cameraTarget - (0,-3,0)) * 0.7

        #self.cameraRight = glm.normalize(glm.cross((0,1,0), self.cameraDirection))
        #self.cameraUp = glm.cross(self.cameraDirection, self.cameraRight)


    def get_view(self):
        radius = 5
        camX = math.sin(glfw.get_time()/5) * radius
        camZ = math.cos(glfw.get_time()/5) * radius
        #return np.array (glm.lookAt(glm.vec3(camX, 0, camZ), glm.vec3(0.0, 0.0, 0.0), self.cameraUp))
        return np.array (glm.lookAt(self.cameraPos,self.cameraTarget, self.cameraUp))
        #return np.array (glm.lookAt(self.cameraTarget-(5,10,5), self.cameraTarget, glm.vec3(0.0, 1.0, 0.0)))


    def key_handler(self,key):
        if key == glfw.KEY_W : print('move forward')
        elif key == glfw.KEY_S : print('move backwwards')
        elif key == glfw.KEY_LEFT : print('move left')
        elif key == glfw.KEY_RIGHT : print('move right')
        elif key == glfw.KEY_UP : print('move Up')
        elif key == glfw.KEY_DOWN : print('move down')
