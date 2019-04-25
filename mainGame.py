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
        if self.curr_type == 0:
            # draw lines on road
            line_x = 0
            for i in range(10):
                pygame.draw.rect(self.screen,(255,255,0), pygame.Rect(line_x,HEIGHT//2,50,25))
                line_x += 100

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 20
        self.frame = 0
        self.animation = pygame.transform.scale((pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-idle-00.png')), (120,120))
        self.animations = [pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-idle-00.png'), pygame.image.load('/home/blackn/preAPCS/mygame-t-chart-nation/images/adventurer-run-04.png')]
        self.rect = self.animation.get_rect()
        self.rect.x = 120
        self.rect.y = 120

        

    def draw(self,screen):
        screen.blit(self.animation,(self.rect.x,self.rect.y))

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.rect.x -= 5
        else:
            self.rect.x += 5
        self.frame += 25

session = Game()
session.start()
