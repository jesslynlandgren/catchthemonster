#Catch The Monster Game (pygame)

##Summary:
This project is a graphic game run through the command line and created using Python and the pygame module. The game simulates a "chase" where a hero character that is controlled by key input from the user must capture the monster character to win, while simultaneously being chased by goblin characters that will destroy the hero on contact.

This project was completed as part of the Python curriculum for Digital Crafts

##Github Link
[Catch the Monster](https://github.com/jesslynlandgren/catchthemonster)

##Live Demo (In-Progress!)
[Catch the Monster](https://jesslynlandgren.com/catchthemonster.html)

##What was used:
* Python 2.7.12 (Including the following modules):
  - sys
  - pygame
  - random
  - math

##Requirements:
* Python 2 or Python 3

##Goals:
* Three types of characters: Hero, Monster, & Goblin
* Characters should be created using a super and sub class hierarchy
* Hero character should be controlled by user input via arrow keys
* Monster and Goblin characters change movement in one of the four cardinal directions approximately every 2 seconds
* When the Hero and any of the Goblin objects collide, the goblins "kill" the hero and the user loses the round.  When the Hero and the Monster collide, the Hero "kills" the monster and the hero wins the round.
* Display to the user on a collision event whether they won or lost, play a corresponding sound, and allow them to continue playing
* Each time the user wins, there is an additional goblin added to the game (level increases)  There are 3 goblins on the first level.


##Code Snippets
With pygame, the game runs as a loop where the display, attributes, or position of elements are updated at every iteration.  In this game, the game loop runs, checks for inputs from the user, checks the state of elements within the game, makes the programmed changes to the elements, and then displays all the game elements in their updated states. The Catch the Monster game loop is inside a main function that allows the game to be restarted by the user after a win or loss of the game.

The objects in the pygame window are moved by setting an initial position and an incremental change from one loop iteration to another.  By manipulating this incremental change value, the direction and speed of objects within the display window can be modified.  The starting super class is class Character that sets the position instance variables and basic methods for updating the position of a character and also rendering it to the game display.  The subclasses of class Character are Hero and Evil.  The subclasses of class Evil are Monster and Goblin.

```Python
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
```
The characters for each level are initialized using these classes
```Python
#Create Character objects (1 hero, 1 monster, 2+level goblins)
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
```
A collision between two characters is what determines a win or loss.  A collision is detected if the proximity of two characters is above a hard-coded threshold.
```Python
#Determines if there is a collision between 2 characters
#Character that is the second parameter is the one who will die in collision
def collide(char1,char2):
    dist = math.sqrt((char1.x - char2.x)**2 + (char1.y - char2.y)**2)
    if dist < 32:
        char2.dead = True
        return True
    else:
        return False
```
The win and loss events execute similar functions that display a message, play a sound using pygame.mixer.music, and allow the user to continue playing.  In the win function, the loop restarts with an increased level (more goblins!)
```Python
#Determine if hero has caught monster = WIN, if so break game loop
    if collide(hero,monster):
        win(level+1,screen)

    #Determine if hero has run into any goblins = LOSS, if so break game loop
    for goblin in goblins:
        if collide(goblin,hero):
            lose(screen)
```

```Python
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
```

##Screenshots

![CatchTheMonster1](/images/screenshots/cthm3.png)
![CatchTheMonster1](/images/screenshots/cthm1.png)
![CatchTheMonster1](/images/screenshots/cthm2.png)
