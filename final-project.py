from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
import random
import subprocess
import sys

try:
    del os.environ['DISPLAY']
except:
    pass


pause = 0
score = 0
change = 1
flag = 0
targets = []
bullets = []
count = 0


class Diamond:
    global change

    def __init__(self, number):

        self.leftx = 420
        self.rightx = 480
        self.top_bottomy = random.randint(150, 300)
        self.bottom_topy = self.top_bottomy-100
        self.top_topy = 439
        self.number = number
        self.check = 0

    def draw(self):

        DrawLine(self.leftx, 0, self.rightx, 0)
        DrawLine(self.leftx, self.bottom_topy, self.rightx, self.bottom_topy)
        DrawLine(self.leftx, 0, self.leftx, self.bottom_topy)
        DrawLine(self.rightx, 0, self.rightx, self.bottom_topy)
        DrawLine(self.leftx, 440, self.leftx, self.top_bottomy)
        DrawLine(self.rightx, 440, self.rightx, self.top_bottomy)
        DrawLine(self.leftx, self.top_bottomy, self.rightx, self.top_bottomy)
        DrawLine(self.leftx, self.top_topy, self.rightx, self.top_topy)
        # if number==1:
        #     glColor3f(1,0,0)
        #     DrawLine(self.leftx, self.bottom_topy + 2, self.leftx, self.top_bottomy - 2)
        #     # DrawLine(self.rightx, self.top_bottomy + 2, self.rightx, self.top_topy - 2)
        #     # DrawLine(self.leftx, self.top_topy - 2, self.rightx, self.top _topy - 2)
        #     # DrawLine(self.leftx, self.top_bottomy + 2, self.leftx, self.top_bottomy + 2)

    # def create(self):
    #     leftx=420
    #     rightx=480
    #     bottom_topy=200
    #     top_bottomy=300
    #     top_topy=500
    #     DrawLine(leftx,0,rightx,0)
    #     DrawLine(leftx,bottom_topy,rightx,bottom_topy)
    #     DrawLine(leftx,0,leftx,bottom_topy)
    #     DrawLine(rightx,0,rightx,bottom_topy)

    def motion(self):
        if self.number == 1 and self.check == 0:
            self.top_bottomy -= 1
            if self.top_bottomy == self.bottom_topy:
                self.check = 1
        if self.number == 1 and self.check == 1:
            self.top_bottomy += 1
            if self.top_bottomy == self.top_topy:
                self.check = 0

    def respawn(self):

        DrawLine(self.leftx, 0, self.rightx, 0)
        DrawLine(self.leftx, self.bottom_topy, self.rightx, self.bottom_topy)
        DrawLine(self.leftx, 0, self.leftx, self.bottom_topy)
        DrawLine(self.rightx, 0, self.rightx, self.bottom_topy)
        DrawLine(self.leftx, 440, self.leftx, self.top_bottomy)
        DrawLine(self.rightx, 440, self.rightx, self.top_bottomy)
        DrawLine(self.leftx, self.top_bottomy, self.rightx, self.top_bottomy)
        DrawLine(self.leftx, self.top_topy, self.rightx, self.top_topy)

    def decrease(self):

        self.leftx -= 4
        self.rightx -= 4


def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx >= 0 and dy <= 0:
            return 7
        elif dx <= 0 and dy <= 0:
            return 4
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx >= 0 and dy <= 0:
            return 6
        elif dx <= 0 and dy <= 0:
            return 5


def convert(x1, y1, zone):
    if zone == 0:
        x1, y1 = x1, y1

    elif zone == 1:
        x1, y1 = y1, x1

    elif zone == 2:
        x1, y1 = -y1, x1

    elif zone == 3:
        x1, y1 = -x1, y1

    elif zone == 4:
        x1, y1 = -x1, y1

    elif zone == 5:
        x1, y1 = -y1, -x1

    elif zone == 6:
        x1, y1 = -y1, x1

    elif zone == 7:
        x1, y1 = x1, -y1

    return x1, y1


