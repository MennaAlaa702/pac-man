from OpenGL.GL import *
import glfw
from numpy import cos, sin
from constants import *
from PIL import Image
import pygame
import colorsys
textures = {}

def load_texture(name, path):
    try:
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     image.width, image.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        textures[name] = tex_id
    except:
        textures[name] = None
        
def setup_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-SCREEN_WIDTH/2, SCREEN_WIDTH/2,
            -SCREEN_HEIGHT/2, SCREEN_HEIGHT/2,
            -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_rect(x, y, w, h, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x - w/2, y - h/2)
    glVertex2f(x + w/2, y - h/2)
    glVertex2f(x + w/2, y + h/2)
    glVertex2f(x - w/2, y + h/2)
    glEnd()

def draw_texture(name, x, y, w, h):
    tex = textures.get(name)

    if tex is None:
        draw_rect(x, y, w, h, (1, 1, 1))
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)

    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0, 0); glVertex2f(x - w/2, y - h/2)
    glTexCoord2f(1, 0); glVertex2f(x + w/2, y - h/2)
    glTexCoord2f(1, 1); glVertex2f(x + w/2, y + h/2)
    glTexCoord2f(0, 1); glVertex2f(x - w/2, y + h/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
def draw_texture_rotated(name, x, y, w, h, angle):
    tex = textures.get(name)

    if tex is None:
        draw_rect(x, y, w, h, (1,1,0))
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)

    glPushMatrix()

    # Move to position
    glTranslatef(x, y, 0)

    # Rotate
    glRotatef(angle, 0, 0, 1)

    # Draw centered quad
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0, 0); glVertex2f(-w/2, -h/2)
    glTexCoord2f(1, 0); glVertex2f(w/2, -h/2)
    glTexCoord2f(1, 1); glVertex2f(w/2, h/2)
    glTexCoord2f(0, 1); glVertex2f(-w/2, h/2)
    glEnd()

    glPopMatrix()

    glDisable(GL_TEXTURE_2D)

    
def draw_text(text, x, y, size=30):
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



def show_win_screen(window, score):
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

    # زر RESTART بألوان زرقاء
    retry_btn = Button3D(0, -280, 220, 60, "RESTART", 
                         front_color=(1/255.0, 1/255.0, 1/255.0), # الواجهة باللون #010101
                         edge_color=(30/255.0, 30/255.0, 30/255.0),              # الحافة باللون الأسود الخالص
                         text_offset_x=-50) # عدلي الرقم ده حسب طول الكلمة # تقدري تغيري الرقم ده عشان تظبطي الكلمة يمين أو شمال

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        draw_texture("win_ui", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT-50)         
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, text_texture)
        
        glBegin(GL_TRIANGLE_FAN)
        half_w, half_h = width / 2, height / 2
        y_text_offset = -150  
        glTexCoord2f(0, 0); glVertex2f(-half_w, y_text_offset - half_h)
        glTexCoord2f(1, 0); glVertex2f(half_w, y_text_offset - half_h)
        glTexCoord2f(1, 1); glVertex2f(half_w, y_text_offset + half_h)
        glTexCoord2f(0, 1); glVertex2f(-half_w, y_text_offset + half_h)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        # --- التعامل مع الزر الجديد ---
        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        is_pressed = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        
        retry_btn.update(mouse_x, mouse_y, is_pressed)
        retry_btn.draw()

        # لو الماوس فوق الزر وتم الضغط (وبعدها رفعنا إيدنا لتجنب التكرار)
        if retry_btn.state == "pressed":
            return "RESTART"

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteTextures(1, [text_texture])

def show_game_over_screen(window, score):
  
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

    # زر TRY AGAIN باللون #13100a
    retry_btn = Button3D(0, -250, 220, 60, "TRY AGAIN!", 
                         front_color=(19/255.0, 16/255.0, 10/255.0), 
                         edge_color=(10/255.0, 8/255.0, 5/255.0),
                         text_offset_x=-65) # تقدري تغيري الرقم ده عشان تظبطي الكلمة يمين أو شمال

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        draw_texture("game_over_ui", 0, 50, SCREEN_WIDTH, 1000) 
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, text_texture)
        
        glBegin(GL_TRIANGLE_FAN)
        half_w, half_h = width / 2, height / 2
        y_text_offset = -80 
        glTexCoord2f(0, 0); glVertex2f(-half_w, y_text_offset - half_h)
        glTexCoord2f(1, 0); glVertex2f(half_w, y_text_offset - half_h)
        glTexCoord2f(1, 1); glVertex2f(half_w, y_text_offset + half_h)
        glTexCoord2f(0, 1); glVertex2f(-half_w, y_text_offset + half_h)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        # --- التعامل مع الزر الجديد ---
        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        is_pressed = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        
        retry_btn.update(mouse_x, mouse_y, is_pressed)
        retry_btn.draw()

        if retry_btn.state == "pressed":
            return "RESTART"

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteTextures(1, [text_texture])

class Button3D:
    # ضفنا الألوان، وضفنا text_offset_x عشان نظبط النص في النص يدوياً
    def __init__(self, x, y, w, h, text, front_color, edge_color, text_offset_x):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.front_color = front_color
        self.edge_color = edge_color
        self.text_offset_x = text_offset_x
        self.state = "normal"
        
    def update(self, mouse_x, mouse_y, is_pressed):
        mx = mouse_x - SCREEN_WIDTH / 2
        my = SCREEN_HEIGHT / 2 - mouse_y
        
        if (self.x - self.w/2 <= mx <= self.x + self.w/2) and \
           (self.y - self.h/2 <= my <= self.y + self.h/2):
            if is_pressed:
                self.state = "pressed"
            else:
                self.state = "hover"
        else:
            self.state = "normal"
            
    def draw(self):
        # الحركة: offset (فوق وشمال) للواجهة، shadow (تحت ويمين) للظل
        if self.state == "normal":
            offset = 4    
            shadow = 2    
        elif self.state == "hover":
            offset = 6
            shadow = 4
        elif self.state == "pressed":
            offset = 2
            shadow = 1

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 1. الظل (Shadow) - لتحت ويمين (+X, -Y)
        glColor4f(0.0, 0.0, 0.0, 0.25)
        self._draw_quad(self.x + shadow, self.y - shadow, self.w, self.h)
        
        # 2. الحافة (Edge) - في المركز
        glColor3f(*self.edge_color) 
        self._draw_quad(self.x, self.y, self.w, self.h)
        
        # 3. الواجهة (Front) - لفوق وشمال (-X, +Y)
        front_x = self.x - offset
        front_y = self.y + offset
        
        glColor3f(*self.front_color) 
        self._draw_quad(front_x, front_y, self.w, self.h)
        
        # 4. النص - بيتحرك مع الواجهة
        glColor3f(1.0, 1.0, 1.0)
        # استخدمنا text_offset_x عشان نرجع الكلمة لورا شوية فتبان في النص
        draw_text(self.text, front_x + self.text_offset_x, front_y + 12, 30)

    def _draw_quad(self, cx, cy, w, h):
        glBegin(GL_QUADS)
        glVertex2f(cx - w/2, cy - h/2)
        glVertex2f(cx + w/2, cy - h/2)
        glVertex2f(cx + w/2, cy + h/2)
        glVertex2f(cx - w/2, cy + h/2)
        glEnd()
        