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
        self.groups = game.all_sprites,  game.players, game.weight_act
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game           = game; self.name = name; self._layer = 1
        self.facing = None
        self.solid          = True
        self.width          = 30; self.height = 40
        self.image          =  pg.Surface((self.width,self.height)); self.image.fill((255,255,0)); self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.dist_from_right = 0; self.dslopest_from_left = 0; self.dist_from_top = 0; self.dist_from_bottom = 0
        self.on_collided_surface = False; self.stop_falling = False
        #self.interactRect   = self.interact()
        self.locked = False
        
        self.relativePosition = self.pos.copy()
        self.lives = 9
        self.catnip_level = 0

    def takeDamage(self):
        self.lives -= 1
        return self.lives

    def heal(self):
        self.lives += 1
        return self.lives

    def addCatnip(self):
        self.catnip_level += 1
        return self.catnip_level


    def initKeys(self,jump, left, right, crouch):
        self.jump_key = jump

    # --> The different things that updates the position of the player
    def update(self):                                                         # Updating pos, vel and acc.
        self.move()
        self.applyPhysics(self.game.rayIntersecters) 
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()

    # ---> Checks for pressed keys to move left/right and jump
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT]:                                             # If it's left arrow
            if self.locked == False:
                self.facing = "left"
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT]:
            if self.locked == False:
                self.facing = "right"
            self.acc.x = PLAYER_ACC                                          
        if keys[pg.K_SPACE] and not self.inAir:                                                 
            self.inAir = True                                                    
            self.vel.y = -PLAYER_JUMP 

    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        super().hitsSolid(hitObject, hitPosition , relativeHitPos)
        print(hitObject,hitPosition)

    """def testNextFrame(self,sprite):

        temp_pos = copy.copy(self.pos)
        temp_vel = copy.copy(self.vel)
        self.pos += temp_vel
        possibleHits = pg.sprite.collide_rect(self,sprite, False)
        self.pos = temp_pos
        return possibleHits
    """

