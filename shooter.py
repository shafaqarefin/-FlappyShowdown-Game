import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
import subprocess
import sys


SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
bird_y, bird_size, bird_speed = SCREEN_HEIGHT / 2, 8, 20
rocks = []
bullet_y, bullet_x, bullet_size, bullet_speed = SCREEN_WIDTH / 2, 9, 2, 8
max_rocks = 1
rocks_speed = 5
paused, game_over = data_received = False, False
bullet_active = False
mistake = 0
started = False
miss = 0
score = 0


def main():
    global score
    if len(sys.argv) != 2:
        print("Usage: python shooter.py <score>")
        sys.exit(1)

    try:
        score = int(sys.argv[1])
    except ValueError:
        print("Invalid score value provided.")
        sys.exit(1)

    print("Received score:", score)
    return score


if __name__ == "__main__":
    main()


def findZone(x1, y1, x2, y2):
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


def ConvertToZone0(x1, y1, zone):
    if zone == 0:
        x1, y1 = int(x1), int(y1)
    elif zone == 1:
        x1, y1 = int(y1), int(x1)
    elif zone == 2:
        x1, y1 = -int(y1), int(x1)
    elif zone == 3:
        x1, y1 = -int(x1), int(y1)
    elif zone == 4:
        x1, y1 = -int(x1), int(y1)
    elif zone == 5:
        x1, y1 = -int(y1), -int(x1)
    elif zone == 6:
        x1, y1 = -int(y1), int(x1)
    elif zone == 7:
        x1, y1 = int(x1), -int(y1)
    return x1, y1


def ConvertBackToOriginalZone(x1, y1, zone):
    if zone == 0:
        x1, y1 = int(x1), int(y1)
    elif zone == 1:
        x1, y1 = int(y1), int(x1)
    elif zone == 2:
        x1, y1 = -int(y1), int(x1)
    elif zone == 3:
        x1, y1 = -int(x1), int(y1)
    elif zone == 4:
        x1, y1 = -int(x1), int(y1)
    elif zone == 5:
        x1, y1 = -int(y1), -int(x1)
    elif zone == 6:
        x1, y1 = int(y1), -int(x1)
    elif zone == 7:
        x1, y1 = int(x1), -int(y1)
    return x1, y1


def circlePoints(x, y, x0, y0):
    WritePixel(x + x0, y + y0)
    WritePixel(y + x0, x + y0)
    WritePixel(y + x0, -x + y0)
    WritePixel(x + x0, -y + y0)
    WritePixel(-x + x0, -y + y0)
    WritePixel(-y + x0, -x + y0)
    WritePixel(-y + x0, x + y0)
    WritePixel(-x + x0, y + y0)


def midpointCircle(radius, x0, y0):
    d = 1 - radius
    x = 0
    y = radius

    circlePoints(x, y, x0, y0)

    while x < y:

        if d < 0:
            d = d + 2*x + 3
            x += 1
        else:
            d = d + 2*x - 2*y + 5
            x += 1
            y = y - 1

        circlePoints(x, y, x0, y0)


def draw_circle(radius, x0, y0):
    midpointCircle(radius, x0, y0)


def WritePixel(x, y):
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def DrawLine(x1, y1, x2, y2):
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    current_zone = findZone(x1, y1, x2, y2)
    x1, y1 = ConvertToZone0(x1, y1, current_zone)
    x2, y2 = ConvertToZone0(x2, y2, current_zone)

    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    y = y1

    for x in range(x1, x2 + 1):
        x_original, y_original = ConvertBackToOriginalZone(x, y, current_zone)
        WritePixel(x_original, y_original)

        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE


def back():
    glColor3f(0, 1, 0)
    DrawLine(40, SCREEN_HEIGHT - 40, 60, SCREEN_HEIGHT - 40)
    DrawLine(40, SCREEN_HEIGHT - 40, 50, SCREEN_HEIGHT - 50)
    DrawLine(40, SCREEN_HEIGHT - 40, 50, SCREEN_HEIGHT - 30)


def pause():
    glColor3f(1, 0.8, 0)
    DrawLine(240, SCREEN_HEIGHT - 50, 240, SCREEN_HEIGHT - 30)
    DrawLine(260, SCREEN_HEIGHT - 50, 260, SCREEN_HEIGHT - 30)


