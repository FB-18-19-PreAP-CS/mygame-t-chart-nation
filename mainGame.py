import pygame
import time
from random import choice
from pygame import math as mt
from pygame.locals import *
import random
WIDTH = 800
HEIGHT = 800
RED = (255,0,0)

class Game:
    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Stalin")
        self.clock = pygame.time.Clock()
        self.mob = Slime1(10)
        self.character = Hero()
        self.existingdoors = []
        
        image1 = pygame.image.load('dunegon.png')
        # Door pattern: left right up down
        self.room1 = Room([LockedDoor(35,360), Door(700,360), HiddenDoor(367,120)], image1)
        self.room2 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room3 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room4 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room5 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room6 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room7 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room8 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room9 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.room10 = Room([LockedDoor(35,360), Door(700,360)], image1)
        self.roomList = [self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7, self.room8, self.room9, self.room10]
        self.currentRoom = choice(self.roomList)
        self.exploredRoomList = []
        self.exploredRoomList.append(self.currentRoom)

    def start(self):
        done = False
        pygame.mixer.music.load('541681556736144.ogg')
        pygame.mixer.music.play(-1)
        self.pastRoom = self.currentRoom
        self.loadRoom(self.currentRoom)
        
        while not done:
            
            self.screen.fill((0,0,0))
            if self.currentRoom != self.pastRoom:
                self.loadRoom(self.currentRoom)
                self.pastRoom = self.currentRoom
                
            if self.currentRoom not in self.exploredRoomList:
                self.exploredRoomList.append(self.currentRoom)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            pressed = pygame.key.get_pressed()
            if not self.character.attacking:
                if pressed[pygame.K_UP]:
                    if not self.checkEdges("up"):
                        self.character.move('up')
                        self.mob.follow(self.character)
                if pressed[pygame.K_DOWN]:
                    if not self.checkEdges("down"):
                        self.character.move('down')
                        self.mob.follow(self.character)
                if pressed[pygame.K_LEFT]:
                    if not self.checkEdges("left"):
                        self.character.move('left')
                        self.mob.follow(self.character)
                if pressed[pygame.K_RIGHT]:
                    if not self.checkEdges("right"):
                        self.character.move('right')
                        self.mob.follow(self.character)
            if pressed[pygame.K_SPACE]:
                self.character.attacking = True
                self.character.attackAnimation = 0
                self.mob.follow(self.character)

            if self.character.attackAnimation != -1:
                self.character.attackAnimation += .25
                self.character.attack(((int(self.character.attackAnimation)) % 7), self.screen)
                if self.character.attackAnimation == 5.75:
                    self.character.attackAnimation = -1
                    self.character.attacking = False 

            self.draw_bg(self.currentRoom.background)
            if not self.character.attacking:
                self.character.draw(self.screen)
                self.mob.draw(self.screen)
            else:
                self.character.draw(self.screen,False,True)
                self.mob.draw(self.screen)
            for door in self.existingdoors:
                door.draw(self.screen)
            pygame.display.flip()

            if self.checkCollisions() == True:
                newRoomLoop = True
                while newRoomLoop:
                    room = choice(self.roomList)
                    if room not in self.exploredRoomList or len(self.exploredRoomList) == len(self.roomList):
                        if len(self.exploredRoomList) == len(self.roomList):
                            pass
                        self.currentRoom = room
                        newRoomLoop = False
            pygame.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        for door in self.existingdoors:
            if self.character.rect.colliderect(door.rect):
                if door.__class__.__name__ != "LockedDoor": # https://stackoverflow.com/questions/45667541/how-to-compare-to-type-of-custom-class
                    return True
        return False

    def checkEdges(self, direction):
        if direction == "up":
            if self.character.rect.y < 50:
                return True
        elif direction == "down":
            if self.character.rect.y > HEIGHT-250:
                return True
        elif direction == "left":
            if self.character.rect.x < 50:
                return True
        elif direction == "right":
            if self.character.rect.x > WIDTH-170:
                return True
        else:
            print("Direction must be cardinal")
        return False


    def loadRoom(self, Room):
        time.sleep(2)
        self.draw_bg(Room.background)
        self.existingdoors = []
        for door in Room.doorList:
            self.existingdoors.append(door)
        self.character.draw(self.screen,True)
        self.mob.draw(self.screen)

    def draw_bg(self, image):
        self.screen.blit(pygame.transform.scale(image, (800,800)),(0,0))
    
        

