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
# ------- OBJECTS ------- #


# LevelGoal SubClass - Inherits from CustomSprite
class LevelGoal(CustomSprite):
    def __init__(self,plat, placement, width = 100, height = 20, name = "Goal"): 
        self.pos = Vec(plat.left_x() + placement, plat.top_y()) 
        self.width = width; self.height = height
        self.relativePosition = self.pos.copy()
        self.sleepcount = 0

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levelGoals, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        # load image from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.image = sheet.image_at((0,280,55,20),(0,255,0))
        #self.image = pg.transform.scale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def update(self):
        self.endGoal(self.game.player)
        self.rect.midbottom = self.pos.realRound().asTuple()

    # Function that gets called whenever the player reaches a goal
    def nextLevel(self):
       
        self.game.resetCamera()
        current = self.game.level.name
        level = int(current[5:6])
        level+=1
        self.game.level.name = f"level{level}"
        self.game.saveData(levelname = self.game.level.name, lives = self.game.player.lives, catnip = self.game.player.catnip_level)
        self.game.new()

    def endGoal(self, player):
        has_collided = pg.sprite.collide_rect(self, player)
        if has_collided:
            self.game.endinglevel = True
            self.game.player.image = self.game.player.images['sleep']
            self.sleepcount += 1
            pg.draw.rect(self.game.screen, (0,0,0), self.darkener)
            if self.sleepcount > 100:
                self.nextLevel()
                self.sleepcount = 0
            

# Platform SubClass - Inherits from CustomSprite
class Platform(CustomSprite):

    game = None
    def __init__(self, x, y, width, height, name = "plat", vel = Vec(), floorplat = False, maxDist = None, leftMaxDist = 1000, rightMaxDist = 1000, upMaxDist = 2, downMaxDist = 2):
        self.height = height; self.width = width; self.name = name; 
        self.pos = vec(x,y); self.vel = vel
        self.originalVel = self.vel.copy()
        self.floorplat = floorplat
        


        ''' probably not needed'''
        self.typed = "platform"    
        self.solid = True
        self.x = x; self.y = y # change to initX?

        ''' really not sure'''

        ''' pretty sure is needed'''
        self._layer = 2                                                 # Typical self.smth = smth
        self.initX = x
        self.initY = y

        ''' should be revisited'''
        self.relativePosition = self.pos.copy()
        if maxDist == None:
            self.leftMaxDist = leftMaxDist
            self.rightMaxDist = rightMaxDist
            self.downMaxDist = downMaxDist
            self.upMaxDist = upMaxDist
        else: 
            self.leftMaxDist = maxDist
            self.rightMaxDist = maxDist
            self.downMaxDist = maxDist
            self.upMaxDist = maxDist

        self.solidstrength = 30
        if floorplat:
            self.solidstrength = 50
        self.originalsolidstrength = self.solidstrength
        ''' in use'''

        self.update_order = 1
        self.init()
        



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

    # Checking if the enemy is outside it's patrolling area
    def checkDist(self):
        if  self.pos.x - self.x >= self.rightMaxDist and self.vel.x > 0: # right boundary
            self.vel.x = -1 * abs(self.originalVel.x)
        elif self.pos.x - self.x <= -1*self.leftMaxDist and self.vel.x < 0:
            self.vel.x = abs(self.originalVel.x)
        elif self.pos.y - self.y <= -1* abs(self.upMaxDist) and self.vel.y < 0:
            self.vel.y =  abs(self.originalVel.y)
        elif self.pos.y - self.y >= self.downMaxDist and self.vel.y > 0:
            self.vel.y =  -1* abs(self.originalVel.y)

    def update(self):
        if self.vel.x != 0 or self.vel.y != 0:
            self.originalsolidstrength = 29.5
            self.solidstrength = 29.5
            self.init() # Needs to update massHOR and massVER
        self.checkDist()
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updatePos(self):
        self.checkDist()
        super().updatePos()
        self.pygamecolls(self.game.group_solid)


    def pygamecolls(self, group, ignoredSol = None):
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x +=self.r(self.vel.x)
        self.rect.y +=self.r(self.vel.y)
        collideds = pg.sprite.spritecollide(self, group, False)

        if collideds:
            for collided in collideds:
                if collided != self and self.solidstrength <= collided.solidstrength and not collided.floorplat:
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    #coll_side = self.determineSide(collided)
                    if coll_side == "top":
                        self.vel.y = self.originalVel.y * (-1)
                    if coll_side == "left": # left side of collidedd obj
                        if collided.vel.x == 0: # If collided object is not moving, just turn around
                            self.vel.x = self.originalVel.x * (-1)
                    if coll_side == "right":
                        if collided.vel.x == 0:
                            self.vel.x = self.originalVel.x * (-1)
                    if coll_side == "bot": # left side of collidedd obj
                        self.vel.y = self.originalVel.y * (-1)
                    self.pos = correctedPos
        self.rect.midbottom = self.pos.realRound().asTuple()





