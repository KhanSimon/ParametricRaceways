import OpenGL.GL as GL
import numpy as np
import math

from shape import Shape


class Sphere(Shape):
    def __init__(self, shader, sector_count=36, stack_count=36):
        super().__init__(shader)

        self.sector_count = sector_count
        self.stack_count = stack_count

        self.vertices = []
        self.normals = []
        self.indices = []

        self.__build_vertices()
        self.__build_indices()

        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)

        self.buffers = GL.glGenBuffers(3)

        # position attribute
        GL.glEnableVertexAttribArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, np.array(self.vertices, dtype=np.float32), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)

        # normal attribute
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, np.array(self.normals, dtype=np.float32), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)

        # index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[2])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, np.array(self.indices, dtype=np.uint32), GL.GL_STATIC_DRAW)

    def __build_vertices(self):
        # Clear the vertex list
        self.vertices.clear()
        self.normals.clear()

        radius = 0.5
        x, y, z = 0, 0, 0

        sector_step = 2 * math.pi / self.sector_count
        stack_step = math.pi / self.stack_count

        for i in range(self.stack_count + 1):
            stack_angle = math.pi / 2 - i * stack_step
            xy = radius * math.cos(stack_angle)
            z = radius * math.sin(stack_angle)

            for j in range(self.sector_count + 1):
                sector_angle = j * sector_step
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                vertex = [x, y, z]
                normal = np.array(vertex, dtype=np.float32)
                normal /= np.linalg.norm(normal)
                self.vertices.append(vertex)
                self.normals.append(normal)

    def __build_indices(self):
        # Clear the index list
        self.indices.clear()

        k1, k2 = 0, 0

        for i in range(self.stack_count):
            k1 = i * (self.sector_count + 1)
            k2 = k1 + self.sector_count + 1

            for j in range(self.sector_count):
                if i != 0:
                    self.indices.append(k1)
                    self.indices.append(k2)
                    self.indices.append(k1 + 1)

                if i != (self.stack_count - 1):
                    self.indices.append(k1 + 1)
                    self.indices.append(k2)
                    self.indices.append(k2 + 1)

                k1 += 1
                k2 += 1

    def draw(self, model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)
        super().draw(model, view, projection)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)
