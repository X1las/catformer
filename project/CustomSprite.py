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
    isPickedUp = False
    isPlatform = False

    def resetMass(self):
        self.massHOR = self.ori_massHOR
        self.massVER = self.ori_massVER

    def init(self):
        self.new_vel = self.vel.copy()
        self.overwritevel = self.vel.copy()

        
    def updateRect(self):
        #roundedvec = self.relativePosition.realRound()
        roundedvec = self.relativePosition.rounded()

        self.rect.midbottom = roundedvec.asTuple()
        self.acc = vec(0,0)
        

    def resetRects(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    def resetSprite(self):
        self.resetMass
        if self.count < 0:
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
        self.pos.x = xpos - self.width/2
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




    def touchEnemy(self, damager):
        collided = pg.sprite.spritecollide(self, damager, False)
        if collided: 
            for collided_obj in collided:
                self.takeDamage()         
        
    def touchPickUp(self, pickups):
        collided = pg.sprite.spritecollide(self, pickups, False)
        if collided: 
            for collided_obj in collided:
                if collided_obj.type == 'health' and self.lives < 9:
                    self.heal()
                    collided_obj.kill()
                if collided_obj.type == 'catnip':
                    self.addCatnip()
                    collided_obj.kill()

    def pickupSprite(self,  agents, turn, justPickedUp):
        # should ckeck which box is closest
            
        collided = pg.sprite.spritecollide(self, agents, False)
        
        if collided: 
            if turn:
                for collided_obj in collided:
                    collided_obj.rect.midbottom = collided_obj.pos.realRound().asTuple()
                    collided_obj.rect.y -= 4
                    # Kind of bad solution. removed from the group, because otherwise it detects collision with itself
                    self.game.group_solid.remove(collided_obj)
                    testcol = pg.sprite.spritecollideany(collided_obj, self.game.group_solid)
                    self.game.group_solid.add(collided_obj)
                    
                    if not testcol:
                
                        self.colliding = True
                        if justPickedUp:
                            collided_obj.pickupStarted = True
                        collided_obj.has_collided = True
                        #collided_obj.pickUp(self)
                        collided_obj.liftedBy(self)
                    collided_obj.rect.y += 4   
            else:
                self.colliding = False


    def relativeVel(self):
        return self.vel - self.addedVel

    def posCorrection(self):
        pass

    def collisionEffect(self):
        inflation = 2
        self.rect = self.rect.inflate(inflation,inflation)

        #self.rect.x += r(self.vel.x)
        self.rect.y -= 2
        collideds = pg.sprite.spritecollide(self, self.game.all_sprites, False)

        if collideds:
            for collided in collideds:
                try: 
                    if collided != self and collided.solidstrength < self.solidstrength and collided not in self.game.group_interactiveFields and collided not in self.game.group_pickups:
                        #print(f'solid: {self.name} affecting {collided.name}')
                        #print(f'solidvel : {self.vel}')

                        coll_side = collided.determineSide(self)
                        if coll_side == "top":
                            #collided.vel += self.vel
                            #if abs(collided.vel.x) < 0.5:
                            #if not self.isPlatform:
                            #pass
                            collided.addedVel.x = self.vel.x + self.addedVel.x
                except:
                    pass
                    #print(f'2 - acc in coll for {self.name} with {self.acc}')
                    
        
        self.rect.y += 1
        self.rect = self.rect.inflate(-inflation, -inflation)
        self.rect.midbottom = self.pos.rounded().asTuple()

    def pygamecoll(self, group, ignoredSol = None):
        inflationW = 0
        inflationH = 0
        self.rect = self.rect.inflate(inflationW,inflationH)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.x += r(self.relativeVel().x*1.5)
        self.rect.y += r(self.vel.y*1.5) 
        collideds = pg.sprite.spritecollide(self, group, False)
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect = self.rect.inflate(-inflationW, -inflationH)

        if collideds:
            for collided in collideds:
                if collided != self and collided != ignoredSol and not self.isEnemy and collided.solidstrength >= self.solidstrength:
                    if group.has(self):
                        self.solidstrength = collided.solidstrength -1
                    self.count = 2
                    coll_side = self.determineSide(collided)
                    if coll_side == "top":
                        newpos = collided.top_y()
                        if newpos < self.pos.y:
                            self.set_bot(collided.top_y())
                            self.vel.y = 0
                    else:
                        if coll_side == "left":
                            newpos = collided.left_x() - self.width/2 #Left side of object being collided with
                            if newpos <= self.pos.x:
                                self.pos.x = collided.left_x() - self.width/2
                                self.vel.x = self.addedVel.x # otherwise the player would get "pushed" out when touching box on moving platform
                                self.acc.x = 0

                        if coll_side == "right":
                            newpos = collided.right_x() + self.width/2
                            if newpos >= self.pos.x:
                                self.pos.x = collided.right_x() + self.width/2
                                self.vel.x = self.addedVel.x
                                self.acc.x = 0

                        if coll_side == "bot":
                            newpos =  collided.bot_y() + self.height 
                            if newpos > self.pos.y:
                                self.pos.y = newpos
                                self.vel.y = self.addedVel.y
                    #print(f'2 - acc in coll for {self.name} with {self.acc}')
                    
        

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
        

    def applyPhysics(self,Intersecters, ignoreSol = None):
        
        if self.on_solid(Intersecters, ignoredSol = ignoreSol):
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
        if self.isPlayer and abs(self.vel.x) < 0.0001:
            self.vel.x = 0
       
    def updatePos(self, group = None):
        self.pos +=  self.vel +  self.acc * 0.5




    #groups = game.all_sprites
    def rayIntersect(self,local_origin,collidables):   

        #original_pos = self.rayPos + local_origin      # Origin vector for calculations
    
        original_pos = self.pos + local_origin          # Origin vector for calculations
        vel = self.vel                                  # X and Y vector
        #collidables = col_objects                      # Array of collideable objects

        intersection = vel.copy()                       # Default intersection vector for comparison
        hitObject = False                               # Hit object as false by default

        # Will check if the x and y vectors are not equal to 0 and assign a to their quotient if they are not
        slope = False                                               
        if vel.x != 0 and vel.y != 0:                               
            slope = vel.y/vel.x                                         

        # we use the linear function f(x) = ax+b
        # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0
        # so long as v.x or v.y both aren't 0 then we can use the function as f(x) = a*x as b is 0
        # therefore y = a*x AND x = y/a

        if slope:
            for collidable in collidables:
                if collidable != self:
                    # Vertical intersections:
                    y_temp_intersection = collidable.pos.y - collidable.height                              # y equals the tops if moving down
            
                    if vel.y < 0:                                                                           # If jumping
                        y_temp_intersection = collidable.pos.y                                              # y equals the bottoms if moving up

                    y_local_temp = y_temp_intersection - original_pos.y                                     # Making a local y coordinate which is the y intersection - the origin's y position
                    x_local_temp = y_local_temp / slope                                                     # Making a local x coordinate from the local y divided by a
                    

                    x_temp_intersection = original_pos.x + x_local_temp                                     # Using the local x and adding the origin's x to get global x coordinates of the intersection point
            
                    if collidable.left_x() <= x_temp_intersection <= collidable.right_x():                  # Check if collision's x is between the collision object's left and right sides
                        tempVec = vec(x_local_temp , y_local_temp)                                          # Making a temporary vector be equal to the intersection
                        if tempVec.length() <= intersection.length():                                       # Checking if the temporary is shorter than the current intersection vector
                            intersection = tempVec                                                          # If it's true, the intersection will be equal to the temporary
                            hitObject    = collidable                                                       # Hit object will be defined as c
                    
                    # Horizontal intersections:
                    x_temp_intersection = collidable.left_x()                                               # x equals left side if moving right
                    if vel.x < 0:
                        x_temp_intersection = collidable.right_x()                                          # x equals right side if moving left
                    
                    x_local_temp = x_temp_intersection - original_pos.x                                     # Making a local x coordinate which is the x intersection - origin's x position
                    y_local_temp = x_local_temp * slope                                                     # Making a local y coordinate from the local x multiplied by a        

                    y_temp_intersection = original_pos.y + y_local_temp                                     # Global y position is the same as the origin's y + the local intersection's y position
                    
                    if collidable.top_y() <= y_temp_intersection <= collidable.bot_y():                     # check if collision's y is between the collision object's top and bottom sides
                        tempVec = vec(x_local_temp,y_local_temp)
                        if tempVec.length() <= intersection.length():
                            intersection = tempVec
                            hitObject = collidable 
        
        # When we have cases where one side is 0
        # Reduce it later, when we can boil it down more
        # Refer to the bit above if confused, there's a lot of repitition
        else:
            # If v.x is not 0:
            if vel.x != 0:
                for collidable in collidables:   
                    if collidable != self:                                
                        # X intersection will be equal to the left side by default and the right side if we're moving left 
                        #x_temp_intersection = collidable.pos.x - collidable.width/2
                        x_temp_intersection = collidable.left_x()
                        
                        if vel.x < 0:
                            #x_temp_intersection = collidable.pos.x + collidable.width/2
                            x_temp_intersection = collidable.right_x()
                        
                        x_local_temp = x_temp_intersection - original_pos.x                               
                        y_local_temp = 0                                         

                        y_temp_intersection = original_pos.y + y_local_temp                                
                        
                        if collidable.top_y() <= y_temp_intersection <= collidable.bot_y():                  
                            tempVec = vec(x_local_temp , y_local_temp)
                            if tempVec.length() <= intersection.length():
                                intersection = tempVec
                                hitObject = collidable 
            # If v.y is above 0
            if vel.y != 0:
                for collidable in collidables:
                    if collidable != self:
                        # Y intersection will be equal to the top side by default and the bottom if we're moving up
                        y_temp_intersection = collidable.top_y() 
                        if vel.y < 0:                                                             
                            y_temp_intersection = collidable.pos.y                                       

                        y_local_temp = y_temp_intersection - original_pos.y                                
                        x_local_temp = 0                                        
                        
                        x_temp_intersection = original_pos.x + x_local_temp                                
                        
                        if collidable.left_x() <= x_temp_intersection <= collidable.right_x():     
                            tempVec = vec(x_local_temp , y_local_temp)                          
                            if tempVec.length() <= intersection.length():                        
                                intersection = tempVec                                          
                                hitObject = collidable 

        
        if hitObject:
            intersection += original_pos            # Adding the origin's vector in the end to return the global coordinates instead of the local
            
            return [hitObject,intersection]
        else:
            return False
    

    # function that checks intersection using all four corners of moving object
    # input:  objects that might be hit
    # output: uniform point of collision, side of hit object (not implemented yet)
    def quadrupleRayIntersect(self, potential_hit_objects):
        offset = 1
        dicts = [
            {"corner": "TL", "corner pos": self.topleft()+vec(offset,offset),     "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "TR", "corner pos": self.topright()+vec(-offset,offset),    "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "BL", "corner pos": self.bottomleft()+vec(offset,-offset),  "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "BR", "corner pos": self.bottomright()+vec(-offset,-offset), "hitsobject": None, "hit pos": None, "relative hit pos": None}
        ]

        tempLen = self.vel.length()
        finalResult = None
        
        # iterate through all corners and ray intersect for each
        for corner in dicts:
            hitObj = self.rayIntersect(corner["corner pos"]-self.pos, potential_hit_objects)    # rayIntersect for each corner
            if hitObj:
                corner["hitsobject"] = hitObj[0]                                                # store which object the corner will hit
                corner["hit pos"] = hitObj[1]                                                   # store where the corner will hit the object
                corner["relative hit pos"] = corner["hit pos"] - corner["corner pos"]           # store the collision position relative to the corner
                # update final collision point to the closest collision point
                if corner["relative hit pos"].length() < tempLen:
                    tempLen = corner["relative hit pos"].length()
                    finalResult = corner
                        
        return finalResult

    def collisions_rayIntersect(self,Intersecters):  
        corner = self.quadrupleRayIntersect(Intersecters)
        self.rayPos = self.pos.copy()
        if corner:
            hitObject   = corner['hitsobject']
            hitPos      = corner['hit pos']
            relHitPos   = corner['relative hit pos']
            if hitObject.solid:
                self.hitsSolid(hitObject,  hitPos, relHitPos)
    
        # making vase break
        """if self.hitbox:
            vase_intersect = self.hitbox.rayIntersect(self.hitbox.topleft() - self.hitbox.pos, self.obstacles)
            if vase_intersect:
                if self.hitbox.breakable:
                    hit_point = vase_intersect[0]
                    if vase_intersect[1].y == vase_intersect[0].top_y():
                        print("skdjfl")
                        self.hitbox.pos.y = hit_point.top_y()
                        self.hitbox.vel *= 0
                        self.hitbox.fall = False
                        
                        self.hitbox.breaks()
                if self.hitbox.moveable:
                    hitSolid = self.hitsSolid(self.hitbox , vase_intersect[0],  vase_intersect[1] , self.hitbox.topleft())
                    if hitSolid:
                        self.hitbox.shouldApplyPhysics = False
                        print("hit solid")
        """

    # Moves the object when it's about to collide with a solid object
    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        betweenLR = hitObject.right_x() >= hitPosition.x >= hitObject.left_x()
        betweenTB = hitObject.bot_y()   >= hitPosition.y >= hitObject.top_y()
        print(hitObject.name)

        offsetX = 0
        if hitPosition.x == hitObject.left_x() and betweenTB:
            offsetX = -1
            #offsetX = -0.5
            self.vel.x = 0
            self.acc.x = 0
        elif hitPosition.x == hitObject.right_x() and betweenTB:
            offsetX = 1
            #offsetX = 0.5
            self.vel.x = 0
            self.acc.x = 0
        
        offsetY = 0
        if hitPosition.y == hitObject.top_y() and betweenLR:
            offsetY = -1
            self.vel.y = 0
            self.acc.y = 0
            self.inAir = False
        elif hitPosition.y == hitObject.bot_y() and betweenLR:
            offsetY = 1
            self.vel.y = 0
            self.acc.y = 0

        self.pos += relativeHitPos + vec(offsetX,offsetY) 
        self.rayPos = self.pos + vec(offsetX, offsetY)                        
