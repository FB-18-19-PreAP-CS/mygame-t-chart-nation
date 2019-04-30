import pygame
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
            self.character.draw(self.screen)
            # self.character.blitme(self.screen)
            pygame.display.flip()

            # self.check_edge()

            self.clock.tick(60)

    def draw_bg(self):
        self.screen.blit(pygame.image.load('Screenshot_20190409_140137.png'),(0,0))

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 20
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-idle-00.png')), (120,120))
        self.moveRight = []
        for i in range(6):
            self.moveRight.append(pygame.transform.scale(pygame.image.load(f'/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-run-0{i}.png'), (120,120)))
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
class Enemy(pygame.sprite.Sprite):
    def __init__(self,health,range,strength,sprite,frames,pos):
        pygame.sprite.Sprite.__init__(self)
        self.health=health
        self.pos=pos
        self.strength=strength
        self.orientation = 'left'
        self.animation = []
        self.frame = 0
        
        for i in range(4):
            self.animation.append(pygame.image.load(f'./images/{sprite}{i+1}.png'))
        self.rect = self.animation[0].get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def blitme(self,screen):
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
class Spike(Enemy):
    def __init__(self,pos):
        Enemy.__init__(self,10**10,0,1,'Barrel_',1,pos)
class Slime1(Enemy):
    def __init__(self,pos):
        self.count=0
        Enemy.__init__(self,10,0,1,'Slime_Walk_',4,pos)
    def follow(self,hero):
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
                    Enemy.move(-4,-4)
                elif vert=='d' and hori=='l':
                    Enemy.move(-4,4)
                elif vert=='d' and hori=='r':
                    Enemy.move(4,4)
                else:
                    Enemy.move(4,-4)
        elif self.count%10==0:
            for i in range(10):
                if vert=='u' and hori=='l':
                    Enemy.move(-2,-2)
                elif vert=='d' and hori=='l':
                    Enemy.move(-2,2)
                elif vert=='d' and hori=='r':
                    Enemy.move(2,2)
                else:
                    Enemy.move(2,-2)