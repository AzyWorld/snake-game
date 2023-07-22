from typing import Any
import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
import sys, random, numpy


class SnakeHead:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vector = [0, -1]
        self.vector_que = [0, -1]

class SnakeBodyFragment:
    def __init__(self, x, y, vector):
        self.pos = [x, y]
        self.vector = vector

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TextObject:
    def __init__(self, x, y, text, tSize=30, tFont="Halogen.ttf", tColor=(255, 255, 255)):
        self.x = x
        self.y = y
        self.label = text
        self.tFont = tFont
        self.tSize = tSize
        self.tColor = tColor
        self.text = pg.font.Font(tFont, tSize).render(self.label, tColor, (255, 255, 255))
    def draw(self):
        self.text = pg.font.Font(self.tFont, self.tSize).render(self.label, (255, 255, 255), self.tColor)
        win.blit(self.text, (self.x-self.text.get_width()/2, self.y-self.text.get_height()/2))

class Theme:
    def __init__(self, snakeColor1, snakeColor2, appleColor, BgColor, name, txtColor=(255,255,255), cost=10):
        self.snColor1 = snakeColor1
        self.snColor2 = snakeColor2
        self.appleColor = appleColor
        self.bgColor = BgColor
        self.name = name
        self.cost = cost
        self.txtColor = txtColor

pg.init()
pg.font.init()

win = pg.display.set_mode((720, 480))
clock = pg.time.Clock()
pg.display.set_caption("SNAKE")

score = 0

snake = SnakeHead(360, 240)
segments = [snake]

data = open("Saved.txt", "r+")
data1 = data.readlines()
money = int(data1[0].split(' ')[1])

themes = [
    Theme((10, 220, 10), (10, 190, 10), (200, 10, 10), (0, 0, 0), "Base"),
    Theme((200, 10, 10), (230, 10, 10), (10, 200, 10), (0, 0, 0), "Reversed", cost=20),
    Theme((255, 255, 255), (240, 240, 240), (255, 255, 255), (0, 0, 0), "White-Black", cost=10),
    Theme((200, 10, 10), (230, 10, 10), (10, 200, 10), (240, 240, 240), "Reversed-Light", txtColor=(0,0,0), cost=20),
    Theme((10, 220, 10), (10, 190, 10), (200, 10, 10), (240, 240, 240), "Light", txtColor=(0,0,0), cost=10),
    Theme((0, 0, 0), (20, 20, 20), (0, 0, 0), (255, 255, 255), "Black-White", txtColor=(0,0,0), cost=10),
    Theme((34, 40, 49), (57, 62, 70), (0, 173, 181), (238, 238, 238), "Estonian", txtColor=(0,0,0), cost=30),
    Theme((238, 238, 238), (238, 238, 238), (0, 173, 181), (34, 40, 49), "Dark-Estonian",  cost=30),
]

opened_themes = []
for i in data1[1].split(' '):
    if i != "OpenedThemes:":
        opened_themes.append(int(i))

currentTheme = int(data1[2].split(' ')[1])

def lose():
    global segments, apple, score_text, restart_button, menu_button, money
    segments = []
    apple = None
    score_text.y = 85
    score_text.tSize = 60
    restart_button.show()
    menu_button.hide()
    menu_button = menu_button = Button(win, 300, 300, 120, 80, text="menu", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 30))

def restart():
    global score, segments, snake, restart_button, score_text, menu_button, apple, money
    restart_button.hide()
    score_text.y = 25
    score_text.tSize = 30
    score = 0
    apple = None
    segments = [snake]
    snake.pos = [360, 240]
    money += score
    menu_button.hide()
    menu_button = Button(win, 10, 10, 50, 30, text="menu", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))

