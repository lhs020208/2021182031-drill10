from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Bird:
    image = None

    def __init__(self, x, y):
        if Bird.image == None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.dir = 1
        self.frame = 0
        self.framex, self.framey = 0, 0

    def draw(self):
        sizex = 918 // 5
        sizey = 506 // 5
        if self.dir == 1:
            self.image.clip_draw(self.framex * sizex, self.framey * sizey, sizex, sizey, self.x, self.y, 100, 50)
        else:
            self.image.clip_composite_draw(
            self.framex * sizex, self.framey * sizey, sizex, sizey,
            0, 'h',
            self.x, self.y,
            100, 50
        )
    def update(self):

        if self.x >= 700: self.dir = -1
        if self.x <= 100: self.dir = 1

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.framex, self.framey = self.find_frame_position(int(self.frame), 5, 3, 14)
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def find_frame_position(self, frame, w, h, max_frame):
        frame_index = frame

        self.framex = frame_index % w
        self.framey = frame_index // w

        total_rows = (max_frame + w - 1) // w  # Total rows in the sheet
        self.framey = total_rows - 1 - self.framey

        return self.framex, self.framey