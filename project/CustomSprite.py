# Imports
import pygame as pg
from Vector import *
from settings import *
import math
import time
from threading import Timer

# Variables
vec = Vec

# Classes
class CustomSprite(pg.sprite.Sprite):
    



    # Class Variables:


    # Attributes:
        
    ''' probably not needed'''

    ''' just for testing?'''

    ''' really not sure'''

    ''' pretty sure is needed'''

    ''' should be revisited'''
    count               = 5
    originalsolidstrength = 0
    solidstrength       = 0
    massHOR             = 0
    massVER             = 0
    ori_massHOR         = massHOR
    ori_massVER         = massVER

    ''' in use'''
    stoppedHOR      = False
    stoppedVER      = False
    isEnemy         = False
    gravity         = GRAVITY
    friction        = FRICTION
    relativePosition = vec()
    addedVel        = Vec()
    update_order        = 10
    inAir           = True
    collided_right_side = False; collided_left_side = False; collided_bottom = False; collided_top = False
    pos    = vec(); vel  = vec(); acc = vec()

    # Methods

    def r(self, number):
        rounded_num = number
        rounded_num = abs(rounded_num)
        rounded_num = math.ceil(rounded_num)
        if number < 0:
            rounded_num *= -1
        return rounded_num

    def resetMass(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER

    def init(self):
        self.massHOR = self.solidstrength
        self.massVER = self.solidstrength
        self.ori_massHOR = self.massHOR
        self.ori_massVER = self.massVER
        self.new_vel = self.vel.copy()

    def updateRect(self):
        self.rect.midbottom = self.relativePosition.rounded().asTuple()

    def resetRects(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    def resetSprite(self):
        if self.count <= 0:
            self.resetMass()
            self.solidstrength = self.originalsolidstrength
        self.count -= 1
        self.vel -= self.addedVel
        self.addedVel = Vec(0,0)
        self.acc = vec(0,0)
        
    def top_y(self):
        return self.pos.y - self.height
    def bot_y(self):
        return self.pos.y
    def left_x(self):
        return self.pos.x - self.width/2 #- 1
    def right_x(self): 
        return self.pos.x + self.width/2

    def set_top(self, ypos):
        self.pos.y = ypos + self.height
    def set_bot(self, ypos):
        self.pos.y = ypos
    def set_left(self, xpos):
        self.pos.x = xpos + self.width/2
    def set_right(self, xpos):
        self.pos.x = xpos - self.width/2


    def bottomleft(self):
        return vec(self.left_x(), self.bot_y()).realRound()
    def bottomright(self):
        return vec(self.right_x(), self.bot_y()).realRound()
    def topleft(self):
        return vec(self.left_x(), self.top_y()).realRound()
    def topright(self):
        return vec(self.right_x(), self.top_y()).realRound()

    def mid(self):
        return vec(self.pos.x,self.bot_y()-self.height/2)

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

    ''' I gets the side of collision, but also checks whether it should correct the position (and returns the position) '''
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

    def relativeVel(self):
        return self.vel - self.addedVel

    def posCorrection(self):
        pass

    # CLEANED
    def collisionEffect(self):
        inflation = 2
        self.rect = self.rect.inflate(inflation,inflation)
        self.rect.y -= 2
        collided_objects = None
        if not self.isEnemy:
            collided_objects = pg.sprite.spritecollide(self, self.game.group_movables, False)

        if collided_objects:
            for collided in collided_objects:
                if collided != self and collided.lessMassThan(self):
                    coll_side = collided.determineSide(self)
                    if coll_side == "top":
                        collided.addedVel.x = self.vel.x + self.addedVel.x
                        collided.addedVel.y = self.vel.y + self.addedVel.y

        self.rect = self.rect.inflate(-inflation, -inflation)
        self.rect.midbottom = self.pos.rounded().asTuple()

    def lessMassThan(self, other):
        return self.massHOR < other.massHOR or self.massVER < other.massVER

    def pygamecoll(self, group = None, ignoredSol = []):
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x += self.r(self.relativeVel().x*1.5)
        self.rect.y += self.r(self.vel.y) 
        group = self.game.group_solid
        collideds = pg.sprite.spritecollide(self, group, False)
        self.rect.midbottom = self.pos.realRound().asTuple()
        wasstoppedHOR = False
        if collideds:
            for collided in collideds:
                if collided != self and collided not in ignoredSol: #and not self.isEnemy:
                    #if self.lessMassThan(collided) or self.massHOR == collided.massHOR or self.massVER == collided.massVER:#collided.solidstrength >= self.solidstrength :
                    #coll_side = self.determineSide(collided)
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if self.massVER < collided.massVER:
                        if coll_side == "top":
                        #   newpos = collided.top_y()
                            
                        #if newpos <= self.pos.y:
                            #self.set_bot(collided.top_y())
                            self.vel.y = self.addedVel.y
                            self.acc.y = 0
                            if group.has(self):
                                self.count = 2
                                self.massVER = collided.massVER - 1

                        if coll_side == "bot":
                            #newpos =  collided.bot_y() + self.height 
                            #if newpos >= self.pos.y:
                            #self.pos.y = newpos
                            self.vel.y = self.addedVel.y
                            self.acc.y = 0
                            if group.has(self):
                                self.count = 2
                                self.massVER = collided.massVER - 1
                    if self.massHOR <= collided.massHOR:
                        if coll_side == "left":
                            #newpos = collided.left_x() - self.width/2 #Left side of object being collided with
                            #if newpos <= self.pos.x:
                            #    self.pos.x = collided.left_x() - self.width/2
                            self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                            self.acc.x = 0
                            wasstoppedHOR = True
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.count = 2
                                    self.massHOR = collided.massHOR - 1

                        if coll_side == "right":
                            self.count = 2
                            #newpos = collided.right_x() + self.width/2
                            #if newpos >= self.pos.x:
                            #self.pos.x = collided.right_x() + self.width/2
                            self.vel.x = self.addedVel.x
                            self.acc.x = 0
                            wasstoppedHOR = True
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.massHOR = collided.massHOR - 1
                    if correctedPos.y > 0:    
                        self.pos = correctedPos
        # This was implemented so the player couldn't push the dog with the box. 
        if wasstoppedHOR:
            self.stoppedHOR = True
        else: 
            self.stoppedHOR = False

    def determineSide(self, collided):
        leftcoll = abs(self.right_x() - collided.left_x())
        rightcoll = abs(collided.right_x() - self.left_x() )
        topcoll   = abs(abs(self.bot_y()) - abs(collided.top_y()))
        botcoll   = abs(abs(self.top_y()) - abs(collided.bot_y()))
        mins = min(leftcoll, rightcoll, topcoll, botcoll)

        if mins == leftcoll: 
            return "left"
        if mins == rightcoll:
            return "right"
        if mins == topcoll:
            return "top"
        if mins == botcoll:
            return "bot"

    def on_solid(self, group):
        self.rect.bottom += 2
        collideds = pg.sprite.spritecollide(self, group, False)
        result = None
        for collided in collideds:
            if collided != self:
                
                if self.determineSide(collided) == "top":
                    result = collided
        self.rect.bottom -= 2
        return result

        
    def applyPhysics(self,Intersecters = None):
        
        if self.on_solid(self.game.group_solid):
            self.inAir = False
            self.gravity = 0
        else:
            self.inAir = True
            self.gravity = GRAVITY
        
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if abs(self.vel.x + self.addedVel.x) < 0.1:
            self.vel.x = self.addedVel.x
    
    def updatePos(self):
        self.pos +=  self.vel +  self.acc * 0.5
        self.acc = vec(0,0)    # caused problems? 



    def collisionMultipleGroups(self,*groups):
        collidedObjects = []
        for group in groups:
            collisionsInGroup = pg.sprite.spritecollide(self, group, False)
            for collision in collisionsInGroup:
                collidedObjects.append(collision)
        return collidedObjects
