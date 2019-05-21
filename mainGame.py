import pygame
import time
from random import choice, randint

WIDTH = 800
HEIGHT = 800
EDGEXL = 45
EDGEXR = WIDTH - 130
EDGEYT = 85
EDGEYB = HEIGHT - 200

class Game:
    def __init__(self):
        pygame.mixer.pre_init(48000,-16,2,2048)
        pygame.mixer.init()
        pygame.init()

        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render('Dunegon Master', True,(255,255,255),(0,0,0))
        self.endtext = self.font.render('Game Over!',True,(255,255,255),(0,0,0))
        self.wintext = self.font.render('You Win!',True,(255,255,255),(0,0,0))

        self.timer = Timer()
        self.killCounter = KillCounter()
        self.scoreCounter = Score()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dunegon Master")
        self.clock = pygame.time.Clock()
        self.mobs = []
        self.healthBar = HealthBar()
        self.character = Hero()
        self.existingdoors = []
        self.existingwalls = []
        self.existingItems = []
        image1 = pygame.image.load('dungeon.png')
        image2 = pygame.image.load('hiddenRoom.png')
        self.bg = image1
        self.room1 = Room([ Door(700,360), HiddenDoor(367,90)], [], image1, 45) # HiddenDoor(300,300)
        self.room2 = Room([Door(700,360)], [], image1, 45)
        self.room3 = Room([ Door(700,360)], [], image1, 45)
        self.room4 = Room([ Door(700,360), HiddenDoor(367,90)], [], image1, 45)
        self.room5 = Room([ Door(700,360)], [], image1, 45)
        self.room6 = Room([ Door(700,360)], [], image1, 45)
        self.room7 = Room([ Door(700,360), HiddenDoor(367,90)], [], image1, 45)
        self.room8 = Room([ Door(700,360)], [], image1, 45)
        self.room9 = Room([ Door(700,360)], [], image1, 45)
        self.room10 = Room([ Door(700,360), HiddenDoor(367,90)], [], image1, 45)
        self.room11 = Room([ Door(700,360)], [], image1, 45)
        self.room12 = Room([ Door(700,360)], [], image1, 45)
        self.room13 = Room([ Door(700,360), HiddenDoor(367,90)], [], image1, 45)
        self.room14 = Room([ Door(700,360)], [], image1, 45)
        self.room15 = Room([ Door(700,360)], [], image1, 45)
        self.finalRoom = Room([LockedDoor(35,360), Door(700,360)], [], image1, 45)
        self.hiddenRoom = HiddenRoom([Door(700,360)],[],image2, 0)
        self.roomList = [self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7, self.room8, self.room9, self.room10, self.room11, self.room12, self.room13, self.room14, self.room15]
        self.currentRoom = choice(self.roomList)
        self.exploredRoomList = []
        self.exploredRoomList.append(self.currentRoom)

        self.frameCount = 0

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

    def lose_screen(self):
        self.screen.fill((0,0,0))
        self.draw_bg(self.bg)
        textrect = self.endtext.get_rect()
        textrect = (300, 350)
        self.screen.blit(self.endtext,textrect)
        pygame.display.update()
        time.sleep(2)
        self.quitgame
        self.begin()
    
    def win_screen(self):
        self.screen.fill((0,0,0))
        textrect = self.wintext.get_rect()
        textrect = (300,350)
        self.screen.blit(self.wintext,textrect)
        pygame.display.update()
        time.sleep(2)
        self.quitgame
        self.begin()

    def begin(self):
        Game().game_intro()


    def start(self):
        done = False
        pygame.mixer.music.load('escape.wav')
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
                        for mob in self.mobs:
                            if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                                mob.follow(self.character)
                    elif self.checkEdges("up") == True:
                        self.character.rect.y = EDGEYT
                if pressed[pygame.K_DOWN]:
                    if not self.checkEdges("down") and not self.checkWalls("down"):
                        self.character.move('down')
                        for mob in self.mobs:
                            if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                                mob.follow(self.character)
                    elif self.checkEdges("down") == True:
                        self.character.rect.y = EDGEYB
                if pressed[pygame.K_LEFT]:
                    if not self.checkEdges("left") and not self.checkWalls("left"):
                        self.character.move('left')
                        for mob in self.mobs:
                            if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                                mob.follow(self.character)
                    elif self.checkEdges("left") == True:
                        self.character.rect.x = EDGEXL
                if pressed[pygame.K_RIGHT]:
                    if not self.checkEdges("right") and not self.checkWalls("right"):
                        self.character.move('right')
                        for mob in self.mobs:
                            if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                                mob.follow(self.character)
                    elif self.checkEdges("right") == True:
                        self.character.rect.x = EDGEXR
                if pressed[pygame.K_SPACE]:
                    self.character.attacking = True
                    self.character.attackAnimation = 0
                    for mob in self.mobs:
                        if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                            mob.follow(self.character)
            else:
                self.checkEnemies(True)
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
            for mob in self.mobs:
                if mob.__class__.__name__ == "Slime1" or mob.__class__.__name__ == "Hydra":
                    mob.follow(self.character)
                mob.draw(self.screen)
            for door in self.existingdoors:
                door.draw(self.screen)
            for item in self.existingItems:
                item.draw(self.screen)
            pygame.display.flip()

            self.checkEnemies()

            if self.checkItems() == True:
                if self.existingItems[0].__class__.__name__ == "Defense_up":
                    self.character.defense += 1
                elif self.existingItems[0].__class__.__name__ == "Speed_up":
                    self.character.speed += 3
                else:
                    self.character.health += 75
                    if self.character.health > 300:
                        self.character.health = 300
                self.existingItems = []
                newRoomLoop = True
                while newRoomLoop:
                    room = choice(self.roomList)
                    if room not in self.exploredRoomList or len(self.exploredRoomList) == len(self.roomList):
                        if len(self.exploredRoomList) == len(self.roomList):
                            if self.currentRoom == self.finalRoom:
                                self.win_screen()
                            else:
                                self.loadRoom(self.finalRoom)
                        else:
                            self.currentRoom = room
                            newRoomLoop = False

            self.healthBar.draw(self.character.health, self.screen)
            if self.frameCount == 0:
                self.timer.time += 1
            self.timer.draw(self.screen)
            self.frameCount = (self.frameCount + 1) % 30
            self.killCounter.draw(self.screen) 
            self.scoreCounter.score = self.killCounter.killCount - self.timer.time
            self.scoreCounter.draw(self.screen)

            if self.checkDoors() != "HiddenDoor" and self.checkDoors() != "None":
                newRoomLoop = True
                while newRoomLoop:
                    room = choice(self.roomList)
                    if room not in self.exploredRoomList or len(self.exploredRoomList) == len(self.roomList):
                        if len(self.exploredRoomList) == len(self.roomList):
                            self.win_screen()
                        else:
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

    def checkEnemies(self,attacking=False):
        for mob in self.mobs:
            if self.character.rect.colliderect(mob.rect):
                if not attacking:
                    self.character.health -= (1/2 - float(1/16 * self.character.defense))
                    if self.character.health == 0:
                        pygame.mixer.music.stop()
                        self.lose_screen()
                    return
                else:
                    self.killCounter.killCount += 1
                    if mob.__class__.__name__ == "Hydra":
                        for i in range(2):
                            self.mobs.append(Slime1())
                    self.mobs.remove(mob)
                    return

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
        # time.sleep(2)
        self.draw_bg(Room.background)
        self.existingdoors = []
        for door in Room.doorList:
            self.existingdoors.append(door)
        for wall in Room.wallList:
            self.existingwalls.append(wall)
        self.character.draw(self.screen,True)
        self.mobs = []
        for enemy in range(Room.enemyNumber):
            self.spawnEnemy()
        print(Room.__class__.__name__)
        if Room.__class__.__name__ == "HiddenRoom":
            self.generateItem()

    def spawnEnemy(self):
        type = randint(1,3)
        if type == 1:
            enemy = Slime1()
        elif type == 2:
            enemy = EnemyPath()
        elif type == 3:
            enemy = Hydra()
        self.mobs.append(enemy)
        enemy.draw(self.screen)

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
        self.health = 300
        self.defense = 0
        self.speed = 0
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('adventurer-idle-00.png')), (80,80))
        self.orientation = "right"
        self.moveRight = []
        self.moveAttack = []
        self.attackAnimation = -1
        self.attacking = False
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'adventurer-run-0{i}.png'), (80,80)))
        for i in range(6):
            self.moveAttack.append(pygame.transform.scale(pygame.image.load(f'adventurer-attack2-0{i}.png'), (80,80)))
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self,health,strength,sprite,frames):
        pygame.sprite.Sprite.__init__(self)
        self.health=health
        self.strength=strength
        self.orientation = 'left'
        self.animation = []
        for i in range(4):
            self.animation.append(pygame.image.load(f"Slime_Walk_{i}.png"))
       
        self.frame = 0 
        self.rect = self.animation[0].get_rect()
        self.rect.x = randint(400,EDGEXR)
        self.rect.y = randint(100,EDGEYB)
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

class EnemyPath:
    def __init__(self):
        self.walkright = [pygame.image.load('Blue_Slime_0.png'),pygame.image.load('Blue_Slime_1.png'),pygame.image.load('Blue_Slime_0.png'),pygame.image.load('Blue_Slime_1.png')]
        self.walkleft = [pygame.image.load('Blue_Slime_0.png'),pygame.image.load('Blue_Slime_1.png'),pygame.image.load('Blue_Slime_0.png'),pygame.image.load('Blue_Slime_1.png')]
        self.moveType = randint(1,2)
        if self.moveType == 1:
            self.moveType = "y"
        else:
            self.moveType = "x"
        self.rect = self.walkright[0].get_rect()
        self.rect.x = randint(400,600)
        self.rect.y = randint(100,400)
        if self.moveType == "x":
            self.end = randint(600,EDGEXR)
            self.path = [self.rect.x,self.end]
        else:
            self.end = randint(400,EDGEYB)
            self.path = [self.rect.y,self.end]
        self.walkcount = 0
        self.vel = 15

    def draw(self,screen):
        self.move()
        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        if self.vel > 0:
            screen.blit(self.walkright[self.walkcount//3], (self.rect.x,self.rect.y))
            self.walkcount += 1
        else:
            screen.blit(pygame.transform.flip(self.walkleft[self.walkcount//3],True,False), (self.rect.x,self.rect.y))
            self.walkcount += 1
    def move(self):
        if self.moveType == "x":
            if self.vel > 0:
                if self.rect.x < self.path[1] + self.vel:
                    self.rect.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.x += self.vel
                    self.walkcount = 0
            else:
                if self.rect.x > self.path[0] - self.vel:
                    self.rect.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.x += self.vel
                    self.walkcount = 0
        else:
            if self.vel > 0:
                if self.rect.y < self.path[1] + self.vel:
                    self.rect.y += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.y += self.vel
                    self.walkcount = 0
            else:
                if self.rect.y > self.path[0] - self.vel:
                    self.rect.y += self.vel
                else:
                    self.vel = self.vel * -1
                    self.rect.y += self.vel
                    self.walkcount = 0


class Slime1(Enemy):
    def __init__(self):
        self.count=0
        Enemy.__init__(self,10,1,'Slime_Walk',4)
    def follow(self,hero):
        self.frame+=.1
        self.count+=1
        self.count%=41
        hori='l'
        if hero.rect.x>=self.rect.x:
            hori='r'
        vert='u'
        if hero.rect.y>=self.rect.y:
            vert='d'
        if self.count%10==0:
            for i in range(13):
                if vert=='u' and hori=='l':
                    Enemy.move(self,-1,-1)
                elif vert=='d' and hori=='l':
                    Enemy.move(self,-1,1)
                elif vert=='d' and hori=='r':
                    Enemy.move(self,1,1)
                else:
                    Enemy.move(self,1,-1)

class Hydra(Slime1):
    def __init__(self):
        super().__init__()
        self.animation = []
        for i in range(4):
            self.animation.append(pygame.image.load(f"Hydra_{i}.png"))




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
    def __init__(self, doorList, wallList, background, enemyNumber):
        self.doorList = doorList
        self.wallList = wallList
        self.background = background
        self.enemyNumber = enemyNumber

class HiddenRoom(Room):
    def __init__(self,doorList,wallList,background,enemyNumber):
        super().__init__(doorList,wallList,background,enemyNumber)

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

class HealthBar():
    def __init__(self):
        pass

    def draw(self, health, screen):
        pygame.draw.rect(screen, (0,255,0), (30,30,300,10))
        pygame.draw.rect(screen, (255,0,0), (30+health,30,300-health,10))

class Timer():
    def __init__(self):
        self.time = 0
        self.font = pygame.font.Font('freesansbold.ttf',15)
    
    def draw(self, screen):
        time = self.font.render("Time: " + str(self.time),True,(255,0,0),(0,0,0))
        textrect = time.get_rect()
        textrect = (600,10)
        screen.blit(time, textrect)
        pygame.display.update()

class KillCounter():
    def __init__(self):
        self.killCount = 0
        self.font = pygame.font.Font('freesansbold.ttf',15)

    def draw(self, screen):
        killcount = self.font.render("Enemies Slain: " + str(self.killCount),True,(255,0,0),(0,0,0))
        textrect = killcount.get_rect()
        textrect = (400,10)
        screen.blit(killcount, textrect)
        pygame.display.update()

class Score():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf',15)

    def draw(self, screen):
        score = self.font.render("Score: " + str(self.score),True,(255,0,0),(0,0,0))
        textrect = score.get_rect()
        textrect = (700,10)
        screen.blit(score, textrect)
        pygame.display.update()

        

        
        
        


session = Game()
session.game_intro()
