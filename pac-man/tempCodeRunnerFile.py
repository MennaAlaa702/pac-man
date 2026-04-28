import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * # المصدر الأساسي للخطوط
import time
import random
import pygame
import math
from ctypes import c_void_p # الحل السحري اللي Python 3.13 طلبه في الإيرور

from constants import *
from renderer import *
from maze import calculate_maze_data
from actors import Player, Enemy
from utils import vec, distance

# --- متغير الحالة لفتح اللعبة ---
game_started = False 

# --- دوال رسم شاشة البداية (Start Screen) ---

def draw_text_clean(text, x, y):
    """رسم النص باستخدام خطوط GLUT مع حل مشكلة الـ ctypes"""
    glRasterPos2f(x, y)
    # رقم 2 هو المعرف الرقمي لخط GLUT_BITMAP_9_BY_15
    # بنحوله لـ c_void_p عشان الـ Traceback اللي ظهر عندك يختفي
    font = c_void_p(2) 
    for char in text:
        glutBitmapCharacter(font, ord(char))

def draw_circle_custom(x, y, radius, color, start_angle=0, end_angle=360):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    if end_angle < 360: glVertex2f(x, y)
    for i in range(start_angle, end_angle + 1):
        theta = math.radians(i)
        glVertex2f(x + radius * math.cos(theta), y + radius * math.sin(theta))
    glEnd()

def draw_ghost_custom(x, y, color):
    glColor3f(*color)
    glBegin(GL_POLYGON) # الرأس
    for i in range(0, 181):
        theta = math.radians(i)
        glVertex2f(x + 30 * math.cos(theta), y + 30 * math.sin(theta))
    glEnd()
    glBegin(GL_QUADS) # الجسم
    glVertex2f(x - 30, y); glVertex2f(x + 30, y)
    glVertex2f(x + 30, y - 35); glVertex2f(x - 30, y - 35)
    glEnd()
    draw_circle_custom(x - 12, y + 10, 6, (1, 1, 1)) # العيون
    draw_circle_custom(x + 12, y + 10, 6, (1, 1, 1))

def draw_my_start_screen():
    # 1. إطار النقط البيضاء (بناءً على أبعاد constants.py)
    glColor3f(1, 1, 1)
    glPointSize(3)
    glBegin(GL_POINTS)
    for x in range(int(-SCREEN_WIDTH/2 + 20), int(SCREEN_WIDTH/2 - 20), 30):
        glVertex2f(x, -SCREEN_HEIGHT/2 + 20); glVertex2f(x, SCREEN_HEIGHT/2 - 20)
    for y in range(int(-SCREEN_HEIGHT/2 + 20), int(SCREEN_HEIGHT/2 - 20), 30):
        glVertex2f(-SCREEN_WIDTH/2 + 20, y); glVertex2f(SCREEN_WIDTH/2 - 20, y)
    glEnd()

    # 2. العنوان الرئيسي (PAC MAN THE PROJECT)
    glColor3f(1, 0.8, 0)
    draw_text_clean("PAC MAN", -40, 200)
    draw_text_clean("THE PROJECT", -60, 160)

    # 3. الأشباح في الأركان
    draw_ghost_custom(-SCREEN_WIDTH/2 + 80, SCREEN_HEIGHT/2 - 100, (1, 0, 0))    # أحمر
    draw_ghost_custom(SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 100, (1, 0.7, 0.8)) # بينك
    draw_ghost_custom(-SCREEN_WIDTH/2 + 80, -SCREEN_HEIGHT/2 + 120, (0, 1, 1))   # لبني
    draw_ghost_custom(SCREEN_WIDTH/2 - 80, -SCREEN_HEIGHT/2 + 120, (1, 0.5, 0))  # برتقالي

    # 4. الزرار في السنتر (0,0)
    glColor3f(0, 0, 0); glRectf(-115, -45, 115, 45) # الظل
    glColor3f(0.1, 0.3, 0.7); glRectf(-110, -40, 110, 40) # الزرار الأساسي
    
    # 5. نص الزرار
    glColor3f(1, 1, 1)
    draw_text_clean("START GAME", -55, -8)

    # 6. باكمان الزينة الصغير
    draw_circle_custom(-160, 0, 25, (1, 1, 0), 35, 325)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(-125, 0); glVertex2f(-110, 0)
    glEnd()

# --- المنطق الأصلي لمشروع التيم ---

def init_audio():
    pygame.mixer.init()
    sounds = {
        "eat": pygame.mixer.Sound("assets/eat.wav"),
        "death": pygame.mixer.Sound("assets/death.wav"),
    }
    return sounds

def load_assets():
    load_texture("pacman", "assets/pacman.gif")
    load_texture("wall", "assets/wall.gif")
    load_texture("enemy", "assets/enemy.gif")
    load_texture("power", "assets/power.png")

def main():
    global game_started
    if not glfw.init():
        return

    # إنشاء النافذة بناءً على أبعاد constants.py
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man Project", None, None)
    glfw.make_context_current(window)
    
    # ضروري جداً لتفعيل وظائف النصوص من GLUT
    glutInit()

    setup_ortho()
    load_assets()
    sounds = init_audio()

    walls, pellets, power = calculate_maze_data()
    player = Player(walls)
    player.pos = vec(*random.choice(pellets))

    enemies = []
    for _ in range(ENEMY_NUMBER):
        x, y = random.choice(pellets)
        enemies.append(Enemy(x, y, walls, player))

    last_time = time.time()

    while not glfw.window_should_close(window):
        now = time.time()
        dt = now - last_time
        last_time = now

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if not game_started:
            # التحقق من الماوس بمكتبة GLFW
            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                x_pos, y_pos = glfw.get_cursor_pos(window)
                # فحص الضغط على الزرار (بناءً على أبعاد الشاشة 1000x850)
                if 390 < x_pos < 610 and 385 < y_pos < 465:
                    game_started = True
            
            draw_my_start_screen()
        
        else:
            # كود تحكم وحركة التيم
            if glfw.get_key(window, glfw.KEY_RIGHT): player.set_dir(1,0)
            if glfw.get_key(window, glfw.KEY_LEFT): player.set_dir(-1,0)
            if glfw.get_key(window, glfw.KEY_UP): player.set_dir(0,1)
            if glfw.get_key(window, glfw.KEY_DOWN): player.set_dir(0,-1)

            player.move(dt)
            for e in enemies:
                e.move(dt)
                e.go_after_player()
                if distance(player.pos, e.pos) < CELL_SIZE/2:
                    sounds["death"].play()
                    player.lives -= 1
                    player.pos = vec(*random.choice(pellets))

            for p in pellets[:]:
                if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                    sounds["eat"].play()
                    pellets.remove(p)
                    player.score += 2

            # رسم المتاهة والشخصيات (كود التيم)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            for w in walls: draw_texture("wall", w[0], w[1], CELL_SIZE, CELL_SIZE)
            for p in pellets: draw_texture("pellet", p[0], p[1], 10, 10)
            for p in power: draw_texture("power", p[0], p[1], 30, 30)
            
            angle = player.get_angle()
            draw_texture_rotated("pacman", player.pos[0], player.pos[1], 25, 25, angle)
            for e in enemies: draw_texture("enemy", e.pos[0], e.pos[1], CELL_SIZE, CELL_SIZE)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()