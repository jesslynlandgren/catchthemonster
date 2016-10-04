import pygame
import random
import math
import sys

KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275

#Class for all characters (hero, monster, and goblin)
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
        #Set distance of bushes inset (prevent Hero from leaving that box)
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

#Super class for monsters and goblins
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

    #Evil characters randomly change to one of 4 directions every 120 game loops
    def changeDir(self,width,height):
        direction = random.choice(['up','right','down','left'])
        # print direction
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

#Determines if there is a collision between 2 characters
#Character that is the second parameter is the one who will die in collision
def collide(char1,char2):
    dist = math.sqrt((char1.x - char2.x)**2 + (char1.y - char2.y)**2)
    if dist < 32:
        char2.dead = True
        return True
    else:
        return False

#Display changes that occur with a win (hero collides with monster)
def win(newlevel,screen):
    pygame.mixer.music.load('sounds/win.wav')
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 25)
    text = font.render('YOU WIN :) Hit ENTER to play again!', True, (0, 0, 0))
    screen.blit(text, (100, 220))
    pygame.display.update()
    wait()
    main(newlevel)

#Display changes that occur with a loss (goblin collides with hero)
def lose(screen):
    pygame.mixer.music.load('sounds/lose.wav')
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 25)
    text = font.render('YOU LOSE :( Hit ENTER to play again!', True, (0, 0, 0))
    screen.blit(text, (100, 220))
    pygame.display.update()
    wait()
    main(1)

#Waits for the user to press enter to continue the game after a win or lose
def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

#Main method, called recursively with each additional win
def main(level):
    ################################
    #Initialization Code

    #play 8-bit background music
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.music.load('sounds/music.wav')
    pygame.mixer.music.play(-1)  #infinite loop

    # declare the size of the canvas
    width = 512
    height = 480

    # initialize the pygame framework
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((width, height))

    # set window caption
    pygame.display.set_caption('Hero vs. MONSTERS!!!')

    # create a clock
    clock = pygame.time.Clock()

    # Load background image
    bckgrd = pygame.image.load("images/background.png").convert()

    #Create loop counter to set timing of Evil character direction changes
    loop_count = 0;

    #Create Character objects (1 hero, 1 monster, 3+level goblins)
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

    ################################
    # game loop
    stop_game = False
    while not stop_game:
        # look through user events fired
        # Controls navigation of hero character via smooth scrolling with arrow keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # activate the cooresponding speeds
                # when an arrow key is pressed down
                if event.key == KEY_DOWN:
                    hero.y_change = 2
                elif event.key == KEY_UP:
                    hero.y_change = -2
                elif event.key == KEY_LEFT:
                    hero.x_change = -2
                elif event.key == KEY_RIGHT:
                    hero.x_change = 2

            if event.type == pygame.KEYUP:
                # deactivate the cooresponding speeds
                # when an arrow key is released
                if event.key == KEY_DOWN:
                    hero.y_change = 0
                elif event.key == KEY_UP:
                    hero.y_change = 0
                elif event.key == KEY_LEFT:
                    hero.x_change = 0
                elif event.key == KEY_RIGHT:
                    hero.x_change = 0

            if event.type == pygame.QUIT:
                # if they closed the window, set stop_game to True
                # to exit the main loop
                stop_game = True


        #######################################
        # Update Game State

        hero.update(width,height)
        for char in evil:
            if loop_count % 120 == 0:
                char.changeDir(width,height)
            else:
                char.update(width,height)

        #Determine if hero has caught monster = WIN, if so break game loop
        if collide(hero,monster):
            win(level+1,screen)

        #Determine if hero has run into any goblins = LOSS, if so break game loop
        for goblin in goblins:
            if collide(goblin,hero):
                lose(screen)

        #######################################
        #Update Game Display

        #Display game image background
        screen.blit(bckgrd,[0,0])

        #Display current level
        font = pygame.font.Font(None, 25)
        text = font.render('LEVEL ' + str(level), True, (0, 0, 0),(255,255,255))
        screen.blit(text, (50, 50))

        #Render each character every loop - ONLY alive characters
        for char in characters:
            if not char.dead:
                char.render(screen)
            else:
                pass

        # update the canvas display with the currently drawn frame
        pygame.display.update()

        # tick the clock to enforce a max framerate
        clock.tick(60)

        #increase loop iteration count
        loop_count += 1

    # quit pygame properly to clean up resources
    #pygame.quit()

if __name__ == '__main__':
    main(1)
