import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
import sys, random


class SnakeHead:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.pos_t = [x, y]
        self.vector = [0, -1]
        self.vector_que = [0, -1]

class SnakeBodyFragment:
    def __init__(self, x, y, vector):
        self.pos = [x, y]
        self.pos_t = [x, y]
        self.vector = vector
        self.num = 0

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y


pg.init()
pg.font.init()


WIDTH = 720
HEIGHT = 480

win = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("SNAKE")

win.fill((0,0,0))

score = 0

snake = SnakeHead(360, 240)
segments = [snake]

my_font = pg.font.Font("Halogen.ttf", 30)

def restart():
    global score
    global segments
    global snake
    global restart_button
    global score_txt_pos
    restart_button.hide()
    restart_button = Button(win, 10, 10, 50, 30, text="restart", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15), onClick=restart)
    score_txt_pos = [0, 10]
    score = 0
    segments = [snake]
    snake.pos = [360, 240]

restart_button = Button(win, 10, 10, 50, 30, text="restart", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15), onClick=restart)
score_txt_pos = [0, 10]

def game():
    global score
    global snake
    global segments
    global clock
    global win
    global my_font
    global restart_button
    global score_txt_pos
    Processing = True
    apple = None
    Frame = 0

    while Processing:

        Frame += 1

        win.fill((0,0,0))

        if apple == None:
            apple = Apple(random.randint(6, 35)*20, random.randint(6, 23)*20)

        keystate = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Processing = False
                sys.exit()
                break
        if keystate[pg.key.key_code("w")] and snake.vector[1] != 1:
            snake.vector_que[1], snake.vector_que[0] = -1, 0
        if keystate[pg.key.key_code("s")] and snake.vector[1] != -1:
            snake.vector_que[1], snake.vector_que[0] = 1, 0
        if keystate[pg.key.key_code("d")] and snake.vector[0] != -1:
            snake.vector_que[0], snake.vector_que[1] = 1, 0
        if keystate[pg.key.key_code("a")] and snake.vector[0] != 1:
            snake.vector_que[0], snake.vector_que[1] = -1, 0

        if [snake.pos[0]%720, snake.pos[1]%480] == [apple.x, apple.y]:
            apple = None
            score += 1
            segments.append(SnakeBodyFragment(snake.pos[0], snake.pos[1], [0,0]))
        
        if Frame == 10:
            Frame = 0
            snake.vector[0], snake.vector[1] = snake.vector_que[0], snake.vector_que[1]
            for i, segment in enumerate(segments):
                if i != 0:
                    if segment.pos == snake.pos:
                        segments = []
                        score_txt_pos[1] = 75
                        restart_button.hide()
                        restart_button = Button(win, 300, 200, 120, 80, text="restart", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 30), onClick=restart)
                segment.pos[0] += segment.vector[0]*20
                segment.pos[1] += segment.vector[1]*20
                if i != 0 and len(segments) > 1:
                    segment.vector = [(segments[i-1].pos[0] - segment.pos[0])/20, (segments[i-1].pos[1] - segment.pos[1])/20]
        for i, seg in enumerate(segments):
            pg.draw.rect(win, (10, 190+i%2*30, 10), (seg.pos[0]%720, seg.pos[1]%480, 20, 20))
        if apple != None:
            pg.draw.rect(win, (200, 10, 10), (apple.x, apple.y, 22, 22))

        score_text = my_font.render("Score: " + str(score), (255, 255, 255), (255, 255, 255))
        win.blit(score_text, (360-score_text.get_width()/2, score_txt_pos[1]))

        pg_w.update(pg.event.get())
        pg.display.update()
        clock.tick(60)

game()

def main_menu():
    pass