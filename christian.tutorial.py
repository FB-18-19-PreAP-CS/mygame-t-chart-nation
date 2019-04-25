from random import *
from math import *

class dMap:
   def __init__(self):
       self.roomList=[]
       self.cList=[]

   def makeMap(self,xsize,ysize,fail,b1,mrooms):
       """Generate random layout of rooms, corridors and other features"""
       # makeMap can be modified to accept arguments for values of failed, and percentile of features.
       # Create first room
       self.size_x = xsize
       self.size_y = ysize
       # initialize map to all walls
       self.mapArr=[] 
       for y in range(ysize):
           tmp = []
           for x in range(xsize):
               tmp.append(1)
           self.mapArr.append( tmp )

       w,l,t=self.makeRoom()
       while len(self.roomList)==0:
           y=randrange(ysize-1-l)+1
           x=randrange(xsize-1-w)+1
           p=self.placeRoom(l,w,x,y,xsize,ysize,6,0)
       failed=0
       while failed<fail: #The lower the value that failed< , the smaller the dungeon
           chooseRoom=randrange(len(self.roomList))
           ex,ey,ex2,ey2,et=self.makeExit(chooseRoom)
           feature=randrange(100)
           if feature<b1: #Begin feature choosing (more features to be added here)
               w,l,t=self.makeCorridor()
           else:
               w,l,t=self.makeRoom()
           roomDone=self.placeRoom(l,w,ex2,ey2,xsize,ysize,t,et)
           if roomDone==0: #If placement failed increase possibility map is full
               failed+=1
           elif roomDone==2: #Possiblilty of linking rooms
               if self.mapArr[ey2][ex2]==0:
                   if randrange(100)<7:
                       self.makePortal(ex,ey)
                   failed+=1
           else: #Otherwise, link up the 2 rooms
               self.makePortal(ex,ey)
               failed=0
               if t<5:
                   tc=[len(self.roomList)-1,ex2,ey2,t]
                   self.cList.append(tc)
                   self.joinCorridor(len(self.roomList)-1,ex2,ey2,t,50)
           if len(self.roomList)==mrooms:
               failed=fail
       self.finalJoins()

   def makeRoom(self):
       """Randomly produce room size"""
       rtype=5
       rwide=randrange(8)+3
       rlong=randrange(8)+3
       return rwide,rlong,rtype

   def makeCorridor(self):
       """Randomly produce corridor length and heading"""
       clength=randrange(18)+3
       heading=randrange(4)
       if heading==0: #North
           wd=1
           lg=-clength
       elif heading==1: #East
           wd=clength
           lg=1
       elif heading==2: #South
           wd=1
           lg=clength
       elif heading==3: #West
           wd=-clength
           lg=1
       return wd,lg,heading

   def placeRoom(self,ll,ww,xposs,yposs,xsize,ysize,rty,ext):
       """Place feature if enough space and return canPlace as true or false"""
       #Arrange for heading
       xpos=xposs
       ypos=yposs
       if ll<0:
           ypos+=ll+1
           ll=abs(ll)
       if ww<0:
           xpos+=ww+1
           ww=abs(ww)
       #Make offset if type is room
       if rty==5:
           if ext==0 or ext==2:
               offset=randrange(ww)
               xpos-=offset
           else:
               offset=randrange(ll)
               ypos-=offset
       #Then check if there is space
       canPlace=1
       if ww+xpos+1>xsize-1 or ll+ypos+1>ysize:
           canPlace=0
           return canPlace
       elif xpos<1 or ypos<1:
           canPlace=0
           return canPlace
       else:
           for j in range(ll):
               for k in range(ww):
                   if self.mapArr[(ypos)+j][(xpos)+k]!=1:
                       canPlace=2
       #If there is space, add to list of rooms
       if canPlace==1:
           temp=[ll,ww,xpos,ypos]
           self.roomList.append(temp)
           for j in range(ll+2): #Then build walls
               for k in range(ww+2):
                   self.mapArr[(ypos-1)+j][(xpos-1)+k]=2
           for j in range(ll): #Then build floor
               for k in range(ww):
                   self.mapArr[ypos+j][xpos+k]=0
       return canPlace #Return whether placed is true/false

   def makeExit(self,rn):
       """Pick random wall and random point along that wall"""
       room=self.roomList[rn]
       while True:
           rw=randrange(4)
           if rw==0: #North wall
               rx=randrange(room[1])+room[2]
               ry=room[3]-1
               rx2=rx
               ry2=ry-1
           elif rw==1: #East wall
               ry=randrange(room[0])+room[3]
               rx=room[2]+room[1]
               rx2=rx+1
               ry2=ry
           elif rw==2: #South wall
               rx=randrange(room[1])+room[2]
               ry=room[3]+room[0]
               rx2=rx
               ry2=ry+1
           elif rw==3: #West wall
               ry=randrange(room[0])+room[3]
               rx=room[2]-1
               rx2=rx-1
               ry2=ry
           if self.mapArr[ry][rx]==2: #If space is a wall, exit
               break
       return rx,ry,rx2,ry2,rw

   def makePortal(self,px,py):
       """Create doors in walls"""
       ptype=randrange(100)
       if ptype>90: #Secret door
           self.mapArr[py][px]=5
           return
       elif ptype>75: #Closed door
           self.mapArr[py][px]=4
           return
       elif ptype>40: #Open door
           self.mapArr[py][px]=3
           return
       else: #Hole in the wall
           self.mapArr[py][px]=0

   def joinCorridor(self,cno,xp,yp,ed,psb):
       """Check corridor endpoint and make an exit if it links to another room"""
       cArea=self.roomList[cno]
       if xp!=cArea[2] or yp!=cArea[3]: #Find the corridor endpoint
           endx=xp-(cArea[1]-1)
           endy=yp-(cArea[0]-1)
       else:
           endx=xp+(cArea[1]-1)
           endy=yp+(cArea[0]-1)
       checkExit=[]
       if ed==0: #North corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<self.size_x-2:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
       elif ed==1: #East corridor
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<self.size_x-2:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<self.size_y-2:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       elif ed==2: #South corridor
           if endx<self.size_x-2:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<self.size_y-2:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
       elif ed==3: #West corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endy<self.size_y-2:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       for xxx,yyy,xxx1,yyy1 in checkExit: #Loop through possible exits
           if self.mapArr[yyy][xxx]==0: #If joins to a room
               if randrange(100)<psb: #Possibility of linking rooms
                   self.makePortal(xxx1,yyy1)

   def finalJoins(self):
       """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
       for x in self.cList:
           self.joinCorridor(x[0],x[1],x[2],x[3],10)

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
startx=20   # map width
starty=10   # map height
themap= dMap()
themap.makeMap(startx,starty,110,50,60) 
for y in range(starty):
        line = ""
        for x in range(startx):
                if themap.mapArr[y][x]==0:
                        line += "."
                if themap.mapArr[y][x]==1:
                        line += " "
                if themap.mapArr[y][x]==2:
                        line += "#"
                if themap.mapArr[y][x]==3 or themap.mapArr[y][x]==4 or themap.mapArr[y][x]==5:
                        line += "="
        print (line)

# # see also http://spielend-programmieren.at 
# import pygame 
# import random



# level1 = """
# ##########################################
# #...Kh#.:.$$$$$#..Dh..c..G..E..G..p..G..E#
# #$.K:K#...$.$.$#.#######################.#
# #$..K.#...$$$$$#..#....K..E..G..a..#####.#
# #$....###########.#K##.###########G..E..b#
# #$....#...........#h#..#.........#########
# #$.p..#.#############.##.#######.#.G.#.G.#
# #$b.r.#.............#....#.......#E#.E.#E#
# #$.h.c#.......#####D######.#######..####G#
# #$b.r.#......Ks#$$$$$$$$$#......hD#G#.KE.#
# #$.p..###########################.E.#h####
# #$.....#>#...#...#...#...#...#.G.####D####
# #$$$s.>#...#...#...#...#...#...#.h$$$$$$$#
# ##########################################
# """

