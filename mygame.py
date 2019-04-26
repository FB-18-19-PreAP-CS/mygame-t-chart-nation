import pygame
pygame.init()
disp = pygame.display.set_mode((500,475))

pygame.display.set_caption("Dungeon Master")

# walkright = [pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png')]
# walkleft = [pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png'), pygame.image.load('sensei.png')]

walkright = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkleft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
tile = pygame.image.load('generic-rpg-tile07.png')

clock = pygame.time.Clock()
x = 50 
y = 400
width = 64
height = 64
vel = 5
left = False
right = False
walkcount = 0



def home_screen:
    for i in range(0,500):
        for j in range(0,500):
            disp.blit(bg, (i,j))
            




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

run = True
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
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
    
    
pygame.quit()

https://www.geeksforgeeks.org/python-display-text-to-pygame-window/