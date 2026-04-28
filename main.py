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
    pygame.font.init()
    sounds = {
        "eat": pygame.mixer.Sound("assets/eat.wav"),
        "death": pygame.mixer.Sound("assets/death.wav"),
        # "start": pygame.mixer.Sound("assets/start.wav"),
        "game_over": pygame.mixer.Sound("assets/game-over-sound.wav"), 
        "win":pygame.mixer.Sound("assets/winning-sound.wav")
    }
    return sounds


def load_assets():
    load_texture("pacman", "assets/pacman.gif")
    load_texture("wall", "assets/wall.gif")
    # load_texture("enemy", "assets/enemy.gif")
    #load_texture("pellet", "assets/pellet.png")
    load_texture("power", "assets/power.png")
    load_texture("game_over_ui", "assets/game-over-img.png")
    load_texture("win_ui","assets/winning-img.png")
    load_texture("enemy_red", "assets/enemy-red.png")    
    load_texture("enemy_blue", "assets/enemy-blue.png")   
    load_texture("enemy_purple", "assets/enemy-pink.png")  
    load_texture("heart_red", "assets/heart.png")   
    load_texture("heart_broken", "assets/broken-heart.png")

def get_safe_pos(target_pos, positions_list, min_dist):
    # نختار فقط النقاط التي تبعد عن الهدف أكثر من المسافة المحددة
    safe_choices = [p for p in positions_list if distance(target_pos, vec(*p)) > min_dist]
    return vec(*random.choice(safe_choices if safe_choices else positions_list))

def draw_text(window, text, x, y, size=30):
    try:
        font = pygame.font.SysFont("Impact", size) 
    except:
        font = pygame.font.SysFont("Arial", size, bold=True)

    text_surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y - height)
    glTexCoord2f(1, 0); glVertex2f(x + width, y - height)
    glTexCoord2f(1, 1); glVertex2f(x + width, y)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDeleteTextures(1, [tex])

def draw_retry_button():
    # رسم مستطيل الزر (خلفية زرقاء)
    glColor3f(0.1, 0.3, 0.7)
    glRectf(-110, -320, 110, -240) # وضعته في الأسفل تحت نص الـ Score
    
    # رسم كلمة RETRY باللون الأبيض
    glColor3f(1, 1, 1)
    # ملاحظة: سنستخدم دالة draw_text التي عرفناها سابقاً
    # تأكدي من إحداثيات النص ليكون فوق الزر
    draw_text(None, "RETRY", -45, -270, 35)


def show_win_screen(window, score):
    """شاشة الفوز"""
    try:
        font = pygame.font.SysFont("Impact", 65) 
    except:
        font = pygame.font.SysFont("Arial", 65, bold=True)

    text_surface = font.render(f"Final Score: {score}", True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    text_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # رسم الخلفية
        draw_texture("win_ui", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) 
        
        # رسم نص النتيجة
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, text_texture)
        
        glBegin(GL_QUADS)
        half_w, half_h = width / 2, height / 2
        y_text_offset = -200  
        glTexCoord2f(0, 0); glVertex2f(-half_w, y_text_offset - half_h)
        glTexCoord2f(1, 0); glVertex2f(half_w, y_text_offset - half_h)
        glTexCoord2f(1, 1); glVertex2f(half_w, y_text_offset + half_h)
        glTexCoord2f(0, 1); glVertex2f(-half_w, y_text_offset + half_h)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        # استدعاء الزر
        draw_retry_button()

        # فحص الضغط على الزر
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
            mouse_x, mouse_y = glfw.get_cursor_pos(window)
            # الإحداثيات المتوافقة مع مكان الزر في الأسفل
            if (SCREEN_WIDTH/2 - 120) < mouse_x < (SCREEN_WIDTH/2 + 120) and \
               (SCREEN_HEIGHT/2 + 150) < mouse_y < (SCREEN_HEIGHT/2 + 220):
                return "RESTART"

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteTextures(1, [text_texture])


