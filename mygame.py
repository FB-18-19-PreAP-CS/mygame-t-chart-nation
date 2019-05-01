import pygame
pygame.init()
disp = pygame.display.set_mode((500,475))

pygame.display.set_caption("Dungeon Master")

# walkright = [pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png')]
# walkleft = [pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png')]

walkright = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkleft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

bg = pygame.image.load('R9.png')
char = pygame.image.load('standing.png')
tile = pygame.image.load('bg.jpg')

clock = pygame.time.Clock()
x = 50 
y = 400
width = 64
height = 64
vel = 5
left = False
right = False
walkcount = 0

font = pygame.font.Font('freesansbold.ttf',32)
text = font.render('Dungeon Master', True,(255,255,255),(0,0,0))
text1 = font.render('Press Backspace to continue',True,(255,255,255),(0,0,0))

def home_screen():
    game_intro = True
    while game_intro:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            game_intro = False
        textrect = text.get_rect()
        textrect.center = (500//2,475//2)
        disp.blit(text,textrect)
        textrect1 = text.get_rect()
        textrect1.center = (150,400)
        disp.blit(text1,textrect1)
        pygame.display.update


def button(msg,x,y,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mous[0] and y + h > mouse[1] > y:
        pygame.draw.rect(disp, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(disp, ic,(x,y,w,h))

    smalltext = pygame.font.Font("freesansbold.ttf",20)
    textsurf, textrect = text_objects(msg,smalltext)
    textrect.center = ( (x+(w/2)), (y(h/2)) )
    disp.blit(textsurf, textrect)
    





def redrawgamewindow():
    global walkcount
    disp.blit(bg, (0,0))
    if walkcount + 1 >= 27:
        walkcount = 0
    
    if left:
        disp.blit(walkleft[walkcount//3],(x,y))
        walkcount += 1
    elif right:
        disp.blit(walkright[walkcount//3],(x,y))
        walkcount += 1
    else:
        disp.blit(char ,(x,y))
   
    pygame.display.update()

def quitgame():
    pygame.quit()
    quit()
def game_intro():
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            textrect = text.get_rect()
            textrect.center = (500//2,475//2)
            disp.blit(text,textrect)
            button('GO!',150,450,100,50,(0,255,0),(0,200,0),game_loop)
            button("Quit!",550,450,100,50,(255,0,0),(200,0,0),quitgame)

            pygame.display.update()
            clock.tick(27)
run = True
def game_loop():
    while run:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        game_intro()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and x > vel:
            x -= vel
            left = True
            right = False
        if keys[pygame.K_d] and x < 480:
            x += vel
            left = False
            right = True
        if keys[pygame.K_w] and y > 0:
            y -= vel
            left = False
            right = False
            walkcount = 0
        if keys[pygame.K_s] and y <  450:
            y += vel
            left = False
            right = False
            walkcount = 0
        redrawgamewindow()
        pygame.display.update()
        
    pygame.quit()

# https://pythonprogramming.net/pygame-button-function/?completed=/placing-text-pygame-buttons/