def play():
    glColor3f(1, 0.8, 0)
    DrawLine(240, SCREEN_HEIGHT - 50, 240, SCREEN_HEIGHT - 30)
    DrawLine(240, SCREEN_HEIGHT - 50, 260, SCREEN_HEIGHT - 40)
    DrawLine(240, SCREEN_HEIGHT - 30, 260, SCREEN_HEIGHT - 40)


def close():
    glColor3f(1, 0, 0)
    DrawLine(450, SCREEN_HEIGHT - 50, 470, SCREEN_HEIGHT - 30)
    DrawLine(450, SCREEN_HEIGHT - 30, 470, SCREEN_HEIGHT - 50)


def bird():
    for i in range(1, 24):
        glColor3f(1.0, 0.0, 0.0)
        midpointCircle(i, 30, bird_y)
        i = i+1
    glColor3f(0.0, 0.0, 0.0)
    midpointCircle(23, 30, bird_y)
    # eye
    for i in range(1, 8):
        glColor3f(1.0, 1.0, 1.0)
        midpointCircle(i, 43, bird_y + 10)
        i = i+1
    glColor3f(0.0, 0.0, 0.0)
    midpointCircle(10, 43, bird_y + 10)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(43, bird_y + 10)
    glVertex2f(43, bird_y + 9)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(39, bird_y - 4.5)
    glEnd()
    # beak
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(8)
    DrawLine(44, bird_y + 7, 56, bird_y + 7)
    DrawLine(44, bird_y + 2, 51, bird_y + 2)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3)
    DrawLine(50, bird_y + 4.5, 64, bird_y + 4.5)
    DrawLine(45, bird_y + 12, 55, bird_y + 12)
    DrawLine(35, bird_y + 4.5, 45, bird_y - 2)
    DrawLine(35, bird_y + 4.5, 45, bird_y + 12)
    DrawLine(45, bird_y - 2, 52, bird_y - 2)
    DrawLine(52, bird_y - 2, 58, bird_y + 4.5)
    DrawLine(55, bird_y + 12, 65, bird_y + 4.5)
    # wing
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(8)
    DrawLine(8, bird_y + 6, 17, bird_y + 6)
    DrawLine(6, bird_y + 12, 17, bird_y + 8)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3)
    DrawLine(0, bird_y + 15, 20, bird_y + 15)
    DrawLine(20, bird_y, 20, bird_y + 15)
    DrawLine(8, bird_y, 20, bird_y)
    DrawLine(8, bird_y, 0, bird_y + 15)


def bullet(x, size):
    global bullet_x
    if game_over:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1, 1, 1)

    draw_circle(size, bullet_x, x)


def bullet_initializer():
    global bullet_x, bullet_y
    bullet_x = 9


def animate(_):
    global rocks, paused, game_over, bullet_x, bullet_active, mistake, bird_y, score

    if not game_over and not paused:
        for i in range(len(rocks)):
            rocks[i][0] -= rocks_speed

        if bullet_active:
            bullet_x += bullet_speed

            if bullet_x > SCREEN_WIDTH - 20:
                mistake += 1
                bullet_initializer()
                bullet_active = False
                print('Misfire', mistake)
            if mistake == 3:
                game_over = True
                paused = True
                print("Game Over. Your Score:", main())

        # Limit bird movement to stay within the screen
        if bird_y < SCREEN_HEIGHT - 20 and bird_y > 10:
            bird_y -= 6

    glutPostRedisplay()
    glutTimerFunc(20, animate, 0)


def generate_rocks():
    global rocks, r, g, b
    r, g, b = random.uniform(0.1, 1), random.uniform(
        0.1, 1), random.uniform(0.1, 1)
    if len(rocks) < max_rocks:
        for i in range(max_rocks - len(rocks)):
            rocks.append(
                [SCREEN_WIDTH - 20, random.uniform(20, SCREEN_HEIGHT - 70 - i * 50), 7])


def reset_game():
    global score, paused, game_over, rocks, bullet_active, mistake, miss, started, bullet_speed, bird_speed, rocks_speed
    score = 0
    paused = False
    game_over = False
    rocks = []
    bullet_active = False
    mistake = 0
    miss = 0
    # started = False
    bird_speed = 20
    bullet_speed = 20
    rocks_speed = 5
    generate_rocks()
    print("Starting Over. Your Score:", score)


def detect_collision():
    global score, game_over, paused, rocks_speed, bird_speed, rocks, bullet_active, started, miss

    bullet_box = {'x': bullet_x - 2*bullet_size, 'y': bullet_y - 2 *
                  bullet_size, 'width': 2 * 2*bullet_size, 'height': 2 * 2*bullet_size}
    bird_box = {'x': 30 - bird_size, 'y': bird_y - bullet_size,
                'width': 2 * bird_size, 'height': 2 * bird_size}

    for rocks_info in rocks:
        rocks_box = {'x': rocks_info[0] - rocks_info[2], 'y': rocks_info[1] - rocks_info[2],
                     'width': 2 * rocks_info[2], 'height': 2 * rocks_info[2]}
        if collided(bullet_box, rocks_box):
            score += 1

            if score == 2:
                game_over = True
                glutLeaveMainLoop()
            rocks.remove(rocks_info)

            print("Score:", main())
            bullet_active = False
            bullet_initializer()
            generate_rocks()

        elif rocks_info[0] < 9:
            miss += 1
            rocks.remove(rocks_info)
            generate_rocks()
            print("Rocks failed to hit", miss)
            if miss == 3:
                game_over = True
                paused = True

                print("Game Over. Your Score:", main())

        else:
            if collided(bird_box, rocks_box):
                game_over = True
                paused = True
                print("Game Over. Your Score:", main())


def collided(box1, box2):
    return (box1['x'] <= box2['x'] + box2['width'] and
            box1['x'] + box1['width'] >= box2['x'] and
            box1['y'] <= box2['y'] + box2['height'] and
            box1['y'] + box1['height'] >= box2['y'])


def rockfiller(radius, x, y):
    glColor3f(0.8, 0.5, 0.2)  # Set color to brown
    x0, y0 = 0, radius
    d = 1 - radius

    while y0 >= x0:
        # Drawing vertical lines to fill the circle
        DrawLine(x - x0, y + y0, x + x0, y + y0)
        DrawLine(x - x0, y - y0, x + x0, y - y0)
        DrawLine(x - y0, y + x0, x + y0, y + x0)
        DrawLine(x - y0, y - x0, x + y0, y - x0)

        if d < 0:
            d = d + 2 * x0 + 3
        else:
            d = d + 2 * (x0 - y0) + 5
            y0 -= 1
        x0 += 1


def display():
    global bird_y, bird_size, paused, game_over, bullet_active

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    if not game_over:

        bird()
        for rocks_info in rocks:
            rockfiller(rocks_info[2], rocks_info[0], rocks_info[1])

        if bullet_active:
            bullet(bullet_y, bullet_size)

        if paused:
            play()
        else:
            pause()
        close()
        detect_collision()

        glutSwapBuffers()

    else:
        bird()
        for rocks_info in rocks:
            rockfiller(rocks_info[2], rocks_info[0], rocks_info[1])

        if bullet_active:
            bullet(bullet_y, bullet_size)

        pause()
        close()

        glutSwapBuffers()


def keyboardListener(key, x, y):
    global bullet_active, bullet_y, bird_y, paused, game_over, bird_speed
    if key == b' ':

        if bullet_active == False:
            bullet_y = bird_y
            bullet_initializer()

        bullet_active = True


def keyboard(key, x, y):
    global bird_y, paused, game_over, bird_speed
    if not game_over and not paused:
        if key == GLUT_KEY_DOWN and bird_y - bird_size > 20:
            bird_y -= bird_speed
        elif key == GLUT_KEY_UP and bird_y + bird_size < SCREEN_WIDTH - 25:
            bird_y += bird_speed

    glutPostRedisplay()


def mouse(button, state, x, y):
    global bird_y, bird_size, paused, game_over, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if 30 <= x <= 70 and 20 <= y <= 70:

            if game_over:
                paused = False
                game_over = False

            else:
                paused = False
                game_over = False
                reset_game()

        elif 220 <= x <= 280 and 20 <= y <= 70:
            if not paused:
                paused = True
            else:
                paused = False

        elif 430 <= x <= 490 and 20 <= y <= 70:
            game_over = True
            paused = True
            print("Goodbye. Your Score:", main())
            glutLeaveMainLoop()

    glutPostRedisplay()


# def execute_code():
#         script_path="C:\\Users\\shafa\\Desktop\\423 LAB AS-2\\project\\final-project.py"
#         subprocess.run(["python", script_path])

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Project")
glutTimerFunc(0, animate, 0)

glClearColor(0, 0, 0, 0)

glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(keyboard)
glutMouseFunc(mouse)

generate_rocks()
reset_game()

glutMainLoop()
