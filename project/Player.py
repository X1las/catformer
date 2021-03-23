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
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.surfaces)
        self.game           = game; self.name = name; self._layer = 1
        self.facing = None
        self.jumping        = False
        self.width          = 30; self.height = 40
        self.image          =  pg.Surface((self.width,self.height)); self.image.fill((255,255,0)); self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_slopeight = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.dist_from_right = 0; self.dslopest_from_left = 0; self.dist_from_top = 0; self.dist_from_bottom = 0
        self.on_collided_surface = False; self.stop_falling = False
        self.interactRect   = self.interact()
        self.locked = False
        self.lives = 9
        self.catnip_level = 0

    def takeDamage(self):
        self.lives -= 1
        print(self.lives)
        
        return self.lives

    def heal(self):
        self.lives += 1
        print(self.lives)
        return self.lives


    def addCatnip(self):
        self.catnip_level += 1
        print(self.catnip_level)
        return self.catnip_level

    def interact(self):

        
        pass



    def initKeys(self,jump, left, right, crouch):
        self.jump_key = jump

    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        self.jump()
        #self.touches()    
        self.move()
        self.applyPhysics() 
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        round(self.pos)
    
    def update_pos(self):
        self.rect.midbottom = self.pos.asTuple()

    # -->  This function will check if a player stands on a platform and well when jump if space is pressed
    def jump(self):                                                              # jump only if standing on a platform
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.surfaces, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2                                                         # undo 2 lines before
        if hits and not self.jumping:                                            # If you are on aslopeplatform and not jumping
            keys = pg.key.get_pressed()                                            # Checks for keys getting pressed
            if keys[pg.K_SPACE]:                                                 # If it's left arrow
                self.jumping = True                                                    # then you jump
                self.vel.y = -PLAYER_JUMP                                                  #\\

    # ---> Checks for pressed keys to move left/right
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT] and not self.touching_left:                  # If it's left arrow
            if self.locked == False:
                self.facing = "left"
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT] and not self.touching_right:
            if self.locked == False:
                self.facing = "right"
            self.acc.x = PLAYER_ACC
 
    def testNextFrame(self,sprite):

        temp_pos = copy.copy(self.pos)
        temp_vel = copy.copy(self.vel)
        self.pos += temp_vel
        possibleHits = pg.sprite.collide_rect(self,sprite, False)
        self.pos = temp_pos
        return possibleHits

    def collisions_rayIntersect(self,Intersecters):
        self.jumping = True
        super().collisions_rayIntersect(Intersecters)

    # Moves the object when it's about to collide with a solid object
    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        betweenLR = hitObject.right_x() > hitPosition.x > hitObject.left_x()
        self.jumping = not (hitPosition.y == hitObject.top_y() and betweenLR)
        super().hitsSolid(hitObject, hitPosition , relativeHitPos)

    def poo(self):
        pass
