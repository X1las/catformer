# Description:

# Imports
import pygame as pg

from settings import *

from CustomSprite import CustomSprite
from Vector import Vec
from random import choice, randrange, uniform
import copy
import time
from threading import Timer

import Spritesheet as ss
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
    def __init__(self,x,y, width, height, name = None): 
        self.width = width; self.height = height
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levelGoals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def update(self):
        self.rect.midbottom = self.pos.realRound().asTuple()

    # Function that gets called whenever the player reaches a goal
    def activate(self):
        self.game.resetCamera()
        current = self.game.level.name
        level = int(current[5:6])
        level+=1
        print(level)
        self.game.level.name = "level"+str(level)
        self.game.new()  


# Platform SubClass - Inherits from CustomSprite
class Platform(CustomSprite):
    game = None
    def __init__(self, x, y, width, height, name, vel = Vec(), maxDist = 1000, leftMaxDist = 1000, rightMaxDist = 1000, upMaxDist = 0, downMaxDist = 0):
        self.solid  = True
        self.vel    = vel
        self.initX  = x
        self.initY  = y
        self.leftMaxDist = leftMaxDist
        self.rightMaxDist = rightMaxDist
        self.downMaxDist = downMaxDist
        self.upMaxDist = upMaxDist
        self.height = height; self.width = width; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.solidstrength = 10
        self.originalsolidstrength = self.solidstrength
        self.x = x; self.y = y
        self.update_order = 1
        self.typed = "platform"    
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self._layer = 2
        self.init()
        self.isPlatform = True


    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_platforms, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get sprite sheet
        platformSheet = ss.Spritesheet('resources/platforms.png')
        # get individual sprites
        end_left   = platformSheet.image_at((47 ,51, 34,26), colorkey=(0,0,0))
        end_right  = platformSheet.image_at((175,51, 34,26), colorkey=(0,0,0))
        mid        = platformSheet.image_at((303,51, 35,26), colorkey=(0,0,0))
        brownPiece = platformSheet.image_at((303,176,34,32), colorkey=(0,0,0))
        #prettyPlatform = platformSheet.image_at((269,435,102,26), colorkey=(0,0,0))
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        fill = 0
        # blit left end
        self.image.blit(end_left,(0,0))
        fill += end_left.get_height()
        # blit middle parts depending on platform width
        numOfMidParts = math.ceil(self.width/mid.get_width()-2)
        for i in range(numOfMidParts):
            self.image.blit(mid, ((i+1)*end_left.get_width(),0))
        # blit right end
        self.image.blit(end_right,(self.width-end_right.get_width(),0))
        # blit bottom layers until fully filled
        numOfBrownParts_h = math.ceil(self.width/mid.get_width())
        while fill < self.height:
            for i in range(numOfBrownParts_h):
                self.image.blit(brownPiece, (i*end_left.get_width(),fill))
            fill += brownPiece.get_height()

            
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.rect.midbottom = (self.pos.x,self.pos.y)

    """
    def collisionEffect(self):
        inflation = 0
        self.rect = self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()

        self.rect.x += r(self.vel.x)
        self.rect.y -= 2
        collideds = pg.sprite.spritecollide(self, self.game.all_sprites, False)

        if collideds:
            for collided in collideds:
                try: 
                    if collided != self and collided.solidstrength < self.solidstrength:
                    
                        coll_side = collided.determineSide(self)
                        if coll_side == "top":
                            collided.addedVel = self.vel
                except:
                    pass
                    #print(f'2 - acc in coll for {self.name} with {self.acc}')
                    
        
        self.rect = self.rect.inflate(-inflation, -inflation)
    """


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
                    #self.solidstrength = collided.solidstrength - 1 # So, if enemy is pushed towards platform, it must be "heavier" than box, so box can't push
                    #self.count = 5

                    #if not self.stopMoving: # If it was inbetween solids
                    coll_side = self.determineSide(collided)
                    if coll_side == "left": # left side of collidedd obj
                        newpos = collided.left_x() - self.width/2
                        if newpos <= self.pos.x: # Make sure it is only if moving the enemy would actually get pushed out on the left side 
                            if collided.vel.x == 0: # If collided object is not moving, just turn around
                                #self.vel.x = 1
                                self.vel.x *= -1
                    if coll_side == "right":
                        newpos = collided.right_x() + self.width/2
                        if newpos >= self.pos.x:
                            if collided.vel.x == 0:
                                #self.vel.x = 1
                                self.vel.x *= -1
                        self.vel.x *= -1
                    if coll_side == "bot": # left side of collidedd obj
                        newpos = collided.bot_y() - self.height
                        if newpos >= self.pos.y: # Make sure it is only if moving the enemy would actually get pushed out on the left side 
                            if collided.vel.y == 0: # If collided object is not moving, just turn around
                                #self.vel.x = 1
                                self.vel.y *= -1

    # Checking if the enemy is outside it's patrolling area
    def checkDist(self):
        if  self.pos.x - self.x >= self.rightMaxDist: # right boundary
            self.area = "right"
            self.vel.x = -1 * abs(self.vel.x)
        elif self.pos.x - self.x <= -1*self.leftMaxDist:
            self.vel.x = abs(self.vel.x)
            self.area = "left"
        elif self.pos.y - self.y <= -1*self.upMaxDist:
            self.vel.y = abs(self.vel.y)
            self.area = "left"
        elif self.pos.y - self.y >= -1*self.downMaxDist:
            self.vel.y = abs(self.vel.y)
            self.area = "left"

    def update(self):
        #round(self.pos)
        if self.vel.x != 0 or self.vel.y != 0:
            self.originalsolidstrength = 9
            self.solidstrength = 9
        #self.pygamecolls(self.game.group_solid)
        self.checkDist()
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updatePos(self, solid):
        super().updatePos(solid)
        self.pygamecolls(self.game.group_solid)

