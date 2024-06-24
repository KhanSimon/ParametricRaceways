import OpenGL.GL as GL
import numpy as np
import glm
import glfw
import math
from shape import Shape



class Wheel(Shape):
    """Cylinder object"""


    def __init__(self, shader, transform= glm.identity(glm.mat4), height=0.25, radius=0.25, segments=20):
        super().__init__(shader)
        self.transform = transform
        # generate vertices
        vertices = []
        angle_increment = 2 * np.pi / segments

        for i in range(segments):
            angle = i * angle_increment
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append((x, height / 2, z))  # Top circle

        for i in range(segments):
            angle = i * angle_increment
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append((x, -height / 2, z))  # Bottom circle

        for i in range(segments):
            angle = i * angle_increment
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append((x, height / 2, z))    # Top circle
            vertices.append((x, -height / 2, z))   # Bottom circle

        # generate indices
        indices = []
        for i in range(1, segments - 1):
            indices.append(0)
            indices.append(i)
            indices.append(i + 1)

        start_index = segments
        for i in range(start_index + 1, start_index + segments - 1):
            indices.append(start_index)
            indices.append(i + 1)
            indices.append(i)

        for i in range(segments):
            next_i = (i + 1) % segments
            top_i = i
            bottom_i = i + segments
            next_top_i = next_i
            next_bottom_i = next_i + segments

            indices.append(top_i)
            indices.append(bottom_i)
            indices.append(next_top_i)

            indices.append(next_top_i)
            indices.append(bottom_i)
            indices.append(next_bottom_i)

        # convert to numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)
        # create vertex buffer
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)
        # create index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)
        self.num_indices = len(indices)

        #######
        self.translation_vector = glm.vec3(0, 0, 0)
        self.rotationAxe = glm.vec3(0, 1, 0)
        self.cylinderUP = glm.vec3(1, 0, 0)
        self.angle = 0
        #######



    def draw(self,model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)
        cylinder_transform = glm.rotate(self.angle, self.cylinderUP)
        model =  model @ self.transform @ cylinder_transform
        super().draw(model, view, projection)
        GL.glDrawElements(GL.GL_TRIANGLES, self.num_indices, GL.GL_UNSIGNED_INT, None)



    def draw2(self, model, car_transform, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)
        cylinder_transform = glm.rotate(self.angle, self.cylinderUP)
        model =  model @ car_transform @ self.transform @ cylinder_transform
        super().draw(model, view, projection)
        GL.glDrawElements(GL.GL_TRIANGLES, self.num_indices, GL.GL_UNSIGNED_INT, None)



    def key_handler(self,key):
        if key == glfw.KEY_LEFT :
            self.angle += 0.05
            if self.angle > 0.8 :self.angle = 0.8
        elif key == glfw.KEY_RIGHT :
            self.angle -= 0.05
            if self.angle < -0.8 :self.angle = -0.8






    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(2, self.buffers)
