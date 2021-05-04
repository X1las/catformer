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
    


    def __init__(self, game, spawn, name=None):
        
        self.game       = game
        self._layer     = 2
        self.spawn      = spawn
        self.pos        = spawn
        self.update_order        = 2
        self.name = name

        self.groups = game.all_sprites, game.group_pressureActivator
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image                  =  pg.Surface((self.width,self.height)); self.image.fill((255,255,0)); self.rect = self.image.get_rect()
        self.rect.midbottom         = (spawn.x,spawn.y)

        self.prevpos = vec() # delete
        self.prevvel = vec()
        self.prevrelpos = vec()
        self.prevrelvel = vec()

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
        self.pygamecoll(self.game.group_solid)
        self.vel += self.addedVel

        self.rect.midbottom = self.pos.realRound().asTuple()

    # ---> Checks for pressed keys to move left/right and jump
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT]:                                             # If it's left arrow
            if self.locked == False:
                self.facing = "left"
                #print("WALKING LEFT")
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT]:
            if self.locked == False:
                self.facing = "right"
                #print("WALKING RIGHT")

            self.acc.x = PLAYER_ACC                                          
        if keys[pg.K_SPACE] and not self.inAir:                                                 
            self.inAir = True                                                    
            self.vel.y = -PLAYER_JUMP 

    def resetRects(self):
        super().resetRects()


    def updatePos(self, Intersecters):
        #tempvel = self.vel.copy()
        #self.vel = self.new_vel
        #if self.vel.x < 0.001:
         #   self.vel.x = 0

        self.pos += self.vel +  self.acc * 0.5
        #self.vel -= self.addedVel
        #if self.vel.x < 0.001:
         #   self.vel.x = 0
        #self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)
        #self.vel = tempvel
        #self.new_vel = self.vel.copy()
       # print((self.pos - self.prevpos + self.prevvel).x)
        #print((self.relativePosition - self.prevrelpos + self.prevrelvel).x)
        
        #print(f'player pos diff: {self.pos - self.prevpos + self.prevvel}')
        #print(f'player pos: {self.pos}')
        self.prevrelvel = self.relativePosition - self.prevrelpos
        self.prevrelpos = self.relativePosition.copy()

        self.prevvel = self.pos - self.prevpos
        self.prevpos = self.pos.copy()



    def posCorrection(self):
        if self.can_fall_and_move:
            self.pygamecoll(self.game.group_solid)
        #self.count -= 1
        #if self.count <= 0:
         #   self.solidstrength = 0
        

    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        super().hitsSolid(hitObject, hitPosition , relativeHitPos)


# Interactive Field SubClass - Inherits from CustomSprite
class Interactive(CustomSprite):
    def __init__(self, game,  player, facing):

        # anchor depends on which way player faces
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.group_interactiveFields)  
        self._layer = 2
        self.update_order = 3
        self.player = player
        width = self.player.width/2 + 30
        height = self.player.height       
        self.facing = facing
        self.image = pg.Surface((width,height)); 
        self.image.fill((0,200,0)) 
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.colliding = False
        self.faceinput = self.player.facing
        self.relativePosition = self.pos.copy()
        self.vel = self.player.vel
        if self.facing == "left":
            self.rect.bottomright = (player.pos.x,player.pos.y)   
        else: 
            self.rect.bottomleft = (player.pos.x,player.pos.y)   

        

    def intUpdate(self, facing, pos):

        #bob = self.rect.bottomleft
        #bob = self.rect.bottomright

        if facing == "left":
            if pos == "global":
                #bob = (self.player.pos.x,self.player.pos.y)   

                self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
            else:
                #bob = self.player.relativePosition.realRound().asTuple()

                self.rect.bottomright = self.player.relativePosition.realRound().asTuple()
        else: 
            if pos == "global":
                self.rect.bottomleft = (self.player.pos.x,self.player.pos.y)   
            else: 
                self.rect.bottomleft = self.player.relativePosition.realRound().asTuple()
    
    def update(self):
        """
        if self.player.facing == "left":
            self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
        else: 
            self.rect.bottomleft = (self.player.pos.x,self.player.pos.y) 
        """
        self.pos = self.player.pos
        self.vel = self.player.vel
        self.acc = self.player.acc
    
    def updateRect(self):
        if not self.colliding:
            self.faceinput = self.player.facing
        else: 
            self.player.solidstrength = 6
            self.player.count = 10
            
        self.colliding = False
        self.intUpdate(self.faceinput, "rel")
    
    def resetRects(self):
        self.intUpdate(self.faceinput, "global")

