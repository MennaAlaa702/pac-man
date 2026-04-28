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

pygame.font.init()

def init_audio():
    pygame.mixer.init()
    sounds = {
        "eat": pygame.mixer.Sound("D:/IT/3rd year/SECOUND TERM/IT354 COMPUTER GRAPHICS/PROJECT/assets/eat.wav"),
        "death": pygame.mixer.Sound("D:/IT/3rd year/SECOUND TERM/IT354 COMPUTER GRAPHICS/PROJECT/assets/death.wav"),
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
    # حالات اللعبة
    GAME_START = 0
    GAME_PLAYING = 1
    GAME_WIN = 2
    game_state = GAME_START

    start_timer = 3.0  # مؤقت البداية
    popup_timer = 0    # مؤقت رسالة الـ +20
    show_popup = False

    if not glfw.init():
        return

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man", None, None)
    glfw.make_context_current(window)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
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

        # --- 1. UPDATE LOGIC ---
        if game_state == GAME_START:
            start_timer -= dt
            if start_timer <= 0:
                game_state = GAME_PLAYING

        elif game_state == GAME_PLAYING:
            # INPUT
            if glfw.get_key(window, glfw.KEY_RIGHT): player.set_dir(1,0)
            if glfw.get_key(window, glfw.KEY_LEFT):  player.set_dir(-1,0)
            if glfw.get_key(window, glfw.KEY_UP):    player.set_dir(0,1)
            if glfw.get_key(window, glfw.KEY_DOWN):  player.set_dir(0,-1)

            # MOVE
            player.move(dt)
            for e in enemies:
                e.move(dt)
                e.go_after_player()
                if distance(player.pos, e.pos) < CELL_SIZE/2:
                    sounds["death"].play()
                    player.lives -= 1
                    player.pos = vec(*random.choice(pellets))

            # Pellets
            for p in pellets[:]:
                if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                    sounds["eat"].play()
                    pellets.remove(p)
                    player.score += 2

            # Power (الكورة الصفراء)
            for p in power[:]:
                if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                    sounds["eat"].play()
                    power.remove(p)
                    player.score += 20 # خليتها 20 زي ما طلبتي في الرسالة
                    show_popup = True
                    popup_timer = 1.5

            # WIN CHECK
            if len(pellets) == 0:
                game_state = GAME_WIN

        elif game_state == GAME_WIN:
            # إعادة اللعب عند الضغط
            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                main() # إعادة تشغيل الدالة
                return # نخرج من النسخة الحالية

        # --- 2. RENDER ---
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if game_state == GAME_START:
            draw_text("START GAME", 0, 0, size=70)
            draw_text(f"Starting in {int(start_timer) + 1}...", 0, -60, size=30)

        elif game_state == GAME_PLAYING:
            for w in walls: draw_texture("wall", w[0], w[1], CELL_SIZE, CELL_SIZE)
            for p in pellets: draw_texture("pellet", p[0], p[1], 10, 10)
            for p in power: draw_texture("power", p[0], p[1], 30, 30)

            angle = player.get_angle()
            draw_texture_rotated("pacman", player.pos[0], player.pos[1], 25, 25, angle)
            for e in enemies: draw_texture("enemy", e.pos[0], e.pos[1], CELL_SIZE, CELL_SIZE)
            
            # تحديث وقت الـ Popup
            if show_popup:
                draw_text("+20 SCORE!", player.pos[0], player.pos[1] + 40, size=24, color=(255, 255, 0))
                popup_timer -= dt
                if popup_timer <= 0:
                    show_popup = False

        elif game_state == GAME_WIN:
            draw_text("YOU WIN!", 0, 100, size=80, color=(0, 255, 0))
            draw_text(f"Score: {player.score}", 0, 0, size=40)
            draw_text("Press anywhere to play again", 0, -100, size=30)

        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()
