import OpenGL.GL as GL
import numpy as np
import glm
from glm import vec3
import glfw
from math import cos, sin
from shape import Shape
import ctypes

class Cube(Shape):
    """Cube object"""

    def __init__(self, shader, texture):
        super().__init__(shader)
        self.wheels = []
        # cube vertex positions
        positions = np.array((
            # front face
            (-0.5,  0.5,  0.75),   # Vertex 0
            (-0.5, -0.5,  0.75),   # Vertex 1
            ( 0.5, -0.5,  0.75),   # Vertex 2
            ( 0.5,  0.5,  0.75),   # Vertex 3

            # left side
            (-0.5,  0.5,  0.75),   # Vertex 4
            (-0.5, -0.5,  0.75),   # Vertex 5
            (-0.5, -0.5, -0.75),   # Vertex 6
            (-0.5,  0.5, -0.75),   # Vertex 7

            # right side
            ( 0.5,  0.5,  0.75),   # Vertex 8
            ( 0.5, -0.5,  0.75),   # Vertex 9
            ( 0.5, -0.5, -0.75),   # Vertex 10
            ( 0.5,  0.5, -0.75),   # Vertex 11

            # up side
            (-0.5,  0.5,  0.75),   # Vertex 12
            (-0.5,  0.5, -0.75),   # Vertex 13
            ( 0.5,  0.5, -0.75),   # Vertex 14
            ( 0.5,  0.5,  0.75),   # Vertex 15

            # down side
            (-0.5, -0.5,  0.75),   # Vertex 16
            (-0.5, -0.5, -0.75),   # Vertex 17
            ( 0.5, -0.5, -0.75),   # Vertex 18
            ( 0.5, -0.5,  0.75),   # Vertex 19

            # back face
            (-0.5,  0.5, -0.75),   # Vertex 20
            (-0.5, -0.5, -0.75),   # Vertex 21
            ( 0.5, -0.5, -0.75),   # Vertex 22
            ( 0.5,  0.5, -0.75),   # Vertex 23
        ), dtype=np.float32)


        textures = np.array((

            #backface
            (0.75,  0.333),   # Vertex 20
            (1, 0.333),  # Vertex 21
            ( 1.0, 0.666),  # Vertex 22
            ( 0.75,0.666),  # Vertex 23

            #left side
            (0.25,  0.3333),   # Vertex 4
            (0.25,  0.0),  # Vertex 5
            (0.75,  0.0),  # Vertex 6
            (0.75,  0.3333),   # Vertex 7

            #right side
            (0.25,  0.666),  # Vertex 8
            ( 0.25, 1.0),  # Vertex 9
            ( 0.75, 1.0),  # Vertex 10
            ( 0.75,0.666),  # Vertex 11

            #up side
            (0.25,  0.333),   # Vertex 12
            (0.75,  0.333),   # Vertex 13
            (0.75,  0.666),  # Vertex 14
            (0.25,  0.666),  # Vertex 15



            #down side
            (0.25,  0.333),   # Vertex 12
            (0.75,  0.333),   # Vertex 13
            (0.75,  0.666),  # Vertex 14
            (0.25,  0.666),  # Vertex 15


            #front face
            (0.25,  0.3333),   # Vertex 0
            (0.0, 0.333),  # Vertex 1
            ( 0.0, 0.666),  # Vertex 2
            ( 0.25, 0.666)  # Vertex 3

            ), dtype=np.float32)


        colors = np.array((
            #front face
            (1,0,0),
            (1,0,0),
            (1,0,0),
            (1,0,0),


            #left side
            (0,1,0),
            (0,1,0),
            (0,1,0),
            (0,1,0),


            #right side
            (0,1,0),
            (0,1,0),
            (0,1,0),
            (0,1,0),


            #up side
            (0,0,1),
            (0,0,1),
            (0,0,1),
            (0,0,1),



            #down side todooooooooo
            (0,0,1),
            (0,0,1),
            (0,0,1),
            (0,0,1),


            #backface
            (1,0,0),
            (1,0,0),
            (1,0,0),
            (1,0,0),

            ), dtype=np.float32)


        interleaved_data = np.hstack((positions, colors))
        interleaved_data = np.hstack((interleaved_data, textures))


        # Define the 12 triangles (two per face)
        indices = np.array((
            (0, 2, 1), (0, 3, 2),  # Front face
            (4, 5, 6), (4, 6, 7),  # left side face
            (8, 10, 9), (8, 11, 10),  # right side face
            (12, 13, 14), (12, 14, 15),  # Top side
            (16, 18, 17), (16, 19, 18),  # down face
            (20, 21, 22), (20, 22, 23)   # back face
        ), dtype=np.uint32)

        #GL.glEnable(GL.GL_CULL_FACE)
        #GL.glCullFace(GL.GL_FRONT)


        ##################################
        #create VBO
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, interleaved_data, GL.GL_STATIC_DRAW)
        # position attribute
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * interleaved_data.itemsize, ctypes.c_void_p(0))

        col = GL.glGetAttribLocation(shader.glid, 'color')
        GL.glEnableVertexAttribArray(col)
        GL.glVertexAttribPointer(col, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * interleaved_data.itemsize, ctypes.c_void_p(12))

        texCoord = GL.glGetAttribLocation(shader.glid, "texCoord")
        GL.glEnableVertexAttribArray(texCoord)
        GL.glVertexAttribPointer(texCoord, 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * interleaved_data.itemsize, ctypes.c_void_p(24))

        #create EBO
        # indexbuffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)
        ################################
        self.texture = texture
        #######
        self.cube_transform = glm.translate((0,0,0)) @ glm.scale((1, 1, 1)) @ glm.rotate(0, (0, 1, 0))
        self.translation_vector = glm.vec3(0, 0, 0)
        self.directionVector = glm.vec3(0, 0, -1)
        self.angleX = 0
        self.angleY = 0

        # Dictionary to track key states
        self.keys = {
            glfw.KEY_W: False,
            glfw.KEY_S: False,
            glfw.KEY_A: False,
            glfw.KEY_D: False,
            glfw.KEY_UP: False,
            glfw.KEY_DOWN: False,
            glfw.KEY_SPACE: False  # For acceleration
        }

        self.speed = 0.02 *4
        self.angle_speed = 0.005 *8
        self.gravity = 0.05
        self.base_speed = self.speed
        self.acceleration_factor = 3  # Speed multiplier when accelerating

        # State for falling
        self.is_falling = False
        self.fall_start_time = None
        self.fall_duration = 3  # seconds
        self.start_position = glm.vec3(0, 0, 0)

        self.road_positions = None
        self.road_indices = None

        # Time tracking for collision checking
        self.last_collision_check_time = glfw.get_time()

    def set_road_indices(self, road_indices):
        self.road_indices = road_indices

    def get_vertices(self):
        return self.vertices

    def set_road_position(self, road_positions):
        self.road_positions = road_positions

    def apply_gravity(self):
        self.translation_vector.y -= self.gravity

    def draw(self, model, view, projection):
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_FRONT)
        for wheel in self.wheels: wheel.draw2(model, self.cube_transform, view, projection)


        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)
        ###########
        # texture access setups
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        #GL.glUniform1i(self.loc_diffuse_map, 0)
        ###########
        self.directionVector = glm.vec3(0, 0, -1)
        self.cube_transform = glm.translate(self.translation_vector) @ glm.scale((1, 1, 1)) @ glm.rotate(self.angleX, (0, 1, 0)) @ glm.rotate(self.angleY,(1,0,0))
        self.directionVector = self.cube_transform @ glm.vec3(0, 0, -1)
        model =  model @ self.cube_transform
        super().draw(model, view, projection)
        GL.glDrawElements(GL.GL_TRIANGLES, 12*3 , GL.GL_UNSIGNED_INT, None)
        ###########
        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
        GL.glDisable(GL.GL_CULL_FACE)
        ###########

    def update_position(self):
        if not self.is_falling:
            # Adjust speed if accelerating
            current_speed = self.speed * self.acceleration_factor if self.keys[glfw.KEY_SPACE] else self.speed

            if self.keys[glfw.KEY_W]:
                self.translation_vector.z -= cos(self.angleX) * current_speed
                self.translation_vector.x -= sin(self.angleX) * current_speed
                self.translation_vector.y += sin(self.angleY) * current_speed

            if self.keys[glfw.KEY_S]:
                self.translation_vector.z += cos(self.angleX) * current_speed
                self.translation_vector.x += sin(self.angleX) * current_speed
                self.translation_vector.y -= sin(self.angleY) * current_speed

            if self.keys[glfw.KEY_A]:
                self.angleX += self.angle_speed

            if self.keys[glfw.KEY_D]:
                self.angleX -= self.angle_speed

            if self.keys[glfw.KEY_UP]:
                self.angleY += self.angle_speed

            if self.keys[glfw.KEY_DOWN]:
                self.angleY -= self.angle_speed

            # Check collisions only if 100 ms have passed beacause of performance reasons
            current_time = glfw.get_time()
            if current_time - self.last_collision_check_time > 0.1:
                self.check_collisions()
                self.last_collision_check_time = current_time

        else:
            self.apply_gravity()
            current_time = glfw.get_time()
            if current_time - self.fall_start_time > self.fall_duration:
                self.reset_position()

    def check_collisions(self):
        if self.road_positions is None or self.road_indices is None:
            return False  # No road positions or indices to check against

        # Define the size of the car
        car_corners = [
            vec3(self.translation_vector.x - 0.5, self.translation_vector.y, self.translation_vector.z - 0.75),
            vec3(self.translation_vector.x - 0.5, self.translation_vector.y, self.translation_vector.z + 0.75),
            vec3(self.translation_vector.x + 0.5, self.translation_vector.y, self.translation_vector.z - 0.75),
            vec3(self.translation_vector.x + 0.5, self.translation_vector.y, self.translation_vector.z + 0.75)
        ]

        def point_in_triangle(pt, v1, v2, v3):
            def sign(p1, p2, p3):
                return (p1.x - p3.x) * (p2.z - p3.z) - (p2.x - p3.x) * (p1.z - p3.z)

            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)

            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

            return not (has_neg and has_pos)

        # Check if any of the car's corners are within any road triangle
        on_road = False
        for i in range(0, len(self.road_indices), 3):
            v1 = vec3(self.road_positions[self.road_indices[i]])
            v2 = vec3(self.road_positions[self.road_indices[i + 1]])
            v3 = vec3(self.road_positions[self.road_indices[i + 2]])

            for corner in car_corners:
                if point_in_triangle(corner, v1, v2, v3):
                    on_road = True
                    self.translation_vector.y = max(self.translation_vector.y, 0)  # Reset to ground level if above road
                    break
            if on_road:
                break

        if not on_road:
            self.start_falling()

    def start_falling(self):
        self.is_falling = True
        self.fall_start_time = glfw.get_time()

    def reset_position(self):
        self.is_falling = False
        self.translation_vector = glm.vec3(0, 0, 0)  # Reset to start position
        self.angleX = 0
        self.angleY = 0
        for key in self.keys:
            self.keys[key] = False

    def addWheel(self,wheel):
            self.wheels = self.wheels + [wheel]

    def key_handler(self, key, action):
        if action == glfw.PRESS:
            if key in self.keys:
                self.keys[key] = True
        elif action == glfw.RELEASE:
            if key in self.keys:
                self.keys[key] = False

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(2, self.buffers)
