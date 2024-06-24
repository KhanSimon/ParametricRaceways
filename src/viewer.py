#!/usr/bin/env python3

import pathlib
import OpenGL.GL as GL
import glfw
from glm import rotate, translate, scale, perspective, identity, mat4, vec3, radians
from numpy import array

from shader import Shader
from node import Node
from road import Road
from cube import Cube
from camera import Camera
import outilsFonction
import numpy as np
import ask

from camera import Camera
from wheel import Wheel
from textured_sphere import TexturedSphere
from texture import Texture

class Viewer:
    def __init__(self, width=640, height=480):
        # Get monitor resolution for window size
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)

        # Create a windowed mode window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.win = glfw.create_window(mode.size.width, mode.size.height, 'Viewer', None, None)
        if not self.win:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        glfw.make_context_current(self.win)
        glfw.set_key_callback(self.win, self.on_key)

        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL', GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() + ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)

        self.scene_root = Node()
        self.camera = Camera()
        self.road = None

    def run(self):
        while not glfw.window_should_close(self.win):
            self.scene_root.update_position()
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            model = array(identity(mat4))
            rot_mat = identity(mat4)
            tra_mat = translate(vec3(0, 0, -4))
            sca_mat = identity(mat4)
            view =  array(tra_mat @ rot_mat @ sca_mat)

            self.camera.update_target(self.cube.directionVector)
            view = self.camera.get_view()

            projection = array(perspective(45, 1, 0, 10))
            self.scene_root.draw(model, view, projection)
            glfw.swap_buffers(self.win)
            glfw.poll_events()

    def on_key(self, _win, key, _scancode, action, _mods):
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
        self.scene_root.key_handler(key, action)

def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    shaders_dir = str(pathlib.Path().parent.absolute()) + "/shaders/"
    textures_dir = str(pathlib.Path().parent.absolute()) + "/textures/"

    """Color shader for car TP3"""
    basic_shader = Shader(shaders_dir + "node.vert", shaders_dir + "node.frag")
    color_shader = Shader(shaders_dir + "node0.vert", shaders_dir + "node0.frag")
    texture_shader = Shader(shaders_dir + "texture.vert", shaders_dir + "texture.frag")
    color_shader_road = Shader(shaders_dir + "road.vert", shaders_dir + "road.frag")

    texture0 = Texture(textures_dir + "texture0.jpeg")
    texture1 = Texture(textures_dir + "texture1.jpeg")
    texture2 = Texture(textures_dir + "texture2.png")
    texture3 = Texture(textures_dir + "texture3.jpeg")

    # Add the sun and the earth
    sky = Node(transform= scale((10000, 10000, 10000)))
    sky.add(TexturedSphere(texture_shader, texture3))
    viewer.scene_root.add(sky)
    earth = Node(transform=translate((200, 0, -1000))@ scale((100, 100, 100)))
    earth.add(TexturedSphere(texture_shader, texture1))
    viewer.scene_root.add(earth)
    sun = Node(transform=translate((-200, 5, -1000))@ scale((300, 300, 300)))
    sun.add(TexturedSphere(texture_shader, texture0))
    viewer.scene_root.add(sun)


    road_node = Node()

    function, boolDeniv = ask.ask()
    N = 900
    X, Y = outilsFonction.getXYvectors(function, N)

    viewer.road = Road(color_shader_road, N, X, Y, boolDeniv)
    road_node.add(viewer.road)
    viewer.scene_root.add(road_node)

    viewer.cube = Cube(color_shader,texture2)
    viewer.cube.set_road_position(viewer.road.get_positions())
    viewer.cube.set_road_indices(viewer.road.get_indices())
    cube_node = Node()
    cube_node.add(viewer.cube)
    viewer.scene_root.add(cube_node)

    yaxis=-0.6
    xaxis = 0.45
    zaxis = 0.5
    wscaling = 0.5
    # add wheels
    wheel_transform1 = translate((xaxis, yaxis, zaxis)) @ scale((wscaling, wscaling, wscaling)) @ rotate(radians(90), (0, 0, 1))
    wheel1 = Wheel(basic_shader,transform=wheel_transform1)
    viewer.cube.addWheel(wheel1)


    wheel_transform2 = translate((-xaxis, yaxis, zaxis)) @ scale((wscaling, wscaling, wscaling)) @ rotate(radians(90), (0, 0, 1))
    wheel2 = Wheel(basic_shader,transform=wheel_transform2)
    viewer.cube.addWheel(wheel2)


    wheel_transform3 = translate((-xaxis, yaxis, -zaxis)) @ scale((wscaling, wscaling, wscaling)) @ rotate(radians(90), (0, 0, 1))
    wheel3 = Wheel(basic_shader,transform=wheel_transform3)
    viewer.cube.addWheel(wheel3)


    wheel_transform4 = translate((xaxis, yaxis, -zaxis)) @ scale((wscaling, wscaling, wscaling)) @ rotate(radians(90), (0, 0, 1))
    wheel4 = Wheel(basic_shader,transform=wheel_transform4)
    viewer.cube.addWheel(wheel4)

    viewer.run()

if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()
