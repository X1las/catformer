# Description:

# Imports
import pygame as pg

from settings import *

from CustomSprite import CustomSprite
from Vector import Vec
from random import choice, randrange, uniform
import copy

import spritesheet as ss
import math


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


def re(number):
    inte = math.floor(number)
    dec = number - inte
    if dec*10 >= 5:
        result = 1
    else:
        result = 0
    return inte + result



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
    def __init__(self, game, x, y, width, height, name, typ = None, vel = Vec(), maxDist = 0):
        self.solid = True
        self.vel = vel
        self.maxDist = maxDist
        self.height = height; self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.group_platforms, game.group_solid
        self.solidstrength = 10
        self.originalsolidstrength = self.solidstrength
        self.x = x
        
        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)

        # get sprite sheet
        platformSheet = ss.Spritesheet('resources/platforms.png')
        # get individual sprites
        #prettyPlatform = platformSheet.image_at((269,435,102,26), colorkey=(0,0,0))
        end_left = platformSheet.image_at((47,51,34,26), colorkey=(0,0,0))
        end_right = platformSheet.image_at((175,51,34,26), colorkey=(0,0,0))
        mid = platformSheet.image_at((303,51,35,26), colorkey=(0,0,0))
        
    
        #images = platformSheet.images_at([(47,51,34,26),(303,51,35,26),(175,51,34,26)])
        
        # create surface with right size
        self.image = pg.Surface((width,height))
        # blit left end
        self.image.blit(end_left,(0,0))
        # blit middle parts depending on platform width
        numOfMidParts = math.ceil(width/mid.get_width()-2)
        for i in range(numOfMidParts):
            self.image.blit(mid, ((i+1)*end_left.get_width(),0))
        # blit right end
        self.image.blit(end_right,(width-end_right.get_width(),0))


        #self.image = pg.Surface((width,height))
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.typed = "platform"    
        self.pos = vec(x,y);
        self.rect.midbottom = (x,y)
        self.relativePosition = self.pos.copy()
        self._layer = 2
        self.init()


  # Checking if the enemy is outside it's patrolling area
    def checkDist(self):
        if  self.pos.x - self.x >= self.maxDist: # right boundary
            self.area = "right"
            self.vel.x = -1 * abs(self.vel.x)
        elif self.pos.x - self.x <= -1*self.maxDist:
            self.vel.x = abs(self.vel.x)
            self.area = "left"

    def update(self):
        #round(self.pos)
        self.checkDist()
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
        
        self.getImageFromFile('box.png', width, height)

        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.can_fall_and_move = True
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.friction = 0
        self.init()
        self.isPickedUp = False
        self.lift = vec()


    def resetRects(self):
        super().resetRects()
        # Currently, trying to add a "pick UP" effect. This reverses it so it can be added again next time lol
        self.pos.y -= self.lift.y
    

    def update(self):
        self.applyPhysics(self.game.group_solid)
        self.rect.midbottom = self.pos.rounded().asTuple()

    def posCorrection(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.pygamecoll(self.game.group_solid)

    def pickUp(self, interacter):
        # Technically if is IS COLLIDING* but ye
        self.has_collided = True
        
        # Checking which side the box is on. If the box is too close to player upon pickup, most the box away a bit
        if interacter.pos.x < self.pos.x: # if box is right of player
            if abs(interacter.player.right_x() - self.left_x()) < 2: 
                self.pos.x = interacter.player.right_x() + self.width/2 + 2
        else:
            if abs(interacter.player.left_x() - self.right_x()) < 2: 
                self.pos.x = interacter.player.left_x() - self.width/2 - 2

        # Setting how much box should be lifted
        self.lift.y = -3

        # Grapping vel and acc from the interactive field
        self.new_vel.x = interacter.vel.x
        self.new_acc.x = interacter.acc.x
        self.rect.midbottom = self.pos.rounded().asTuple()

    

    def updatePos(self, Intersecters):
        # Only if the box is being picked up, should it get the vel/acc from the interactive field
        if self.has_collided:
            #if not self.isPickedUp:
            self.vel.x = self.new_vel.x
            self.acc.x = self.new_acc.x
            self.isPickedUp = True
            self.addedVel = vec(0,0)
        else:
            if self.isPickedUp == True:
                self.lift.y = 0
            self.vel.x = 0
            self.acc.x = 0
            self.isPickedUp = False
        self.vel += self.addedVel
        self.has_collided = False
        self.pos.y += self.lift.y       # Adding the pick UP effect

        self.pos += self.vel +  self.acc * 0.5
        
        self.rect.midbottom = self.pos.rounded().asTuple()
 
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    def posCorrection(self):
        # I am not sure this is needed
        if self.can_fall_and_move:
            self.pygamecoll(self.game.group_solid)
        self.rect.midbottom = self.pos.rounded().asTuple()
        


# Case SubClass - Inherits from CustomSprite
class Vase(CustomSprite):
    def __init__(self, game, plat : Platform, placement : str, name = None):
        
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
        self.fell_fast_enough = False
        self.init()


    def update(self):
        # Check whether the vase has even fallen yet
        if self.vel.y > 1:
            self.fell_fast_enough = True
        
        self.touchplat(self.game.group_solid)
        
        # fall is set to true in knockover() if conditions are satisfied
        if self.fall == True:
            self.inAir = True
            self.applyGrav()
        self.rect.midbottom = self.pos.rounded().asTuple()

    def breaks(self):
        self.image.fill((250,250,250))
        newPickup = PickUp(self.game, self.pos.x, self.pos.y, 15,15, "health", "spawned pickup")
        self.kill()
        self.broken = True

    # Applies basic gravity
    def applyGrav(self):
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.vel   += self.acc                              # equations of motion
        self.pos += self.vel +  self.acc * 0.5     
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # When it thouches a platform or other solid
    def touchplat(self, group):

        self.rect.midbottom = self.pos.realRound().asTuple()
        collideds = pg.sprite.spritecollide(self, group, False)
        if collideds:
            for collided in collideds:
                if collided != self and collided != self.ignoreSol:
                    if self.fell_fast_enough:
                        self.set_bot(collided.top_y())
                        self.breaks()
                        self.fall = False
                        self.gravity = 0
                        self.vel.y = 0



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
          
            self.rect.update(self.pos.asTuple(), (self.width, self.height))
        # whatever else it needs to deactivate

    def update(self):
       
            
        self.activated = False

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
            
            healthSheet = ss.Spritesheet('resources/heart2.png')
            #self.image = healthSheet.image_at((11,11,27,30), colorkey=(255,255,255))       # for heart1.png
            self.image = healthSheet.image_at((0,0,16,16), colorkey=(0,255,0))          # for heart2.png
            self.image = pg.transform.scale(self.image, (width, height))  # scale Surface to size
            
            #self.getImageFromFile('heart.png',width,height)
        
        if self.type == 'catnip':
            self.getImageFromFile('catnip.png',width,height)

        
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
        self.isEnemy = True
        self.stopMoving = False


    # Checking if the enemy is outside it's patrolling area
    def checkDist(self):
        if  self.pos.x - self.x >= self.maxDist: # right boundary
            self.area = "right"
            self.vel.x = -1 * abs(self.vel.x)
        elif self.pos.x - self.x <= -1*self.maxDist:
            self.vel.x = abs(self.vel.x)
            self.area = "left"

    def updatePos(self, group):
        self.pos +=  self.vel +  self.acc * 0.5


    def update(self):
        self.area = "mid" #Doesn't matter rn, but maybe later?
        # No matter what vel if may have been given (from box e.g.) it should stay at 1 or whatever we choose
        if self.vel.x > 0:
            self.vel.x = 1
        else: 
            self.vel.x = -1
        self.checkDist()
        
        self.acc = vec(0,0)    
        self.collidingWithWall()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def posCorrection(self):
        pass
        #self.pygamecolls(self.game.group_solid)

    # The part that checks whether to just turn around or be pushed
    def pygamecolls(self, group, ignoredSol = None):
        inflation = 0
        self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x += r(self.vel.x)
        self.rect.y += r(self.vel.y)
        collideds = pg.sprite.spritecollide(self, group, False)

        if collideds:
            for collided in collideds:

                if collided != self and collided.name != "p_floor" and self.solidstrength < collided.solidstrength:
                    #if collided.solidstrength > self.solidstrength:
                    self.solidstrength = collided.solidstrength - 1 # So, if enemy is pushed towards platform, it must be "heavier" than box, so box can't push
                    self.count = 5

                    if not self.stopMoving: # If it was inbetween solids
                        coll_side = self.determineSide(collided)
                        if coll_side == "left": # left side of collidedd obj
                            newpos = collided.left_x() - self.width/2
                            if newpos <= self.pos.x: # Make sure it is only if moving the enemy would actually get pushed out on the left side 
                                if collided.vel.x != 0: # If being pushed (so only if being pushed by moving box)
                                    self.pos.x = newpos
                                    self.vel.x = copy.copy(collided.vel.x) #no copy
                                    self.acc.x = collided.acc.x
                                if collided.vel.x == 0: # If collided object is not moving, just turn around
                                    self.vel.x = 1
                                    self.vel.x *= -1
                                if self.collides_left: #remove?
                                    self.vel.x *= 0
                        if coll_side == "right":
                            newpos = collided.right_x() + self.width/2
                            if newpos >= self.pos.x:
                                if collided.vel.x !=  0:
                                    self.pos.x = newpos
                                    self.vel.x = copy.copy(collided.vel.x) # no copy
                                    self.acc.x = collided.acc.x
                                if collided.vel.x == 0:
                                    self.vel.x = 1
                                    self.vel.x *= -1
                                if self.collides_right: #remove?
                                    self.vel.x *= 0
                            self.vel.x *= -1
 
    # Will make the enemy stand still if inbetween solids (instead of vibrating)
    def inbetweenSolids(self):
        inflation = 4
        self.rect = self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        collideds = pg.sprite.spritecollide(self, self.game.group_solid, False)
        result = False
        if collideds:
            for collided in collideds:
                if collided != self and collided.name != "p_floor":
                    if self.solidstrength < collided.solidstrength:
                        self.solidstrength = collided.solidstrength -1
                        count = 2
                    coll_side = self.determineSide(collided)
                    if coll_side == "left": # left side of collidedd obj
                        if self.collides_left:
                            self.vel.x *= 0
                            result = True
                        self.collides_right = True
                    if coll_side == "right":
                        if self.collides_right:
                            result = True
                            self.vel.x *= 0
                        self.collides_left = True
        self.rect = self.rect.inflate(-inflation,-inflation)
          
        return result           
 
        

    def collidingWithWall(self):

        self.stopMoving = self.inbetweenSolids()
        self.pygamecolls(self.game.group_solid)
        self.collides_left = False
        self.collides_right = False


# AI Enemy SubClass 
class AiEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass






