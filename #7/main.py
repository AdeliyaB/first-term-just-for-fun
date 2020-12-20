import pygame
from pygame.draw import *
from random import randint
import math
import pygame.freetype
pygame.init()

FPS = 30
SC_W = 1200
SC_H = 900
screen = pygame.display.set_mode((SC_W, SC_H))


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

MAX_N = 5

SC_CIRCLE = 1
SC_SQUARE = 2

try:
    file = open('goal.txt', 'r')
except:
    print("Scoreboard file not found. Creating a new one")
    file = open('goal.txt', 'w')
    file.close()
    file = open('goal.txt', 'r')

def open_f(file):
    lines = file.readlines()
    data = [[], []]
    for i in lines:
        data[0].append(list(i.split())[0])
        data[1].append(list(i.split())[1])
    file.close()
    return data

def save_f(data, file):
    for i in range(len(data[0])):
        print(data[0][i], data[1][i], file=file)

data = open_f(file)
file = open('goal.txt', 'w')
pl_name = input("Пожалуйста, введите Ваше имя: ")
if not (pl_name in data[0]):
    data[0].append(pl_name)
    data[1].append(0)

global pl_number
pl_number = 0
for i in range(len(data[0])):
    if data[0][i] == pl_name:
        pl_number = i
        print(pl_number)
        break



def display_score(score):
    FONT = pygame.freetype.Font("Calibri.ttf", 50)
    FONT.render_to(screen, (50, 50), "Score: " + str(score), (70, 70, 0))

def display_scoreboard(file_data, x, y):
    FONT = pygame.freetype.Font("Calibri.ttf", 50)

    FONT.render_to(screen, (x, y), "Scoreboard", (0, 200, 0))
    for i in range(len(data[0])):
        FONT.render_to(screen, (x, y + 55 * (i + 1)), str(i + 1) + ". " + str(data[0][i]) + ": " +str(data[1][i]), (0, 150, 0))
def draw_ball(x, y, r, color):
    circle(screen, color, (x, y), r)

def draw_square(x, y, r, color):
    polygon(screen, color, [(x - r, y - r), (x - r, y + r), (x + r, y + r), (x + r, y - r)])

def check_ball_click(ball_x, ball_y, ball_r, mouse_pos):
    distance = math.sqrt(abs(ball_x - mouse_pos[0]) ** 2 + abs(ball_y - mouse_pos[1]) ** 2)
    if distance <= ball_r:
        return True
    return False

def check_square_click(square_x, square_y, square_r, mouse_pos):
    if abs(square_x - mouse_pos[0]) <= square_r and abs(square_y - mouse_pos[1]) <= square_r:
        return True
    return False

def check_balls_click(balls, mouse_pos):
    ans = []
    for i in range(len(balls) - 1, -1, -1):
        if balls[i][7] == 1:
            if check_ball_click(balls[i][3], balls[i][4], balls[i][5], mouse_pos):
                ans.append(i)
        else:
            if check_square_click(balls[i][3], balls[i][4], balls[i][5], mouse_pos):
                ans.append(i)
    return ans


pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = int(data[1][pl_number])
balls = []

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in check_balls_click(balls, event.pos):
                if balls[i][7] == 1:
                    score += SC_CIRCLE
                else:
                    score += SC_SQUARE
                balls.pop(i)
            data[1][pl_number] = str(score)

    for i in range(len(balls), MAX_N):
        ball_frames = 1
        ball_speed_x = randint(-8, 8)
        ball_speed_y = randint(-8, 8)
        ball_r = randint(40, 100)
        ball_x = randint(ball_r + 50, SC_W - ball_r - 50)
        ball_y = randint(ball_r + 50, SC_H - ball_r - 50)
        color = COLORS[randint(0, 5)]
        shape = randint(30, 70) // 30
        balls.append([ball_frames, ball_speed_x, ball_speed_y, ball_x, ball_y, ball_r, color, shape])
    for i in range(len(balls)):
        ball = balls[i]
        ball_frames = ball[0]
        ball_speed_x = ball[1]
        ball_speed_y = ball[2]
        ball_x = ball[3]
        ball_y = ball[4]
        ball_r = ball[5]
        color = ball[6]
        shape = ball[7]

        ball_frames += 1

        if ball_x <= ball_r or ball_x >= SC_W - ball_r:
            ball_speed_x *= -1
        elif ball_y <= ball_r or ball_y >= SC_H - ball_r:
            ball_speed_y *= -1

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if shape == 1:
            draw_ball(ball_x, ball_y, ball_r, color)
        else:
            draw_square(ball_x, ball_y, ball_r, color)

        balls[i] = [ball_frames, ball_speed_x, ball_speed_y, ball_x, ball_y, ball_r, color, shape]
    display_score(score)
    display_scoreboard(data, SC_W - 350, 50)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
save_file(data, file)
print("Scoreboard saved")
file.close()