# Box SubClass - Inherits from CustomSprite
class Box(CustomSprite):
    game = None
    def __init__(self, x, y, width, height, name):
        self.width  = width; self.height = height; self.name = name
        self.initX = x; self.initY = y
        self._layer = 5
        self.solid = True
        self.moveable = True
        self.solidstrength = 5
        self.originalsolidstrength = self.solidstrength
        self.update_order = 5
        
        self.can_fall_and_move = True
        self.pos = vec(x,y)
        self.savedPos = self.pos.copy()
        self.relativePosition = self.pos.copy()
        self.friction = 0
        self.init()
        #self.gravity = PLAYER_GRAV
        self.isPickedUp = False
        self.lift = vec()
        self.beingHeld = False
        self.interacter = None
        

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_boxes, game.group_pressureActivator , game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # load image from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.img = sheet.image_at((0,34,52,41),(0,255,0))
        self.image = pg.transform.scale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.initX,self.initY)

        


    def respawn(self):
        self.pos = vec(self.initX, self.initY)
        self.rect.midbottom = self.pos.rounded().asTuple()

    def resetRects(self):
        super().resetRects()
        # Currently, trying to add a "pick UP" effect. This reverses it so it can be added again next time lol

    def applyPhysics(self,Intersecters, ignoreSol = None):
        
        if self.on_solid(self.game.group_solid):
            self.inAir = False
        else:
            self.inAir = True

        #if self.inAir:
        #   self.gravity = GRAVITY
        #else:
        #   self.gravity = 0

        
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if self.isPlayer and abs(self.vel.x) < 0.0001:
            self.vel.x = 0

        #if self.can_fall_and_move:
        #  self.pygamecoll(Intersecters)
        #self.pos += self.vel +  self.acc * 0.5
        #self.acc = vec(0,0)                   
    def update(self):
        #self.pos.y = self.savedPos.y
        if not self.inAir:
            self.pickupStarted = False
        self.savedpos = self.pos.copy()

        self.rect.midbottom = self.pos.realRound().asTuple()
        #print(f'vel: {self.vel}')
        self.applyPhysics(self.game.group_solid)
        self.vel += self.addedVel 
        if self.has_collided:
            #if not self.isPickedUp:
            """ DO NOT DELETE """
            self.new_vel.x = self.interacter.vel.x
            self.new_acc.x = self.interacter.acc.x
            self.rect.midbottom = self.pos.realRound().asTuple()
            if self.beingHeld:
                self.vel.x = self.new_vel.x
                self.acc.x = self.new_acc.x
                self.gravity = 0
            """"""
            #self.pos.x += self.new_vel.x +  self.new_acc.x * 0.5
            
            self.isPickedUp = True
            #self.addedVel = vec(0,0)
        else:
            if self.isPickedUp == True:
                self.lift.y = 0
            self.isPickedUp = False
            #print(f'addedVel: {self.addedVel}')
            #self.vel.x = 0
            #self.acc.x = 0
            self.beingHeld = False
        if self.beingHeld == False:
            #self.addedVel = vec(0,0)
            self.gravity = GRAVITY
        self.pygamecoll(self.game.group_solid)
    




    def resets(self):
        pass
        #self.pos.y -= self.lift.y # MOVE AWAY



    def posCorrection(self):
        self.rect.midbottom = self.pos.realRound().asTuple()

    def liftedBy(self,interacter):
        #if not pg.sprite.spritecollideany(self, self.game.group_solid):
        if interacter.pos.x < self.pos.x: # if box is right of player
            if abs(interacter.player.right_x() - self.left_x()) < 4: 
                self.pos.x = interacter.player.right_x() + self.width/2 + 4
        else:
            if abs(interacter.player.left_x() - self.right_x()) < 4: 
                self.pos.x = interacter.player.left_x() - self.width/2 - 4
        # Setting how much box should be lifted
        #self.lift.y = -3
        #self.pos.y += self.lift.y       # Adding the pick UP effect
        self.interacter = interacter
        self.solidstrength = self.originalsolidstrength -1
        #self.interacter.player.solidstrength = 6
        if not interacter.player.inAir:
            self.beingHeld = True
            self.pos.y = interacter.player.pos.y - 5
        else: 
            self.beingHeld = False
        self.rect.midbottom = self.pos.realRound().asTuple()




    def pickUp(self, interacter):
        # Technically if is IS COLLIDING* but ye
        #self.has_collided = True
        
        # Checking which side the box is on. If the box is too close to player upon pickup, most the box away a bit
            #self.gravity = GRAVITY
        #else:   
        #   self.inAir = True
        #if not interacter.player.inAir:
        #   self.pos.y = interacter.player.pos.y - 3
        #  self.inAir = True
        # Grapping vel and acc from the interactive field
        pass
    

    

    def updatePos(self, Intersecters):
        # Only if the box is being picked up, should it get the vel/acc from the interactive field
            #self.pos.x += self.vel.x +  self.acc.x * 0.5
        #self.pos.y += self.vel.y +  self.acc.y * 0.5
        """DO NOT DELETE """
        self.pos += self.vel +  self.acc * 0.5
        """"""
        self.has_collided = False
        self.rect.midbottom = self.pos.realRound().asTuple()

        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)



    def posCorrection(self):
        # I am not sure this is needed
        #if self.can_fall_and_move:
        self.pygamecoll(self.game.group_solid)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.vel.x = self.addedVel.x
        


