# Description:

# Imports
import pygame as pg

from settings import *

from CustomSprite import CustomSprite
from Vector import Vec
from random import choice, randrange, uniform
import copy

# Variables
vec = Vec

# Functions
def r(number):
    rounded_num = number
    rounded_num = abs(rounded_num)
    rounded_num = math.ceil(rounded_num)
    if number < 0:
        rounded_num *= -1
    return rounded_num


# Tester SubClass - Inherits from CustomSprite
class Tester(CustomSprite):
    def __init__(self, game,  pos):

        # anchor depends on which way player faces
        pg.sprite.Sprite.__init__(self, game.all_sprites)  
        self.player = player
        width = self.player.width/2 + 50
        height = self.player.height       
        self.facing = facing
        self.image = pg.Surface((width,height)); 
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.image.fill((255,255,255))
        self.relativePosition = self.pos.copy()
        self.midbottom = pos


# ------- OBJECTS ------- #


# LevelGoal SubClass - Inherits from CustomSprite
class LevelGoal(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.group_levelGoals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()


    def update(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    # Function that gets called whenever the player reaches a goal
    def activate(self):
        self.game.resetCamera()
        current = self.game.level.name
        level = int(current[5:6])
        level+=1
        self.game.level.name = "level"+str(level)
        self.game.new()  


# Platform SubClass - Inherits from CustomSprite
class Platform(CustomSprite):
    def __init__(self, game, x, y, width, height, name, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        self.solid = True
        self.height = height; self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.group_platforms, game.group_solid
        self.solidstrength = 10
        self.originalsolidstrength = self.solidstrength
        
        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.typed = "platform"    
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y); self.vel = vec(0,0)
        self.relativePosition = self.pos.copy()
        self._layer = 2
        self.init()

 
    


    def update(self):
        #round(self.pos)
        self.rect.midbottom = self.pos.rounded().asTuple()


# Box SubClass - Inherits from CustomSprite
class Box(CustomSprite):
    def __init__(self, game, x, y, width, height, name):
        self.game   = game;  self.width  = width; self.height = height; self.name = name
        self._layer = 5
        self.solid = True
        self.moveable = True
        self.groups = game.all_sprites, game.group_boxes, game.group_pressureActivator , game.group_solid
        self.solidstrength = 5
        self.originalsolidstrength = self.solidstrength
        self.update_order = 3
        
        image = pg.image.load("resources/box.png")              # load box image
        self.image = pg.Surface((width, height))                # create box size
        pg.transform.scale(image, (width, height), self.image)  # scale image to size

        pg.sprite.Sprite.__init__(self, self.groups)
        #self.image = pg.Surface((width,height))
        #self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.can_fall_and_move = True
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.friction = 0
        self.init()
        self.isPickedUp = False
        self.lift = vec()


   
    def update(self):
        self.applyPhysics(self.game.group_solid)
        #self.vel.x = self.overwritevel.x
        #self.pos += self.vel
        #self.pygamecoll(self.game.group_solid)
        #self.pos += self.vel 

        self.rect.midbottom = self.pos.rounded().asTuple()
        self.pos -= self.lift
        #wself.pos.y -= self.lift.y
        #self.pos -= self.lift

    def posCorrection(self):
        self.pygamecoll(self.game.group_solid)
    def pickUp(self, interacter):
        self.has_collided = True

        self.new_vel.x = interacter.vel.x
        if interacter.pos.x <self.pos.x:
            self.lift.x = 2
        else:
            self.lift.x = -2
        self.lift.y = -3
        #if self.new_vel.x <= 0.0000000000000000001:
         #   self.new_vel.x = 0
        self.new_acc.x = interacter.acc.x


    

    def updatePos(self, Intersecters):
        if self.has_collided:
            if not self.isPickedUp:
                self.lift.x = 0
            self.vel.x = self.new_vel.x
            self.acc.x = self.new_acc.x
            self.isPickedUp = True
        else:
            if self.isPickedUp == True:
                self.pos.x += self.lift.x 
                self.lift = vec(0,0)
            self.vel.x = 0
            self.acc.x = 0
            self.isPickedUp = False
            
        self.has_collided = False
        self.pos += self.lift
        print(f'vel: {self.name}: {self.vel}')
        print(f'acc: {self.name}: {self.acc}')
        self.pos += self.vel +  self.acc * 0.5
        self.rect.midbottom = self.pos.rounded().asTuple()

        """
        try:
            self.pos -= vec(addx, lift)
        except:
            pass
        """
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)
        #if self.can_fall_and_move:
         #   self.pygamecoll(Intersecters)

    def posCorrection(self):
        if self.can_fall_and_move:
            self.pygamecoll(self.game.group_solid)


# Case SubClass - Inherits from CustomSprite
class Vase(CustomSprite):
    def __init__(self, game, plat : Platform, placement : str , name = None):
        
        try:
            if placement == "left":
                pos = plat.topleft()
             
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos.x, pos.y = plat.rect.midtop.x, plat.rect.midtop.y 
            game = game; x = pos.x+ push; y = pos.y; name = name; ignoreSol = plat
            
        except:
            print("Must choose left, right or mid")    
            game = game; x = plat.rect.midtop[0]; y = plat.rect.midtop[1]; ignoreSol = plat


        self.broken = False; self.name = name
        self.breakable = True
        self.width = 20
        self.height = 30
        self.game = game
        self.groups = game.all_sprites, game.group_vases
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.fall = False
        self.gravity = PLAYER_GRAV
        self.can_fall_and_move = True
        self.ignoreSol = plat
        self.relativePosition = self.pos.copy()
        self.isVase = True
        self.init()


    def update(self):
        
        #round(self.pos)
        self.touchplat(self.game.group_solid)
        if self.fall == True:
            print("should fall")
            self.inAir = True
            self.applyGrav()
        
        
        #if self.on_solid(self.game.group_solid) != self.ignoreSol:
         #   self.breaks()
          #  self.fall = False
        self.rect.midbottom = self.pos.rounded().asTuple()

    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True

    def applyGrav(self):
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        self.pos += self.vel +  self.acc * 0.5     
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    def touchplat(self, group):
        inflation = 2

        self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x += r(self.vel.x)
        self.rect.y += r(self.vel.y)
        collideds = pg.sprite.spritecollide(self, group, False)

        if collideds:
            for collided in collideds:
                if collided != self and collided != self.ignoreSol:
                  

                    self.set_bot(collided.top_y())
                    self.breaks()
                    self.fall = False
                    self.gravity = 0
                    self.vel.y = 0
                  
        self.rect.inflate(-inflation, -inflation)




    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str , name = None):
        try:
            if placement == "left":
                pos = plat.topleft()
             
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos.x, pos.y = plat.rect.midtop.x, plat.rect.midtop.y 
            return cls(game = game, x = pos.x+ push, y = pos.y, name = name, ignoreSol = plat)
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1], ignoreSol = plat)
        #print(plat)
        self.ignoreSol = plat