# level2 = """
# ##########################################
# #>...>####...............................#
# ###G######...............................#
# #.....####...............................#
# #.########...............................#
# #.#...####...............................#
# #.#.#.####...............................#
# #...#.####...............................#
# #####.####...............................#
# #.....####...............................#
# #.########...............................#
# #..#...#<#################################
# ##...#.#.#################################
# ##########################################
# """

# level3 = """
# ##########################################
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.....#..................................#
# #.########...............................#
# #...#...##...............................#
# #s#...#.<#...............................#
# ##########################################
# """

# #        key :   name   hunger hp
# food = {"a":("apple",5,0),
#         "b":("banana",6,2),
#         "p":("pork",9,0),
#         "r":("rotten meat",4,-2),
#         "c":("cake",17,0),
#         "h":("big health potion",0,42)}



# def shop():
#     #msg = "number  |  potion    | price\n"
#     #msg +="--------+------------+-------\n"
#     store = {}
#     for number in range(10):
#         # number : ( name, effect, price )
#         store[number] = ( random.choice(("health", "tohit", "evade", "food", "maxdamage")),
#                           random.randint(-1, 5),
#                           random.randint(4,44) )
#         #msg += "     {:>2} | {:<10} | {:>3}\n".format(number, store[number][0],
#         #                                        store[number][2])
#     return store
  
       

