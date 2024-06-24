import OpenGL.GL as GL
import numpy as np

from shape import Shape
import outilsFonction


class Road(Shape):

    def __init__(self, shader, N, X, Y, booleanD, color=(1, 0, 0, 1) ):
        super().__init__(shader)

        self.color = np.array(color, dtype=np.float32)
        self.booleanD = booleanD

        offset = 0.5

        positions = self.getPositionsMatrice(N, X, Y, offset)
        positions = positions.astype(np.float32)

        indices = self.getIndicesVecteur(N)
        indices = indices.astype(np.uint32)

        self.positions = positions
        self.indices = indices

        # Remember indice count
        self.size = len(indices)

        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)

        self.buffers = GL.glGenBuffers(2)

        # Position attribute
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # Index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

    def getPositionsMatrice(self, N, x, y, delta): #delta représente la moitié de la largeur de la piste
        A = np.zeros((3, N))
        B = np.zeros((3, N))
        
        #x devient y
        A[0] = y - delta
        B[0] = y + delta
        #z devient - x 
        A[2] = -x
        B[2] = -x
        #y devient z (=0) , sauf si on veut du dénivelé : 
        if (self.booleanD == True):
            A[1] = outilsFonction.generationVecteurDenivele(N, 3)
            B[1] = outilsFonction.generationVecteurDenivele(N, 3)

        position = Road.interleave_columns(A,B)
        position_transposed = np.transpose(position)

        return position_transposed

    
    def getIndicesVecteur(self, N):
        if (N == 2): 
            return np.array([0,1,2,1,2,3])
        else : 
            return np.concatenate((self.getIndicesVecteur(N-1),np.array([2*N-4,2*N-3,2*N-2,2*N-3,2*N-2,2*N-1])))

         
    
    def interleave_columns(a, b):
    
        # On créer un tableau c pour accueillir le résultat final
        M, N = np.shape(a)
        c = np.empty((M, 2 * N)) 
        
        c[:, 0::2] = a  # Les collones avec des index pairs prennent les valeurs de a
        c[:, 1::2] = b  # Les collones avecdes index impairs prennent les valeurs de b
        
        return c

    def get_positions(self):
        return self.positions

    def get_indices(self):
        return self.indices
    
    def draw(self, model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)

        super().draw(model, view, projection)

        loc = GL.glGetUniformLocation(self.shader.glid, 'color')
        GL.glUniform4fv(loc, 1, self.color)

        GL.glDrawElements(GL.GL_TRIANGLES, self.size, GL.GL_UNSIGNED_INT, None)
