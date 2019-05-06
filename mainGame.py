import pygame
import time
from random import choice

WIDTH = 800
HEIGHT = 800

class Game:
    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Stalin")
        self.clock = pygame.time.Clock()
        # self.bgmusic = pygame.mixer.music.load('/home/cormierc/preAPCS/mygame-t-chart-nation/541681556736144.ogg')
        self.character = Hero()
        self.curr_type = 0
        self.existingdoors = []
        image1 = pygame.image.load('dunegon.png')
        image2 = pygame.image.load('thanos.jpg')
        image3 = pygame.image.load('endgame.png')
        image4 = pygame.image.load('thanos3.jpg')
        image5 = pygame.image.load('thanos4.jpg')
        image2 = pygame.image.load('thanos5.jpg')
        image6 = pygame.image.load('thanos6.jpg')
        image7 = pygame.image.load('thanos7.png')
        image8 = pygame.image.load('loss.png')
        image9 = pygame.image.load('loss2.jpg')
        self.bg = pygame.image.load('R9.png')
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
        self.exploredRoomList = []
        self.exploredRoomList.append(self.currentRoom)
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render('Dungeon Master', True,(255,255,255),(0,0,0))

    def start(self):
        done = False
        # pygame.mixer.music.load('/home/cormierc/preAPCS/mygame-t-chart-nation/541681556736144.ogg')
        # pygame.mixer.music.play(-1)
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
            if pressed[pygame.K_UP]:
                if not self.checkEdges("up"):
                    self.character.move('up')
            if pressed[pygame.K_DOWN]:
                if not self.checkEdges("down"):
                    self.character.move('down')
            if pressed[pygame.K_LEFT]:
                if not self.checkEdges("left"):
                    self.character.move('left')
            if pressed[pygame.K_RIGHT]:
                if not self.checkEdges("right"):
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

            if self.checkCollisions() == True:
                newRoomLoop = True
                while newRoomLoop:
                    room = choice(self.roomList)
                    if room not in self.exploredRoomList or len(self.exploredRoomList) == len(self.roomList):
                        if len(self.exploredRoomList) == len(self.roomList):
                            print("Eyy")
                        self.currentRoom = room
                        newRoomLoop = False

            # self.check_edge()

            self.clock.tick(60)

    def checkCollisions(self):
        for door in self.existingdoors:
            if self.character.rect.colliderect(door.rect):
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
        self.character.draw(self.screen)

    def draw_bg(self, image):
        self.screen.blit(pygame.transform.scale(image, (800,800)),(0,0))

    def text_objects(self,text, font):
        textsurface = font.render(text, True, (255,255,255))
        return textsurface, textsurface.get_rect()
    
    def button(self,msg,x,y,w,h,ic,ac,action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic,(x,y,w,h))

        smalltext = pygame.font.Font("freesansbold.ttf",20)
        textsurf, textrect = self.text_objects(msg,smalltext)
        textrect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textsurf, textrect)
    
    def quitgame(self):
        pygame.quit()
        quit()
    
    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.blit(self.bg,(0,0))
            textrect = self.text.get_rect()
            textrect.center = (500//2,475//2)
            self.screen.blit(self.text,textrect)
            self.button('GO!',300,500,100,50,(0,255,0),(0,200,0),session.start())
            self.button("Quit!",500,500,100,50,(255,0,0),(200,0,0),self.quitgame)

            pygame.display.update()
            self.clock.tick(27)
class Hero:
    def __init__(self):
        self.x = 300
        self.y = 100
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('adventurer-idle-00.png')), (120,120))
        self.orientation = "right"
        self.moveRight = []
        self.moveAttack = []
        self.attackAnimation = 0
        self.attacking = False
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'adventurer-run-0{i}.png'), (120,120)))
        for i in range(6):
            self.moveAttack.append(pygame.transform.scale(pygame.image.load(f'adventurer-attack2-0{i}.png'), (120,120)))
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
        
        
        

session = Game()
session.game_intro()
