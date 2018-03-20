
from tkinter import *

import random

WIDTH = 900
HEIGHT = 300

PAD_W = 10
PAD_H = 100

BALL_RADIUS = 40
BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0

#очки для каждого игрока
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

#счет скорости
INITIAL_SPEED = 20

root = Tk() #создание окна 
root.title("Пинг-понг") #заголовок окна

c = Canvas(root, width = WIDTH, height = HEIGHT, background = "#00FF00") #объект-холст
c.pack() #упаковщик (отвечает за то, как виджеты будут располагаться на главном окне)
#левая линия
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill = "white")
#правая линия
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill = "white")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill = "white")
#ball
BALL = c.create_oval(WIDTH/2 - BALL_RADIUS/2, HEIGHT/2 - BALL_RADIUS/2, WIDTH/2 + BALL_RADIUS/2, HEIGHT/2 + BALL_RADIUS/2, fill = "#C0C0C0")

#ракетки
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width = PAD_W, fill  = "#DC143C")
#правая ракетка
RIGHT_PAD = c.create_line(WIDTH - PAD_W/2, 0, WIDTH - PAD_W/2, PAD_H, width = PAD_W, fill  = "#DC143C")

#ТЕКСТ ОЧКОВ
p_1_text  = c.create_text(WIDTH - WIDTH/6, PAD_H/4, 
	text = PLAYER_1_SCORE, 
	font = "Arial 20", 
	fill = "aqua")

p_2_text  = c.create_text(WIDTH/6, PAD_H/4, 
	text = PLAYER_2_SCORE, 
	font = "Arial 20", 
	fill = "aqua")

right_side_distance = WIDTH - PAD_W


#скорости ракеток
PAD_SPEED = 20

LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

BALL_SPEED_UP = 1.00

MAX_BALL_SPEED = 30

BALL_X_SPEED = 20
BALL_Y_SPEED = 20

#счет
def update_score(player):
	global PLAYER_1_SCORE, PLAYER_2_SCORE
	if player == "right":
		PLAYER_1_SCORE += 1
		c.itemconfig(p_1_text, text = PLAYER_1_SCORE)
	else:
		PLAYER_2_SCORE += 1
		c.itemconfig(p_2_text, text = PLAYER_2_SCORE)

#респаунд мячика

def spawn_ball():
	global BALL_X_SPEED
	c.coords(BALL, WIDTH/2 - BALL_RADIUS/2, 
		HEIGHT/2 - BALL_RADIUS/2, 
		WIDTH/2 + BALL_RADIUS/2, 
		HEIGHT/2 + BALL_RADIUS/2)
	BALL_X_SPEED = (BALL_X_SPEED*(-INITIAL_SPEED))/abs(BALL_X_SPEED)


def bounce(action):
	global BALL_X_SPEED, BALL_Y_SPEED
	if action == "strike":
		BALL_Y_SPEED = random.randrange(-10, 10)
		if abs(BALL_X_SPEED) < MAX_BALL_SPEED:
			BALL_X_SPEED *= -BALL_SPEED_UP
		else:
			BALL_X_SPEED = - BALL_X_SPEED
	else:
		BALL_Y_SPEED = -BALL_Y_SPEED





#движение мяча
def move_the_ball():
	ball_left, ball_top, ball_right, ball_bttm = c.coords(BALL)
	ball_center = (ball_top + ball_bttm)/2

	if ball_right + BALL_X_SPEED < right_side_distance and ball_left + BALL_X_SPEED > PAD_W:
		c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
	elif ball_right == right_side_distance or ball_left == PAD_W:
		if ball_right > WIDTH/2:
			if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
				bounce("strike")
			else:
				update_score("left")
				spawn_ball()

		else:
			if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
				bounce("strike")
			else:
				update_score("right")
				spawn_ball()
	else:
		if ball_right > WIDTH/2:
			c.move(BALL, right_side_distance - ball_right, BALL_Y_SPEED)
		else:
			c.move(BALL, ball_left + PAD_W, BALL_Y_SPEED)
		if ball_top + BALL_Y_SPEED < 0 or ball_bttm + BALL_Y_SPEED > HEIGHT:
			bounce("ricochet")



#функция движения ракеток
def move_the_pads():

	PADS = {LEFT_PAD: LEFT_PAD_SPEED, RIGHT_PAD: RIGHT_PAD_SPEED}

	for pad in PADS:
		c.move(pad, 0, PADS[pad])

		if c.coords(pad)[1] < 0:
			c.move(pad, 0, -c.coords(pad)[1])
		elif c.coords(pad)[3] > HEIGHT:
			c.move(pad, 0, HEIGHT - c.coords(pad)[3])





def call_again():
	move_the_ball()
	move_the_pads()
	root.after(30, call_again)
#вызов функции
call_again()


#фокус на Canvas (реакция на клавиши)
c.focus_set()

# обработка нажатий клавиш
def move_event(event):
	global LEFT_PAD_SPEED, RIGHT_PAD_SPEED

	if event.keysym == "w":
		LEFT_PAD_SPEED = - PAD_SPEED

	elif event.keysym == "s":
		LEFT_PAD_SPEED = PAD_SPEED

	elif event.keysym == "Up":
		RIGHT_PAD_SPEED = - PAD_SPEED

	elif event.keysym == "Down":
		RIGHT_PAD_SPEED = PAD_SPEED

c.bind("<KeyPress>", move_event)



def stop_the_pad(event):
	global LEFT_PAD_SPEED, RIGHT_PAD_SPEED

	if event.keysym in "ws":
		LEFT_PAD_SPEED = 0

	elif event.keysym in ("Up", "Down"):
		RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_the_pad)

root.mainloop() #запуск окна с игрой


