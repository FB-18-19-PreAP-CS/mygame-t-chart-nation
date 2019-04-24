import pygame
pygame.init()
disp = pygame.display.set_mode((500,500))

pygame.display.set_caption("Dungeon Master")

x = 50 
y = 50
width = 40
height = 60
vel = 5

run = True
while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_A]:
        x -= vel
    if keys[pygame.K_D]:
        x += vel
    if keys[pygame.K_W]:
        y -= vel
    if keys[pygame.K_S]:
        y += vel
    
    win.fill((0,0,0))
    pygame.draw.rect(win, (255,0,0), (x,y,width,height))
    pygame.display.update()
pygame.quit()