# Case SubClass - Inherits from CustomSprite
class Vase(CustomSprite):
    def __init__(self, plat : Platform, placement : str, name = None):
        self.plat = plat
        self.pos = vec()
        self.placement = placement
        try:
            if self.placement == "left":
                self.pos = self.plat.topleft()
            
                push = 20   
            elif self.placement == "right":
                self.pos = self.plat.rect.topright
                push = -20
            elif self.placement == "mid":
                push = 0
                self.pos.x, self.pos.y = self.plat.rect.midtop.x, self.plat.rect.midtop.y 
            self.pos.x = self.pos.x+ push; self.pos.y = self.pos.y; self.ignoreSol = self.plat
            
        except Exception as e:
            print(e)
            print("Must choose left, right or mid")    
            #x = self.plat.rect.midtop[0]; y = self.plat.rect.midtop[1]; self.ignoreSol = self.plat
        self.broken = False
        self.name = name
        self.breakable = True
        
        self.fall = False
        self.gravity = PLAYER_GRAV
        self.can_fall_and_move = True
        self.ignoreSol = plat
        self.relativePosition = self.pos.copy()
        self.isVase = True
        self.fell_fast_enough = False
        self.init()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_vases
        pg.sprite.Sprite.__init__(self, self.groups)
        self.width  = 29
        self.height = 26
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        whole = pg.Rect( 0,0,29,26)
        broken = pg.Rect(30,0,29,26)
        rects = [whole, broken]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     
        self.image_whole = self.images[0]
        self.image_broken = self.images[1]
        self.image = self.image_whole
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)


    def update(self):
        # Check whether the vase has even fallen yet
        if not self.broken:
            if self.vel.y > 1:
                self.fell_fast_enough = True
            
            self.touchplat(self.game.group_solid)
            
            # fall is set to true in knockover() if conditions are satisfied
        self.vel += self.addedVel
        if self.fall == True:
            self.inAir = True
            self.applyGrav()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def breaks(self):
        self.image.blit(self.images[1],(0,0))
        self.vel.x = 0
        #self.addedVel.x = 0
        newPickup = PickUp(self.pos.x, self.pos.y, 15,15, "health", "spawned pickup")
        newPickup.startGame(self.game)
        #self.game.all_sprites.remove(self)
        #self.game.group_passives.add(self)
        #self.kill()
        self.broken = True

    # Applies basic gravity
    def applyGrav(self):
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.vel   += self.acc                              # equations of motion
        #self.pos += self.vel +  self.acc * 0.5     

    def posCorrection(self):
        if self.broken:
            self.pygamecoll(self.game.group_solid)
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)


    # When it thouches a platform or other solid
    def touchplat(self, group):

        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.y += r(self.vel.y + 4) 
        collideds = pg.sprite.spritecollide(self, group, False)
        if collideds:
            for collided in collideds:
                if collided != self and collided != self.ignoreSol:
                    if self.fell_fast_enough:
                        self.set_bot(collided.top_y())
                        if not self.broken:
                            self.breaks()
                        #self.fall = False
                        #self.gravity = 0
                        self.vel.y = 0
                        #self.vel.x = 0
                        #self.addedVel.x = 0