# Box SubClass - Inherits from CustomSprite
class Box(CustomSprite):
    game = None
    def __init__(self, x, y, width = 44, height = 44, name = "box"):
        self.width  = width; self.height = height; self.name = name
        self.pos = vec(x,y)
        self.savedPos = self.pos.copy()

                
        ''' probably not needed'''
        self.friction = 0
        self.solid = True
        self.moveable = True

        ''' just for testing?'''

        ''' really not sure'''
        self.initX = x; self.initY = y

        ''' pretty sure is needed'''
        self._layer = 5

        ''' should be revisited'''
        self.solidstrength = 5
        self.originalsolidstrength = self.solidstrength
        self.relativePosition = self.pos.copy() # go to init() ?


        ''' in use'''
        #self.new_vel = Vec(), self.new_acc = Vec() 
        self.has_collided = False
        self.beingHeld = False
        self.interacter = None
        self.justreleased = False
        self.update_order = 5
        self.init()





    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_boxes, game.group_pressureActivator , game.group_solid, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        # create surface with correct size
        #self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # load image from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.img = sheet.image_at((0,34,52,41),(0,255,0))
        self.image = pg.transform.scale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.initX,self.initY)

        


    def respawn(self):
        self = self.__init__(self.initX, self.initY, self.width, self.height, self.name)

    def update(self):
        self.savedpos = self.pos.copy()
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.applyPhysics()
        self.vel += self.addedVel 
        if self.has_collided:
            """ DO NOT DELETE """
            if self.beingHeld:
                self.new_vel = self.interacter.vel.copy()
                self.new_acc = self.interacter.acc.copy()
                self.vel.x = self.new_vel.x
                self.vel.y = 0
                self.acc.x = self.new_acc.x
                self.gravity = 0
            """"""
            
        else:
            self.beingHeld = False
            if self.justreleased:
                self.pos = self.pos.realRound()
                self.justreleased = False
        if self.beingHeld == False:
            self.gravity = GRAVITY
        self.solidCollisions(self.game.group_solid)
        self.rect.midbottom = self.pos.rounded().asTuple()




    def liftedBy(self,interacter):
        """ remove?
        if interacter.pos.x < self.pos.x: # if box is right of player
            if abs(interacter.player.right_x() - self.left_x()) < 4: 
                self.pos.x = interacter.player.right_x() + self.width/2 
        else:
            if abs(interacter.player.left_x() - self.right_x()) < 4: 
                self.pos.x = interacter.player.left_x() - self.width/2
        """
        # Setting how much box should be lifted
        self.interacter = interacter
        if not interacter.player.inAir or interacter.player.vel.y > 0:
            self.beingHeld = True
            self.pos.y = interacter.player.pos.y - 3
            if not self.stoppedHOR:
                self.interacter.player.massHOR = self.ori_massHOR + 1
            self.justreleased = True
        else: 
            self.beingHeld = False
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updatePos(self):
        # Only if the box is being picked up, should it get the vel/acc from the interactive field
        """DO NOT DELETE """
        self.pos += self.vel +  self.acc * 0.5
        """"""
        self.has_collided = False
        self.rect.midbottom = self.pos.realRound().asTuple()

        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)



    def posCorrection(self):
        # I am not sure this is needed
        self.solidCollisions(self.game.group_solid)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.vel.x = self.addedVel.x
        


