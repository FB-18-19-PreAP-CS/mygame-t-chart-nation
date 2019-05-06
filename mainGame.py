import pygame
import time
from random import choice
WIDTH = 800
HEIGHT = 800
class Enemy(pygame.sprite.Sprite):
    '''
    Spawn an enemy
    '''
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Slime_Walk_1")
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
    def move(self):
        distance = 20
        speed = 15
        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance*2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

class Game:
    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Stalin")
        self.clock = pygame.time.Clock()
        self.bgmusic = pygame.mixer.music.load('541681556736144.ogg')
        self.character = Hero()
        self.curr_type = 0
        self.existingdoors = []
        image1 = pygame.image.load('dunegon.png')
        image2 = pygame.image.load('dunegon.png')
        image3 = pygame.image.load('dunegon.png')
        image4 = pygame.image.load('dunegon.png')
        image5 = pygame.image.load('dunegon.png')
        image2 = pygame.image.load('dunegon.png')
        image6 = pygame.image.load('dunegon.png')
        image7 = pygame.image.load('dunegon.png')
        image8 = pygame.image.load('dunegon.png')
        image9 = pygame.image.load('dunegon.png')
        self.room1 = Room([Door(60,360), Door(700,360)], image1)
        self.room2 = Room([Door(60,360), Door(700,360)], image2)
        self.room3 = Room([Door(60,360), Door(700,360)], image3)
        self.room4 = Room([Door(60,360), Door(700,360)], image4)
        self.room5 = Room([Door(60,360), Door(700,360)], image5)
        self.room6 = Room([Door(60,360), Door(700,360)], image6)
        self.room7 = Room([Door(60,360), Door(700,360)], image7)
        self.room8 = Room([Door(60,360), Door(700,360)], image8)
        self.room9 = Room([Door(60,360), Door(700,360)], image9)
        self.room10 = Room([Door(60,360), Door(700,360)], image1)
        self.roomList = [self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7, self.room8, self.room9, self.room10]
        self.currentRoom = choice(self.roomList)

    def start(self):
        enemy   = Enemy(20,200,'yeti.png')# spawn enemy
        enemy_list = pygame.sprite.Group()   # create enemy group 
        enemy_list.add(enemy)       
        goblin = enemy(100, 410, 64, 64, 300)
        done = False
        pygame.mixer.music.load('541681556736144.ogg')
        pygame.mixer.music.play(-1)
        self.pastRoom = self.currentRoom
        self.loadRoom(self.currentRoom)
        while not done:
            enemy_list.draw(self.screen)
            for e in enemy_list:
                e.move()
            self.screen.fill((0,0,0))
            if self.currentRoom != self.pastRoom:
                self.loadRoom(self.currentRoom)
                self.pastRoom = self.currentRoom
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
            if pressed[pygame.K_SPACE]:
                self.character.attackAnimation = 1
            if self.character.attackAnimation != 0:
                self.character.attack(self.character.attackAnimation-1, self.screen)
                self.character.attackAnimation = (self.character.attackAnimation + 1) % 6 

            self.draw_bg(self.currentRoom.background)
            self.character.draw(self.screen)
            for door in self.existingdoors:
                door.draw(self.screen)
            pygame.display.flip()
            goblin = enemy(100, 410, 64, 64, 300)
            goblin.draw(self.screen)
            pygame.display.update()
            if self.checkCollisions() == True:
                self.currentRoom = choice(self.roomList)


            # self.check_edge()

            self.clock.tick(60)

    def checkCollisions(self):
        for door in self.existingdoors:
            if self.character.rect.colliderect(door.rect):
                return True
        return False


    def loadRoom(self, Room):
        time.sleep(2)
        self.draw_bg(Room.background)
        self.existingdoors = []
        for door in Room.doorList:
            self.existingdoors.append(door)
        self.character.draw(self.screen)

    def draw_bg(self, image):
        
        self.screen.blit(pygame.transform.scale(image, (800,800)),(0,0))
        
class Hero:
    def __init__(self):
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('adventurer-idle-00 (1).png')), (120,120))
        self.orientation = "right"
        self.moveRight = []
        self.moveAttack = []
        self.attackAnimation = 0
        self.attacking = False
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'adventurer-run-0{i} (1).png'), (120,120)))
        for i in range(6):
            self.moveAttack.append(pygame.transform.scale(pygame.image.load(f'adventurer-attack2-0{i} (1).png'), (120,120)))
        self.rect = self.animation.get_rect()
        self.rect.x = 120
        self.rect.y = 120

        

    def draw(self,screen):
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
        screen.blit(self.moveAttack[animation],(self.rect.x,self.rect.y))



class Door:
    def __init__(self, spawnx, spawny):
        self.animation = pygame.transform.scale((pygame.image.load('door.png')), (50,50))
        self.rect = self.animation.get_rect()
        self.rect.x = spawnx
        self.rect.y = spawny

    def draw(self,screen):
        screen.blit(self.animation,(self.rect.x,self.rect.y))

    
class Room:
    def __init__(self, doorList, background):
        self.doorList = doorList
        self.background = background
        
        
        




