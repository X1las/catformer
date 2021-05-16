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
    pos    = vec(); vel  = vec(); acc = vec()
    isOnPlatform = False
    distanceOrder = []
    name = "sprite"
    isPlayer = False #Remove later


    # Methods

    # i dont think this is necessary anymore
    def r(self, number):
        rounded_num = number
        rounded_num = abs(rounded_num)
        rounded_num = math.ceil(rounded_num)
        if number < 0:
            rounded_num *= -1
        return rounded_num

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
        return vec(self.left_x(), self.bot_y()).rounded()
    def bottomright(self):
        return vec(self.right_x(), self.bot_y()).rounded()
    def topleft(self):
        return vec(self.left_x(), self.top_y()).rounded()
    def topright(self):
        return vec(self.right_x(), self.top_y()).rounded()
    def mid(self):
        return vec(self.pos.x,self.bot_y()-self.height/2)
    
    def relativeVel(self):
        return self.vel - self.addedVel

    def init(self):
        self.massHOR = self.solidstrength
        self.massVER = self.solidstrength
        self.ori_massHOR = self.massHOR
        self.ori_massVER = self.massVER
        self.relativePosition = self.pos.copy()
    
    def resetMass(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER

    def resetSprite(self):
        self.resetMass()
        self.vel -= self.addedVel
        self.addedVel = Vec(0,0)
        self.acc = vec(0,0)
        #self.pos *= 100
        #self.vel *= 100
        #self.acc *= 100
        
    def updatePos(self):
        self.pos +=  self.vel +  self.acc * 0.5

    def posCorrection(self):
        pass

    def updateRect(self):
        #self.pos = self.pos / 100
        #self.vel = self.vel / 100
        #self.acc = self.acc / 100
        self.rect.midbottom = self.relativePosition.rounded().asTuple()

    def resetRects(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    def determineSide(self, collided):

        leftcoll  = abs(self.right_x() - collided.left_x())
        rightcoll = abs(collided.right_x() - self.left_x() )

        topcoll   = abs(self.bot_y() - collided.top_y())
        botcoll   =  abs(self.top_y() - collided.bot_y())
        #sides ={ "top" : abs(self.bot_y() - collided.top_y()), "left" : abs(self.right_x() - collided.left_x()), "right":abs(collided.right_x() - self.left_x() ), "bot": abs(self.top_y() - collided.bot_y())}
        #sortedSides = (sorted(sides.items(), key = lambda side: side[1]))
        #self.distanceOrder = sortedSides
        #return self.distanceOrder[0][0]
        
        #for side in sortedSides:
        #   self.distanceOrder.append(side[0])

        #print(self.distanceOrder)
        #distanceOrder = sorted( topcoll, leftcoll, rightcoll, botcoll)
        #self.distanceOrder
        mins      = min( topcoll, leftcoll, rightcoll, botcoll)
        #return self.distanceOrder
        if mins == topcoll:
            #mins2 = min(leftcoll, rightcoll, botcoll)
            return "top"
        if mins == leftcoll: 
            return "left"
        if mins == rightcoll:
            return "right"
        if mins == botcoll:
            return "bot"

    ''' It gets the side of collision, but also checks whether it should correct the position (and returns the position) '''
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

    def collisionDetection(self, groups):
        #appendedGroups = []
        #for i in groups:
        #  for j in i:
        #       appendedGroups.append(j)
        collided_objects = []
        #print(f'all the sprites: {appendedGroups}')
        #print(f'new collision')
        #self.pos *= 100
        for other in groups:
            #print(other)
            """
            if  (   self.left_x()  <= other.right_x() 
                and self.right_x() >= other.left_x() 
                and self.top_y()   <= other.bot_y() 
                and self.bot_y()   >= other.top_y()  ):
            """
            #other.pos *= 100
            """
            if  (   min(self.pos.x, self.pos.x - self.width/2)  <= max(other.pos.x, other.pos.x + other.width/2)
                and min(self.pos.y, self.pos.y - self.height)   <= other.pos.y 
                and max(self.pos.x, self.pos.x + self.width/2)  >= min(other.pos.x, other.pos.x - other.width/2) 
                and self.pos.y                      >=  min(other.pos.y, other.pos.y  - other.height)):
                collided_objects.append(other)
            """
            if  (   min(self.pos.x, self.pos.x - self.width*100/2)  <= max(other.pos.x, other.pos.x + other.width*100/2)
                and min(self.pos.y, self.pos.y - self.height*100)   <= other.pos.y 
                and max(self.pos.x, self.pos.x + self.width*100/2)  >= min(other.pos.x, other.pos.x - other.width*100/2) 
                and self.pos.y                      >=  min(other.pos.y, other.pos.y  - other.height*100)):
                collided_objects.append(other)
            #other.pos /= 100
            """
            if ((other.left_x() <= self.right_x() <= other.right_x() and other.top_y() <= (self.top_y()) <= other.bot_y())
                or (other.left_x() <= (self.right_x()) <= other.right_x() and other.top_y() <= (self.bot_y()) <= other.bot_y())
                or (other.left_x() <= (self.left_x()) <= other.right_x() and other.top_y() <= (self.top_y()) <= other.bot_y())
                or (other.left_x() <= (self.left_x()) <= other.right_x() and other.top_y() <= (self.bot_y()) <= other.bot_y())):
                collided_objects.append(other)
            """
            """
            if ((other.left_x() < self.right_x() < other.right_x() and other.top_y() < (self.top_y()) < other.bot_y())
                or (other.left_x() < (self.right_x()) < other.right_x() and other.top_y() < (self.bot_y()) < other.bot_y())
                or (other.left_x() < (self.left_x()) < other.right_x() and other.top_y() < (self.top_y()) < other.bot_y())
                or (other.left_x() < (self.left_x()) < other.right_x() and other.top_y() < (self.bot_y()) < other.bot_y())):
                collided_objects.append(other)
                #print(f'other: {collided_objects}')
            """
            #elif other.left_x() < (self.right_x()) < other.right_x() and other.top_y() < (self.bot_y()) < other.bot_y():
            #   collided_objects.append(other)
            #elif other.left_x() < (self.left_x()) < other.right_x() and other.top_y() < (self.top_y()) < other.bot_y():
            #   collided_objects.append(other)
            #elif other.left_x() < (self.left_x()) < other.right_x() and other.top_y() < (self.bot_y()) < other.bot_y():
            #   collided_objects.append(other)
        #self.pos /= 100
        return collided_objects




    # CLEANED
    def collisionEffect(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.y -= 5
        collided_objects = None
        if not self.isEnemy:
            #collided_objects = pg.sprite.spritecollide(self, self.game.group_movables, False)
            collided_objects = self.collisionDetection(self.game.group_movables)
        if collided_objects:
            for collided in collided_objects:
                if collided != self: # and self.massVER < collided.massVER:
                    coll_side = collided.determineSide(self)
                    if coll_side == "top":
                        collided.addedVel.x = self.vel.x + self.addedVel.x
                        #if self.vel.y >= 0: # if it is added when something goes up, it will push sprite too far up
                        collided.addedVel.y = self.vel.y + self.addedVel.y
                        if collided in self.game.group_solid:
                            collided.collisionEffect()
        self.rect.midbottom = self.pos.rounded().asTuple()




    def solidCollisions(self, group = None):#, ignoredSol = []):
        """
        self.rect.midbottom = self.pos.rounded().asTuple()
        if self.vel.x < 0:
            self.rect.x += self.r(self.relativeVel().x-2)
        if self.vel.x > 0:
            self.rect.x += self.r(self.relativeVel().x+2)
        if self.vel.y < 0:
            self.rect.y += self.r(self.vel.y - 1) 
        elif self.vel.y > 0:
            self.rect.y += self.r(self.vel.y + 1) 
        savedPos = self.pos.copy()
        """
        """
        if self.vel.x < 0:
            self.pos.x += self.relativeVel().x-0.01
        if self.vel.x > 0:
            self.pos.x += self.relativeVel().x+0.01
        if self.vel.y < 0:
            self.pos.y += self.vel.y - 0.01
        if self.vel.y > 0:
            self.pos.y += self.vel.y + 0.01
        """
        group = self.game.group_solid
        collided_objects = self.collisionDetection(group)
        #print(f'own: {collided_objects}')
        #self.pos = savedPos
        #collided_objects = pg.sprite.spritecollide(self, group, False)
        #print(f'test: {test}')
        #print(f'pygame: {collided_objects}')
        #self.rect.midbottom = self.pos.rounded().asTuple()
        #round(self.pos)
        wasstoppedHOR = False
        posCorrected=False
        onNoofPlats = 0
        setleft = False
        setright = False
        if collided_objects:
            for collided in collided_objects:
                if collided != self: # and collided not in ignoredSol: #and not self.isEnemy:
                    #round(collided.pos)
                    coll = self.collisionSide_Conditional(collided)

                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if self.massVER < collided.massVER:
                        if coll_side == "top" or coll_side == "bot":
                            if (coll_side == "top" and self.vel.y > 0) or (coll_side == "bot" and self.vel.y < 0):
                                self.vel.y = self.addedVel.y
                                self.acc.y = 0
                            if coll_side == "top":
                                onNoofPlats += 1
                            self.pos = correctedPos
                            if group.has(self):
                                self.massVER = collided.massVER - 1
                            #other = self.distanceOrder[1]
                            # if a box or something is right at an edge, it would stand still because everything is so accurate lol
                            #if self.distanceOrder[1][1] < 4:
                             #   if self.distanceOrder[1][0] == "left":
                              #      #self.set_right(collided.left_x() - 1)
                               #     setright = collided.left_x() - 1
                                #if self.distanceOrder[1][0] == "right":
                                 #   setleft = collided.right_x() + 1
                                    #self.set_left(collided.right_x()+ 1)
                    if self.massHOR <= collided.massHOR:
                        if coll_side == "left" or coll_side == "right":
                            if (coll_side == "left" and self.vel.x > 0 )or (coll_side == "right" and self.vel.x < 0):
                                self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                                self.acc.x = 0
                            wasstoppedHOR = True
                            self.pos = correctedPos
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.massHOR = collided.massHOR - 1
                        """
                        if coll_side == "top" or coll_side == "bot":
                            self.vel.y = self.addedVel.y
                            self.acc.y = 0
                            if group.has(self):
                                self.massVER = collided.massVER - 1

                        #if coll_side == "bot":
                        #   self.vel.y = self.addedVel.y
                        #  self.acc.y = 0
                            #if group.has(self):
                            #   self.massVER = collided.massVER - 1
                    if self.massHOR <= collided.massHOR:
                        if coll_side == "left" or coll_side == "right":
                            self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                            self.acc.x = 0
                            wasstoppedHOR = True
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.massHOR = collided.massHOR - 1
                        #if coll_side == "right":
                        #   self.vel.x = self.addedVel.x
                        #  self.acc.x = 0
                        # wasstoppedHOR = True
                            #if self.massHOR < collided.massHOR:
                            #   if group.has(self):
                            #      self.massHOR = collided.massHOR - 1
                            """
                    #if correctedPos.y > 0:    
                    #self.pos = correctedPos
                    posCorrected = True
        # This was implemented so the player couldn't push the dog with the box. 
        if wasstoppedHOR:
            self.stoppedHOR = True
        else: 
            self.stoppedHOR = False
        if onNoofPlats <= 1:
            if setright:
                self.set_right(setright)
            elif setleft:
                self.set_left(setleft)

    def solidCollisionss(self, group = None):#, ignoredSol = []):
        self.rect.midbottom = self.pos.rounded().asTuple()
        if self.vel.x < 0:
            self.rect.x += self.r(self.relativeVel().x-2)
        if self.vel.x > 0:
            self.rect.x += self.r(self.relativeVel().x+2)
        if self.vel.y < 0:
            self.rect.y += self.r(self.vel.y - 1) 
        elif self.vel.y > 0:
            self.rect.y += self.r(self.vel.y + 1) 
        savedPos = self.pos.copy()
        """
        if self.vel.x < 0:
            self.pos.x += self.relativeVel().x-0.01
        if self.vel.x > 0:
            self.pos.x += self.relativeVel().x+0.01
        if self.vel.y < 0:
            self.pos.y += self.vel.y - 0.01
        if self.vel.y > 0:
            self.pos.y += self.vel.y + 0.01
        """
        group = self.game.group_solid
        #collided_objects = self.collisionDetection(group)
        #print(f'own: {collided_objects}')
        self.pos = savedPos
        collided_objects = pg.sprite.spritecollide(self, group, False)
        #print(f'test: {test}')
        #print(f'pygame: {collided_objects}')
        self.rect.midbottom = self.pos.rounded().asTuple()
        wasstoppedHOR = False
        posCorrected=False
        onNoofPlats = 0
        setleft = False
        setright = False
        if collided_objects:
            for collided in collided_objects:
                if collided != self: # and collided not in ignoredSol: #and not self.isEnemy:
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if self.massVER < collided.massVER:
                        if coll_side == "top" or coll_side == "bot":
                            if (coll_side == "top" and self.vel.y > 0) or (coll_side == "bot" and self.vel.y < 0):
                                self.vel.y = self.addedVel.y
                                self.acc.y = 0
                            if coll_side == "top":
                                onNoofPlats += 1
                            self.pos = correctedPos
                            if group.has(self):
                                self.massVER = collided.massVER - 1
                            #other = self.distanceOrder[1]
                            # if a box or something is right at an edge, it would stand still because everything is so accurate lol
                            #if self.distanceOrder[1][1] < 4:
                             #   if self.distanceOrder[1][0] == "left":
                              #      #self.set_right(collided.left_x() - 1)
                               #     setright = collided.left_x() - 1
                                #if self.distanceOrder[1][0] == "right":
                                 #   setleft = collided.right_x() + 1
                                    #self.set_left(collided.right_x()+ 1)
                    if self.massHOR <= collided.massHOR:
                        if coll_side == "left" or coll_side == "right":
                            if (coll_side == "left" and self.vel.x > 0 )or (coll_side == "right" and self.vel.x < 0):
                                self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                                self.acc.x = 0
                            wasstoppedHOR = True
                            self.pos = correctedPos
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.massHOR = collided.massHOR - 1
                        """
                        if coll_side == "top" or coll_side == "bot":
                            self.vel.y = self.addedVel.y
                            self.acc.y = 0
                            if group.has(self):
                                self.massVER = collided.massVER - 1

                        #if coll_side == "bot":
                        #   self.vel.y = self.addedVel.y
                        #  self.acc.y = 0
                            #if group.has(self):
                            #   self.massVER = collided.massVER - 1
                    if self.massHOR <= collided.massHOR:
                        if coll_side == "left" or coll_side == "right":
                            self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                            self.acc.x = 0
                            wasstoppedHOR = True
                            if self.massHOR < collided.massHOR:
                                if group.has(self):
                                    self.massHOR = collided.massHOR - 1
                        #if coll_side == "right":
                        #   self.vel.x = self.addedVel.x
                        #  self.acc.x = 0
                        # wasstoppedHOR = True
                            #if self.massHOR < collided.massHOR:
                            #   if group.has(self):
                            #      self.massHOR = collided.massHOR - 1
                            """
                    #if correctedPos.y > 0:    
                    #self.pos = correctedPos
                    posCorrected = True
        # This was implemented so the player couldn't push the dog with the box. 
        if wasstoppedHOR:
            self.stoppedHOR = True
        else: 
            self.stoppedHOR = False

        #else:
        #if not posCorrected:
        #   self.pos = savedPos


    # Checking whether anything is on a solid
    def on_solid(self, group):
        self.rect.bottom += 2
        collided_objects = pg.sprite.spritecollide(self,group, False)
        savedPos = self.pos.copy()
        self.pos.y += 1
        #collided_objects = self.collisionDetection(group)
        self.pos = savedPos
        isOnPlatform = False
        result = None
        for collided in collided_objects:
            if collided != self:
                if self.determineSide(collided) == "top":
                    isOnPlatform = True
                    result = collided
        if isOnPlatform:
            self.isOnPlatform = True
        else:
            self.isOnPlatform = False
        self.rect.bottom -= 2
        #self.pos.y -= 2
        return result

    # Applies gravity and friction to the velocity of the sprite
    def applyPhysics(self):
        self.acc.y += self.gravity                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if abs(self.vel.x + self.addedVel.x) < 0.01:
            self.vel.x = self.addedVel.x