# Lever SubClass - Inherits from CustomSprite
class Lever(CustomSprite):
    def __init__(self,x,y, width, height, name = None, effect = None, movespeed = None, target = None, autodeactivate = None): 
        self.width = width; self.height = height
        self.effect = effect; self.target = target; self.movespeed = movespeed
        self.auto_deactivate = autodeactivate
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.deactivate_counter = 30
        self.activated = False
        self.deactivated = True
        self.x = x; self.y = y
        
    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,200,200))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x,self.y)


    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.image.fill((255,255,255))
            if self.auto_deactivate:
                t = Timer(2, self.deactivate)
                t.start()
            if self.effect == "respawn":
                self.target.respawn()
            if self.effect == "move":
                self.target.vel.x = self.movespeed

        # whatever else it needs to activate
    

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
        
            self.image.fill((0,200,200))
            if self.effect == "move":
                self.target.vel.x = 0
        # whatever else it needs to deactivate
            
    

    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.realRound().asTuple()


# Button SubClass - Inherits from CustomSprite
class Button(CustomSprite):
    #def __init__(self,game,x,y, width, height, name = None, effect = [None], movespeed = None, target = None): 
    def __init__(self,x,y, width, height, name = None, effect = {}): 
        self.x = x; self.y = y
        self.effect = effect; #self.target = target; self.movespeed = movespeed
        self.width = width; self.height = height
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.activated = False
        self.deactivated = True

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((200,0,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x,self.y)






    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
            try:
                for e,v in self.effect.items():
                    if e == "respawn":
                        self.target.respawn()
                    if e == "move":

                        for move in v:
                            move['target'].vel = move["movespeed"]
            except: 
                pass
                    #self.target.vel = self.movespeed
            
        # whatever else it needs to activate
        

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
        
            self.rect.update(self.pos.asTuple(), (self.width, self.height))
        # whatever else it needs to deactivate
            try: # shouldn't be try except, I think
                for e,v in self.effect.items():
                    if e == "respawn":
                        self.target.respawn()
                    if e == "move":

                        for move in v:
                            target = move["target"]
                            #nextpos = target.pos + target.vel  
                            #if not (target.x -1 < nextpos.x < target.x + 1) and not (target.y -1 < nextpos.y < target.y + 1):  
                            move['target'].vel = move["movespeed"] * (-1)
            except Exception as e:
                print(e) 
                pass
            #for e in self.effect: 
            #   if e == "move":
            #      self.target.vel = vec()
            

    def update(self):
    
            
        self.activated = False

        self.rect.midbottom = self.pos.realRound().asTuple()


# Pickup SubClass - Inherits from CustomSprite
class PickUp(CustomSprite):

    def __init__(self,x,y, width, height, type_, name = None): 
        self.width = width; self.height = height
        self.type = type_
        self.pickup = True
        
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_pickups
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.Surface((self.width,self.height))
        if self.type == 'health':
            
            healthSheet = ss.Spritesheet('resources/heart.png')
            self.image = healthSheet.image_at((0,0,16,16), colorkey=(0,255,0))
            self.image = pg.transform.scale(self.image, (self.width, self.height))  # scale Surface to size
        
        if self.type == 'catnip':
            self.getImageFromFile('catnip.png',self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)



    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.realRound().asTuple()


# ------- HOSTILES ------- #


# Hostile UpperClass - Inherits from CustomSprite
class Hostile(CustomSprite):
    pass

# Water SubClass - Inherits from Hostile
class Water(Hostile):
    def __init__(self,x,y, width, height, name = None): 
        self.width = width; self.height = height
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def update(self):
        '''
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images)*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        self.image = self.images[math.floor(self.imageIndex/10)]
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        '''
        #round(self.pos) 
        self.rect.midbottom = self.pos.realRound().asTuple()


    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        rect1 = pg.Rect( 0,0,16,16)
        rect2 = pg.Rect(16,0,16,16)
        rect3 = pg.Rect(32,0,16,16)
        rect4 = pg.Rect(48,0,16,16)
        blue  = pg.Rect( 0,4,16,10)
        rects = [rect1, rect2, rect3, rect4, blue]
        # load images from spritesheet
        waterSheet = ss.Spritesheet('resources/water.png')
        self.images = waterSheet.images_at(rects, colorkey=(0,0,0))
        self.imageIndex = 0
        #self.image = self.images[self.imageIndex]

        fill_h = 0      # for tracking how much was filled horizontally
        fill_v = 0      # for tracking how much was filled vertically
        # filling horizontally
        numOfWaveParts = math.ceil(self.width/self.images[0].get_width())
        while fill_h < self.width:
            for i in range(len(self.images)-1):
                self.image.blit(self.images[i], (fill_h,0))
                fill_h += self.images[i].get_width()
        fill_v += self.images[0].get_height()
        # filling vertically
        while fill_v < self.height:
            for i in range(numOfWaveParts):
                self.image.blit(self.images[4], (self.images[4].get_width()*i,fill_v))
            fill_v += self.images[4].get_height()
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

        
    # Catnip
    # Health (fish)


# Patrolling Enemy SubClass - Inherits from Hostile
class PatrollingEnemy(Hostile):
    def __init__(self,x,y, width, height, maxDist, name = "enemy"):
        self._layer = 10
        self.x = x
        self.width          = width; self.height = height
        
        self.pos            = vec(x,y);     self.vel =  vec(1, 0);     self.acc = vec(0, 0)
        self.maxDist = maxDist
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
        #self.facing = None

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        wormSheet = ss.Spritesheet('resources/worm-spritesheet.png')
        # get individual sprites and add to list
        self.images_right = []
        self.images_right.append(wormSheet.image_at((  4, 36, 29, 28), (0,0,0)))    # (x,y,width,height)
        self.images_right.append(wormSheet.image_at(( 36, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at(( 68, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((100, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((132, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((164, 36, 29, 28), (0,0,0)))
        self.images_left = []
        for img in self.images_right:
            self.images_left.append(pg.transform.flip(img,True,False))

        self.imageIndex = 0
        self.image = self.images_right[self.imageIndex]
    
        # scale image to correct size
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)


    # Checking if the enemy is outside its patrolling area
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
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images_right)*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        
        self.area = "mid" #Doesn't matter rn, but maybe later?
        # No matter what vel if may have been given (from box e.g.) it should stay at 1 or whatever we choose
        if self.vel.x > 0:
            self.vel.x = 1
            self.image = self.images_right[math.floor(self.imageIndex/10)]   # update current image
        else: 
            self.vel.x = -1
            self.image = self.images_left[math.floor(self.imageIndex/10)]   # update current image

        
        self.image = pg.transform.scale(self.image, (self.width, self.height))  # rescale image
        
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
                        elif coll_side == "bot":
                            if  abs(self.right_x() - collided.left_x()) < abs(collided.right_x() - self.left_x() ):
                                self.pos.x = collided.left_x() - self.width/2
                            else: 
                                self.pos.x = collided.right_x() + self.width/2

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
    def __init__(self,x,y, width, height, game, name = "enemyai"):
        self._layer = 10
        self.x = x
        self.width          = width; self.height = height
        self.game = game
        self.pos            = vec(x,y)
        self.vel =  vec(0, 0)
        self.acc = vec(0, 0)
        self.relativePosition = self.pos.copy()
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
        #self.facing = None

    def playerLeft(self, game):
        result = False
        if (game.player.pos.x < self.pos.x and self.pos.x - game.player.pos.x < 200):
            result = True
        return result
            
    def onPlayer(self, game):
        result = False
        if (abs(game.player.pos.x - self.pos.x) <5):
            result = True
        return result

    def playerRight(self, game):
        result = False
        if (game.player.pos.x > self.pos.x and game.player.pos.x - self.pos.x < 200):
            result = True
        return result

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        wormSheet = ss.Spritesheet('resources/worm-spritesheet.png')
        # get individual sprites and add to list
        self.images_right = []
        self.images_right.append(wormSheet.image_at((  4, 36, 29, 28), (0,0,0)))    # (x,y,width,height)
        self.images_right.append(wormSheet.image_at(( 36, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at(( 68, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((100, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((132, 36, 29, 28), (0,0,0)))
        self.images_right.append(wormSheet.image_at((164, 36, 29, 28), (0,0,0)))
        self.images_left = []
        for img in self.images_right:
            self.images_left.append(pg.transform.flip(img,True,False))

        self.imageIndex = 0
        self.image = self.images_right[self.imageIndex]
    
        # scale image to correct size
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)



    def updatePos(self, group):
        self.pos +=  self.vel +  self.acc * 0.5


    def update(self):
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images_right)*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        
        # No matter what vel if may have been given (from box e.g.) it should stay at 1 or whatever we choose
        if self.onPlayer(self.game):
            self.vel.x = 0
        elif self.playerRight(self.game):
            self.vel.x = 1
            self.image = self.images_right[math.floor(self.imageIndex/10)]   # update current image
        elif self.playerLeft(self.game): 
            self.vel.x = -1
            self.image = self.images_left[math.floor(self.imageIndex/10)]   # update current image
        else:
            self.vel.x = 0

        
        self.image = pg.transform.scale(self.image, (self.width, self.height))  # rescale image
        
        self.acc = vec(0,0)    
        self.collidingWithWall()
        self.rect.midbottom = self.pos.realRound().asTuple()
        

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






