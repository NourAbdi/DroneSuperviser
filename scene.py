import cv2
from object_3d import *
from camera import *
from projection import *
import pygame as pg

delay = 10000
num_frame = 100
N = 1
k = 50


class SoftwareRender:
    def __init__(self, drones):
        self.frame_count = 0
        self.count = 0
        self.drones = drones
        self.frame = 1
        self.world_axes = Axes
        self.obj_arrow = Arrow
        self.obj = None
        self.objects = []
        self.projection = None
        self.camera = None
        self.IMGFlag = False
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 900, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def get_objects(self, is_next, drone_color, arrow_color):
        if is_next:
            for drone in self.drones:
                self.obj_arrow = Arrow(self)
                self.obj_arrow.take_position(drone.alpha[self.frame])
                self.obj_arrow.scale(100)
                self.obj_arrow.translate(drone.position[self.frame])
                self.obj_arrow.draw_color = True
                self.obj_arrow.color = pg.Color(arrow_color)
                self.obj = self.get_object_from_file('cube.obj')
                self.obj.name = drone.name
                self.obj.draw_color = True
                self.obj.color = pg.Color(drone_color)
                self.obj.draw_name = True
                # self.obj.draw_normals = False
                # self.obj.normal = (0, drone.alpha[self.frame], 0)
                self.obj.translate(drone.position[self.frame])
                # self.obj.rotate_y(drone.alpha[self.frame])
                self.objects.append(self.obj)
                self.objects.append(self.obj_arrow)
        else:
            for drone in self.drones:
                self.obj_arrow = Arrow(self)
                self.obj_arrow.take_position(drone.alpha[self.frame - 1])
                self.obj_arrow.scale(100)
                self.obj_arrow.translate(drone.position[self.frame - 1])
                self.obj_arrow.draw_color = True
                self.obj_arrow.color = pg.Color('red')
                self.obj = self.get_object_from_file('cube.obj')
                self.obj.name = drone.name
                self.obj.draw_color = True
                self.obj.color = pg.Color('blue')
                self.obj.draw_name = True
                # self.obj.draw_normals = False
                # self.obj.normal = (0, drone.alpha[self.frame-1], 0)
                self.obj.translate(drone.position[self.frame - 1])
                # self.obj.rotate_y(drone.alpha[self.frame - 1])
                self.objects.append(self.obj)
                self.objects.append(self.obj_arrow)

    def create_objects(self):
        self.camera = Camera(self, [-100, 100, -100])
        self.projection = Projection(self)
        self.world_axes = Axes(self)
        self.world_axes.scale(100)

        self.get_objects(False, 'red', 'blue')
        if num_frame - self.frame > 1:
            self.get_objects(True, 'orange', 'green')

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.world_axes.draw()
        for obj in self.objects:
            obj.draw()

    def replace_drones(self):
        self.objects.clear()
        self.get_objects(False, 'red', 'blue')
        if num_frame - self.frame > 1:
            self.get_objects(True, 'orange', 'green')

    def slice_pics(self):
        imgs = []
        img = None
        cv2.namedWindow("imgs", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("imgs", self.WIDTH, self.HEIGHT)
        if not self.IMGFlag:
            for drone in self.drones:
                try:
                    imgs.append(drone.videoCaps[self.frame - 1])
                except:
                    return
            if N == 1:
                img = imgs[0]
            elif N == 2:
                img = np.concatenate((imgs[0], imgs[1]), axis=0)
            elif N == 3:
                img = np.concatenate((imgs[0], imgs[1], imgs[2]), axis=0)
            elif N == 4:
                img = np.concatenate(((np.concatenate((imgs[0], imgs[1]), axis=1)),
                                      (np.concatenate((imgs[2], imgs[3]), axis=1))), axis=0)
            self.IMGFlag = True
        if imgs:
            cv2.imshow('imgs', img)

    def run(self):

        while True:

            self.draw()
            self.control_frame()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]

            pg.display.set_caption(
                'frame :' + str(self.frame) + ' ,time : ' + str(
                    pg.time.get_ticks() - self.count * k + self.frame_count * delay))
            pg.display.flip()
            # self.clock.tick(self.FPS)
            self.slice_pics()

            if pg.time.get_ticks() - self.count * k + self.frame_count * delay > delay * self.frame:
                self.frame += 1
                self.IMGFlag = False
                self.replace_drones()
            if self.frame > num_frame:
                break

    def control_frame(self):
        key = pg.key.get_pressed()
        if key[pg.K_j]:
            if self.frame > 1:
                self.frame -= 1
                self.frame_count -= 1
                self.IMGFlag = False
                self.replace_drones()
        if key[pg.K_k]:
            self.count += 1
            # pg.time.wait(k)
            pg.time.delay(k)
            # self.clock.tick(2000)
            # timer_active = False
        if key[pg.K_l]:
            if self.frame < num_frame:
                self.frame += 1
                self.frame_count += 1
                self.IMGFlag = False
                self.replace_drones()