def game():
    global score, snake, segments, clock, win, restart_button, menu_button, score_text, apple, money

    Processing = True
    Frame = 0
    score_text.tColor = themes[currentTheme].txtColor
    bgColor = themes[currentTheme].bgColor
    restart()

    while Processing:
        Frame += 1
        win.fill(bgColor)
        
        if menu_button.clicked:
            menu_button.clicked = False
            money += score
            main_menu()
            break

        keystate = pg.key.get_pressed()
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                data.seek(0)
                data.write("")
                data.truncate()
                data.write("Money: " + str(money) + "\nOpenedThemes:")
                for i in opened_themes:
                    data.write(" " + str(i))
                data.write("\nCurrentTheme: " + str(currentTheme))
                data.close()
                data.close()
                sys.exit()
        if keystate[pg.key.key_code("w")] and snake.vector[1] != 1:
            snake.vector_que = [0, -1]
        if keystate[pg.key.key_code("s")] and snake.vector[1] != -1:
            snake.vector_que = [0, 1]
        if keystate[pg.key.key_code("d")] and snake.vector[0] != -1:
            snake.vector_que = [1, 0]
        if keystate[pg.key.key_code("a")] and snake.vector[0] != 1:
            snake.vector_que = [-1, 0]

        if apple != None and len(segments) > 0 and [snake.pos[0]%720, snake.pos[1]%480] == [apple.x, apple.y]:
            score += 1
            apple = Apple(random.randint(6, 35)*20, random.randint(6, 23)*20)
            segments.append(SnakeBodyFragment(snake.pos[0], snake.pos[1], [0,0]))
        elif apple == None and len(segments) > 0:
            apple = Apple(random.randint(6, 35)*20, random.randint(6, 23)*20)

        if Frame == 6:
            Frame = 0
            snake.vector = [snake.vector_que[0], snake.vector_que[1]]
            for i, segment in enumerate(segments):
                if i != 0:
                    if segment.pos == snake.pos:
                        lose()
                segment.pos[0] += segment.vector[0]*20
                segment.pos[1] += segment.vector[1]*20
                if i != 0 and len(segments) > 1:
                    segment.vector = [(segments[i-1].pos[0] - segment.pos[0])/20, (segments[i-1].pos[1] - segment.pos[1])/20]

        for i, seg in enumerate(segments):
            pg.draw.rect(win, themes[currentTheme].snColor1, (seg.pos[0]%720, seg.pos[1]%480, 20, 20))
        if apple != None:
            pg.draw.rect(win, themes[currentTheme].appleColor, (apple.x, apple.y, 20, 20))

        score_text.label = "Score: " + str(score)
        score_text.draw()

        pg_w.update(events)
        pg.display.update()
        clock.tick(60)

def main_menu():
    global money, menu_button
    Processing = True
    menu_button.hide()
    restart_button.hide()
    shop_button.show()
    play_button.show()
    win.fill((0, 0, 0))
    while Processing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                data.seek(0)
                data.write("")
                data.truncate()
                data.write("Money: " + str(money) + "\nOpenedThemes:")
                for i in opened_themes:
                    data.write(" " + str(i))
                data.write("\nCurrentTheme: " + str(currentTheme))
                data.close()
                data.close()
                sys.exit()
        
        if play_button.clicked:
            play_button.clicked = False
            play_button.hide()
            shop_button.hide()
            game()
            break
        if shop_button.clicked:
            shop_button.clicked = False
            play_button.hide()
            shop_button.hide()
            shop()
            break

        name_text = TextObject(360, 50, "SNAKE", tSize=50)
        name_text.draw()

        pg_w.update(pg.event.get())
        pg.display.update()
        clock.tick(60)