def convert_back(x1, y1, zone):
    if zone == 0:
        x1, y1 = x1, y1

    elif zone == 1:
        x1, y1 = y1, x1

    elif zone == 2:
        x1, y1 = -y1, x1

    elif zone == 3:
        x1, y1 = -x1, y1

    elif zone == 4:
        x1, y1 = -x1, y1

    elif zone == 5:
        x1, y1 = -y1, -x1

    elif zone == 6:
        x1, y1 = y1, -x1

    elif zone == 7:
        x1, y1 = x1, -y1

    return x1, y1


def DrawLine(x1, y1, x2, y2):
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = convert(x1, y1, zone)
    x2, y2 = convert(x2, y2, zone)
    dy = y2 - y1
    dx = x2 - x1
    d = 2 * dy - dx
    x = x1
    y = y1
    glBegin(GL_POINTS)
    a, b = convert_back(x, y, zone)
    glVertex2f(a, b)
    while x <= x2:
        x += 1
        a, b = convert_back(x, y, zone)
        glVertex2f(a, b)
        if d < 0:
            d += (2 * dy)
        elif d >= 0:
            d += ((2 * dy) - (2 * dx))
            y += 1
    glEnd()


def DrawCircle(x1, y1, r):

    d = 1-r
    x = 0
    y = r
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0)
    while x <= y:
        glVertex2f(x1+x, y1+y)
        glVertex2f(x1+y, y1+x)
        glVertex2f(x1-y, y1+x)
        glVertex2f(x1-x, y1+y)
        glVertex2f(x1-x, y1-y)
        glVertex2f(x1-y, y1-x)
        glVertex2f(x1+y, y1-x)
        glVertex2f(x1+x, y1-y)
        if d < 0:
            d = d+(2*x)+3
            x += 1
        else:
            d = d+(2*x)-(2*y)+3
            x += 1
            y -= 1

    glEnd()


def midpointCircle(r, c1, c2):
    d = 1 - r
    x = 0
    y = r
    while x < y:
        if d < 0:
            d = d + 2*x + 3
            x = x + 1
        else:
            d = d + 2*x - 2*y + 5
            x = x + 1
            y = y - 1
        add_center(x, y, c1, c2)


def add_center(x, y, c1, c2):
    glBegin(GL_POINTS)
    glVertex2f(x+c1, y+c2)
    glVertex2f(y+c1, x+c2)
    glVertex2f(y+c1, -x+c2)
    glVertex2f(-x+c1, y+c2)
    glVertex2f(-x+c1, -y+c2)
    glVertex2f(-y+c1, -x+c2)
    glVertex2f(-y+c1, x+c2)
    glVertex2f(x+c1, -y+c2)
    glEnd()