# class Monster():
#     number = 0
#     zoo = {}
    
#     def __init__(self, x=0, y=1, z=0, hp=10, name = "monster",
#                  tohit = 0.5, evade = 0.25, maxdamage = 3, char="?"):
#         self.hp = hp
#         self.x = x
#         self.y = y
#         self.z = z
#         self.name = name
#         self.tohit = tohit
#         self.evade = evade
#         self.maxdamage = maxdamage
#         self.number = Monster.number
#         Monster.number += 1
#         Monster.zoo[self.number] = self
#         self.char = char
#         self.color = (255,0,0)
    
#     def report(self):
#         return "monster: {} hp: {} tohit: {} ev: {} maxdmg: {}".format(self.name,  self.hp, self.tohit, self.evade, self.maxdamage)
    
#     def move(self):
#         return 0, 0
 
# class Bunny(Monster):
#     def __init__(self, posx, posy, posz):
#         Monster.__init__(self, posx, posy, posz, 2, "Bunny", 0.6, 0.8, 1, "B")
#         self.color = (255,255,0)
    
# class Dog(Monster):
#     def __init__(self, posx, posy, posz):
#         Monster.__init__(self, posx, posy, posz, 10, "Dog", 0.4, 0.35, 3, "G")
#         self.color = (255,165,0)
                
# class Dragon(Monster):
#     def __init__(self,posx, posy, posz):
#         Monster.__init__(self, posx, posy, posz, 30, "Dragon", 0.25, 0.1, 22, "D")
         
#     def move(self):
#         return random.choice((-1,0,1)), random.choice((-1,0,1)) # the dragon moves or waits
        
# class Duck(Monster):
#     def __init__(self,posx, posy, posz):
#         Monster.__init__(self,posx, posy, posz, 5, "Evil Duck", 0.47, 0.23, 2, "E")
#         self.color = (255,190,0)
        
# class Kobold(Monster):
#     def __init__(self,posx, posy, posz):
#         Monster.__init__(self,posx, posy, posz, 3, "Kobold", 0.8, 0.01, 1, "K")
        
    
#     def move(self):
#         return random.choice((-1,0,0,0,1)), random.choice((-1,0,0,0,1)) # kobold jumps, sometimes
        