# Case SubClass - Inherits from CustomSprite
class Mug(CustomSprite):
    def __init__(self, plat : Platform, placement, width = 29, height = 26, name = "mug", spawn = None):
        self.plat = plat
        self.pos = vec()
        self.spawn = spawn
        self.width  = width
        self.height = height
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()).rounded() 
        self.placement = placement
        """
        try:
            if self.placement == "left":
                #self.pos = Vec(self.plat.left_x() + 20 + self.width/2, self.plat.top_y()) 
            elif self.placement == "right":
                self.pos = Vec(self.plat.right_x() - 20 - self.width/2, self.plat.top_y())
            elif self.placement == "mid":
                self.pos = Vec(self.plat.mid().x, self.plat.top_y())

            #self.pos.x = self.pos.x+ push; self.pos.y = self.pos.y; self.ignoreSol = self.plat
            
        except Exception as e:
            print(e)
            print("Must choose left, right or mid")    
            #x = self.plat.rect.midtop[0]; y = self.plat.rect.midtop[1]; self.ignoreSol = self.plat
        """
        self.name = name
        self.breakable = True
        self.broken = False
        self.update_order = 11
        self.fall = False
        self.gravity = PLAYER_GRAV
        self.ignoreSol = plat
        self.relativePosition = self.pos.copy()
        self.fell_fast_enough = False
        self.init()

        ''' probably not needed'''

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''

        ''' should be revisited'''

        ''' in use'''





    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_mugs, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create sub-rectangles to load from water spritesheet
        whole  = pg.Rect(  0,0,29,26)
        broken = pg.Rect( 30,0,29,26)
        bigMug = pg.Rect(104,0,77,72)
        rects = [whole, broken, bigMug]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     
        self.image_whole = self.images[0]
        self.image_broken = self.images[1]
        image_big = self.images[2]
        #self.image = image_big
        
        if self.game.level.name == 'level4':
            self.image = image_big
            self.gravity = GRAVITY/2
        else:
            self.image = self.image_whole
        
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)


    def update(self):
        # Check whether the mug has even fallen yet
        if not self.broken:
            if self.vel.y > 1:
                self.fell_fast_enough = True
            
            self.touchplat(self.game.group_solid)
            
            # fall is set to true in knockover() if conditions are satisfied
        
        #self.vel = self.addedVel
        if self.fall == True:
            self.applyGrav()
        #self.pos = self.pos.rounded()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def breaks(self):
        if not self.game.level.name == 'level4':
            self.image.blit(self.images[1],(0,0))
        #self.vel.x = 0
        #newPickup = PickUp(self.pos.x, self.pos.y, 15,15, "health", "spawned pickup")
        self.pos = self.pos.rounded()
        self.spawn.pos = self.pos.copy()
        self.spawn.startGame(self.game)
        self.broken = True

    # Applies basic gravity
    def applyGrav(self):
        self.acc.y += self.gravity                  # Gravity
        self.vel.y   += self.acc.y                              # equations of motion

    def updatePos(self):
        if self.broken:
        #  self.solidCollisions(self.game.group_solid)
            standingon = self.on_solid(self.game.group_platforms)
            if standingon:
                self.pos.y = standingon.top_y()
                self.vel.y = self.addedVel.y; self.acc.y = 0
                self.vel.x = self.addedVel.x
        self.vel.x = self.addedVel.x #here?
        super().updatePos()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def collisionMultipleGroups(self,*groups):
        collidedObjects = []
        for group in groups:
            collisionsInGroup = pg.sprite.spritecollide(self, group, False)
            for collision in collisionsInGroup:
                collidedObjects.append(collision)
        return collidedObjects

    def posCorrection(self):
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # When it thouches a platform or other solid
    def touchplat(self, group):
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.y +=self.r(self.vel.y + 4) 
        collideds = self.collisionMultipleGroups(group, self.game.group_enemies)
        if collideds:
            for collided in collideds:
                if collided != self and collided != self.ignoreSol:
                    if self.fell_fast_enough and not self.broken:
                        self.breaks()

