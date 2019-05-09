import pygame
WIDTH = 800
HEIGHT = 800
from pygame import math as mt
from random import randint
win = pygame.display.set_mode((500,480))
class enemy(object):
    walkRight = [pygame.image.load('Slime_Walk_0.png'), pygame.image.load('Slime_Walk_1.png'), pygame.image.load('Slime_Walk_2.png'), pygame.image.load('Slime_Walk_3.png')]
    walkLeft = [pygame.image.load('Slime_Walk_0.png'), pygame.image.load('Slime_Walk_1.png'), pygame.image.load('Slime_Walk_2.png'), pygame.image.load('Slime_Walk_3.png')]
    # Goes inside the enemy class
    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x > self.path[0] - self.vel: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
    # Goes inside the enemy class
    def draw(self, screen):
        self.move()
        if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33. 
                                    # We will show each image for 3 frames. 3 x 11 = 33.
            self.walkCount = 0
            
        if self.vel > 0: # If we are moving to the right we will display our walkRight images
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:  # Otherwise we will display the walkLeft images
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
    
class Game:

    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        goblin = enemy(100, 410, 64, 64, 300)
        goblin.draw(win)
        pygame.display.set_caption("Stalin")
        self.clock = pygame.time.Clock()
        # self.bgmusic = pygame.mixer.Sound('/home/blackn/preAPCS/mygame_purdy/sounds/main_theme.ogg')
        self.character = Hero()
        # self.room_types = ['street','forrest']
        self.curr_type = 0

    def start(self):
        done = False
        # self.bgmusic.play(-1)
        while not done:
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                self.character.move('up')
            if pressed[pygame.K_DOWN]:
                self.character.move('down')
            if pressed[pygame.K_LEFT]:
                self.character.move('left')
            if pressed[pygame.K_RIGHT]:
                self.character.move('right')

            self.draw_bg()
            pygame.display.flip()
            self.character.draw(self.screen)
            
            # self.character.blitme(self.screen)
            pygame.display.flip()

            # self.check_edge()

            self.clock.tick(60)

    def draw_bg(self):
       
        self.screen.blit(pygame.image.load('dunegon.png'),(100,50))
        self.screen.blit(pygame.image.load('Slime_Walk_1.png'),(100,50))

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 20
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('/home/torresa/PreApcs/mygame-t-chart-nation/images/adventurer-idle-00.png')), (120,120))
        self.moveRight = []
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'/home/torresa/PreApcs/mygame-t-chart-nation/images/adventurer-run-0{i}.png'), (120,120)))
        self.rect = self.animation.get_rect()
        self.rect.x = 120
        self.rect.y = 120

        

    def draw(self,screen):
        f = int(self.frame)%6
        screen.blit(self.moveRight[f],(self.rect.x,self.rect.y))

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.rect.x -= 5
        else:
            self.rect.x += 5
        self.frame += .25

session = Game()
session.start()

 


    
        
        
    