# class Frog(Monster):
#     def __init__(self, posx, posy, posz):
#         Monster.__init__(self, posx, posy, posz, 3, "Frog", 0.2, 0.5, 1, "F")
#         self.color = (220, 79, 44)
        
#     def move(self):
#         return random.choice((-2,0,2)), random.choice((-2,0,2))
        
# class Hero(Monster):
#     def __init__(self,posx, posy, posz):
#         Monster.__init__(self,posx, posy, posz, 10, "Hero", 0.7, 0.3, 7, "@")
#         self.hunger = 0
#         self.money = 0
#         self.color = (0,0,255)


# class Particle(pygame.sprite.Sprite):
    
#     def __init__(self, x, y, speed=50, dx=None, dy=None, color=None):
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.x = x
#         self.y = y
#         if dx is None:
#             self.dx = random.random() * speed - speed/2
#         else:
#             self.dx = dx
#         if dy is None:
#             self.dy = random.random() * speed - speed/2
#         else:
#             self.dy = dy
#         if color is None:
#             self.color = (255, 0, random.randint(0,250))
#         else:
#             self.color = color
#         self.lifetime = 1 + random.random() * 1.5
#         self.image = pygame.Surface((5,5))
#         pygame.draw.circle(self.image, self.color, (2,2), 2)
#         self.image.set_colorkey((0,0,0))
#         self.image.convert_alpha()
#         self.rect = self.image.get_rect()
#         self.rect.center = (self.x, self.y)
        
#     def update(self, seconds):
#         self.lifetime -= seconds
#         if self.lifetime < 0:
#             self.kill()
#         self.x += self.dx * seconds
#         self.y += self.dy * seconds
#         self.rect.center = (round(self.x, 0), round(self.y,0))
        
        

# class PygView(object):
#     width = 0
#     height = 0
#     def __init__(self, width=640, height=400, fps=30):
#         """Initialize pygame, window, background, font,...
#            default arguments """
#         pygame.init()
#         pygame.display.set_caption("Press ESC to quit")
#         self.width = width
#         self.height = height
#         PygView.width = width
#         PygView.height = height
#         self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
#         self.background = pygame.Surface(self.screen.get_size()).convert()  
#         self.background.fill((255,255,255)) # fill background white
#         self.clock = pygame.time.Clock()
#         self.fps = fps
#         self.playtime = 0.0
#         self.font = pygame.font.SysFont('mono', 24, bold=True)
#         self.log = []
#         self.log.append("Welcome in the dungeon")
#         self.turn = 0
#         self.store = {} # empty store
#         self.allgroup = pygame.sprite.LayeredUpdates()
#         self.particlegroup = pygame.sprite.Group()
#         Particle.groups = self.allgroup, self.particlegroup
#         # ------ generiere monster -------
#         self.hero = Hero(1,1,0)

#         self.levels = []
#         for z, levelstring in enumerate((level1, level2, level3)):
            
#             level = []
#             for line in levelstring.split():
#                 level.append(list(line))
                

#             for y, line in enumerate(level):
#                 for x, char in enumerate(line):
#                     if char in "GDEKFB":
#                         level[y][x] = "."
#                         if char == "G":
#                             Dog(x,y,z)
#                         elif char == "D":
#                             Dragon(x,y,z)
#                         elif char == "E":
#                             Duck(x,y,z)
#                         elif char == "K":
#                             Kobold(x,y,z)
#                         elif char == "B":
#                             Bunny(x,y,z)
#                         elif char == "F":
#                             Frog(x,y,z)
            
#             self.levels.append(level)

