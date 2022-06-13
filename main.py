import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os

BoxVAO, program = None, None
def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()

def init():
    global BoxVAO, program
    pygame.init()
    display = (920, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(.30, 1.0, 0.7, 1.0)
    glViewport(0, 0, 500, 500)
    vertexShaderContent=getFileContents("box.vertex.shader")
    fragmentShaderContent=getFileContents("box.fragment.shader")
    
    vertexShader=compileShader(vertexShaderContent,GL_VERTEX_SHADER)
    fragmentShader=compileShader(fragmentShaderContent,GL_FRAGMENT_SHADER)

    program=glCreateProgram()
  
    glAttachShader(program,vertexShader)
    glAttachShader(program,fragmentShader)
    glLinkProgram(program)

    vertexes=np.array([[0.5,0.0,0.0 ,   1.0,0.0,0.0],
                       [-0.5,0.0,0.0,   0.0,1.0,0.0],
                        [0,0.5,0.0,     0.0,0.0,1.0]],dtype=np.float32)
    

    vert=(      0.6, -0.6, -0.6,
                0.6, -0.6, -0.6,
                0.6,  0.6, -0.6,
                0.6,  0.6, -0.6,
                -0.6,  0.6, -0.6,
                -0.6, -0.6, -0.6,

                -0.6, -0.6,  0.6,
                0.6, -0.6,  0.6,
                0.6,  0.6,  0.6,
                0.6,  0.6,  0.6,
                -0.6,  0.6,  0.6,
                -0.6, -0.6,  0.6,

                -0.6,  0.6,  0.6,
                -0.6,  0.6, -0.6,
                -0.6, -0.6, -0.6,
                -0.6, -0.6, -0.6,
                -0.6, -0.6,  0.6,
                -0.6,  0.6,  0.6,

                    0.6,  0.6,  0.6,
                    0.6,  0.6, -0.6,
                    0.6, -0.6, -0.6,
                    0.6, -0.6, -0.6,
                    0.6, -0.6,  0.6,
                    0.6,  0.6,  0.6,

                -0.6, -0.6, -0.6,
                0.6, -0.6, -0.6,
                0.6, -0.6,  0.6,
                0.6, -0.6,  0.6,
                -0.6, -0.6,  0.6,
                -0.6, -0.6, -0.6,

                -0.6,  0.6, -0.6,
                0.6,  0.6, -0.6,
                0.6,  0.6,  0.6,
                0.6,  0.6,  0.6,
                -0.6,  0.6,  0.6,
                -0.6,  0.6, -0.6,)
    verts=np.array(vert,dtype=np.float32)

    
    triangleVBO=glGenBuffers(1)
    #glbindbuffer is used to bind VBO's name to a target buffer.
    glBindBuffer(GL_ARRAY_BUFFER,triangleVBO)

    glBufferData(GL_ARRAY_BUFFER,verts.nbytes,verts,GL_STATIC_DRAW)
    BoxVAO=glGenVertexArrays(1)
    glBindVertexArray(BoxVAO)
    positionLocation=glGetAttribLocation(program,"position")
    # colorLocation=glGetAttribLocation(program,"color")

    glVertexAttribPointer(positionLocation,3,GL_FLOAT,GL_FALSE,6*vertexes.itemsize,ctypes.c_void_p(0))
    glEnableVertexAttribArray(positionLocation)

    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,6*vertexes.itemsize,ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER,0)
    glBindVertexArray(0)

def draw():
    global BoxVAO, program
    glUseProgram(program)
    glBindVertexArray(BoxVAO)
    
    glDrawArrays(GL_TRIANGLES,0,3*6)
   
    glBindVertexArray(0)
    
def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT)
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()
