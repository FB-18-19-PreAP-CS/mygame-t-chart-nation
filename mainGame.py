import pygame
import time

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
        # self.bgmusic = pygame.mixer.Sound('/home/blackn/preAPCS/mygame_purdy/sounds/main_theme.ogg')
        self.character = Hero()
        self.curr_type = 0
        self.existingdoors = []
        image1 = pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/dunegon.png')
        self.room1 = Room([Door(60,360), Door(700,360)], image1)
        self.room2 = Room([Door(50,200), Door(600,260)], image1)
        self.currentRoom = self.room1

    def start(self):
        done = False
        # self.bgmusic.play(-1)
        self.pastRoom = self.currentRoom
        self.loadRoom(self.currentRoom)
        while not done:
            self.screen.fill((0,0,0))
            if self.currentRoom != self.pastRoom:
                self.loadRoom(self.currentRoom)
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

            self.draw_bg(self.currentRoom.background)
            self.character.draw(self.screen)
            for door in self.existingdoors:
                door.draw(self.screen)
            # self.character.blitme(self.screen)
            pygame.display.flip()

            if self.checkCollisions() == True:
                self.pastRoom = self.currentRoom
                if self.currentRoom == self.room1:
                    self.currentRoom = self.room2
                else:
                    self.currentRoom = self.room2


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
        for door in Room.doorList:
            self.existingdoors.append(door)

    def draw_bg(self, image):
        self.screen.blit(pygame.transform.scale(image, (800,800)),(0,0))

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 20
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-idle-00.png')), (120,120))
        self.orientation = "right"
        self.moveRight = []
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-run-0{i}.png'), (120,120)))
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
session.start()
