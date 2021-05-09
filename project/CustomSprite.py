# Imports
import pygame as pg
from Vector import *
from settings import *
import math

#import spritesheet as ss

vec = Vec

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


# Classes
class CustomSprite(pg.sprite.Sprite):
    #attributes:
    pos    = vec(); vel  = vec(); acc = vec()
    change_pos = None
    change_vel = None
    adds_pos = []
    solid     = False
    moveable  = False
    breakable = False
    pickup = False
    inAir = True
    collided_right_side = False; collided_left_side = False; collided_bottom = False; collided_top = False
    relativePosition = vec()
    on_platform = False 
    gravity = GRAVITY
    has_collided = False
    new_vel = vec(0,0)
    new_acc = vec(0,0)

    friction = FRICTION
    isPlayer = False
    can_fall_and_move = False
    rayPos = vec()
    isVase = False
    ignoreSol = None
    solidstrength = 0
    originalsolidstrength = 0
    massHOR = 0
    massVER = 0
    ori_massHOR = massHOR
    ori_massVER = massVER

    overwritevel = vec()
    overwrite = False
    update_order = 10
    name = ""
    count = 5
    isEnemy = False
    addedVel = Vec(0,0)
    pickupStarted = False
    isPlatform = False
    stoppedHOR = False
    stoppedVER = False

    def resetMass(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER

    def init(self):
        self.massHOR = self.solidstrength
        self.massVER = self.solidstrength
        self.ori_massHOR = self.massHOR
        self.ori_massVER = self.massVER
        self.new_vel = self.vel.copy()

    def update(self):
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updateRect(self):
        roundedvec = self.relativePosition.rounded()
        self.rect.midbottom = roundedvec.asTuple()
        self.acc = vec(0,0)
        

    def resetRects(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    def resetSprite(self):
        if self.count <= 0:
            self.resetMass()
            self.solidstrength = self.originalsolidstrength
        self.count -= 1
        self.vel -= self.addedVel
        self.addedVel = Vec(0,0)
    
        
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

    def endGoal(self, player):
        has_collided = pg.sprite.collide_rect(self, player)
        if has_collided:
            self.activate()

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

    """
    def buttonPress(self, agents):
        collided = pg.sprite.spritecollide(self, agents, False)
        if collided: 
            for collided_obj in collided:
                self.activate()
                self.prevActivated = True
                return self
        else:
            self.deactivate()
            self.activated = False
            self.deactivated = True
            return None
    """
    def touchEnemy(self):
        damager = self.game.group_enemies
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect = self.rect.inflate(4,4)
        collided = pg.sprite.spritecollide(self, damager, False)
        self.rect = self.rect.inflate(-4,-4)
        if collided: 
            for collided_obj in collided:
                if collided_obj.active:
                    print(f'hit enemy: {collided_obj.name}')
                    self.takeDamage()         
        self.rect.midbottom = self.pos.rounded().asTuple()
        
    def touchPickUp(self):
        pickups = self.game.group_pickups
        collided = pg.sprite.spritecollide(self, pickups, False)
        if collided: 
            for collided_obj in collided:
                if collided_obj.type == 'health' and self.lives < 9:
                    self.heal()
                    collided_obj.kill()
                if collided_obj.type == 'catnip':
                    self.addCatnip()
                    collided_obj.kill()
    """
    def leverPull(self,  agents, turn):
        collided = pg.sprite.spritecollide(self, agents, False)
        if collided: 
            for collided_obj in collided:
                if turn:
                    if not self.activated:
                        self.activate()
                    else:
                        self.deactivate()
                self.prevActivated = True
                return self
    

    def knockOver(self,  agents, turn):
        collided = pg.sprite.spritecollide(self, agents, False)
        if collided: 
            for collided_obj in collided:
                if turn:
                    collided_obj.fall = True
                    collided_obj.gravity = PLAYER_GRAV
    def pickupSprite(self,  agents, turn, justPickedUp):
        # should ckeck which box is closest
        canpickup = True
        collided = pg.sprite.spritecollide(self, agents, False)
        if collided: 
            if turn:
                for collided_obj in collided:
                    collided_obj.rect.midbottom = collided_obj.pos.realRound().asTuple()
                
                    collided_obj.rect.y -= 2
                    # Kind of bad solution. removed from the group, because otherwise it detects collision with itself
                    #self.game.group_solid.remove(collided_obj)
                    testcol = pg.sprite.spritecollide(collided_obj, self.game.group_solid, False)
                    collided_obj.rect.midbottom = collided_obj.pos.realRound().asTuple()
                    #self.game.group_solid.add(collided_obj)
                    for i in testcol:
                        if i != collided_obj:
                            side = i.determineSide(collided_obj)
                            if side == "top":
                                canpickup = False

                    if canpickup:
                
                        self.colliding = True
                        if justPickedUp:
                            collided_obj.pickupStarted = True
                        collided_obj.has_collided = True
                        collided_obj.liftedBy(self)
                    #collided_obj.rect.y += 1 
            else:
                self.colliding = False # remove?

    """
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

    def collisionEffect(self):
        inflation = 2
        self.rect = self.rect.inflate(inflation,inflation)

        #self.rect.x += r(self.vel.x)
        self.rect.y -= 2
        collideds = None
        if not self.isEnemy:
            collideds = pg.sprite.spritecollide(self, self.game.all_sprites, False)

        if collideds:
            for collided in collideds:
                try: 
                    if collided != self and collided.lessMassThan(self) and collided not in self.game.group_interactiveFields and collided not in self.game.group_pickups:
                        #print(f'solid: {self.name} affecting {collided.name}')
                        #print(f'solidvel : {self.vel}')

                        coll_side = collided.determineSide(self)
                        if coll_side == "top":
                            collided.addedVel.x = self.vel.x + self.addedVel.x
                except:
                    pass
                    
        
        self.rect.y += 1
        self.rect = self.rect.inflate(-inflation, -inflation)
        self.rect.midbottom = self.pos.rounded().asTuple()

    def lessMassThan(self, other):
        return self.massHOR < other.massHOR or self.massVER < other.massVER

    def pygamecoll(self, group = None, ignoredSol = []):
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x += r(self.relativeVel().x*1.5)
        self.rect.y += r(self.vel.y) 
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

    def on_solid(self, group, ignoredSol = None):
        self.rect.bottom += 2
        collideds = pg.sprite.spritecollide(self, group, False)
        self.on_platform = False
        result = None
        for collided in collideds:
            if collided != self.ignoreSol and collided != self:
                
                if self.determineSide(collided) == "top":
                    self.on_platform = True
                    result = collided
        self.rect.bottom -= 2
        return result
        

    def applyPhysics(self,Intersecters = None, ignoreSol = None):
        
        if self.on_solid(self.game.group_solid, ignoredSol = ignoreSol):
            self.inAir = False
        else:
            self.inAir = True

        if self.inAir:
            self.gravity = GRAVITY
        else:
            self.gravity = 0
            tempVel = self.vel.copy()
        
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.acc.x += self.vel.x * self.friction            # Friction
        self.vel   += self.acc                              # equations of motion
        if self.isPlayer and abs(self.vel.x) < 0.01:
            self.vel.x = self.addedVel.x
       
    def updatePos(self, group = None):
        self.pos +=  self.vel +  self.acc * 0.5
        self.acc = vec(0,0)    # caused problems? 



    def collisionMultipleGroups(self,*groups):
        collidedObjects = []
        for group in groups:
            collisionsInGroup = pg.sprite.spritecollide(self, group, False)
            for collision in collisionsInGroup:
                collidedObjects.append(collision)
        return collidedObjects