# Lever SubClass - Inherits from CustomSprite
class Lever(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.group_levers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,200,200))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

        self.activated = False
        self.deactivated = True
        

    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.image.fill((255,255,255))
        # whatever else it needs to activate
     
            
        
        

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
          
            self.image.fill((0,200,200))
        # whatever else it needs to deactivate
            
    

    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


# Button SubClass - Inherits from CustomSprite
class Button(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.group_buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((200,0,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.activated = False
        self.deactivated = True

    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
        # whatever else it needs to activate
        

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
            #if self.prevActivated:
          
            self.rect.update(self.pos.asTuple(), (self.width, self.height))
            #    self.prevActivated = False
        # whatever else it needs to deactivate

    def update(self):
       
            
        self.activated = False

        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


# Pickup SubClass - Inherits from CustomSprite
class PickUp(CustomSprite):

    def __init__(self,game,x,y, width, height, type_, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.group_pickups
        self.type = type_
        self.pickup = True
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        if self.type == 'health':
            self.image.fill((255,0, 200))
        
        if self.type == 'catnip':
            self.image.fill((165, 42, 42))

        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


# ------- HOSTILES ------- #


# Hostile UpperClass - Inherits from CustomSprite
class Hostile(CustomSprite):
    pass

# Water SubClass - Inherits from Hostile
class Water(Hostile):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.group_damager
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,0,200))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
    def update(self):

        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


        
    # Catnip
    # Health (fish)
    # Zoomies (yarn)


# Patrolling Enemy SubClass - Inherits from Hostile
class PatrollingEnemy(Hostile):
    def __init__(self,game,x,y, width, height, maxDist, name = "enemy"):
        self._layer = 10
        self.x = x
        self.groups = game.all_sprites, game.group_damager, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)
        self.width          = width; self.height = height
        self.image          =  pg.Surface((self.width,self.height)); self.image.fill((145,12,0)); self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(1, 0);     self.acc = vec(0, 0)
        self.maxDist = maxDist
        self.game = game
        self.relativePosition = self.pos.copy()
        self.area = "mid"
        self.collides_right = False
        self.dontmove = False
        self.collides_left = False
        self.solidstrength = 3
        self.originalsolidstrength = self.solidstrength

        self.name = name
        self.count = 5
        self.init()


    
    def checkDist(self):
        if  self.pos.x - self.x >= self.maxDist: # right boundary
            self.area = "right"
            self.vel.x = -1 * abs(self.vel.x)
        elif self.pos.x - self.x <= -1*self.maxDist:
            self.vel.x = abs(self.vel.x)
            self.area = "left"

    def updatePos(self, group):
        self.pos = self.pos + self.vel +  self.acc * 0.5



    def update(self):
        #self.pos += self.vel  
        self.area = "mid"
        self.count -= 1
        if self.count <= 0:
            self.solidstrength = 3
        if self.vel.x > 0:
            self.vel.x = 1
        else: 
            self.vel.x = -1
        self.checkDist()
        
        self.acc = vec(0,0)    
        self.collidingWithWall()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def posCorrection(self):
        self.pygamecoll(self.game.group_solid)

    def pygamecolls(self, group, ignoredSol = None):
        inflation = 1
        self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        #self.rect.x += r(self.vel.x)
        #self.rect.y += r(self.vel.y)
        collideds = pg.sprite.spritecollide(self, group, False)

        if collideds:
            for collided in collideds:

                if collided != self and collided.name != "p_floor" and self.solidstrength < collided.solidstrength:
                    #if collided.solidstrength > self.solidstrength:
                    self.solidstrength = collided.solidstrength - 1
                    self.count = 5
                    coll_side = self.determineSide(collided)
                    if coll_side == "left": # left side of collidedd obj
                        newpos = collided.left_x() - self.width/2
                        if newpos <= self.pos.x:
                            if collided.vel.x != 0:
                                self.pos.x = newpos
                                self.vel.x = copy.copy(collided.vel.x)
                                self.acc.x = collided.acc.x
                            if collided.vel.x == 0:
                                self.vel.x = 1
                                self.vel.x *= -1
                            if self.collides_left:
                                self.vel.x *= 0
                            
                                #self.add(self.game.group_solid)
                                #self.dontmove = True
                        #self.vel.x = -1 * abs(self.vel.x)
                    if coll_side == "right":
                        newpos = collided.right_x() + self.width/2

                        if newpos >= self.pos.x:
                            if collided.vel.x !=  0:
                                self.pos.x = newpos
                                self.vel.x = copy.copy(collided.vel.x)
                                self.acc.x = collided.acc.x

                            if collided.vel.x == 0:
                                self.vel.x = 1
                                self.vel.x *= -1
                            if self.collides_right:
                                #self.add(self.game.group_solid)
                        
                                self.vel.x *= 0
                            
                                #self.dontmove = True
                            #self.vel.x = abs(self.vel.x)
                    
                        self.vel.x *= -1
                #elif collided.name == "p_floor":
                 #   self.solidstrength = 3
        #else: 
         #   self.solidstrength = 3
        #self.rect.x -= r(self.vel.x)
        #self.rect.y -= r(self.vel.y)
 
        
        

    def collidingWithWall(self):
        #if not self.dontmove:
        self.pygamecolls(self.game.group_solid)
        #else: 
         #   self.vel.x = 0
        #self.pygamecolls2(self.game.group_solid)


# AI Enemy SubClass 
class AiEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass






