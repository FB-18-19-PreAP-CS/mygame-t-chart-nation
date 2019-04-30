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
            enemy   = Enemy(100,100) # spawn enemy
            enemy_list = pygame.sprite.Group()   # create enemy group 
            enemy_list.add(enemy)                # add enemy to group
            pygame.display.flip()
            self.character.draw(self.screen)
            
            # self.character.blitme(self.screen)
            pygame.display.flip()

            # self.check_edge()

            self.clock.tick(60)

    def draw_bg(self):
        self.screen.blit(pygame.image.load('floor.jpeg'),(0,0))

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
class Enemy(pygame.sprite.Sprite):
    '''
    Spawn an enemy
    '''
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Slime_Walk_1.png")
        screen.blt(self.image,0,0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
        
        
    

