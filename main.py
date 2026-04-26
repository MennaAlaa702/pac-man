import glfw
from OpenGL.GL import *
import time
import random
import pygame

from constants import *
from renderer import *
from maze import calculate_maze_data
from actors import Player, Enemy
from utils import vec, distance

def init_audio():
    pygame.mixer.init()
    sounds = {
        "eat": pygame.mixer.Sound("assets/eat.wav"),
        "death": pygame.mixer.Sound("assets/death.wav"),
        #"start": pygame.mixer.Sound("assets/start.wav"),
    }
    return sounds
def load_assets():
    load_texture("pacman", "assets/pacman.gif")
    load_texture("wall", "assets/wall.gif")
    load_texture("enemy", "assets/enemy.gif")
    #load_texture("pellet", "assets/pellet.png")
    load_texture("power", "assets/power.png")
def main():

    if not glfw.init():
        return

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man", None, None)
    glfw.make_context_current(window)

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

        # INPUT
        if glfw.get_key(window, glfw.KEY_RIGHT):
            player.set_dir(1,0)
        if glfw.get_key(window, glfw.KEY_LEFT):
            player.set_dir(-1,0)
        if glfw.get_key(window, glfw.KEY_UP):
            player.set_dir(0,1)
        if glfw.get_key(window, glfw.KEY_DOWN):
            player.set_dir(0,-1)

        # UPDATE
        player.move(dt)

        for e in enemies:
            e.move(dt)
            e.go_after_player()

            if distance(player.pos, e.pos) < CELL_SIZE/2:
                sounds["death"].play()
                player.lives -= 1
                player.pos = vec(*random.choice(pellets))

        # Pellet collision
        for p in pellets[:]:
            if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                sounds["eat"].play()
                pellets.remove(p)
                player.score += 2

        for p in power[:]:
            if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                sounds["eat"].play()
                power.remove(p)
                player.score += 50
                player.speed += 100

        # RENDER
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for w in walls:
            draw_texture("wall", w[0], w[1], CELL_SIZE, CELL_SIZE)

        for p in pellets:
            draw_texture("pellet", p[0], p[1], 10, 10)

        for p in power:
            draw_texture("power", p[0], p[1], 30, 30)

        # Pac-Man animation
        angle = player.get_angle()

        draw_texture_rotated(
            "pacman",
            player.pos[0],
            player.pos[1],
            CELL_SIZE,
            CELL_SIZE,
            angle
        )

        for e in enemies:
            draw_texture("enemy", e.pos[0], e.pos[1], CELL_SIZE, CELL_SIZE)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()