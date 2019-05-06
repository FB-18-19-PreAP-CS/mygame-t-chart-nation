import pygame
class Items:
    def __init__(self,type,pos,sprite,size):
        self.sprite=pygame.transform.scale((pygame.image.load('./images/{sprite}')), size)
        self.rect=self.sprite.get_rect()
        self.rect.x,self.rect.y=pos[0],pos[1]
        self.held=False
    def draw(self,screen):
        screen.blit(self.sprite,(self.rect.x,self.rect.y))
    def check_pickup(self,Hero):
        if self.sprite.rect.colliderect(Hero.rect):
            self.held=True
class Health_up(Items):
    def __init__(self,pos,level):
        self.level=level
        super().__init__('pickup',pos,f'HP_{level}.png',(25,25))
    def check_pickup(self,Hero):
        if super().check_pickup(Hero):
            Hero.health+=self.level+1
class Speed_up(Items):
    def __init__(self,pos,level):
        super().__init__('pickup',pos,f'speed.png',(25,25))
    def check_pickup(self,Hero):
        if super().check_pickup(Hero):
            Hero.speed+=1
class Defence_up(Items):
    def __init__(self,pos,level):
        self.level=level
        super().__init__('pickup',pos,f'shield{level}.png',(25,25))
    def check_pickup(self,Hero):
        if super().check_pickup(Hero):
            Hero.defense+=1