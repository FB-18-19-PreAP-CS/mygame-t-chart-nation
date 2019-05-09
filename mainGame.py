import pygame
import time
from random import choice, randint

WIDTH = 800
HEIGHT = 800
EDGEXL = 85
EDGEXR = WIDTH - 170
EDGEYT = 85
EDGEYB = HEIGHT - 200

class Game:
    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()

        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render('Dungeon Master', True,(255,255,255),(0,0,0))

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Stalin")
        self.clock = pygame.time.Clock()
        self.character = Hero()
        self.existingdoors = []
        self.existingwalls = []
        self.existingItems = []
        image1 = pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/dunegon.png')
        self.room1 = Room([LockedDoor(35,360), Door(700,360), HiddenDoor(300,300)], [], image1)
        self.room2 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room3 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room4 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room5 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room6 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room7 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room8 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room9 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.room10 = Room([LockedDoor(35,360), Door(700,360)], [], image1)
        self.hiddenRoom = HiddenRoom([Door(700,360)],[],image1)
        self.roomList = [self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7, self.room8, self.room9, self.room10]
        self.currentRoom = self.room1 #choice(self.roomList)
        self.exploredRoomList = []
        self.exploredRoomList.append(self.currentRoom)

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
            self.screen.fill((0,0,0))
            textrect = self.text.get_rect()
            textrect.center = (WIDTH//2,300)
            self.screen.blit(self.text,textrect)
            self.button('GO!',200,400,100,50,(0,255,0),(0,200,0),self.start)
            self.button("Quit!",500,400,100,50,(255,0,0),(200,0,0),self.quitgame)

            pygame.display.update()
            self.clock.tick(60)

    def start(self):
        done = False
        pygame.mixer.music.load('/home/blackn/preAPCS/mygame-t-chart-nation/541681556736144.ogg')
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
                    if not self.checkEdges("up") and not self.checkWalls("up"):
                        self.character.move('up')
                    elif self.checkEdges("up") == True:
                        self.character.rect.y = EDGEYT
                if pressed[pygame.K_DOWN]:
                    if not self.checkEdges("down") and not self.checkWalls("down"):
                        self.character.move('down')
                    elif self.checkEdges("down") == True:
                        self.character.rect.y = EDGEYB
                if pressed[pygame.K_LEFT]:
                    if not self.checkEdges("left") and not self.checkWalls("left"):
                        self.character.move('left')
                    elif self.checkEdges("left") == True:
                        self.character.rect.x = EDGEXL
                if pressed[pygame.K_RIGHT]:
                    if not self.checkEdges("right") and not self.checkWalls("right"):
                        self.character.move('right')
                    elif self.checkEdges("right") == True:
                        self.character.rect.x = EDGEXR
            if pressed[pygame.K_SPACE]:
                self.character.attacking = True
                self.character.attackAnimation = 0
            if self.character.attackAnimation != -1:
                self.character.attackAnimation += .25
                self.character.attack(((int(self.character.attackAnimation)) % 7), self.screen)
                if self.character.attackAnimation == 5.75:
                    self.character.attackAnimation = -1
                    self.character.attacking = False 

            self.draw_bg(self.currentRoom.background)
            if not self.character.attacking:
                self.character.draw(self.screen)
            else:
                self.character.draw(self.screen,False,True)
            for door in self.existingdoors:
                door.draw(self.screen)
            for item in self.existingItems:
                item.draw(self.screen)
            pygame.display.flip()

            if self.checkItems() == True:
                if self.existingItems[0].__class__.__name__ == "Defense_up":
                    self.character.defense += 1
                elif self.existingItems[0].__class__.__name__ == "Speed_up":
                    self.character.speed += 1
                else:
                    self.character.health += 1
                print(self.character.health,self.character.defense,self.character.speed)
                self.existingItems = []
                self.loadRoom(self.room1)
                

            if self.checkDoors() != "HiddenDoor" and self.checkDoors() != "None":
                newRoomLoop = True
                while newRoomLoop:
                    room = choice(self.roomList)
                    if room not in self.exploredRoomList or len(self.exploredRoomList) == len(self.roomList):
                        if len(self.exploredRoomList) == len(self.roomList):
                            pass
                        self.currentRoom = room
                        newRoomLoop = False
            elif self.checkDoors() == "HiddenDoor":
                self.loadRoom(self.hiddenRoom)
            pygame.display.update()
            self.clock.tick(60)

    def checkItems(self):
        for item in self.existingItems:
            if self.character.rect.colliderect(item.rect):
                return True
        return False

    def checkDoors(self):
        for door in self.existingdoors:
            if self.character.rect.colliderect(door.rect):
                if door.__class__.__name__ != "LockedDoor": # https://stackoverflow.com/questions/45667541/how-to-compare-to-type-of-custom-class
                    return str(door.__class__.__name__)
                if door.__class__.__name__ == "HiddenDoor":
                    return "HiddenDoor"
        return "None"

    def checkWalls(self,direction):
        for wall in self.existingwalls:
            if direction == "up":
                self.character.rect.y -= (5 + (2.5 * self.character.speed))
                if self.character.rect.colliderect(wall.rect):
                    self.character.rect.y += (5 + (2.5 * self.character.speed))
                    return True
                self.character.rect.y += (5 + (2.5 * self.character.speed))
            if direction == "down":
                self.character.rect.y += (5 + (2.5 * self.character.speed))
                if self.character.rect.colliderect(wall.rect):
                    self.character.rect.y -= (5 + (2.5 * self.character.speed))
                    return True
                self.character.rect.y -= (5 + (2.5 * self.character.speed))
            if direction == "left":
                self.character.rect.x -= (5 + (2.5 * self.character.speed))
                if self.character.rect.colliderect(wall.rect):
                    self.character.rect.x += (5 + (2.5 * self.character.speed))
                    return True
                self.character.rect.x += (5 + (2.5 * self.character.speed))
            if direction == "right":
                self.character.rect.x += (5 + (2.5 * self.character.speed))
                if self.character.rect.colliderect(wall.rect):
                    self.character.rect.x -= (5 + (2.5 * self.character.speed))
                    return True
                self.character.rect.x -= (5 + (2.5 * self.character.speed))
        return False

    def checkEdges(self, direction):
        if direction == "up":
            if self.character.rect.y < 85:
                return True
        elif direction == "down":
            if self.character.rect.y > HEIGHT-200:
                return True
        elif direction == "left":
            if self.character.rect.x < 85:
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
        for wall in Room.wallList:
            self.existingwalls.append(wall)
        self.character.draw(self.screen,True)
        print(Room.__class__.__name__)
        if Room.__class__.__name__ == "HiddenRoom":
            self.generateItem()

    def generateItem(self):
        choice = randint(1,3)
        if choice == 1:
            item = Health_up()
        elif choice == 2:
            item = Defence_up()
        else:
            item = Speed_up()
        self.existingItems.append(item)


    def draw_bg(self, image):
        self.screen.blit(pygame.transform.scale(image, (800,800)),(0,0))

class Hero:
    def __init__(self):
        self.health = 3
        self.defense = 0
        self.speed = 0
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-idle-00.png')), (80,80))
        self.orientation = "right"
        self.moveRight = []
        self.moveAttack = []
        self.attackAnimation = -1
        self.attacking = False
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-run-0{i}.png'), (80,80)))
        for i in range(6):
            self.moveAttack.append(pygame.transform.scale(pygame.image.load(f'/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-attack2-0{i}.png'), (80,80)))
        self.rect = pygame.Rect(0,0,80,80)
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
            self.rect.y -= (5 + (1.5 * self.speed))
        elif direction == "down":
            self.rect.y += (5 + (1.5 * self.speed))
        elif direction == "left":
            self.orientation = "left"
            self.rect.x -= (5 + (1.5 * self.speed))
        else:
            self.orientation = "right"
            self.rect.x += (5 + (1.5 * self.speed)) 
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
        self.rect = pygame.Rect(spawnx,spawny,50,50)

    def draw(self,screen):
        pass
  
class Room:
    def __init__(self, doorList, wallList, background):
        self.doorList = doorList
        self.wallList = wallList
        self.background = background

class HiddenRoom(Room):
    def __init__(self,doorList,wallList,background):
        super().__init__(doorList,wallList,background)

class Wall:
    def __init__(self,spawnx,spawny,lenx,leny):
        self.rect = pygame.Rect(spawnx,spawny,spawnx+lenx,spawny+leny)

    def draw(self):
        pass

class Item:
    def __init__(self,sprite):
        self.sprite = pygame.transform.scale((pygame.image.load(f'{sprite}')), (25,25))
        self.rect = self.sprite.get_rect()
        self.rect.x,self.rect.y = 250,400

    def draw(self,screen):
        screen.blit(self.sprite,(self.rect.x,self.rect.y))

class Health_up(Item):
    def __init__(self):
        super().__init__("HP_3.png")

class Speed_up(Item):
    def __init__(self):
        super().__init__("speed.png")

class Defence_up(Item):
    def __init__(self):
        super().__init__("shield0.png")


        
        
        


session = Game()
session.game_intro()