class Bird:
    def __init__(self):
        # Body coordinates
        self.body_x_coord = 35
        self.body_y_coord = 175

        # Eye coordinates
        self.eye_x_coord = 41
        self.eye_y_coord = 180

        # Beak coordinates
        self.beak_x1, self.beak_y1, self.beak_x2, self.beak_y2 = 42, 173.5, 48, 173.5
        self.beak_x3, self.beak_y3, self.beak_x4, self.beak_y4 = 42, 171, 45.5, 171
        self.beak_x5, self.beak_y5, self.beak_x6, self.beak_y6 = 45, 172.25, 52, 172.25
        self.beak_x7, self.beak_y7, self.beak_x8, self.beak_y8 = 42.5, 176, 47.5, 176
        self.beak_x9, self.beak_y9, self.beak_x10, self.beak_y10 = 37.5, 172.25, 42.5, 169
        self.beak_x11, self.beak_y11, self.beak_x12, self.beak_y12 = 37.5, 172.25, 42.5, 176
        self.beak_x13, self.beak_y13, self.beak_x14, self.beak_y14 = 42.5, 169, 46, 169
        self.beak_x15, self.beak_y15, self.beak_x16, self.beak_y16 = 46, 169, 49, 172.25
        self.beak_x17, self.beak_y17, self.beak_x18, self.beak_y18 = 47.5, 176, 52.5, 172.25

        self.wing_x1, self.wing_y1, self.wing_x2, self.wing_y2 = 24, 173, 28.5, 173
        self.wing_x3, self.wing_y3, self.wing_x4, self.wing_y4 = 23, 176, 28.5, 174
        self.wing_x5, self.wing_y5, self.wing_x6, self.wing_y6 = 20, 177.5, 30, 177.5
        self.wing_x7, self.wing_y7, self.wing_x8, self.wing_y8 = 30, 170, 30, 177.5
        self.wing_x9, self.wing_y9, self.wing_x10, self.wing_y10 = 24, 170, 30, 170
        self.wing_x11, self.wing_y11, self.wing_x12, self.wing_y12 = 24, 170, 20, 177.5

        self.step_up = 30
        self.step_down = 1

    def draw(self):
        # Draw body
        for i in range(1, 12):
            glColor3f(1.0, 0.0, 0.0)
            midpointCircle(i, self.body_x_coord, self.body_y_coord)
            i += 1
        glColor3f(0.0, 0.0, 0.0)
        midpointCircle(11, self.body_x_coord, self.body_y_coord)

        # Draw eye
        for i in range(1, 4):
            glColor3f(1.0, 1.0, 1.0)
            midpointCircle(i, self.eye_x_coord, self.eye_y_coord)
            i += 1
        glColor3f(1.0, 0.0, 0.0)
        midpointCircle(5, self.eye_x_coord, self.eye_y_coord)
        glBegin(GL_POINTS)
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(self.eye_x_coord, self.eye_y_coord)
        glVertex2f(self.eye_x_coord, self.eye_y_coord - 1)
        glColor3f(1.0, 1.0, 0.0)
        glVertex2f(self.eye_x_coord - 2, self.eye_y_coord - 7.75)
        glEnd()

        # Draw beak
        glColor3f(1.0, 1.0, 0.0)
        glPointSize(2)
        DrawLine(self.beak_x1, self.beak_y1, self.beak_x2, self.beak_y2)
        DrawLine(self.beak_x3, self.beak_y3, self.beak_x4, self.beak_y4)
        DrawLine(self.beak_x5, self.beak_y5, self.beak_x6, self.beak_y6)
        DrawLine(self.beak_x7, self.beak_y7, self.beak_x8, self.beak_y8)
        DrawLine(self.beak_x9, self.beak_y9, self.beak_x10, self.beak_y10)
        DrawLine(self.beak_x11, self.beak_y11, self.beak_x12, self.beak_y12)
        DrawLine(self.beak_x13, self.beak_y13, self.beak_x14, self.beak_y14)
        DrawLine(self.beak_x15, self.beak_y15, self.beak_x16, self.beak_y16)
        DrawLine(self.beak_x17, self.beak_y17, self.beak_x18, self.beak_y18)

        # Draw wing
        glColor3f(1.0, 1.0, 0.0)
        glPointSize(4)
        DrawLine(self.wing_x1, self.wing_y1, self.wing_x2, self.wing_y2)
        DrawLine(self.wing_x3, self.wing_y3, self.wing_x4, self.wing_y4)
        DrawLine(self.wing_x5, self.wing_y5, self.wing_x6, self.wing_y6)
        DrawLine(self.wing_x7, self.wing_y7, self.wing_x8, self.wing_y8)
        DrawLine(self.wing_x9, self.wing_y9, self.wing_x10, self.wing_y10)
        DrawLine(self.wing_x11, self.wing_y11, self.wing_x12, self.wing_y12)

    def increase(self):
        self.body_y_coord += self.step_up
        self.eye_y_coord += self.step_up
        self.beak_y1 += self.step_up
        self.beak_y2 += self.step_up
        self.beak_y3 += self.step_up
        self.beak_y4 += self.step_up
        self.beak_y5 += self.step_up
        self.beak_y6 += self.step_up
        self.beak_y7 += self.step_up
        self.beak_y8 += self.step_up
        self.beak_y9 += self.step_up
        self.beak_y10 += self.step_up
        self.beak_y11 += self.step_up
        self.beak_y12 += self.step_up
        self.beak_y13 += self.step_up
        self.beak_y14 += self.step_up
        self.beak_y15 += self.step_up
        self.beak_y16 += self.step_up
        self.beak_y17 += self.step_up
        self.beak_y18 += self.step_up
        self.wing_y1 += self.step_up
        self.wing_y2 += self.step_up
        self.wing_y3 += self.step_up
        self.wing_y4 += self.step_up
        self.wing_y5 += self.step_up
        self.wing_y6 += self.step_up
        self.wing_y7 += self.step_up
        self.wing_y8 += self.step_up
        self.wing_y9 += self.step_up
        self.wing_y10 += self.step_up
        self.wing_y11 += self.step_up
        self.wing_y12 += self.step_up

    def decrease(self):
        self.body_y_coord -= self.step_down
        self.eye_y_coord -= self.step_down
        self.beak_y1 -= self.step_down
        self.beak_y2 -= self.step_down
        self.beak_y3 -= self.step_down
        self.beak_y4 -= self.step_down
        self.beak_y5 -= self.step_down
        self.beak_y6 -= self.step_down
        self.beak_y7 -= self.step_down
        self.beak_y8 -= self.step_down
        self.beak_y9 -= self.step_down
        self.beak_y10 -= self.step_down
        self.beak_y11 -= self.step_down
        self.beak_y12 -= self.step_down
        self.beak_y13 -= self.step_down
        self.beak_y14 -= self.step_down
        self.beak_y15 -= self.step_down
        self.beak_y16 -= self.step_down
        self.beak_y17 -= self.step_down
        self.beak_y18 -= self.step_down
        self.wing_y1 -= self.step_down
        self.wing_y2 -= self.step_down
        self.wing_y3 -= self.step_down
        self.wing_y4 -= self.step_down
        self.wing_y5 -= self.step_down
        self.wing_y6 -= self.step_down
        self.wing_y7 -= self.step_down
        self.wing_y8 -= self.step_down
        self.wing_y9 -= self.step_down
        self.wing_y10 -= self.step_down
        self.wing_y11 -= self.step_down
        self.wing_y12 -= self.step_down

    def respawn(self):
        # Body
        body_x_coord = 35
        body_y_coord = 175

        # Eye
        eye_x_coord = 41
        eye_y_coord = 180

        # Beak
        beak_x1, beak_y1, beak_x2, beak_y2 = 42, 173.5, 48, 173.5
        beak_x3, beak_y3, beak_x4, beak_y4 = 42, 171, 45.5, 171
        beak_x5, beak_y5, beak_x6, beak_y6 = 45, 172.25, 52, 172.25
        beak_x7, beak_y7, beak_x8, beak_y8 = 42.5, 176, 47.5, 176
        beak_x9, beak_y9, beak_x10, beak_y10 = 37.5, 172.25, 42.5, 169
        beak_x11, beak_y11, beak_x12, beak_y12 = 37.5, 172.25, 42.5, 176
        beak_x13, beak_y13, beak_x14, beak_y14 = 42.5, 169, 46, 169
        beak_x15, beak_y15, beak_x16, beak_y16 = 46, 169, 49, 172.25
        beak_x17, beak_y17, beak_x18, beak_y18 = 47.5, 176, 52.5, 172.25

        wing_x1, wing_y1, wing_x2, wing_y2 = 24, 173, 28.5, 173
        wing_x3, wing_y3, wing_x4, wing_y4 = 23, 176, 28.5, 174
        wing_x5, wing_y5, wing_x6, wing_y6 = 20, 177.5, 30, 177.5
        wing_x7, wing_y7, wing_x8, wing_y8 = 30, 170, 30, 177.5
        wing_x9, wing_y9, wing_x10, wing_y10 = 24, 170, 30, 170
        wing_x11, wing_y11, wing_x12, wing_y12 = 24, 170, 20, 177.5
        # Draw body
        for i in range(1, 14):
            glColor3f(1.0, 0.0, 0.0)
            midpointCircle(i, body_x_coord, body_y_coord)
            i += 1
            glColor3f(0.0, 0.0, 0.0)
            midpointCircle(11, body_x_coord, body_y_coord)

        # Draw eye
        for i in range(1, 4):
            glColor3f(1.0, 1.0, 1.0)
            midpointCircle(i, eye_x_coord, eye_y_coord)
            i += 1
            glColor3f(1.0, 0.0, 0.0)
            midpointCircle(5, eye_x_coord, eye_y_coord)
            glBegin(GL_POINTS)
            glColor3f(0.0, 0.0, 0.0)
            glVertex2f(eye_x_coord, eye_y_coord)
            glVertex2f(eye_x_coord, eye_y_coord - 1)
            glColor3f(1.0, 1.0, 0.0)
            glVertex2f(eye_x_coord - 2, eye_y_coord - 7.75)
            glEnd()

            # Draw beak
            glColor3f(1.0, 1.0, 0.0)
            glPointSize(2)
            DrawLine(beak_x1, beak_y1, beak_x2, beak_y2)
            DrawLine(beak_x3, beak_y3, beak_x4, beak_y4)
            DrawLine(beak_x5, beak_y5, beak_x6, beak_y6)
            DrawLine(beak_x7, beak_y7, beak_x8, beak_y8)
            DrawLine(beak_x9, beak_y9, beak_x10, beak_y10)
            DrawLine(beak_x11, beak_y11, beak_x12, beak_y12)
            DrawLine(beak_x13, beak_y13, beak_x14, beak_y14)
            DrawLine(beak_x15, beak_y15, beak_x16, beak_y16)
            DrawLine(beak_x17, beak_y17, beak_x18, beak_y18)

            # Draw wing
            glColor3f(1.0, 1.0, 0.0)
            glPointSize(4)
            DrawLine(wing_x1, wing_y1, wing_x2, wing_y2)
            DrawLine(wing_x3, wing_y3, wing_x4, wing_y4)
            DrawLine(wing_x5, wing_y5, wing_x6, wing_y6)
            DrawLine(wing_x7, wing_y7, wing_x8, wing_y8)
            DrawLine(wing_x9, wing_y9, wing_x10, wing_y10)
            DrawLine(wing_x11, wing_y11, wing_x12, wing_y12)