class Activator(CustomSprite):

    hasActivatedTarget = False
    hasDeactivatedTarget = False
    activated = False
    deactivated = True
    auto_deactivate = False
    

    def activeEffect(self):
        doDeactivate = False
        try:
            for e,v in self.effect.items():
                if e == "respawn":
                    for respawn in v:
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            target = respawn['target']
                            #self.hasActivatedTarget = True
                            target.respawn()
                if e == "spawn":
                    for spawn in v:
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            #self.hasActivatedTarget = True
                            target = spawn['target']
                            target.startGame(self.game)
                if e == "move":
                    self.hasDeactivatedTarget = False
                    for move in v:
                        target = move["target"]
                        move['target'].vel = move["movespeed"].copy() + target.originalVel
                if e == "conMove":
                    for conMove in  v:
                        
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            target = conMove["target"]
                            target.originalVel = conMove['movespeed'].copy()
                            target.vel = target.originalVel.copy()
            if doDeactivate:
                self.hasActivatedTarget = True
        except Exception as e:
            print(f'button activate: {e}') 

    def deactiveEffect(self):
        doActivate = False
        try: # shouldn't be try except, I think
            for e,v in self.effect.items():
                if e == "respawn":
                    self.hasActivatedTarget = False
                if e == "move":
                    if not self.hasDeactivatedTarget:
                        doActivate = True
                        for move in v:
                            target = move["target"]
                            move['target'].vel = move["deactspeed"].copy() + target.originalVel

                if e == "conMove":
                    self.hasActivatedTarget = False
                    for conMove in v:
                        target = conMove["target"]
                        target.originalVel *= 0
                        target.vel = target.originalVel
            if doActivate:
                self.hasDeactivatedTarget = True
        except Exception as e:
            print(f'button deact: {e}') 



    def activate(self):
        if not self.activated:
            self.activated = True
            self.deactivated = False
            self.image = self.image_active
            if self.auto_deactivate:
                t = Timer(1, self.deactivate)
                t.start() 
            #self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
    def deactivate(self):
        if not self.deactivated:
            self.deactivated = True
            self.activated = False
            self.image = self.image_inactive
    def update(self):
        if self.activated:
            self.activeEffect()
        elif self.deactivated:
            self.deactiveEffect()
        self.rect.midbottom = self.pos.realRound().asTuple()

# Lever SubClass - Inherits from CustomSprite
class Lever(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
    def __init__(self, plat, placement, width = 30, height = 20, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        self.plat = plat
        
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement
        self.width = width; self.height = height; self.effect = effect; 
        self.auto_deactivate = autodeactivate
        #self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        
        self.deactivate_counter = 30
        #self.x = x; self.y = y
        '''move to super'''



    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levers, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        #self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from spritesheet
        left  = pg.Rect( 0,87,18,13)
        right = pg.Rect(19,87,18,13)
        rects = [left, right]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     

        #self.image_left  = pg.transform.scale(self.images[0], (self.width, self.height))
        #self.image_right = pg.transform.scale(self.images[1], (self.width, self.height))
        #self.image = self.image_left
        self.image_inactive  = pg.transform.scale(self.images[0], (self.width, self.height))
        self.image_active = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)   

# Button SubClass - Inherits from CustomSprite
class Button(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}): 
    def __init__(self, plat:Platform, placement, width = 30, height = 20, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        self.plat = plat
        
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement

        self.effect = effect; 
        self.width = width; self.height = height
        #self.pos = vec(x,y)



        ''' probably not needed'''
        #self.x = x; self.y = y
        #self.activated = False
        #self.deactivated = True

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''
        self.relativePosition = self.pos.copy()

        ''' should be revisited'''

        ''' in use'''

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_buttons, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        #self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from spritesheet
        pressed   = pg.Rect( 0,81,18,5)
        unpressed = pg.Rect(18,76,18,10)
        rects = [pressed, unpressed]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     
        #self.image_pressed = pg.transform.scale(self.images[0], (self.width, int(self.height/2)))
        #self.image_unpressed = pg.transform.scale(self.images[1], (self.width, self.height))
        #self.image = self.image_unpressed
        self.image_active = pg.transform.scale(self.images[0], (self.width, int(self.height/2)))
        self.image_inactive = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def activate(self):
        super().activate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
    def deactivate(self):
        super().deactivate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height))


    def update(self):
        self.buttonPress()
        super().update()
        self.activated = False # Not sure if needed

    def buttonPress(self):
        collided_list = pg.sprite.spritecollide(self, self.game.group_pressureActivator, False)
        if collided_list:
            for collided in collided_list:
                self.activate()
                self.prevActivated = True
                return self
        else:
            self.deactivate()
            self.activated = False
            self.deactivated = True
            return None



