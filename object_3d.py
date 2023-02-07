import pygame as pg
from matrix_functions import *


class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render
        self.vertices = np.array([np.array(v) for v in vertices])
        self.faces = np.array([np.array(face) for face in faces])
        self.font = pg.font.SysFont('Arial', 20, bold=False)
        self.color = pg.Color('orange')
        self.color_faces = [(self.color, face) for face in self.faces]
        self.draw_name = False
        self.draw_vertices = False
        # self.draw_normals = False
        self.draw_color = False
        # self.normal = None
        self.name = ''
        self.label = ''

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        if self.draw_color:
            self.color_faces = [(self.color, face) for face in self.faces]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

        if self.draw_name:
            text = self.font.render(self.name, True, pg.Color('white'))
            self.render.screen.blit(text, vertices[0])

        # if self.draw_normals:
        #     pg.draw.line(self.render.screen, pg.Color('white'), vertices[0], vertices[0] - self.normal, 1)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = True
        self.label = 'XYZ'


class Arrow(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1)])
        self.faces = np.array([(0, 1)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = True
        # self.label = '>'

    def take_position(self, alpha):
        self.vertices = np.array([(0, 0, 0, 1), (0, alpha, 0, 1)])
