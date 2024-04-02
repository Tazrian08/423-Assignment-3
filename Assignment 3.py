from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


def draw_res():
    glColor3f(0.0, 0.5, 0.8)
    midpointLineDrawing(30, 490, 5, 470)
    midpointLineDrawing(5, 470, 30, 450)
    midpointLineDrawing(5, 470, 60, 470)

def draw_pause():
    global pause
    glColor3f(1.0, 1.0, 0.0)
    if pause==True:
        midpointLineDrawing(230, 490, 280, 470)
        midpointLineDrawing(280, 470, 230, 450)
        midpointLineDrawing(230, 450, 230, 490)
    else:
        midpointLineDrawing(250, 490, 250, 450)
        midpointLineDrawing(270, 490, 270, 450)

def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    midpointLineDrawing(460, 490, 490, 450)
    midpointLineDrawing(460, 450, 490, 490)

def findZone(x, y):
    zone = 0
    dx = abs(x[1] - x[0])
    dy = abs(y[1] - y[0])

    if dx >= dy:
        if x[0] <= x[1]:
            if y[0] <= y[1]:
                zone = 0
            else:
                zone = 7
        else:
            if y[0] <= y[1]:
                zone = 3
            else:
                zone = 4
    else:
        if y[0] <= y[1]:
            if x[0] <= x[1]:
                zone = 1
            else:
                zone = 2
        else:
            if x[0] <= x[1]:
                zone = 6
            else:
                zone = 5
    return zone


def convertToZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def convertFromZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def midpointLineDrawing(x1, y1, x2, y2):
    zone = findZone((x1, x2), (y1, y2))
    x1, y1 = convertToZone0(x1, y1, zone)
    x2, y2 = convertToZone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1

    x1,x2=int(x1),int(x2)
    for x in range(x1, x2 + 1):
        x_orig, y_orig = convertFromZone0(x, y, zone)
        WritePixel(x_orig, y_orig)
        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE


def WritePixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def midpointCircleDrawing(cx, cy, r):
    zone = 1
    x = 0
    y = r
    d = 1 - r

    while y > x:
        WritePixel(cx + x, cy + y)
        WritePixel(cx + y, cy + x)
        WritePixel(cx - x, cy + y)
        WritePixel(cx - y, cy + x)
        WritePixel(cx - x, cy - y)
        WritePixel(cx - y, cy - x)
        WritePixel(cx + x, cy - y)
        WritePixel(cx + y, cy - x)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

class Bullet:
    def __init__(self, x):
        self.x = x
        self.y = 20
        self.radius=5

    def draw(self):
        glColor3f(1.0, 0.8, 0.0)
        midpointCircleDrawing(self.x, self.y, self.radius)

class Cir:
    def __init__(self):
        self.radius = random.randint(5, 30)
        self.x = random.randint(self.radius, 500 - self.radius)
        self.y = 500
        self.is_overlapping = False

    def check_collision(self, other_circle):
        distance_squared = (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        min_distance = (self.radius + other_circle.radius) ** 2
        return distance_squared < min_distance

    def check_all_collisions(self, cir_arr):
        for other_circle in cir_arr:
            if other_circle != self:
                if self.check_collision(other_circle):
                    self.is_overlapping = True
                    break
        else:
            self.is_overlapping = False

    def draw(self):
        if not self.is_overlapping:
            glColor3f(1.0, 0.8, 0.0)
            midpointCircleDrawing(self.x, self.y, self.radius)

shooter_x = random.randint(20, 480)
bullet_arr = []
cir_arr=[]
stop=False
score=0
fall=0
miss=0
over=False
pause=False

def drawShooter():
    global shooter_x
    center_x = shooter_x
    center_y = 20
    radius = 10
    glColor3f(1.0, 0.8, 0.0)
    midpointCircleDrawing(center_x, center_y, radius)



def animate():
    global bullet_arr, cir_arr,score,fall,over,miss, pause
    if over==False and pause==False:
        bullets_to_remove = []
        cir_to_remove = []

        for bullet in bullet_arr:
            for cir in cir_arr:
                distance_squared = (bullet.x - cir.x) ** 2 + (bullet.y - cir.y) ** 2
                if distance_squared <= (bullet.radius + cir.radius) ** 2:
                    bullets_to_remove.append(bullet)
                    cir_to_remove.append(cir)
                    score += 1
                    print(f"Score: {score}")
                    break

        for bullet in bullets_to_remove:
            bullet_arr.remove(bullet)
        for cir in cir_to_remove:
            cir_arr.remove(cir)

        for cir in cir_arr:
            cir.y -= 0.1
            if cir.y <= 10:
                cir_arr.remove(cir)
                fall += 1
                if fall == 3:
                    print("Game Over")
                    print(f"Score: {score}")
                    over = True
                if (shooter_x - cir.x) ** 2 + (20 - cir.y) ** 2 <= (cir.radius + 10) ** 2:
                    print("Game Over - Circle collided with the shooter")
                    print(f"Score: {score}")
                    over = True


        for bullet in bullet_arr:
            bullet.y += 0.45
            if bullet.y >= 500:
                miss+=1
                bullet_arr.remove(bullet)
                if miss==3:
                    print("Game Over. You miss fired 3 times.")
                    print(f"Score: {score}")
                    over=True

    glutPostRedisplay()

def display():
    global stop, over
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(1.0)
    drawShooter()
    if over==False:
        if pause == False:
            if random.random() < 0.002:

                c = Cir()
                c.check_all_collisions(cir_arr)
                if not c.is_overlapping:
                    cir_arr.append(c)
        for cir in cir_arr:
            cir.draw()
        for bullet in bullet_arr:
            bullet.draw()
        draw_res()
        draw_pause()
        draw_cross()
    glutSwapBuffers()

def keyboardListener(key, x, y):
    global shooter_x, bullet_arr, over
    if over==False and pause==False:
        if key == b'a':
            if shooter_x >= 20:
                shooter_x -= 8
        if key == b'd':
            if shooter_x <= 480:
                shooter_x += 8
        if key == b' ':
            b = Bullet(shooter_x)
            bullet_arr.append(b)

    glutPostRedisplay()

def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global pause,score, over, bullet_arr, cir_arr
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            if y<=50:
                if 0<=x<=60:
                    bullet_arr=[]
                    cir_arr=[]
                    over=False
                    print(f"Starting Over! Score {score}")
                    score=0
                if 230 <= x <= 280:
                    if pause==False:
                        pause=True
                    else:
                        pause=False
                if 460<=x<=490:
                    print(f"Goodbye! Score {score}")
                    glutLeaveMainLoop()
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 500, 0, 500)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"The Game")
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutDisplayFunc(display)
glutIdleFunc(animate)
init()
glutMainLoop()