# Pickup SubClass - Inherits from CustomSprite
class PickUp(CustomSprite):

    def __init__(self,x,y, type_,  width = 16, height = 16, name = "pickup"): 
        self.width = width; self.height = height
        self.type = type_
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_pickups
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.Surface((self.width,self.height))
        sheet = ss.Spritesheet('resources/spritesheet_green.png')

        if self.type == 'health':
            self.image = sheet.image_at((0,101,16,16), colorkey=(0,255,0))
        
        elif self.type == 'catnip':
            self.image = sheet.image_at((0,134,13,16), colorkey=(0,255,0))

        self.image = pg.transform.scale(self.image, (self.width, self.height))  # scale Surface to size
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)



    def update(self):
        self.rect.midbottom = self.pos.realRound().asTuple()


# ------- HOSTILES ------- #


# Hostile UpperClass - Inherits from CustomSprite
''' trash everything inside?'''
class Hostile(CustomSprite):
    pass
    active = True
    

# Water SubClass - Inherits from Hostile
class Water(Hostile):
    def __init__(self,x,y, width, height, name = None): 
        self.active = True
        self.width = width; self.height = height
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self._layer = 15

    """
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
    """

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        rect1 = pg.Rect( 0,117,16,16)
        rect2 = pg.Rect(16,117,16,16)
        rect3 = pg.Rect(32,117,16,16)
        rect4 = pg.Rect(48,117,16,16)
        blue  = pg.Rect( 0,121,16,10)
        rects = [rect1, rect2, rect3, rect4, blue]
        # load images from spritesheet
        waterSheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = waterSheet.images_at(rects, colorkey=(0,255,0))
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

    #def __init__(self,x,y, width, height, maxDist, vel = vec(1,0), name = "enemy"):
    def __init__(self,plat : Platform, placement, maxDist, width = 23, height = 29, vel = vec(1,0), name = "enemy"):
        self.plat = plat
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement
        self.width  = width;      self.height = height;   self.name = name
        #self.pos    = vec(x,y);   
        self.vel =  vel;        self.acc = vec(0, 0)
        self.maxDist = maxDist

        ''' probably not needed'''
        self.dontmove = False
        #self.x = x
        self.collides_right = False
        self.collides_left = False
        
        '''just for testing?'''
        
        ''' really not sure'''
        self.isEnemy = True

        ''' pretty sure is needed'''
        self.justpoppedup = False
        self.originalVel = vel.copy()
        self.relativePosition = self.pos.copy()
        
        ''' should be revisited'''
        self.solidstrength = 3
        self.originalsolidstrength = self.solidstrength
        
        '''in use'''
        self.initX = self.pos.x
        self.currentplat = None # The platform it stands on/
        self.aboveground = True
        self.wasunderground = False # Only true when worm *just* popped up
        self._layer = 10
        self.active = True

        self.init()



        #self.stopMoving = False
        #self.facing = None

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_enemies, game.group_movables #, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        wormSheet = ss.Spritesheet('resources/worm-spritesheet.png')
        # create sub-rectangles to load from spritesheet
        walk = []
        walk.append(pg.Rect(  4, 36, 28, 28))
        walk.append(pg.Rect( 36, 36, 28, 28))
        walk.append(pg.Rect( 68, 36, 28, 28))
        walk.append(pg.Rect(100, 36, 28, 28))
        walk.append(pg.Rect(132, 36, 28, 28))
        walk.append(pg.Rect(164, 36, 28, 28))
        popup = []
        popup.append(pg.Rect(  4, 4, 28, 28))
        popup.append(pg.Rect( 36, 4, 28, 28))
        popup.append(pg.Rect( 68, 4, 28, 28))
        popup.append(pg.Rect(100, 4, 28, 28))
        popup.append(pg.Rect(132, 4, 28, 28))
        popup.append(pg.Rect(164, 4, 28, 28))
        # load images from spritesheet
        images_walk  = wormSheet.images_at(walk,  colorkey=(0,0,0))
        images_popup = wormSheet.images_at(popup, colorkey=(0,0,0))
        # scale image to correct size
        images_walk  = [pg.transform.scale(img, (self.width, self.height)) for img in images_walk]
        images_popup = [pg.transform.scale(img, (self.width, self.height)) for img in images_popup]
        # define and flip images        
        self.images  = {
            'walk':  {'right': images_walk,  'left': [pg.transform.flip(i, True, False) for i in images_walk]},
            'popup': {'right': images_popup, 'left': [pg.transform.flip(i, True, False) for i in images_popup]}
        }
        # set initial image
        self.facing = 'right'
        self.activity = 'walk'
        self.imageIndex = 0
        self.image = self.images[self.activity][self.facing][self.imageIndex]
    
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)


    # Checking if the enemy is outside its patrolling area
    def checkDist(self):
        if   self.right_x() >= self.currentplat.right_x()  -2:
            self.vel.x = (-1) * abs(self.originalVel.x)# + self.addedVel.x
            self.set_right(self.currentplat.right_x() - 3)
        elif self.left_x() <= self.currentplat.left_x() + 2:
            self.vel.x = abs(self.originalVel.x)# + self.addedVel.x
            self.set_left(self.currentplat.left_x() + 3)

        elif self.pos.x - self.initX >= self.maxDist: # right boundary
            self.vel.x = (-1) * abs(self.originalVel.x)# + self.addedVel.x
        elif self.pos.x - self.initX <= -1*self.maxDist:
            self.vel.x = abs(self.originalVel.x)# + self.addedVel.x

    #def updatePos(self, group):
     #   self.pos +=  self.vel +  self.acc * 0.5



    def updateAnimation(self):
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images['walk']['right'])*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        
        #self.area = "mid" #Doesn't matter rn, but maybe later?
        if self.vel.x < 0:
            self.facing = 'left'
        else:
            self.facing = 'right'

        self.image = self.images[self.activity][self.facing][math.floor(self.imageIndex/10)]
        if self.image == self.images['popup'][self.facing][-1]:
            self.activity = 'walk'
                

    def update(self):

        #self.stopMoving = self.inbetweenSolids()
        self.updateAnimation()
        #self.acc = vec(0,0)    
        try:
            self.hide()
            self.checkDist()
        except Exception as e:
            print(f'touchbox: {e}')
        self.vel += self.addedVel
        self.solidCollision()
        self.active = self.aboveground # Whether it should deal damage
        self.rect.midbottom = self.pos.realRound().asTuple()
    
    
    """
    -> Checks whether aboveground bool is true. If it is, reset the currentplat the worm is on
    -> Move rect above platform to check it is it "free" for boxes.
    -> Checks collisions. If true, set pos to platform bot (inside plat). 
        -> else: set pos to top of current platform.
    """
    def hide(self):
        self.rect.midbottom = self.pos.realRound().asTuple()
        if self.aboveground:
            possibleplat = self.on_solid(self.game.group_platforms)
            if possibleplat != None:
                self.currentplat = possibleplat
        # else if it is inside a plat (self.abovegroun = False), move enemies rect up
        else: 
            self.rect.bottom = self.currentplat.rect.top - 1
        collideds = pg.sprite.spritecollide(self, self.game.group_solid, False)
        self.rect.midbottom = self.pos.realRound().asTuple()
        #justpoppedup = 10
        # If it is above ground, check which platform it is on
        #remove = False
        if collideds:
            for collided in collideds:
                if collided != self.currentplat:
                #if collided not in self.game.group_platforms:
                    self.addedVel = self.currentplat.vel
                    self.pos.y = self.currentplat.pos.y - 1
                    self.aboveground = False
                    self.wasunderground = True
                    #remove = True
        else: 
            self.pos.y = self.currentplat.top_y()
            self.aboveground = True
            if self.wasunderground:
                self.justpoppedup = True
                # go to dirt pile animations
                self.activity = 'popup'
                self.imageIndex = 0
                #t = Timer(5, self.popup)
                #t.start()
            self.wasunderground = False
        self.rect.midbottom = self.pos.realRound().asTuple()
    '''
    def popup(self):
        # go back to old animation
        self.justpoppedup = False
    '''
    # Currently doesn't matter. The worm just hides. so?
    def solidCollision(self):
        self.rect.midbottom = self.pos.realRound().asTuple()
        collideds = pg.sprite.spritecollide(self, self.game.group_platforms, False)

        if collideds:
            for collided in collideds:
                # handle floor plat better
                if collided != self and collided != self.currentplat: #and collided.name != "p_floor" and self.lessMassThan(collided) :
                    
                    #coll_side = self.determineSide(collided)
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if coll_side == "left": # left side of collidedd obj
                        self.vel.x *= -1
                            
                    if coll_side == "right":
                        self.vel.x *= -1
                    self.pos = correctedPos
                            
                    """    
                    if coll_side == "bot":
                        if  abs(self.right_x() - collided.left_x()) < abs(collided.right_x() - self.left_x() ):
                            self.pos.x = collided.left_x() - self.width/2
                        else: 
                            self.pos.x = collided.right_x() + self.width/2
                        #self.count = 5
                    """

    # DEL?
    def posCorrection(self):
        #self.collidingWithWall()
        pass


    # Will make the enemy stand still if inbetween solids (instead of vibrating)
    

        
    # DEL?
    def collidingWithWall(self):
        #self.pygamecolls(self.game.group_solid)

        self.collides_left = False
        self.collides_right = False


