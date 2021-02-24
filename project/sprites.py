# Sprite classes for platform game
import pygame as pg

from vector import *
from settings import *
from random import choice, randrange, uniform
from os import path
import copy
#vec = pg.math.Vector2
vec = Vec


class Player(pg.sprite.Sprite):
    def __init__(self, game, x,y, name = None):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game          = game; self.name = name; self._layer = 1
        self.jumping       = False
        self.image         =  pg.Surface((30,40)); self.image.fill((250,0,0)); self.rect = self.image.get_rect()
        self.rect.midbottom   = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.dist_from_right = 0; self.dist_from_left = 0; self.dist_from_top = 0; self.dist_from_bottom = 0
        self.on_collided_surface = False

    def initKeys(self, jump, left, right, crouch):
        self.jump_key = jump


    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        self.jump()
        self.touches()

        # call rayIntersect(vel, origin, all_sprites)
        # returns [hitObject, intersection] if it hits anything
        # returns False if it hits nothing
        # if rayIntersect(...):
            # set position to intersection, intersection = rayIntersect[1]
        Intersect = self.rayIntersect(self.vel, Vec(self.rect.left,self.rect.top),self.game.all_sprites) 
        if Intersect:
            self.pos = Intersect[1]
            
        self.move()
        self.applyPhysics() 
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()


    # -->  This function will check if a player stands on a platform and well when jump if space is pressed
    def jump(self):                                                              # jump only if standing on a platform
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.surfaces, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2                                                         # undo 2 lines before
        if hits and not self.jumping:                                            # If you are on a platform and not jumping
            keys = pg.key.get_pressed()                                            # Checks for keys getting pressed
            if keys[pg.K_SPACE]:                                                 # If it's left arrow
                self.jumping = True                                                    # then you jump
                self.vel.y = -PLAYER_JUMP                                                  #\\

    # Function to calculate and return the first intersection of a vector given an origin and a group of collision objects
    # Returns false if there are no collisions and a list containing a hit object and the intersection vector if there are
    def rayIntersect(self,vec,origin,collision_objects):   

        O = origin                                          # Origin vector for calculations
        V = vec                                             # X and Y vector
        COL = collision_objects                             # Array of collideable objects

        intersection = V                                    # Default intersection vector for comparison
        hitObject = False                                   # Hit object as false by default
        
        # Will check if the x and y vectors are not equal to 0 and assign A to their quotient if they are not
        A = False                                         
        if V.x != 0 and V.y != 0:                           
            A = V.x/V.y 

        # we use the linear function f(x) = ax+b
        # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0
        # so long as V.x or V.y both aren't 0 then we can use the function as f(x) = a*x as b is 0
        # therefore y = a*x AND x = y/a
        
        if A:
            for c in COL:
                # Vertical intersections:
                y = c.rect.top
                if V.y < 0:
                    y = c.rect.bottom
                x = O.x + (y - O.y) / A
                if c.rect.left < x < c.rect.right:
                    tempVec = Vec(x,y)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = c
                
                # Horizontal intersections:
                x = c.rect.left
                if V.x < 0:
                    x = c.rect.right
                y = O.y + (x - O.x) * A
                if c.rect.top < y < c.rect.bottom:
                    tempVec = Vec(x,y)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = c 
        else:
            # If V.x is not 0:
            #If V.x is above 0
            if V.x > 0:
                for c in COL:
                    x = c.rect.left
                    if O.x < x < O.x+V.x:
                        y = O.y
                        if c.rect.top < y < c.rect.bottom:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.x is below 0
            if V.x < 0:             
                for c in COL:
                    x = c.rect.right
                    if O.x > x > O.x+V.x:
                        y = O.y
                        if c.rect.top < y < c.rect.bottom:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.y is above 0
            if V.y > 0:
                for c in COL:
                    y = c.rect.top
                    if O.y < y < O.y+V.y:
                        x = O.x
                        if c.rect.left < x < c.rect.right:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.y is below 0
            if V.y < 0:
                for c in COL:
                    y = c.rect.bottom
                    if O.y > y > O.y+V.y:
                        x = O.x
                        if c.rect.left < x < c.rect.right:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            # Hi guys :-)
            # Made with love and hate of algebra
        if hitObject:
            return [hitObject,intersection]
        else:
            return False



    # ---> Checks for pressed keys to move left/right
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT] and not self.touching_left:                  # If it's left arrow
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT] and not self.touching_right:
            self.acc.x = PLAYER_ACC
    
    # -->  Applies gravity, friction, mortion etc, nerdy stuff
    def applyPhysics(self):
        #if not self.on_surface:
        self.acc = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION      # Friction
        #self.vel.x = 0.93 * self.vel.x
        self.vel += self.acc                            # equations of motion
        if abs(self.vel.x) < 0.25:
            self.vel.x = 0   
        self.pos += self.vel +  self.acc * 0.5
        #print(f'pos efter grav: {self.pos}')
 
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # -----------CAN BE IGNORED!----------
    # ---> Not important. I just tried to make make it impossible to walk through a platform. Not used atm, but keeping it for later inspiration
    def touches(self):
        """
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2   
        if hits:
            self.on_surface = True
        else:
            self.on_surface = False
        """

        #self.pos.x += self.vel.x
        #hits = pg.sprite.spritecollide(self, self.game.obstacles, False)




        collided_group = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if collided_group:
            for collided_object in collided_group:
       
                #dist_from refers to the distance between the .... 
                self.dist_from_right  = self.rect.left   - collided_object.rect.right
                self.dist_from_left   = self.rect.right  - collided_object.rect.left
                self.dist_from_top    = abs(self.rect.bottom - collided_object.rect.top)
                self.dist_from_bottom = abs(self.rect.top    - collided_object.rect.bottom)

                self.on_collided_surface = abs(self.rect.bottom - collided_object.rect.top) < 5
            
                if not self.on_collided_surface:

                    if abs(self.dist_from_bottom) < PLAYER_ACC * 10:
                        self.touching_top = True
                        self.pos.y -= self.dist_from_bottom
                        #self.rect.top = collided_object.rect.bottom
                        self.acc.y = 0
                        self.vel.y = 0

                    
                    elif abs(self.dist_from_top) < self.vel.length():
                        self.touching_bot = True
                        self.pos.y += self.dist_from_top
                        #self.rect.bottom = collided_object.rect.top
                        self.acc.y = 0
                        self.vel.y = 0

                    elif 10 > abs(self.dist_from_right):
                        self.pos.x += self.dist_from_right
                        if collided_object in self.game.non_moveable:
                            self.touching_left = True
                            self.acc.x = 0
                            if self.vel.x < 0:
                                self.vel.x = 0
                    
                    elif 10 > abs(self.dist_from_left):
                        self.pos.x -= self.dist_from_left
                        if collided_object in self.game.non_moveable:
                            self.touching_right = True      
                            self.acc.x = 0
                            if self.vel.x > 0:
                                self.vel.x = 0




        #self.pos.x -= self.vel.x    
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def testNextFrame(self,sprite):

        temp_pos = copy.copy(self.pos)
        temp_vel = copy.copy(self.vel)
        self.pos += temp_vel
        possibleHits = pg.sprite.collide_rect(self,sprite, False)
        self.pos = temp_pos
        return possibleHits





# --->  The platforms (surprise!)
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, name, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.non_player, game.platforms, game.surfaces, game.obstacles, game.non_moveable 

        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.rect.x = x                                                                       # Put the platform at the given coordinate.
        self.rect.y = y
        self.typed = "platform"                                                                       # \\


# ---> boxes :-o
class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, name):
        self.game   = game;  self.width  = width; self.height = height; self.name = name
        self.groups = game.all_sprites, game.non_player, game.boxes, game.surfaces, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width,height))
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Vase(pg.sprite.Sprite):
    def __init__(self,game,x,y, name = None):
        self.broken = False; self.name = name
        self.width = 20
        self.height = 30
        self.game = game
        self.groups = game.all_sprites, game.vases, game.non_player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        
        self.rect.midbottom = (x,y)
        #self.rect.x = x
        #self.rect.y = y
    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str , name = None):
        try:
            if placement == "left":
                pos = plat.rect.topleft
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos = plat.rect.midtop
            return cls(game = game, x = pos[0] + push, y = pos[1])
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1])


    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True
