from OpenGL.GL import *
from numpy import cos, sin
from constants import *
from PIL import Image

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
    glBegin(GL_QUADS)
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
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-w/2, -h/2)
    glTexCoord2f(1, 0); glVertex2f(w/2, -h/2)
    glTexCoord2f(1, 1); glVertex2f(w/2, h/2)
    glTexCoord2f(0, 1); glVertex2f(-w/2, h/2)
    glEnd()

    glPopMatrix()

    glDisable(GL_TEXTURE_2D)