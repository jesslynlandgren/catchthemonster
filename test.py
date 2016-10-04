from browser import doc
# from browser.timer import request_animation_frame as raf
import pygame
import random
import math
import sys

canvas = doc['stage']
ctx = canvas.getContext('2d')

KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275

class Character(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_change = 0
        self.y_change = 0
        self.dead = False

    def render(self,screen):
        screen.blit(self.img,[self.x,self.y])

    def update(self):
        self.x += self.x_change
        self.y += self.y_change

class Hero(Character):
    def __init__(self):
        Character.__init__(self)
        self.name = "hero"
        self.img = pygame.image.load('images/hero.png').convert()
        self.x = 256
        self.y = 240
        self.x_change = 0
        self.y_change = 0

    def update(self,width,height):
        padding = 70
        super(Hero,self).update()
        if self.x > (width-padding):
            self.x_change = -2
        if self.y > (height-padding):
            self.y_change = -2
        if self.x < (padding-25):
            self.x_change = 2
        if self.y < (padding-25):
            self.y_change = 2

class Evil(Character):
    def __init__(self,x,y):
        Character.__init__(self)
        self.x = x
        self.y = y
        self.x_change = 5
        self.y_change = 5

    def update(self,width,height):
        self.x += self.x_change
        self.y += self.y_change
        if self.x > width:
            self.x = 0
        if self.y > height:
            self.y = 0
        if self.x < 0:
            self.x = width
        if self.y <0:
            self.y = height

    def changeDir(self,width,height):
        direction = random.choice(['up','right','down','left'])
        if direction == 'up':
            self.up(width,height)
        elif direction == 'right':
            self.right(width,height)
        elif direction == 'down':
            self.down(width,height)
        else:
            self.left(width,height)

        self.update(width,height)

    def up(self, width, height):
        self.x_change = 0
        self.y_change = -1
        self.update(width,height)

    def right(self, width, height):
        self.x_change = 1
        self.y_change = 0
        self.update(width,height)

    def down(self, width, height):
        self.x_change = 0
        self.y_change = 1
        self.update(width,height)

    def left(self, width, height):
        self.x_change = -1
        self.y_change = 0
        self.update(width,height)

class Monster(Evil):
    def __init__(self,x,y):
        Evil.__init__(self,x,y)
        self.name = "monster"
        self.img = pygame.image.load('images/monster.png').convert()

class Goblin(Evil):
    def __init__(self,x,y):
        Evil.__init__(self,x,y)
        self.name = "goblin"
        self.img = pygame.image.load('images/goblin.png').convert()

def collide(char1,char2):
    dist = math.sqrt((char1.x - char2.x)**2 + (char1.y - char2.y)**2)
    if dist < 32:
        char2.dead = True
        return True
    else:
        return False

def win(newlevel,screen):
    pygame.mixer.music.load('sounds/win.wav')
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 25)
    text = font.render('YOU WIN :) Hit ENTER to play again!', True, (0, 0, 0))
    screen.blit(text, (100, 220))
    pygame.display.update()
    wait()
    main(newlevel)

def lose(screen):
    pygame.mixer.music.load('sounds/lose.wav')
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 25)
    text = font.render('YOU LOSE :( Hit ENTER to play again!', True, (0, 0, 0))
    screen.blit(text, (100, 220))
    pygame.display.update()
    wait()
    main(1)

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main(level):
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.music.load('sounds/music.wav')
    pygame.mixer.music.play(-1)  #infinite loop

    width = 512
    height = 480

    pygame.init()

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Hero vs. MONSTERS!!!')

    clock = pygame.time.Clock()

    bckgrd = pygame.image.load("images/background.png").convert()

    loop_count = 0;

    hero = Hero()
    monster = Monster(random.randrange(0,width),random.randrange(0,height))
    characters = [hero, monster]
    evil = [monster]
    goblins = []
    numGoblins = level + 2
    for g in range(0,numGoblins):
        gb = Goblin(random.randrange(0,width),random.randrange(0,height))
        characters.append(gb)
        evil.append(gb)
        goblins.append(gb)

    stop_game = False
    while not stop_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_DOWN:
                    hero.y_change = 2
                elif event.key == KEY_UP:
                    hero.y_change = -2
                elif event.key == KEY_LEFT:
                    hero.x_change = -2
                elif event.key == KEY_RIGHT:
                    hero.x_change = 2

            if event.type == pygame.KEYUP:
                if event.key == KEY_DOWN:
                    hero.y_change = 0
                elif event.key == KEY_UP:
                    hero.y_change = 0
                elif event.key == KEY_LEFT:
                    hero.x_change = 0
                elif event.key == KEY_RIGHT:
                    hero.x_change = 0

            if event.type == pygame.QUIT:
                stop_game = True

        hero.update(width,height)
        for char in evil:
            if loop_count % 120 == 0:
                char.changeDir(width,height)
            else:
                char.update(width,height)

        if collide(hero,monster):
            win(level+1,screen)

        for goblin in goblins:
            if collide(goblin,hero):
                lose(screen)

        screen.blit(bckgrd,[0,0])

        font = pygame.font.Font(None, 25)
        text = font.render('LEVEL ' + str(level), True, (0, 0, 0),(255,255,255))
        screen.blit(text, (50, 50))

        for char in characters:
            if not char.dead:
                char.render(screen)
            else:
                pass

        pygame.display.update()

        clock.tick(60)

        loop_count += 1


main(1)