#     def levelchange(self):
#         """calculating tiles and dimension of new level"""
#         self.tilesy = len(self.levels[self.hero.z])
#         self.tilesx = len(self.levels[self.hero.z][0])
#         self.widthx = (self.width - 100) / self.tilesx
#         self.widthy = (self.height - 100) / self.tilesy
#         self.gridsizex = self.width - 100
#         self.gridsizey = self.height - 100
#         self.tile = int(min(self.widthx, self.widthy))
#         self.wall = pygame.Surface((self.tile, self.tile))
#         self.wall.fill((128,128,128))
#         self.wall.convert()
#         self.ground = pygame.Surface((self.tile, self.tile))
#         self.ground.fill((64,32,64))
#         self.ground.convert()
        
#     def paintgrid(self, color=(117,43,218)):
#         for x in range(0, self.tilesx * self.tile, self.tile):
#             pygame.draw.line(self.background, color, (x,0),
#                 (x, self.tilesy * self.tile), 1)
#         for y in range(0, self.tilesy * self.tile, self.tile):
#             pygame.draw.line(self.background, color, (0,y),
#                 (self.tilesx * self.tile, y), 1)
                    
#     def paintlog(self):
#         self.background.fill((255,0,255)) # fill background white
#         y = self.height - 20
#         i = 0
#         for line in self.log:
#             self.draw_text(line,  5, y, (i,i,i), 15, self.background)
#             y -= 20
#             i += 5
#             i = min(255,i) 
#             if y < self.tile * self.tilesy:
#                 break
        
#     def paint(self):
#         """painting on the surface"""
#         self.paintlog()
#         #self.background.fill((255,0,255)) # fill background white
        
#         for y, line in enumerate(self.levels[self.hero.z]):
#             for x, char in enumerate(line):
#                 self.background.blit(self.ground,
#                             (x*self.tile, y*self.tile))
#                 for num, monster in Monster.zoo.items():
#                     if monster.hp < 1:
#                         continue
#                     if monster.x == x and monster.y == y and monster.z == self.hero.z:
#                         self.draw_text(monster.char, x*self.tile,
#                              y*self.tile, monster.color, 24, self.background)
#                         break
#                 else:        
#                     if char == "#":
#                         self.background.blit(self.wall,
#                             (x*self.tile, y*self.tile))
#                     elif char == ".":
#                         pass
#                     elif char in food:
#                         self.draw_text(char, x*self.tile,
#                              y*self.tile, (103,233,29), 24, self.background)
#                     else:
#                         self.draw_text(char, x*self.tile,
#                              y*self.tile, (43,216,218), 24, self.background)
#         self.paintgrid()
#         # status
#         x = self.gridsizex - self.tile / 2 
#         self.draw_text("HP: {}".format(self.hero.hp), x ,
#                                        10, (0,0,200), 20, self.background)
#         self.draw_text("Hunger: {}".format(self.hero.hunger), x ,
#                                        25, (0,0,200), 15, self.background)
#         self.draw_text("Gold: {}".format(self.hero.money), x,
#                                        40, (0,0,200), 15, self.background)
#         self.draw_text("x:{} y:{} z:{}".format(self.hero.x, self.hero.y, self.hero.z),
#                                        x, 55, (0,0,100), 15, self.background)
#         self.draw_text("turn: {}".format(self.turn), x,
#                                        70, (0,0,100), 15, self.background)
#         self.draw_text("evade: {:.1f}%".format(self.hero.evade*100), x,
#                                        85, (255,255,0), 15, self.background)
#         self.draw_text("toHit: {:.1f}%".format(self.hero.tohit*100), x,
#                                        100, (255,255,0), 15, self.background)
#         self.draw_text("maxDamge: {}".format(self.hero.maxdamage), x,
#                                        115, (255,255,0), 15, self.background)
#         if self.levels[self.hero.z][self.hero.y][self.hero.x] != "s":
#             self.store = {}
#         if len(self.store) > 0:
#             self.draw_text("Shopping!", x, 130, (0, 200, 0), 15, self.background)
#             y = 145
#             for nr in self.store:
#                 # nr : ( name, effect, price )
#                 name, effect, price = self.store[nr]
#                 self.draw_text("{}: {}$ {}".format(nr,price, name[:5]),
#                                x, y, (0,100,0), 15, self.background)
#                 y += 15
                
        
        
