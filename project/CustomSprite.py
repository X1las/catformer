# Imports
# Extenal Modules:
import pygame as pg
import math

# Project Imports
from Vector import Vec
from settings import *

# Classes
class CustomSprite(pg.sprite.Sprite):
    
    # Class Variables:
    # Variables for the masses
    solidstrength           = 0
    massHOR = ori_massHOR   = 0
    massVER = ori_massVER   = 0
    # default physics constants
    gravity                 = GRAVITY
    friction                = FRICTION
    # Used in SolidCollisions(). Whether something was corrected that iteration
    stoppedHOR              = False
    # "is..." values which are overwritten in the corresponding class
    isEnemy                 = False
    isPlatform              = False
    # Default value for general update order and draw player (for SpriteGroup class)
    _layer                  = 10
    draw_layer              = 0
    # Making sure all sprites have these vectors
    pos    = Vec(); vel  = Vec(); acc = Vec()
    relativePosition = Vec()

    # initializer. Should not be used to create a sprite. Should only be called by subclasses
    def __init__(self):
        self.addedVel        = Vec()



    """ ----- Methods ---------------- """

    # Method for rounding away from zero
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
        return self.pos.x - self.width/2 
    def right_x(self): 
        return self.pos.x + self.width/2


    # Methods for setting sides of a sprite based on its sides
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
        return Vec(self.left_x(), self.bot_y()).rounded()
    def bottomright(self):
        return Vec(self.right_x(), self.bot_y()).rounded()
    def topleft(self):
        return Vec(self.left_x(), self.top_y()).rounded()
    def topright(self):
        return Vec(self.right_x(), self.top_y()).rounded()
    def mid(self):
        return Vec(self.pos.x,self.bot_y()-self.height/2)
    

    # Returns the velocity of a sprite relative to the moving sprite below it
    def relativeVel(self):
        return self.vel - self.addedVel

    # Method to call on nearly all sprites upon their __init__. 
    # just to keep the individual sprite __init__ shorter
    def init(self):
        self.massHOR = self.solidstrength
        self.massVER = self.solidstrength
        self.ori_massHOR = self.massHOR
        self.ori_massVER = self.massVER
        self.relativePosition = self.pos.copy()
   
    def updateRect(self):
        self.rect.midbottom = self.pos.rounded().asTuple()


    """ ----------- For iterative purposes (SpriteGroup) ---------------------- """

    # Resets a few values that may have been temporarily changed during last iteration
    def resetSprite(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER
        if not self.isPlatform:
            self.vel -= self.addedVel
        self.addedVel = Vec(0,0)
        self.acc = Vec(0,0)

    # Updates rectangles before drawing so it matches the screen position
    def toRelativeRect(self):
        self.rect.midbottom = self.relativePosition.rounded().asTuple()


    # Resets rectangles after drawing so they match the global position
    def resetRects(self):
        self.updateRect()

    # The base update for the first updates each sprite does
    def update(self):
        self.updateRect()
        

    # Adds velocity given from another sprite below it (see dragAlongSprite() and pushEffect())
    def updateAddedVel(self):
        self.vel += self.addedVel

    # Adds velocity and acceleration to the position vector
    def updatePos(self):
        self.pos +=  self.vel +  self.acc * 0.5
    
    # For the few sprites that need to update something after previous methods were called
    def update2(self):
        pass

    # For correcting positions such as colliding with a solid
    def posCorrection(self):
        pass


    """ ------------ For detecting and/or returning collided sides --------------------- """

    # Determines the side of collisions
    def determineSide(self, collided):
        leftcoll  = abs(self.right_x() - collided.left_x())
        rightcoll = abs(collided.right_x() - self.left_x() )
        topcoll   = abs(self.bot_y() - collided.top_y())
        botcoll   = abs(self.top_y() - collided.bot_y())
        mins      = min(leftcoll, rightcoll, topcoll, botcoll)
        if mins == leftcoll: 
            return "left"
        elif mins == rightcoll:
            return "right"
        elif mins == topcoll:
            return "top"
        elif mins == botcoll:
            return "bot"


    # Gets the side of collision, but also checks whether it should correct the position and then returns it
    def collisionSide_Conditional(self, collided):
        coll_side = self.determineSide(collided)
        result = {"side" : "None", "correctedPos" : self.pos}
        if coll_side == "top": # Top of the collided object. A platform for example. 
            newpos = Vec(self.pos.x, collided.top_y())
            if newpos.y <= self.pos.y: # Only if the sprite would actually get pushed upwards from the correction
                return {"side" : "top", "correctedPos" : newpos}
        elif coll_side == "left":
            newpos = Vec(collided.left_x() - self.width/2, self.pos.y)
            if newpos.x <= self.pos.x:
                return {"side" : "left", "correctedPos" : newpos}
        elif coll_side == "right":
            newpos = Vec(collided.right_x() + self.width/2, self.pos.y)
            if newpos.x >= self.pos.x:
                return {"side" : "right", "correctedPos" : newpos}
        elif coll_side == "bot": 
            newpos = Vec(self.pos.x, collided.bot_y() + self.height)
            if newpos.y >= self.pos.y: 
                return {"side" : "bot", "correctedPos" : newpos}
        return result 


    """ --------------- For handling collisions with solid sprites ------------------------------ """

    # Can push another 'movable' sprite. Such as if a dog pushes a box. 
    # This method is called on the sprite that pushes.
    def pushEffect(self):
        # Check a bit ahead of itself
        self.updateRect()
        self.rect.x += self.r(self.relativeVel().x)
        # Check collisions with objects sorted by their horizontal 'mass'
        group = self.game.group_movables
        grouplist = group.massSort("massHOR")
        collided_objects = pg.sprite.spritecollide(self, grouplist, False)
        if collided_objects:
            for collided in collided_objects:
                if collided != self and not collided.isPlatform and self.massHOR >= collided.massHOR: 
                    coll_side = collided.determineSide(self)
                    if (coll_side == "right" and self.vel.x > 0) or (coll_side == "left" and self.vel.x < 0):
                        collided.addedVel.x += self.vel.x + self.addedVel.x
        # Check for top collision as well
        self.dragAlongSprite()

    # Takes care of moving things on top of itself with the same velocity. 
    # A player standing on a platform will move with the platform
    def dragAlongSprite(self):
        if not self.isEnemy: # Someone on top of the enemy should not move with the enemy
            # Make sure it catches things above itself and a bit ahead of it's x-velocity
            self.updateRect()
            self.rect.y -= 5
            self.rect.x += self.r(self.relativeVel().x)
            # Check collisions with objects sorted by their y-position
            group = self.game.all_sprites
            grouplist = group.heightSort()
            collided_objects = pg.sprite.spritecollide(self, group, False)
            if collided_objects:
                for collided in collided_objects:
                    if collided != self and not collided.isPlatform:
                        coll_side = collided.determineSide(self)
                        if coll_side == "top":
                            collided.addedVel.x = self.vel.x + self.addedVel.x
                            if self.vel.y >= 0: # If it is added when something goes up, it will push sprite too far up
                                collided.addedVel.y = self.vel.y + self.addedVel.y
                            if collided in self.game.group_solid: # Run it again in case of stacking on platform
                                collided.dragAlongSprite()
            self.updateRect()

    # Checking if a sprite is colliding with a solid sprite and pushes it out/stops its velocity and acceleration
    def solidCollisions(self):
        wasstoppedHOR = False
        recursiveList = [] 
        # Move rect a bit ahead
        self.updateRect()
        self.rect.x += self.r(self.relativeVel().x)
        self.rect.y += self.r(self.relativeVel().y)
        # Sorting the solids so it will check for the heavier ones first
        group = self.game.group_solid
        grouplist = group.createMassOrdered() 
        collided_objects = pg.sprite.spritecollide(self, grouplist, False)
        if collided_objects:
            for collided in collided_objects:
                if collided != self:
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    # If the sprite is 'vertically lighter' or equeally heavy in case the sprite is movable 
                    if self.massVER < collided.massVER  or (self.massVER == collided.massVER and self.game.group_movables.has(self)):
                        if coll_side == "top" or coll_side == "bot":
                            self.vel.y = self.addedVel.y
                            self.acc.y = 0
                            self.pos.y = correctedPos.y
                            # Temporarily making the sprite slightly less heavy than the solid object. 
                            if group.has(self):
                                self.massVER = collided.massVER - 1
                            recursiveList.append(collided)                                       
                    # If the sprite is 'horizontally lighter' or equeally heavy in case the sprite is movable 
                    if self.massHOR < collided.massHOR or (self.massHOR == collided.massHOR and self.game.group_movables.has(self)):
                        if coll_side == "left" or coll_side == "right":
                            self.vel.x = self.addedVel.x 
                            self.acc.x = 0
                            self.pos.x = correctedPos.x
                            wasstoppedHOR = True
                            if group.has(self):
                                self.massHOR = collided.massHOR - 1
                            recursiveList.append(collided)
        # For sprite to access whether it was stopped horizontically
        if wasstoppedHOR:
            self.stoppedHOR = True
        else: 
            self.stoppedHOR = False
        for i in recursiveList: # Run again on solids that corrected in case of chain-collisions
            i.solidCollisions()


    # Checking whether anything is on a solid. Mostly used for if-statements
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


    """ Physics application"""
    # Applies gravity and friction to the velocity of the sprite
    def applyPhysics(self):
        self.acc.y += self.gravity                          # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if abs(self.vel.x + self.addedVel.x) < 0.01:        # In case the velocity so small, just set it to non-moving. Otherwise, will get infinitely small
            self.vel.x = self.addedVel.x
