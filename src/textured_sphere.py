import OpenGL.GL as GL

from sphere import Sphere


class TexturedSphere(Sphere):
    def __init__(self, shader, texture):
        super().__init__(shader)
        self.loc_diffuse_map = GL.glGetUniformLocation(shader.glid, 'diffuse_map')
        # setup texture and upload it to GPU
        self.texture = texture

    def draw(self, model, view, projection):

        GL.glUseProgram(self.shader.glid)
        # texture access setups
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(self.loc_diffuse_map, 0)
        super().draw(model, view, projection)

        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