def show_game_over_screen(window, score):
    """شاشة الخسارة"""
    try:
        font = pygame.font.SysFont("Impact", 65) 
    except:
        font = pygame.font.SysFont("Arial", 65, bold=True)

    text_surface = font.render(f"Final Score: {score}", True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    text_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # رسم خلفية جيم أوفر
        draw_texture("game_over_ui", 0, 50, SCREEN_WIDTH, 1000) 
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, text_texture)
        
        glBegin(GL_QUADS)
        half_w, half_h = width / 2, height / 2
        y_text_offset = -50 
        glTexCoord2f(0, 0); glVertex2f(-half_w, y_text_offset - half_h)
        glTexCoord2f(1, 0); glVertex2f(half_w, y_text_offset - half_h)
        glTexCoord2f(1, 1); glVertex2f(half_w, y_text_offset + half_h)
        glTexCoord2f(0, 1); glVertex2f(-half_w, y_text_offset + half_h)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        # استدعاء الزر
        draw_retry_button()

        # فحص الضغط على الزر
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
            mouse_x, mouse_y = glfw.get_cursor_pos(window)
            if (SCREEN_WIDTH/2 - 120) < mouse_x < (SCREEN_WIDTH/2 + 120) and \
               (SCREEN_HEIGHT/2 + 150) < mouse_y < (SCREEN_HEIGHT/2 + 220):
                return "RESTART"

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteTextures(1, [text_texture])


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
   # نضع اللاعب أولاً
    player.pos = vec(*random.choice(pellets))
    
    # نضع الأشباح بعيداً عنه بمسافة 300 بيكسل مثلاً
    enemies = []
    for _ in range(ENEMY_NUMBER):
        start_p = get_safe_pos(player.pos, pellets, 300)
        enemies.append(Enemy(start_p[0], start_p[1], walls, player))
    last_time = time.time()


    while not glfw.window_should_close(window):
        now = time.time()
        dt = now - last_time
        last_time = now

        glfw.poll_events()

        # INPUT
        if glfw.get_key(window, glfw.KEY_RIGHT):
            player.set_dir(1,0)
        elif glfw.get_key(window, glfw.KEY_LEFT):
            player.set_dir(-1,0)
        elif glfw.get_key(window, glfw.KEY_UP):
            player.set_dir(0,1)
        elif glfw.get_key(window, glfw.KEY_DOWN):
            player.set_dir(0,-1)

        #UPDATE
        
        player.move(dt)

        win_margin = 10  # قللت المسافة شوية عشان يلقط الفوز بسرعة
        if abs(player.pos[0]) > (SCREEN_WIDTH/2 - win_margin) or \
           abs(player.pos[1]) > (SCREEN_HEIGHT/2 - win_margin):
            
            # نوقف اللاعب مكانه عشان ميفضلش يتحرك بره الشاشة
            player.set_dir(0, 0) 
            
            if "win" in sounds:
                sounds["win"].play()
            
            # إظهار شاشة الفوز
            show_win_screen(window, player.score)
            
            # نقفل اللعبة بعد ما الشاشة تخلص
            glfw.set_window_should_close(window, True)
            break
        
        for e in enemies:
            e.move(dt)
            e.go_after_player()

            if distance(player.pos, e.pos) < CELL_SIZE/2:
                sounds["death"].play()
                player.lives -= 1

                if player.lives <= 0:
                    sounds["game_over"].play()
                    show_game_over_screen(window, player.score)
                    glfw.set_window_should_close(window, True)
                    break
                else:
                    # عند العودة للحياة (Respawn)
                    # 1. نختار مكان جديد للاعب
                    player.pos = vec(*random.choice(pellets))
                    # 2. نبعد كل الأشباح عن مكان اللاعب الجديد فوراً
                    for enemy_to_reset in enemies:
                        enemy_to_reset.pos = get_safe_pos(player.pos, pellets, 300)
                break

        for p in pellets[:]:
            if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                sounds["eat"].play()
                pellets.remove(p)
                player.score += 2
        
        for p in power[:]:
            if distance(player.pos, vec(*p)) < CELL_SIZE/2:
                sounds["eat"].play()
                power.remove(p)
                player.score += 20
                player.speed += 40


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

        for i, e in enumerate(enemies):
            enemy_skins = ["enemy_red", "enemy_blue", "enemy_purple"]
            current_skin = enemy_skins[i % len(enemy_skins)]
            
            if current_skin == "enemy_red":
                draw_texture(current_skin, e.pos[0], e.pos[1], 45, 35)
            else:
                draw_texture(current_skin, e.pos[0], e.pos[1], 35, 35)

        angle = player.get_angle()
        draw_texture_rotated(
            "pacman",
            player.pos[0],
            player.pos[1],
            26,
            26,
            angle
        )

        glDisable(GL_BLEND) 

# ... (بعد رسم باك مان والأشباح) ...

        # --- RENDER UI (داخل منطقة الـ Blend) ---
        glLoadIdentity()
        
        # 1. رسم عداد النقاط
        draw_text(window, f"Score: {player.score}", -SCREEN_WIDTH/2 + 20, SCREEN_HEIGHT/2 - 20, 35)

        # 2. رسم القلوب
       # 2. رسم القلوب
        max_lives = 5 
        heart_size = 30
        start_x = SCREEN_WIDTH/2 - 220 
        y_pos = SCREEN_HEIGHT/2 - 40

        for i in range(max_lives):
            # التأكد أن الاسم "heart_broken" مطابق تماماً لـ load_assets
            heart_type = "heart_red" if i < player.lives else "heart_broken"
            
            draw_texture(
                heart_type, 
                start_x + (i * (heart_size + 10)), 
                y_pos, 
                heart_size, 
                heart_size
            )

        glDisable(GL_BLEND) # نقفل الـ Blend هنا في الآخر خالص

        glfw.swap_buffers(window)
        time.sleep(0.01)

    glfw.terminate()

if __name__ == "__main__":
    main()