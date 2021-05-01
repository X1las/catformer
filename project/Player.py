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
    catnip_level        = PLAYER_CATNIP
    lives               = PLAYER_LIVES

    isPlayer            = True
    facing              = None
    solid               = True
    on_collided_surface = False 
    stop_falling        = False
    locked              = False
    can_fall_and_move   = True

    width               = 30 
    height              = 40
    vel                 = vec(0, 0)   
    acc                 = vec(0, 0)
    dist_from_right     = 0
    dslopest_from_left  = 0
    dist_from_top       = 0
    dist_from_bottom    = 0
    name = "player"

    def __init__(self, game, spawn):
        
        self.game       = game
        self._layer     = 1
        self.spawn      = spawn
        self.pos        = spawn

        self.groups = game.all_sprites, game.group_pressureActivator
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image                  =  pg.Surface((self.width,self.height)); self.image.fill((255,255,0)); self.rect = self.image.get_rect()
        self.rect.midbottom         = (spawn.x,spawn.y)

    def respawn(self):
        self.pos        = self.spawn

    def setSpawn(self,spawn):
        self.spawn      = spawn

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
        self.applyPhysics(self.game.group_solid) 
        self.rect.midbottom = self.pos.rounded().asTuple()

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

    def updatePos(self, Intersecters):
        self.pos += self.vel +  self.acc * 0.5
        
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)
        if self.can_fall_and_move:
            self.pygamecoll(Intersecters)

    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        super().hitsSolid(hitObject, hitPosition , relativeHitPos)