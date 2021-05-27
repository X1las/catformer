# Imports
# Extenal Modules:
import pygame as pg
import math

# Project Imports
from Vector import Vec
from settings import *

# Variables
vec = Vec

# Classes
class CustomSprite(pg.sprite.Sprite):
    
    # Class Variables:
    solidstrength       = 0
    massHOR             = 0
    massVER             = 0
    ori_massHOR         = massHOR
    ori_massVER         = massVER
    stoppedHOR      = False
    stoppedVER      = False
    isEnemy         = False
    gravity         = GRAVITY
    friction        = FRICTION
    relativePosition = vec()
    inAir           = True
    isPlatform = False
    pos    = vec(); vel  = vec(); acc = vec()
    _layer = 10
    isPlayer = False #Remove later
    latestCorrectedPos = Vec()
    savedPos = vec()
    draw_layer = 0


    def __init__(self):
        self.addedVel        = Vec()



    # Methods
    # Method for rounding
    def r(self, number):
        rounded_num = number
        rounded_num = abs(rounded_num)
        rounded_num = math.ceil(rounded_num)
        if number < 0:
            rounded_num *= -1
        return rounded_num


    # Methods for getting sides of a sprite's rectangle
    def top_y(self):
        return self.pos.y - self.height
    def bot_y(self):
        return self.pos.y
    def left_x(self):
        return self.pos.x - self.width/2 #- 1
    def right_x(self): 
        return self.pos.x + self.width/2


    # Methods for setting sides of a sprite's rectangle
    def set_top(self, ypos):
        self.pos.y = ypos + self.height
    def set_bot(self, ypos):
        self.pos.y = ypos
    def set_left(self, xpos):
        self.pos.x = xpos + self.width/2
    def set_right(self, xpos):
        self.pos.x = xpos - self.width/2


    # Methods for getting corners of a sprite's rectangle
    def bottomleft(self):
        return vec(self.left_x(), self.bot_y()).rounded()
    def bottomright(self):
        return vec(self.right_x(), self.bot_y()).rounded()
    def topleft(self):
        return vec(self.left_x(), self.top_y()).rounded()
    def topright(self):
        return vec(self.right_x(), self.top_y()).rounded()
    def mid(self):
        return vec(self.pos.x,self.bot_y()-self.height/2)
    

    # Function for returning relative velocity of a sprite
    def relativeVel(self):
        return self.vel - self.addedVel


    # Function for updating velocity
    def updateAddedVel(self):
        self.vel += self.addedVel


    # Does init?
    def init(self):
        try:
            print(f'{self.name} : {self.addedVel.x}')
        except:
            print(f'FAILED FOR {self.name}')
        #self.addedVel = vec(0,0)
        self.massHOR = self.solidstrength
        self.massVER = self.solidstrength
        self.ori_massHOR = self.massHOR
        self.ori_massVER = self.massVER
        self.relativePosition = self.pos.copy()
   

    # Resets sprite?
    def resetSprite(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER
        #print(f'{self.name} -- {self.vel}')
        if not self.isPlatform:
            self.vel -= self.addedVel
        self.addedVel = Vec(0,0)
        self.acc = vec(0,0)
        

    # Updates position? don't we have like 50 of these?
    def updatePos(self):
        self.pos +=  self.vel +  self.acc * 0.5


    # Updates rectangles? don't we also have like 50 of these?
    def updateRect(self):
        self.rect.midbottom = self.relativePosition.rounded().asTuple()


    # Resets rectangles??
    def resetRects(self):
        self.rect.midbottom = self.pos.rounded().asTuple()


    # Default functions for SpriteGroup:
    def update(self):
        pass

    def update2(self):
        pass

    def posCorrection(self):
        pass


    # Determines the side of collisions?
    def determineSide(self, collided):
        leftcoll  = abs(self.right_x() - collided.left_x())
        rightcoll = abs(collided.right_x() - self.left_x() )
        topcoll   = abs(self.bot_y() - collided.top_y())
        botcoll   = abs(self.top_y() - collided.bot_y())
        mins      = min(leftcoll, rightcoll, topcoll, botcoll)

        if mins == leftcoll: 
            return "left"
        if mins == rightcoll:
            return "right"
        if mins == topcoll:
            return "top"
        if mins == botcoll:
            return "bot"


    # Gets the side of collision, but also checks whether it should correct the position and returns it
    def collisionSide_Conditional(self, collided):
        coll_side = self.determineSide(collided)
        result = {"side" : "None", "correctedPos" : self.pos}

        if coll_side == "top":
            newpos = Vec(self.pos.x, collided.top_y())
            if newpos.y <= self.pos.y:
                return {"side" : "top", "correctedPos" : newpos}
        elif coll_side == "left": # left side of collidedd obj
            newpos = Vec(collided.left_x() - self.width/2, self.pos.y)
            if newpos.x <= self.pos.x: # Make sure it is only if moving the enemy would actually get pushed out on the left side 
                return {"side" : "left", "correctedPos" : newpos}
        elif coll_side == "right":
            newpos = Vec(collided.right_x() + self.width/2, self.pos.y)
            if newpos.x >= self.pos.x:
                return {"side" : "right", "correctedPos" : newpos}
        elif coll_side == "bot": # left side of collidedd obj
            newpos = Vec(self.pos.x, collided.bot_y() + self.height)
            if newpos.y >= self.pos.y: # Make sure it is only if moving the enemy would actually get pushed out on the left side 
                return {"side" : "bot", "correctedPos" : newpos}
        return result 


    # Does stuff when colliding maybe?
    def collisionEffect(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.y -= 5
        self.rect.x += self.r(self.relativeVel().x)
        collided_objects = None
        if not self.isEnemy:
            group = self.game.all_sprites
            grouplist = group.massSort("massVER")
            collided_objects = pg.sprite.spritecollide(self, group, False)
        if collided_objects:
            for collided in collided_objects:
                if collided != self and not collided.isPlatform: # and self.massVER < collided.massVER:
                    coll_side = collided.determineSide(self)
                    if coll_side == "top":
                        #print(f'{self.name} added to {collided.name}')
                        #print(f'{self.vel.x + self.addedVel.x} AND {collided.vel.x}')
                        collided.addedVel.x = self.vel.x + self.addedVel.x
                        if self.vel.y >= 0: # if it is added when something goes up, it will push sprite too far up
                            collided.addedVel.y = self.vel.y + self.addedVel.y
                        if collided in self.game.group_solid:
                            collided.collisionEffect()

        self.rect.midbottom = self.pos.rounded().asTuple()


    # Oooh, does a pushing effect
    def pushEffect(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.x += self.r(self.relativeVel().x)
        """
        if self.vel.x > 0:
            self.rect.x += 2
        if self.vel.x < 0:
            self.rect.x -= 2
        """
        collided_objects = None
        group = self.game.group_movables
        grouplist = group.massSort("massHOR")
        collided_objects = pg.sprite.spritecollide(self, grouplist, False)
        if collided_objects:
            for collided in collided_objects:
                if collided != self and not collided.isPlatform and self.massHOR >= collided.massHOR: # and self.massVER < collided.massVER:
                    coll_side = collided.determineSide(self)
                    if (coll_side == "right" and self.vel.x > 0) or (coll_side == "left" and self.vel.x < 0):
                        collided.addedVel.x += self.vel.x + self.addedVel.x
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.collisionEffect()


    # Solid collision i think?
    def solidCollisions(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        """
        if self.vel.x < 0:
            #self.rect.x += self.r(self.relativeVel().x-2)
            self.rect.x += self.r(self.relativeVel().x)
        if self.vel.x > 0:
            #self.rect.x += self.r(self.relativeVel().x+2)
            self.rect.x += self.r(self.relativeVel().x)
        if self.vel.y < 0:
            self.rect.y += self.r(self.vel.y - 1) 
        elif self.vel.y > 0:
            self.rect.y += self.r(self.vel.y + 1) 
        """
        self.rect.x += self.r(self.relativeVel().x)
        self.rect.y += self.r(self.relativeVel().y)

        group = self.game.group_solid
        grouplist = group.createMassOrdered()
        collided_objects = pg.sprite.spritecollide(self, grouplist, False)
        self.rect.midbottom = self.pos.rounded().asTuple()
        wasstoppedHOR = False
        recursiveList = []
        if collided_objects:
            for collided in collided_objects:
                if collided != self: # and collided not in ignoredSol: #and not self.isEnemy:
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if self.massVER < collided.massVER  or (self.massVER == collided.massVER and self.game.group_movables.has(self)):
                        if coll_side == "top" or coll_side == "bot":
                            self.vel.y = self.addedVel.y
                            
                            self.acc.y = 0
                            if group.has(self):
                                self.massVER = collided.massVER - 1
                            recursiveList.append(collided)
                            self.pos.y = correctedPos.y
                    #                                          it is ok that they are equally heavy it is supposed to be movable
                    if self.massHOR < collided.massHOR or (self.massHOR == collided.massHOR and self.game.group_movables.has(self)):
                        if coll_side == "left" or coll_side == "right":
                            self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                            self.acc.x = 0
                            wasstoppedHOR = True
                            if group.has(self):
                                self.massHOR = collided.massHOR - 1
                            recursiveList.append(collided)
                            self.pos.x = correctedPos.x
        # This was implemented so the player couldn't push the dog with the box. 
        if wasstoppedHOR:
            self.stoppedHOR = True
        else: 
            self.stoppedHOR = False
        for i in recursiveList:
            i.solidCollisions()


    # Checking whether anything is on a solid
    def on_solid(self, group):
        self.rect.bottom += 2
        collided_objects = pg.sprite.spritecollide(self,group, False)
        result = None
        for collided in collided_objects:
            if collided != self:
                if self.determineSide(collided) == "top":
                    result = collided
        self.rect.bottom -= 2
        return result


    # Applies gravity and friction to the velocity of the sprite
    def applyPhysics(self):
        self.acc.y += self.gravity                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if abs(self.vel.x + self.addedVel.x) < 0.01:
            self.vel.x = self.addedVel.x
