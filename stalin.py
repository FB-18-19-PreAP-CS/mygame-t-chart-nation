import pygame
pygame.init()

disp = pygame.display.set_mode((500,500))

pygame.display.set_caption("dungeon master")

walkRight = [pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png')]
walkLeft = [pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png'), pygame.image.load('mani-idle-run.png')]
bg = pygame.image.load('generic-rpg-tile-waterfall03.png')
char = pygame.image.load('sensei.png')

clock = pygame.time.Clock()

x = 50
y = 50
width = 64
height = 64
vel = 5
left = False
right = False
walk_count = 0

def redrawgamewindow():
    global walkCount
    disp.blit(bg, (0,0))
    if walkCount + 1 >= 27:
        walkCount = 0
    
    if left:
        disp.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        disp.blit(walkRight[walkCount//3],(x,y))
        walkCount += 1
    try:
        disp.blit(char, (x,y))
    except expression as identifier:
        pass
    else:
        pass
    finally:
        pass
    pygame.display.update()

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
        left = True
        right = False
    if keys[pygame.K_RIGHT]:
        x += vel
        left = False
        right = True
    else:
        right = False
        left = False
        walkCount = 0
    if keys[pygame.K_UP]:
        y -= vel
        left = False
        right = False

    if keys[pygame.K_DOWN]:
        y += vel
    redrawgamewindow()
pygame.quit()