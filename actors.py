import random
import numpy as np
from constants import *
from utils import vec, distance

class Player:
    def __init__(self, walls):
        self.pos = vec(0, 0)
        self.dir = vec(0, 0)
        self.speed = PLAYER_MOVE_SPEED
        self.walls = walls

        self.lives = 3
        self.score = 0
        self.anim_timer = 0
        self.anim_frame = 0      

    def update_animation(self, dt):
        self.anim_timer += dt
        if self.anim_timer > 0.1:
            self.anim_timer = 0
            self.anim_frame = 1 - self.anim_frame
    def move(self, dt):
        next_pos = self.pos + self.dir * self.speed * dt

        if not self.collides(next_pos):
            self.pos = next_pos

        self.wrap()

    def wrap(self):
        if self.pos[0] < -SCREEN_WIDTH/2:
            self.pos[0] = SCREEN_WIDTH/2
        if self.pos[0] > SCREEN_WIDTH/2:
            self.pos[0] = -SCREEN_WIDTH/2
        if self.pos[1] < -SCREEN_HEIGHT/2:
            self.pos[1] = SCREEN_HEIGHT/2
        if self.pos[1] > SCREEN_HEIGHT/2:
            self.pos[1] = -SCREEN_HEIGHT/2

    def collides(self, pos):
        for w in self.walls:
            if distance(vec(*w), pos) < CELL_SIZE * 0.7:
                return True
        return False

    def set_dir(self, x, y):
        self.dir = vec(x, y)
    
    def get_angle(self):
        if self.dir[0] == 1:
            return 0
        elif self.dir[0] == -1:
            return 180
        elif self.dir[1] == 1:
            return 90
        elif self.dir[1] == -1:
            return 270
        return 0


class Enemy:
    def __init__(self, x, y, walls, player):
        self.pos = vec(x, y)
        self.dir = vec(1, 0)
        self.walls = walls
        self.player = player

    def move(self, dt):
        next_pos = self.pos + self.dir * ENEMY_MOVE_SPEED * dt

        if self.collides(next_pos):
            self.start_move()
        else:
            self.pos = next_pos

    def collides(self, pos):
        for w in self.walls:
            if distance(vec(*w), pos) < CELL_SIZE * 0.7:
                return True
        return False

    def start_move(self):
        dirs = [vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)]
        random.shuffle(dirs)
        for d in dirs:
            if not self.collides(self.pos + d * CELL_SIZE):
                self.dir = d
                return

    def go_after_player(self):
        if distance(self.pos, self.player.pos) < ENEMY_RADAR:
            diff = self.player.pos - self.pos
            if abs(diff[0]) > abs(diff[1]):
                self.dir = vec(np.sign(diff[0]), 0)
            else:
                self.dir = vec(0, np.sign(diff[1]))