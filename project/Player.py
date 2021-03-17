# Description:

# Imports
import pygame as pg
import copy

from settings import *

from Vector import Vec
from CustomSprite import CustomSprite
from random import choice, randrange, uniform

# Variables
vec = Vec

# Classes
class Player(CustomSprite):
    def __init__(self, game, x, y, name = None):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game           = game; self.name = name; self._layer = 1
        self.jumping        = False
        self.width          = 30; self.height = 40
        self.image          =  pg.Surface((self.width,self.height)); self.image.fill((250,0,0)); self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.dist_from_right = 0; self.dist_from_left = 0; self.dist_from_top = 0; self.dist_from_bottom = 0
        self.on_collided_surface = False; self.stop_falling = False

    def initKeys(self,jump, left, right, crouch):
        self.jump_key = jump

    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        self.jump()
        self.touches()    
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
        #if not self.on_collided_surface:
        
        #print(f"stop falling?: {self.stop_falling}")
        #print(f'acc before: {self.acc}')
        if not self.stop_falling:
            self.acc = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION          # Friction
        
        #self.vel.x = 0.93 * self.vel.x
        self.vel += self.acc                                # equations of motion
        
        if abs(self.vel.x) < 0.25:                          
            self.vel.x = 0                                  
        

        self.pos += self.vel +  self.acc * 0.5


        
        self.stop_falling = False
        
        #print(f'pos efter grav: {self.pos}')
 
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)



    # -----------CAN BE IGNORED!----------
    # ---> Not important. I just tried to make make it impossible to walk through a platform. Not used atm, but keeping it for later inspiration
    def touches(self):


        #self.pos.x += self.vel.x
        #hits = pg.sprite.spritecollide(self, self.game.obstacles, False)

        self.rect.midbottom = self.pos.asTuple()
        #print("stuff")
        #Vec(self.pos.x - self.width/2 ,self.pos.y - self.height)
        # Time testing

        #errCorrect = time.perf_counter()
        #errCorrect = time.perf_counter()-errCorrect
        
        #print(f"Error correction in {errCorrect} seconds")
        
        #t = time.perf_counter()
        
        Intersect = self.rayIntersect(self.vel , self.game.non_player)
        
        #t = time.perf_counter() - t - errCorrect
        
        #print(f"Execution took {t} seconds")
        #print(Intersect)
        if Intersect:
            collided_object = Intersect[0]
            
            collided_object_point = Intersect[1]
            print(collided_object_point)


            self.dist_from_right  = collided_object_point.x   ==  collided_object.pos.x + collided_object.width/2
            self.dist_from_left   = collided_object_point.x  == collided_object.pos.x - collided_object.width/2
            self.dist_from_top  = collided_object_point.y == collided_object.pos.y - collided_object.height
            self.dist_from_bottom    =  collided_object_point.y == collided_object.pos.y

            self.dist_from_right  = abs(collided_object_point.x   - collided_object.pos.x - collided_object.width/2) 
            self.dist_from_left   = abs(collided_object_point.x  + collided_object.pos.x - collided_object.width/2)
            self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - collided_object_point.y)
            self.dist_from_bottom    = abs(collided_object_point.y   - collided_object.pos.y)

            hit_side = min(self.dist_from_bottom, self.dist_from_left, self.dist_from_right, self.dist_from_top)



            #self.dist_from_right  = abs(self.pos.x - self.width/2   - collided_object.pos.x - collided_object.width/2) 
            #self.dist_from_left   = abs(- self.pos.x - self.width/2  + collided_object.pos.x - collided_object.width/2)
            #self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - self.pos.y)
            #self.dist_from_bottom    = abs(self.pos.y - self.height    - collided_object.pos.y)
                        
            if not self.on_collided_surface:

                if hit_side == self.dist_from_bottom:
                    self.touching_top = True
                    #self.pos.y -= self.dist_from_bottom
                    print("from bottom")
                    
                    #self.rect.top = collided_object.rect.bottom
                    #self.acc.y = 0
                    if self.vel.y < 0:
                        self.vel.y = 0
                    #self.vel.y = 0

                
                elif hit_side == self.dist_from_top:
                    self.touching_bot = True
                    print("on platform ---------------------------------------------------------------------------------")
                    #self.pos.y += self.dist_from_top
                    #self.rect.bottom = collided_object.rect.top
                    self.acc.y = 0
                    if self.vel.y > 0:
                        self.vel.y = 0
                    self.stop_falling = True
                    #self.vel.y = 0

                elif hit_side == self.dist_from_right:
                    #self.pos.x += self.dist_from_right
                    print("right side")
                    if collided_object in self.game.non_moveable:
                        self.touching_left = True
                        self.acc.x = 0
                        if self.vel.x < 0:
                            self.vel.x = 0
                    
                
                elif hit_side == self.dist_from_left:
                    #self.pos.x -= self.dist_from_left
                    
                    print("left side")
                    if collided_object in self.game.non_moveable:
                        self.touching_right = True      
                        self.acc.x = 0
                        if self.vel.x > 0:
                            self.vel.x = 0

                            
            self.pos = collided_object_point

        """
        collided_group = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if collided_group:
            for collided_object in collided_group:
       
                #dist_from refers to the distance between the .... 
                self.dist_from_right  = abs(self.pos.x - self.width/2   - collided_object.pos.x - collided_object.width/2) 
                self.dist_from_left   = abs(- self.pos.x - self.width/2  + collided_object.pos.x - collided_object.width/2)
                self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - self.pos.y)
                self.dist_from_bottom    = abs(self.pos.y - self.height    - collided_object.pos.y)
                
                #print(f"dist from bottom platform: {self.dist_from_bottom} ")
                #print(f"dist from top platform: {self.dist_from_top} ")
                #print(f"y position: {self.pos.y} ")
                #print(f"collided object y position: {collided_object.pos.y} ")
                #print(f"dist from right platform: {self.dist_from_right} ")
                #print(f"dist from left platform: {self.dist_from_left} ")
                self.on_collided_surface = abs(self.rect.bottom - collided_object.rect.top) < 5
                
                if not self.on_collided_surface:

                    if abs(self.dist_from_bottom) < 6:
                        self.touching_top = True
                        self.pos.y -= self.dist_from_bottom
                        print("from bottom")
                        
                        #self.rect.top = collided_object.rect.bottom
                        #self.acc.y = 0
                        if self.vel.y < 0:
                            self.vel.y = 0
                        #self.vel.y = 0

                    
                    elif abs(self.dist_from_top) < 10:
                        self.touching_bot = True
                        print("on platform ---------------------------------------------------------------------------------")
                        self.pos.y += self.dist_from_top
                        #self.rect.bottom = collided_object.rect.top
                        self.acc.y = 0
                        if self.vel.y > 0:
                            self.vel.y = 0
                        self.stop_falling = True
                        #self.vel.y = 0

                    elif 10 > abs(self.dist_from_right):
                        self.pos.x += self.dist_from_right
                        print("right side")
                        if collided_object in self.game.non_moveable:
                            self.touching_left = True
                            self.acc.x = 0
                            if self.vel.x < 0:
                                self.vel.x = 0
                        
                    
                    elif 10 > abs(self.dist_from_left):
                        self.pos.x -= self.dist_from_left
                        print("left side")
                        if collided_object in self.game.non_moveable:
                            self.touching_right = True      
                            self.acc.x = 0
                            if self.vel.x > 0:
                                self.vel.x = 0
        """
                    

        #print(f'acc: {self.acc}')
        #print(f'vel: {self.vel}')
        #print(f'pos: {self.pos}')
        #self.pos.x -= self.vel.x    
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def testNextFrame(self,sprite):

        temp_pos = copy.copy(self.pos)
        temp_vel = copy.copy(self.vel)
        self.pos += temp_vel
        possibleHits = pg.sprite.collide_rect(self,sprite, False)
        self.pos = temp_pos
        return possibleHits
