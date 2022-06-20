from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
import numpy as np

class Camera:
    def __init__(self):
        self.camera_Pos = np.array([0.0, 5.0, 3.0])
        self.camera_Up = np.array([0.0, 1.0, 0.0])
        self.camera_Frnt = np.array([0.0, 0.0, 0.0])
        self.camera_Rght = np.array([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.1
        self.pitch = 0
        self.jaw = -90


    def get_view_matrix(self):
        eye = np.asarray(self.camera_Pos)
        target = np.asarray(self.camera_Pos + self.camera_frnt)
        up = np.asarray(self.camera_up)

        forward = vector.normalize(target - eye)
        side = vector.normalize(np.cross(forward, up))
        up = vector.normalize(np.cross(side, forward))

        return np.array((
                (side[0], up[0], -forward[0], 0.),
                (side[1], up[1], -forward[1], 0.),
                (side[2], up[2], -forward[2], 0.),
                (-np.dot(side, eye), -np.dot(up, eye), np.dot(forward, eye), 1.0)
            ))
        # return matrix44.create_look_at(self.camera_Pos, self.camera_Pos + self.camera_frnt, self.camera_up)

    def process_mouse_movement(self, x_Offset, y_Offset):
        x_Offset *= self.mouse_sensitivity
        y_Offset *= self.mouse_sensitivity

        self.jaw += x_Offset
        self.pitch += y_Offset

        self.update_camera_vectors()

    def update_camera_vectors(self):
        frnt = np.array([0.0, 0.0, 0.0])
        frnt[0] = cos(radians(self.jaw)) * cos(radians(self.pitch))
        frnt[1] = sin(radians(self.pitch))
        frnt[2] = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_frnt = vector.normalise(frnt)
        self.camera_right = vector.normalise(vector3.cross(self.camera_frnt, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_frnt))

    #  camera for  movement
    def process_keyboard(self, drctn, vlcty):
        if drctn == "forward":
            self.camera_Pos += self.camera_frnt * vlcty
        if drctn == "backward":
            self.camera_Pos -= self.camera_frnt * vlcty
        if drctn == "left":
            self.camera_Pos -= self.camera_right * vlcty
        if drctn == "right":
            self.camera_Pos += self.camera_right * vlcty