bird = Bird()


def pausebutton():
    # 440 er aro iktu beshi niyue oi jaigai ami amar button guli banaitesi
    glColor3f(1.0, 0.75, 0.0)

    DrawLine(240, 450, 240, 480)
    DrawLine(250, 450, 250, 480)

    # Drawing box
    glColor3f(0, 0, 0)
    DrawLine(220, 440, 270, 440)
    DrawLine(220, 496, 270, 496)
    DrawLine(220, 440, 220, 496)
    DrawLine(270, 440, 270, 496)


def playbutton():
    glColor3f(1.0, 0.75, 0.0)

    DrawLine(220, 496, 270, 468)
    DrawLine(220, 440, 270, 468)
    DrawLine(220, 440, 220, 496)  # left verti

    glColor3f(0, 0, 0)
    DrawLine(220, 440, 270, 440)  # bottom hori
    DrawLine(220, 496, 270, 496)  # top hori
    DrawLine(270, 440, 270, 496)  # right verti


def cross():
    glColor3f(1, 0, 0)

    DrawLine(460, 450, 480, 480)
    DrawLine(460, 480, 480, 450)

    glColor3f(0, 0, 0)
    DrawLine(440, 490, 490, 490)
    DrawLine(440, 440, 490, 440)
    DrawLine(440, 490, 440, 440)
    DrawLine(490, 440, 490, 490)