#     def teleport(self, distance=5):
#         targets = [] # list of valid targets
#         targets.append((0,0)) # add start position
#         for dy in range(-distance, distance+1):
#             if self.hero.y + dy < 0:
#                 continue
#             if self.hero.y + dy > len(self.levels[self.hero.z]):
#                 continue
#             for dx in range(-distance, distance+1):                    
#                 if self.hero.x + dx < 0:
#                     continue
#                 if self.hero.x + dx > len(self.levels[self.hero.z][self.hero.y]):
#                     continue
#                 if (dx**2 + dy**2)**0.5 > distance:
#                     continue
#                 if self.levels[self.hero.z][self.hero.y+dy][self.hero.x+dx] == ".":
#                     targets.append((dx,dy))
#         dx, dy = random.choice(targets)
#         if dx == 0 and dy == 0:
#             self.log.insert(0,"The telporter sends you to your old position.")
#             return
#         self.log.insert(0,"The telporter sends you to a new random position.")
#         self.hero.x += dx
#         self.hero.y += dy
            
            
    
    
#     def gameturn(self, command="", arg2=None):
#         # ------------ new game turn  -------------
#         self.turn += 1
#         self.hero.hunger += 1
       
#         print("pos:", self.hero.x, self.hero.y, self.hero.z)
#         dx = 0
#         dy = 0
#         mytile = self.levels[self.hero.z][self.hero.y][self.hero.x]
#         if command == "go west":
#             dx = -1
#         elif command == "go east":
#             dx = 1
#         elif command == "go north":
#             dy = -1
#         elif command == "go south":
#             dy = 1
#         elif command == "wait":
#             self.log.insert(0,"you rest a bit and wait a turn")
#         elif command == "climb":
#             if mytile == ">":
#                 self.hero.z += 1
#                 self.levelchange()
#                 #self.paint()
#             elif mytile == "<":
#                 self.hero.z -= 1
#                 self.levelchange()
#         elif command == "buy":
#             if len(self.store) > 0:
#                 name, effect, price = self.store[arg2]
#                 if price > self.hero.money:
#                     self.log.insert(0,"you can not afford this price!")
#                 else:
#                     self.hero.money -= price
#                     del self.store[arg2]
#                     self.log.insert(0,"you buy an potion for {} gold".format(price))
#                     self.log.insert(0,"You wait for the magic effect")
#                     # ---- potion effect ----
#                     if effect == 0:
#                         self.log.insert(0,"the potion was rotten and has no effect at all")
#                     elif effect < 0:
#                         self.log.insert(0,"the potion was cursed and has a negative effect!")
#                     else:
#                         self.log.insert(0,"the potion works! You feel better")
#                         if name == "health":
#                             self.hero.hp += effect
#                         elif name == "tohit":
#                             self.hero.tohit += effect / 100
#                         elif name == "evade":
#                             self.hero.evade += effect / 100
#                         elif name == "food":
#                             self.hero.hunger -= effect
#                         elif name == "maxdamage":
#                             self.hero.maxdamage += effect     
    
#         # --------legal move? ---------
#         if (self.hero.x + dx < 0 or 
#             self.hero.x + dx > len(self.levels[self.hero.z][self.hero.y]) or
#             self.hero.y < 0 or
#             self.hero.y > len(self.levels[self.hero.z])):
#             self.log.insert(0, "You can not leave the level")
#             dx = 0
#             dy = 0
#         elif self.levels[self.hero.z][self.hero.y + dy][self.hero.x + dx] == "#":
#             dx = 0
#             dy = 0
#             self.log.insert(0,"You can not go through a wall")
#         else:
#             # --- run into Monster? -----
#             for monster in Monster.zoo.values():
#                 if monster.number == self.hero.number:
#                     continue
#                 elif monster.hp <1:
#                     continue
#                 elif monster.z != self.hero.z:
#                     continue
#                 elif monster.x == self.hero.x + dx and monster.y == self.hero.y + dy:
#                     self.log.insert(0, "You fight against " + monster.report())
#                     self.fight(self.hero, monster)
#                     if monster.hp < 1:
#                         self.hero.money += random.randint(0,10)
#                     dx = 0
#                     dy = 0
#                     break
#             self.hero.x += dx
#             self.hero.y += dy
#             self.paint()
                