class Hero:
    def __init__(self):
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('adventurer-idle-00 (1).png')), (120,120))
        self.orientation = "right"
        self.moveRight = []
        self.moveAttack = []
        self.attackAnimation = -1
        self.attacking = False
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'adventurer-run-0{i} (1).png'), (120,120)))
        for i in range(6):
            self.moveAttack.append(pygame.transform.scale(pygame.image.load(f'adventurer-attack2-0{i} (1).png'), (120,120)))
        self.rect = self.animation.get_rect()
        self.rect.x = 100
        self.rect.y = 310

        

    def draw(self,screen, newScreen=False, attack=False):
        if newScreen == True:
            self.rect.x = 100
            self.rect.y = 310
        elif attack == True:
            if self.orientation == "right":
                screen.blit(self.moveAttack[int(self.attackAnimation) % 6], (self.rect.x,self.rect.y))
            else:
                screen.blit(pygame.transform.flip(self.moveAttack[int(self.attackAnimation) % 6],True,False),(self.rect.x,self.rect.y))
        else:
            f = int(self.frame)%6
            if self.orientation == "right":
                screen.blit(self.moveRight[f],(self.rect.x,self.rect.y))
            else:
                screen.blit(pygame.transform.flip(self.moveRight[f],True,False),(self.rect.x,self.rect.y))


    def move(self, direction):
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.orientation = "left"
            self.rect.x -= 5
        else:
            self.orientation = "right"
            self.rect.x += 5
        self.frame += .25

    def attack(self, animation, screen):
        self.draw(screen,False,True)



class Door:
    def __init__(self, spawnx, spawny):
        self.animation = pygame.transform.scale((pygame.image.load('door.png')), (50,50))
        self.rect = self.animation.get_rect()
        self.rect.x = spawnx
        self.rect.y = spawny

    def draw(self,screen):
        screen.blit(self.animation,(self.rect.x,self.rect.y))

class LockedDoor(Door):
    def __init__(self,spawnx,spawny):
        super().__init__(spawnx,spawny)
        self.animation = pygame.transform.scale((pygame.image.load('lockeddoor.PNG')), (50,50))

class HiddenDoor(Door):
    def __init__(self,spawnx,spawny):
        super().__init__(spawnx,spawny)
        self.rect = pygame.Rect(spawnx,spawny,spawnx+50,spawny+50)

    def draw(self,screen):
        pass
  
class Room:
    def __init__(self, doorList, background):
        self.doorList = doorList
        self.background = background
            
        

        
class Enemy(pygame.sprite.Sprite):
    def __init__(self,health,strength,sprite,frames,pos):
        pygame.sprite.Sprite.__init__(self)
        self.health=health
        self.pos=pos
        self.strength=strength
        self.orientation = 'left'
        # self.animation = [pygame.image.load('Slime_Walk_0.png'),pygame.image.load('Slime_Walk_1.png'),pygame.image.load('Slime_Walk_2.png'),pygame.image.load('Slime_Walk_3.png')]
        self.animation = []
        for i in range(4):
            self.animation.append(pygame.image.load(f"Slime_Walk_{i}.png"))
       
        self.frame = 0 
        self.rect = self.animation[0].get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = random.randint(0,400)
    def draw(self,screen):
        f = int(self.frame)%4
        if self.orientation == 'right':
            screen.blit(self.animation[f],(self.rect.x,self.rect.y))
        elif self.orientation == 'left':
            screen.blit(pygame.transform.flip(self.animation[f],True,False),(self.rect.x,self.rect.y))
    def check_dead(self):
        if self.health==0:
            pass
    def move(self,horizontal,vertical):
        if horizontal<0:
            self.orientation='left'
        if horizontal>0:
            self.orientation='right'
        self.rect.x+=horizontal
        self.rect.y+=vertical   
    def attack(self,power):
        pass
        #need to use attack animation and 
        #when to deal damage
class Slime1(Enemy):
    def __init__(self,pos):
        self.count=0
        Enemy.__init__(self,10,1,'Slime_Walk',4,pos)
    def follow(self,hero):
        self.frame+=.2
        self.count+=1
        self.count%=41
        hori='l'
        if hero.rect.x>=self.rect.x:
            hori='r'
        vert='u'
        if hero.rect.y>=self.rect.y:
            vert='d'
        if self.count%40==0:
            for i in range(10):
                if vert=='u' and hori=='l':
                    Enemy.move(self,-3,-3)
                elif vert=='d' and hori=='l':
                    Enemy.move(self,-3,3)
                elif vert=='d' and hori=='r':
                    Enemy.move(self,3,3)
                else:
                    Enemy.move(self,3,-3)
        elif self.count%10==0:
            for i in range(10):
                if vert=='u' and hori=='l':
                    Enemy.move(self,-1,-1)
                elif vert=='d' and hori=='l':
                    Enemy.move(self,-1,1)
                elif vert=='d' and hori=='r':
                    Enemy.move(self,1,1)
                else:
                    Enemy.move(self,1,-1)
       

session = Game()
session.start()