def backbutton():
    glColor3f(0.0, 0.5, 0.5)

    DrawLine(50, 460, 10, 460)
    DrawLine(10, 460, 30, 480)
    DrawLine(10, 460, 30, 440)

    glColor3f(0, 0, 0)

    DrawLine(50, 440, 0, 440)
    DrawLine(50, 490, 0, 490)
    DrawLine(50, 440, 50, 490)
    DrawLine(0, 440, 0, 490)


def mouseListener(button, state, x, y):
    global pause, score, diamond, flag, end, change, count, bird

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 440 <= x <= 490 and 10 <= y <= 60:
            print("Final Score:", score)
            print("Goodbye")
            glutLeaveMainLoop()

        # if 220 <= x <= 270 and 4<= y <= 60:
        #     if pause==0 :
        #         pause=1
        #         flag=1

        #     else:
        #         pause=0
        #         flag=0

        # if 0 <= x <= 50 and 10<= y <= 60:

        #     print("Starting Over")
        #     score=0
        #     change=1
        #     flag=0
        #     pause=0
        #     bird.respawn()
        #     targets.clear()
        #     animate()
        #     createNewBalls(1)


def iterate():
    glViewport(0, 0, 500, 500)
    glClearColor(0.529, 0.808, 0.922, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global diamond, targets, pause, score, once, chosen_idx, bird
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    bird.draw()
    for target_index, target in enumerate(targets):

        target.draw()
        if target.leftx < 0 and target.rightx < 0:
            del targets[target_index]
            score += 1
            print(score)

    # if flag==0:
    #     pausebutton()
    # else:
    #     playbutton()
    # backbutton()
    cross()
    glutSwapBuffers()


def keyboardListener(key, x, y):
    global bird
    if key == b'a':
        bird.increase()

    glutPostRedisplay()


def execute_other_code():
    global score
    script_path = "C:\\Users\\shafa\\Desktop\\423 LAB AS-2\\project\\shooter.py"
    subprocess.Popen(["python", script_path, str(score)])
    glutLeaveMainLoop()


def animate():
    global pause, diamond, score, obj, change, flag, targets, count, door, chosen_idx

    # self.leftx=420
    # self.rightx=480
    # self.bottom_topy=200
    # self.top_bottomy=300
    # self.top_topy=439
    # self.number=number
    # self.check=0
    if pause == 0:

        # if score == random.randint(10, 15):
        #     execute_other_code()
        for target_index, target in enumerate(targets):
            if bird.body_y_coord > target.top_bottomy and target.leftx < bird.body_x_coord < target.rightx:
                print("Game Over")
                print("Total Score:", score)
                targets.clear()
                pause = 1
                flag = 0
                count = 0

            if bird.body_y_coord < target.bottom_topy and target.leftx < bird.body_x_coord < target.rightx:
                print("Game Over")
                print("Total Score:", score)
                targets.clear()
                pause = 1
                flag = 0
                count = 0
            if bird.body_y_coord == -10:
                print("Game Over")
                print("Total Score:", score)
                targets.clear()
                pause = 1
                flag = 0
                count = 0

        glutPostRedisplay()


def createNewBalls(value):
    global targets, bullets, score, pause

    if pause == 0:
        choose_motion = random.randint(0, 1)

        new_target = Diamond(choose_motion)

        targets.append(new_target)

        glutTimerFunc(1000, createNewBalls, 0)


def movedown(value):
    global targets, bullets, score, pause, count, end

    if pause == 0:

        for target in targets:
            target.decrease()

    glutTimerFunc(20, movedown, 0)


def controlmotion(value):
    global targets
    for target in targets:
        target.motion()
    glutTimerFunc(10, controlmotion, 0)


def controlbird(value):
    global bird
    bird.decrease()
    glutTimerFunc(10, controlbird, 0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Project")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutTimerFunc(1000, createNewBalls, 0)
glutTimerFunc(10, controlmotion, 0)
glutTimerFunc(10, controlbird, 0)
glutTimerFunc(20, movedown, 0)
glutMainLoop()
