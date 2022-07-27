"""from tkinter import *
import time

SPEED = 20
ball_yspeed = 10
ball_xspeed = 60

def left_player_up(event):
    canvas.move(left_player, 0, -SPEED)

def left_player_down(event):
    canvas.move(left_player, 0, SPEED)


def right_player_up(event):
    canvas.move(right_player, 0, -SPEED)


def right_player_down(event):
    canvas.move(right_player, 0, SPEED)

def point_score():
    return False

width = 1400
height = 800

window = Tk()
window.geometry("1400x800")
window.title("Pong game")
window.config(bg="green")

canvas = Canvas(window, width=width, height=height)
left_player = canvas.create_rectangle(0, height/2-75, 20, height/2+75, fill="purple")
right_player = canvas.create_rectangle(width-20, height/2-75, width, height/2+75, fill="orange")
ball = canvas.create_oval(width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20, fill="red")
canvas.pack()

window.bind("<w>",left_player_up)
window.bind("<s>",left_player_down)
window.bind("<Up>",right_player_up)
window.bind("<Down>",right_player_down)

window.mainloop()

while True:
    canvas.move(ball, ball_xspeed, ball_yspeed)
    time.sleep(0.1)
    window.update()"""
import sys

import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
PURPLE = (240,0,255)
ORANGE = (255,100,10)

WIDTH = 1200
HEIGHT = 800

pygame.init()
game_font = pygame.font.SysFont("Consolas", 42)

delay = 15
pads_speed = 20
pads_width = 10
pads_height = 150

left_pad_x = 0
left_pad_y = HEIGHT/2 - pads_height/2

right_pad_x = WIDTH - pads_width
right_pad_y = HEIGHT/2 - pads_height/2

left_score = 0
right_score = 0

left_up = False
left_down = False
right_up = False
right_down = False

ball_x = WIDTH/2
ball_y = HEIGHT/2
ball_width = 10
ball_x_vel = -10
ball_y_vel = random.randint(-5,5)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
screen.fill(BLACK)

def draw_objects():
    pygame.draw.rect(screen, ORANGE, (int(left_pad_x), int(left_pad_y), pads_width, pads_height))
    pygame.draw.rect(screen, PURPLE, (int(right_pad_x), int(right_pad_y), pads_width, pads_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_width)
    score = game_font.render(f"{str(left_score)} - {str(right_score)}", False, WHITE)
    screen.blit(score, (WIDTH/2 - 60, 30))

def apply_player_movement():
    global left_pad_y
    global right_pad_y

    if left_up:
        left_pad_y = max(left_pad_y - pads_speed, 0)
    elif left_down:
        left_pad_y = min(left_pad_y + pads_speed, HEIGHT - pads_height)

    if right_up:
        right_pad_y = max(right_pad_y - pads_speed, 0)
    elif right_down:
        right_pad_y = min(right_pad_y + pads_speed, HEIGHT - pads_height)

def apply_ball_movement():
    global ball_y
    global ball_x
    global ball_y_vel
    global ball_x_vel
    global left_score
    global right_score

    if (ball_x + ball_x_vel < left_pad_x + pads_width) and (left_pad_y < ball_y + ball_y_vel + ball_width < left_pad_y + pads_height):
        ball_x_vel = -ball_x_vel*1.05
        ball_y_vel = (left_pad_y + pads_height/2 - ball_y) / 15
        ball_y_vel = -ball_y_vel
    elif ball_x + ball_x_vel < 0:
        right_score +=1
        ball_x = WIDTH/2
        ball_y = HEIGHT/2
        ball_x_vel = 10
        ball_y_vel = random.randint(-5,5)
    if (ball_x + ball_x_vel> right_pad_x - pads_width) and (right_pad_y < ball_y + ball_y_vel + ball_width < right_pad_y + pads_height):
        ball_x_vel = -ball_x_vel*1.05
        ball_y_vel = (right_pad_y + pads_height/2 - ball_y) / 15
        ball_y_vel = -ball_y_vel
    elif ball_x + ball_x_vel > WIDTH:
        left_score +=1
        ball_x = WIDTH/2
        ball_y = HEIGHT/2
        ball_x_vel = -10
        ball_y_vel = random.randint(-5,5)
    if ball_y + ball_y_vel > HEIGHT or ball_y + ball_y_vel < 0:
        ball_y_vel = -ball_y_vel

    ball_x += ball_x_vel
    ball_y += ball_y_vel

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                left_up = True
            if event.key == pygame.K_s:
                left_down = True
            if event.key == pygame.K_UP:
                right_up = True
            if event.key == pygame.K_DOWN:
                right_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                left_up = False
            if event.key == pygame.K_s:
                left_down = False
            if event.key == pygame.K_UP:
                right_up = False
            if event.key == pygame.K_DOWN:
                right_down = False
    screen.fill(BLACK)
    apply_player_movement()
    apply_ball_movement()
    draw_objects()
    pygame.display.flip()
    pygame.time.wait(delay)