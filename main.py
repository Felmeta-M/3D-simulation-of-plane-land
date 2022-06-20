
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
# import transform
from PIL import Image
from pywavefront import Wavefront
import pyrr
import pywavefront
from texture_loader import *

vao, program, texture = None, None, None
from camera import Camera
cam = Camera()
lst_X, lst_Y = 1000 / 2, 800 / 2
frst_mouse = True

def mouse_lk(x_pos, y_pos):
    global frst_mouse, lst_X, lst_Y

    if frst_mouse:
        lst_X = x_pos
        lst_Y = y_pos
        frst_mouse = False

    x_off_set = x_pos - lst_X
    y_off_set = lst_Y - y_pos

    lst_X = x_pos
    lst_Y = y_pos
    cam.process_mouse_movement(x_off_set, y_off_set)

pyrr.matrix44.create_look_at(
            (47.697, -8.147, 24.498),
            (0.0, 0.0, 8.0),
            (0.0, 0.0, 1.0),
        )

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()
    
    
def init():
    global vao, program, texture, proj, tran, view, vertexes, tran2, ground
    pygame.init()
    display = (1500, 1500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(.30, 0.20, 0.20, 1.0)
    glViewport(0, 0, 1500,1500)

    vertexShader = compileShader(getFileContents(
        "vertex.shader"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents(
        "fragment.shader"), GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)
    # vertexes = np.array([
    #     # position          # color           # texture s, r
    #     # [0.5, 0.5, -.50,    1.0, 0.20, 0.8,  1.0, 1.0],
    #     # [0.5, -0.5, -.50,   1.0, 1.0, 0.0,   1.0, 0.0],
    #     # [-0.5, 0.5, -.50,   0.0, 0.7, 0.2,   0.0, 1.0],

    #     # [0.5, -0.5, -.50,   1.0, 1.0, 0.0,   1.0, 0.0],
    #     # [-0.5, -0.5, -.50,  0.0, 0.4, 1.0,   0.0, 0.0],
    #     # [-0.5, 0.5, -.50,   0.0, 0.7, 0.2,   0.0, 1.0],

    # ], dtype=np.float32)
    wav = Wavefront("airplane.obj", collect_faces=True , create_materials=True)
    for name,material in wav.materials.items():
        print(material.vertex_format)
        print(material.vertex_format)
    
        vertexes = np.array(material.vertices,dtype=np.float32)
        break
    wav2 = Wavefront("ground.obj", collect_faces=True)
    for name,material in wav2.materials.items():
        # print(material.vertex_format)
        ground = np.array(material.vertices,dtype=np.float32)
        break
    print(vertexes)
    proj = pyrr.matrix44.create_perspective_projection(45.0, 1, 0.1, 1000.0)

    view = pyrr.matrix44.create_look_at(
        (50,0,100),
            (0.0, 0.0, 0.0),
            (0.0, 1.0, .0))


    vao = glGenVertexArrays(2)
    vbo = glGenBuffers(2)

    #airplane vtx buffersssssssssssssssssssssssssssssss
    tran = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,0]))
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)
    glBindVertexArray(vao[0])

    texLocation = glGetAttribLocation(program, "textCoord")
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize,
    ctypes.c_void_p(0))
    glEnableVertexAttribArray(texLocation)

    colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(2*vertexes.itemsize))
    glEnableVertexAttribArray(1)

    position_location = glGetAttribLocation(program, "position")
    glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(5*vertexes.itemsize))
    glEnableVertexAttribArray(position_location)


    #ground vtx buffer
    tran2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,0]))
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, ground.nbytes, ground, GL_STATIC_DRAW)

    glBindVertexArray(vao[1])

    texLocation = glGetAttribLocation(program, "textCoord")
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE,
                          8 * ground.itemsize,
    ctypes.c_void_p(0))
    glEnableVertexAttribArray(texLocation)

    colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          8 * ground.itemsize, ctypes.c_void_p(2*ground.itemsize))
    glEnableVertexAttribArray(1)

    position_location = glGetAttribLocation(program, "position")
    glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE,
                          8 * ground.itemsize, ctypes.c_void_p(5*ground.itemsize))
    glEnableVertexAttribArray(position_location)

    texture = glGenTextures(2)
    txloader("color.png", texture[0])
    txloader("gorund.png", texture[1])

    glGenerateMipmap(GL_TEXTURE_2D)

    

    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # unbind VAO
    glBindVertexArray(0)

    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

i=0
def draw():
    global vao, program, texture, tran,i
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    view_loc = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, cam.get_view_matrix())
    view_loc = glGetUniformLocation(program, "projection")
    print(tran)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, proj)
    view_loc = glGetUniformLocation(program, "transform")
    tran = pyrr.matrix44.create_from_translation([0,i,0])
    glUniformMatrix4fv(view_loc, 1, GL_TRUE, tran)
    i+=2


    glBindVertexArray(vao[1])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glDrawArrays(GL_TRIANGLES, 0, len(ground)//8)

    glBindVertexArray(vao[0])

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, tran2)
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glDrawArrays(GL_TRIANGLES, 0, len(vertexes)//8)



    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            

            keys_clicked = pygame.key.get_pressed()
            if keys_clicked[pygame.K_a]:
                cam.process_keyboard("left", 0.08)
            if keys_clicked[pygame.K_d]:
                cam.process_keyboard("right", 0.08)
            if keys_clicked[pygame.K_w]:
                cam.process_keyboard("forward", 0.8)
            if keys_clicked[pygame.K_s]:
                cam.process_keyboard("backward", 0.8)

            mouse_pos = pygame.mouse.get_pos()
            mouse_lk(mouse_pos[0], mouse_pos[1])

            # look around 360 degrees, still not perfect
            if mouse_pos[0] <= 0:
                pygame.mouse.set_pos((1279, mouse_pos[1]))
            elif mouse_pos[0] >= 1279:
                pygame.mouse.set_pos((0, mouse_pos[1]))

            ct = pygame.time.get_ticks() / 1000

        draw()
        pygame.display.flip()
        pygame.time.wait(10)



main()