# AI Enemy SubClass 
class AiEnemy(Hostile):
    def __init__(self,plat, placement, width = 36, height = 28, speed = 1, name = "enemyai"):
    #def __init__(self, plat, placement, width, height, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        self.plat = plat
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement
        self.speed = speed
        #self.x = x
        self.width = width;  self.height = height
        #self.game  = game;   
        self.name = name
        #self.pos = vec(x,y); 
        self.vel = vec(speed,0); self.acc = vec()
        
        self.relativePosition = self.pos.copy()
        #self.dontmove = False

        ''' probably not needed'''

        '''just for testing?'''
        self.isEnemy = True


        ''' pretty sure is needed'''
        self.target = None # The player



        ''' should be revisited'''
        self.solidstrength = 5
        self.originalsolidstrength = self.solidstrength


    
        """in use"""
        self.ori_massVER = 8
        self._layer = 10
        self.update_order = 9
        self.currentplat = None


        self.init()
        #self.stopMoving = False
        #self.facing = None
    
    def onSameLevel(self):
        return (abs(self.target.pos.y - self.pos.y) < 125)

    def playerLeft(self):
        return (self.target.pos.x < self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
            
    def onPlayer(self):
        return (abs(self.target.pos.x - self.pos.x) <5)

    def playerRight(self):
        return (self.target.pos.x > self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
    
    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_solid, game.group_enemies, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        wormSheet = ss.Spritesheet('resources/Hyena_walk.png')
        # create sub-rectangles to load from spritesheet
        '''
        rect1 = pg.Rect( 12, 20, 36, 28)
        rect2 = pg.Rect( 59, 20, 36, 28)
        rect3 = pg.Rect(106, 21, 36, 28)
        rect4 = pg.Rect(155, 21, 36, 28)
        '''
        rect1 = pg.Rect(  3, 21, 45, 27)
        rect2 = pg.Rect( 50, 21, 45, 27)
        rect3 = pg.Rect( 99, 21, 45, 27)
        rect4 = pg.Rect(147, 21, 45, 27)
        rect5 = pg.Rect(195, 21, 45, 27)
        rect6 = pg.Rect(243, 21, 45, 27)
        rects = [rect1, rect2, rect3, rect4, rect5, rect6]
        # load images from spritesheet
        self.images_left = wormSheet.images_at(rects, colorkey=(0,0,0))
        self.images_right = []
        for img in self.images_left:
            self.images_right.append(pg.transform.flip(img,True,False))
        self.imageIndex = 0
        self.image = self.images_left[self.imageIndex]
    
        # scale image to correct size
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
        #self.target = self.game.player
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)

    def detectPlayer(self):
        if self.onSameLevel():
            if self.onPlayer():
                self.vel.x = self.addedVel.x
            elif self.playerRight():
                self.vel.x = self.speed + self.addedVel.x
                self.image = self.images_right[math.floor(self.imageIndex/10)]   # update current image
            elif self.playerLeft(): 
                self.vel.x = - self.speed + self.addedVel.x
                self.image = self.images_left[math.floor(self.imageIndex/10)]   # update current image
            else: 
                self.vel.x = self.addedVel.x
        else:
            self.vel.x = self.addedVel.x


    def updatePos(self): # fix
        self.acc   += vec(0, self.gravity)                  # Gravity
        #self.vel += self.acc
        self.pos +=  self.vel +  self.acc * 0.5
        self.acc = vec(0,0)     


    def update(self):
        self.target = self.game.player
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images_right)*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        
        # No matter what vel if may have been given (from box e.g.) it should stay at 1 or whatever we choose
        self.image = pg.transform.scale(self.image, (self.width, self.height))  # rescale image
        self.vel += self.addedVel
        #self.applyPhysics()

        self.detectPlayer()
        self.checkCliff()
        self.pygamecolls(self.game.group_solid)
        #self.stopMoving = self.inbetweenSolids()
        self.rect.midbottom = self.pos.realRound().asTuple()

        #self.pygamecolls(self.game.group_solid)


    def posCorrection(self):
        self.collidingWithWall()

    def checkCliff(self):
        # should it have a max dist?
        """
        if  self.pos.x - self.x >= self.maxDist: # right boundary
            self.area = "right"
            self.vel.x = -1 * abs(self.vel.x)
        elif self.pos.x - self.x <= -1*self.maxDist:
            self.vel.x = abs(self.vel.x)
            self.area = "left"
        """
        possibleplat = self.on_solid(self.game.group_platforms)
        if possibleplat != None:
            self.currentplat = possibleplat
            self.gravity = 0
        else: 
            self.gravity = GRAVITY
        try:
            if self.right_x() >= self.currentplat.right_x()  -1:
                self.vel = self.addedVel
                self.set_right(self.currentplat.right_x() - 2) # Number here must be bigger than 3 lines before. Otherwise dog stands still on edges
            elif self.left_x() <= self.currentplat.left_x() +1: 
                self.vel = self.addedVel
                self.set_left(self.currentplat.left_x() + 2)
        except Exception as e:
            print(f'check cliff: {e}')

    def collidingWithWall(self):
        self.pygamecolls(self.game.group_solid)
        self.collides_left = False
        self.collides_right = False