def shop():
    global money, win, currentTheme, menu_button, opened_themes
    Processing = True
    menu_button = Button(win, 10, 10, 50, 30, text="menu", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
    menu_button.show()

    left_theme_button = Button(win, 10, 80, 20, 140, text="<", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
    right_theme_button = Button(win, 690, 80, 20, 140, text=">", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
    buy_buttons = []
    theme_counter = 0

    while Processing:
        win.fill((0, 0, 0))
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                data.seek(0)
                data.write("")
                data.truncate()
                data.write("Money: " + str(money) + "\nOpenedThemes:")
                for i in opened_themes:
                    data.write(" " + str(i))
                data.write("\nCurrentTheme: " + str(currentTheme))
                data.close()
                Processing = False
                sys.exit()

        if left_theme_button.clicked:
            left_theme_button.clicked = False
            if theme_counter > 0:
                theme_counter -= 1
        if right_theme_button.clicked:
            right_theme_button.clicked = False
            if theme_counter+5 < len(themes):
                theme_counter += 1
        for i, button in enumerate(buy_buttons):
            button.hide()
            if button.clicked:
                if button.string == "use":
                    currentTheme = i+theme_counter
                elif button.string == "buy" and themes[i+theme_counter].cost <= money:
                    money -= themes[i+theme_counter].cost
                    opened_themes.append(i+theme_counter)
        buy_buttons = []
        for i in range(5):
            if theme_counter+4 < len(themes):
                pg.draw.rect(win, (255, 255, 255), (38 + i*130, 78, 124, 124))
                pg.draw.rect(win, rect=(40 + i*130, 80, 120, 120), color=(themes[i+theme_counter].bgColor))
                pg.draw.rect(win, rect=(60 + i*130, 110, 20, 20), color=themes[i+theme_counter].snColor2)
                pg.draw.rect(win, rect=(60 + i*130, 130, 20, 20), color=themes[i+theme_counter].snColor1)
                pg.draw.rect(win, rect=(80 + i*130, 110, 20, 20), color=themes[i+theme_counter].snColor1)
                pg.draw.rect(win, rect=(60 + i*130, 150, 20, 20), color=themes[i+theme_counter].snColor2)
                pg.draw.rect(win, rect=(120 + i*130, 110, 20, 20), color=themes[i+theme_counter].appleColor)
                if i+theme_counter in opened_themes:
                    buy_buttons.append(Button(win, 38 + i*130, 203, 95, 20, text="use", font=pg.font.Font("Halogen.ttf", 15), inactiveColour=(50, 50, 50), textColour=(255, 255, 255)))
                    if i+theme_counter == currentTheme:
                        buy_buttons[-1].inactiveColour = (10, 10, 10)
                        buy_buttons[-1].hoverColour = (10, 10, 10)
                        buy_buttons[-1].pressedColour = (10, 10, 10)
                else:
                    buy_buttons.append(Button(win, 38 + i*130, 203, 95, 20, text="buy", font=pg.font.Font("Halogen.ttf", 15), inactiveColour=(50, 50, 50), textColour=(255, 255, 255)))
                theme_name = TextObject(105 + 130*i, 65, themes[i+theme_counter].name, tSize=15)
                theme_cost = TextObject(150 + 130*i, 215, str(themes[i+theme_counter].cost), tSize=20, tColor=(200, 200, 10))
                theme_cost.draw()
                theme_name.draw()

        if menu_button.clicked:
            menu_button.clicked = False
            left_theme_button.hide()
            right_theme_button.hide()
            for i in buy_buttons:
                i.hide()
            buy_buttons = []
            main_menu()
            break
        
        money_text = TextObject(630, 25, "Money: " + str(money))
        money_text.draw()

        pg_w.update(events)
        pg.display.update()
        clock.tick(60)


restart_button = Button(win, 300, 200, 120, 80, text="restart", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 30), onClick=restart)
score_text = TextObject(360, 25, "Score: " + str(score), tColor=themes[currentTheme].txtColor)
restart_button.hide()

menu_button = Button(win, 10, 10, 50, 30, text="menu", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
play_button = Button(win, 300, 220, 120, 40, text="play", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
shop_button = Button(win, 300, 300, 120, 40, text="shop", inactiveColour=(50, 50, 50), textColour=(255, 255, 255), font=pg.font.Font("Halogen.ttf", 15))
main_menu()