#         ## ----------Auswertung----------
#         stuff = self.levels[self.hero.z][self.hero.y][self.hero.x]
#         ## ------ Rätselkiste ---- 
#         #if stuff == "?":
#             #riddlebox(hero)
                
#         ## ------ teleport --------
#         if stuff == ":":
#             self.teleport()
#             self.paint()
#         ## ------ food and money -----
#         elif stuff in food:
#                 #print("You eat : ", food[stuff][0])
#                 self.log.insert(0,"You eat : {}".format(food[stuff][0]))
#                 self.hero.hunger -= food[stuff][1]
#                 self.hero.hp += food[stuff][2]
#                 self.levels[self.hero.z][self.hero.y][self.hero.x] = "."
#         elif stuff == "$":
#                 self.log.insert(0, "You found gold!")
#                 self.hero.money += random.randint(1, 20)
#                 self.levels[self.hero.z][self.hero.y][self.hero.x] = "."
#         elif stuff == ">":
#             self.log.insert(0,"You found a stair down. press c to climb down")
#         elif stuff == "<":
#             self.log.insert(0,"You found a stair up. press c to climb up")
#         elif stuff == "s":
#             if len(self.store) == 0:
#                 self.store = shop()
#         # ---- end ----
#         self.paint()
#         # -------- moving monsters -----
#         for monster in Monster.zoo.values():
#             if monster.number == self.hero.number:
#                 continue 
#             if monster.z != self.hero.z:
#                 continue
#             if monster.hp < 1:
#                 continue # no dead monsters moving around!
#             dx, dy = monster.move()
#             if dx == 0 and dy == 0:
#                 continue
#             try:
#                 target = self.levels[self.hero.z][monster.y+dy][monster.x+dx]
#             except:
#                 continue
#             #if monster.x + dx < 0 or monster.x + dx > len(line) or monster.y + dy < 0 or monster.y+dy >len(level):
#                 #dx = 0
#                 #dy = 0
#             if target in "#<>:sd":
#                 continue
#             for monster2 in Monster.zoo.values():
#                 if monster2.number == monster.number:
#                     continue
#                 if monster2.hp < 1:
#                     continue
#                 if monster2.z != self.hero.z:
#                     continue
#                 if monster.x + dx == monster2.x and monster.y+dy == monster2.y:
#                     dx = 0
#                     dy = 0
#                     if monster2.number == self.hero.number:
#                         self.log.insert(0, "A wandering monster attacks you!")
#                         self.fight(monster, self.hero)
                        
#                     break
#             monster.x += dx
#             monster.y += dy
#             #if hero.hp <1:
#                 #break


    
    
#     def run(self):
#         self.levelchange()
#         self.paint() 
#         running = True
#         while running:
#             milliseconds = self.clock.tick(self.fps)
#             seconds = milliseconds / 1000.0
#             self.playtime += seconds
#             self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
#                            self.clock.get_fps(), " "*5, self.playtime), 
#                            self.width-250, self.height-10, (0,0,0), 10)
            