# The part that checks whether to just turn around or be pushed
    def pygamecolls(self, group, ignoredSol = None):
        inflation = 0
        self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x +=self.r((self.vel.x-self.addedVel.x)*1.5)
        self.rect.y +=self.r(self.vel.y*1.5)
        collideds = pg.sprite.spritecollide(self, group, False)

        # lol the if if i f if if if if if if if if if if if if if fif if if if if
        if collideds:
            for collided in collideds:

                if collided != self and collided.name != "p_floor":
                    #if not self.stopMoving: # If it was inbetween solids
                    if self.ori_massHOR <= collided.massHOR:
                        coll = self.collisionSide_Conditional(collided)
                        coll_side = coll['side']
                        correctedPos = coll['correctedPos']
                        
                        if coll_side == "left": # left side of collidedd obj
                            self.vel.x = self.addedVel.x
                                
                        if coll_side == "right":
                            self.vel.x = self.addedVel.x
                                
                        self.pos = correctedPos
                    """    
                    if self.ori_massVER < collided.massVER:
                        coll_side = self.determineSide(collided)
                            
                        if coll_side == "bot":
                            if  abs(self.right_x() - collided.left_x()) < abs(collided.right_x() - self.left_x() ):
                                self.pos.x = collided.left_x() - self.width/2
                            else: 
                                self.pos.x = collided.right_x() + self.width/2
                            self.massVER = collided.massVER - 1
                    """