#             if self.hero.hp < 1 or self.hero.hunger > 100:
#                 break
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False 
#                 elif event.type == pygame.KEYDOWN:
#                     # keys that you press once and release
#                     if event.key == pygame.K_ESCAPE:
#                         running = False
#                     elif event.key == pygame.K_w or event.key == pygame.K_UP:
#                         self.gameturn("go north")
#                     elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
#                         self.gameturn("go south")
#                     elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
#                         self.gameturn("go west")
#                     elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
#                         self.gameturn("go east")
#                     elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_PERIOD:
#                         self.gameturn("wait")
#                     elif event.key == pygame.K_c:
#                         self.gameturn("climb")
#                     elif event.key == pygame.K_0:
#                         self.gameturn("buy", 0)
#                     elif event.key == pygame.K_1:
#                         self.gameturn("buy", 1)
#                     elif event.key == pygame.K_2:
#                         self.gameturn("buy", 2)
#                     elif event.key == pygame.K_3:
#                         self.gameturn("buy", 3)
#                     elif event.key == pygame.K_4:
#                         self.gameturn("buy", 4)
#                     elif event.key == pygame.K_5:
#                         self.gameturn("buy", 5)
#                     elif event.key == pygame.K_6:
#                         self.gameturn("buy", 6)
#                     elif event.key == pygame.K_7:
#                         self.gameturn("buy", 7)
#                     elif event.key == pygame.K_8:
#                         self.gameturn("buy", 8)
#                     elif event.key == pygame.K_9:
#                         self.gameturn("buy", 9)
                        
                        
#             pressedkeys = pygame.key.get_pressed() # keys that you can press all the time
#             #self.allgroup.clear(self.screen, self.background)
#             self.screen.blit(self.background, (0, 0))
#             self.allgroup.update(seconds)
#             self.allgroup.draw(self.screen)    
#             pygame.display.flip()
            
#         pygame.quit()

#     def attack(self, angreifer, verteidiger):
#         msg = "{} is attacking {}!".format(angreifer.name, verteidiger.name)
#         self.log.insert(0, msg)
#         attack = random.random() # 0...1
#         evade = random.random()
#         damage = random.randint(1, angreifer.maxdamage)
#         if attack < angreifer.tohit:
#              msg = "Attack successfull!!"
#              self.log.insert(0,msg)
#              if evade < verteidiger.evade:
#                  msg = "but {} can evade!".format(verteidiger.name)
#                  self.log.insert(0, msg)
#              else:
#                  msg = "{} make {} damage ({} hp left)".format(angreifer.name, damage, verteidiger.hp-damage)
#                  self.log.insert(0, msg)
#                  verteidiger.hp -= damage
#         else:
#              msg = "Attack failed!"
#              self.log.insert(0, msg)
#         #return msg

#     def fight(self, angreifer, verteidiger):
#         x = verteidiger.x * self.tile + self.tile/2
#         y = verteidiger.y * self.tile + self.tile/2
#         for p in range(25):
#             Particle(x,y)
#         #battleround = 0
#         #battleround += 1
#         #print("---------- Battle Round {} ----------".format(battleround))
#         self.attack(angreifer, verteidiger)
#         if verteidiger.hp < 1:
#             self.log.insert(0,"{} wins!".format(angreifer.name))
#             #del Monster.zoo[verteidiger.number]
#             return
#         self.paint()
#         self.attack(verteidiger, angreifer)
#         if angreifer.hp < 1:
#             self.log.insert(0,"{} wins!".format(verteidiger.name))
#             return
#             #input("press enter")
#         self.paint()
        


#     def draw_text(self, text, x=None, y=None, textcolor=None, fontsize=None, surface=None):
#         """Center text in window"""
#         if x is None:
#             x = 50
#         if y is None:
#             y = 150
#         if fontsize is None:
#             fontsize = 24
#         if textcolor is None:
#             textcolor = (0, 0, 0)
#         if surface is None:
#             surface = self.screen
#         font = pygame.font.SysFont('mono', fontsize, bold=True)
#         fw, fh = font.size(text)
#         output = font.render(text, True, (textcolor))
#         surface.blit(output, (x, y))


# if __name__ == '__main__':
#     PygView(1600,800).run() # call with width of window and fps