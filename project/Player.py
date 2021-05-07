# Description:

# Imports
import pygame as pg
import copy

from settings import *

from Vector import Vec
from CustomSprite import CustomSprite
from random import choice, randrange, uniform
import Spritesheet as ss

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

    width               = 47 
    height              = 46
    vel                 = vec(0, 0)   
    acc                 = vec(0, 0)
    dist_from_right     = 0
    dslopest_from_left  = 0
    dist_from_top       = 0
    dist_from_bottom    = 0
    collides_left = False; collides_right = False
    
    name = "player"
    


    def __init__(self, spawn, name="player"):
        
        self._layer     = 2
        self.spawn      = spawn
        self.pos        = spawn
        self.update_order        = 2
        self.name = name



        self.prevpos = vec() # delete
        self.prevvel = vec()
        self.prevrelpos = vec()
        self.prevrelvel = vec()
        self.init()
        self.ignoredSolids = []

    def startGame(self, game):    
        self.game       = game
        self.groups = game.all_sprites, game.group_pressureActivator
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        sit  = pg.Rect(0,151,38,46)
        walk = pg.Rect(40,151,47,46)
        #interact = pg.Rect(32,117,16,16)
        #jump = 
        rects = [sit, walk]#, interact]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        images = sheet.images_at(rects,(0,255,0))
        self.image_sit    = images[0]
        self.image_walk_r = images[1]
        self.image_walk_l = pg.transform.flip (self.image_walk_r, True, False)
        self.image_sit    = pg.transform.scale(self.image_sit,    (self.width, self.height))
        self.image_walk_r = pg.transform.scale(self.image_walk_r, (self.width, self.height))
        self.image_walk_l = pg.transform.scale(self.image_walk_l, (self.width, self.height))
        self.image = self.image_sit

        self.rect = self.image.get_rect()
        self.rect.midbottom         = (self.spawn.x,self.spawn.y)

    def respawn(self):
        self.pos        = self.spawn

    def setSpawn(self,spawn):
        self.spawn      = spawn

    def takeDamage(self):
        self.lives -= 1
        self.respawn()
        self.game.resetCamera()
        #self.game.damageScreen()
        self.game.isDamaged = True
        #self.game.paused = True
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
        #self.massHOR = self.ori_massHOR
        self.move()
        self.applyPhysics(self.game.group_solid) 
        self.vel += self.addedVel
        # there for a picked up box to register that the player stands still
        self.pygamecoll(self.game.group_solid, ignoredSol = self.ignoredSolids)
        self.rect.midbottom = self.pos.realRound().asTuple()
        #self.pygamecoll(self.game.group_solid)

    # ---> Checks for pressed keys to move left/right and jump
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT]:                                             # If it's left arrow
            if self.locked == False:
                self.facing = "left"
                self.image = self.image_walk_l
                #print("WALKING LEFT")
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT]:
            if self.locked == False:
                self.facing = "right"
                self.image = self.image_walk_r
                #print("WALKING RIGHT")

            self.acc.x = PLAYER_ACC                                          
        if keys[pg.K_SPACE] and not self.inAir:                                                 
            self.inAir = True                                                    
            self.vel.y = -PLAYER_JUMP 

    def resetRects(self):
        super().resetRects()

    def inbetweenSolids(self):
        inflation = 0
        self.rect = self.rect.inflate(inflation,inflation)
        self.rect.midbottom = self.pos.realRound().asTuple()
        collideds = pg.sprite.spritecollide(self, self.game.group_solid, False)
        result = False
        moving = False
        if collideds:
            for collided in collideds:
                if collided != self and collided.name != "p_floor":
                    if self.solidstrength < collided.solidstrength:
                        self.solidstrength = collided.solidstrength -1
                        count = 2
                    coll_side = self.determineSide(collided)
                    if coll_side == "left": # left side of collidedd obj
                        if self.collides_left:
                            #print(f'{collided.name} vel: {collided.vel}')
                            if round(collided.vel.x) != 0:
                                moving = True
                            if moving:
                                self.takeDamage()
                            result = True
                        self.collides_right = True
                    if coll_side == "right":
                        if self.collides_right:
                            if round(collided.vel.x) != 0:
                                moving = True
                            if moving:
                                self.takeDamage()
                            result = True
                            self.vel.x *= 0
                        self.collides_left = True
        self.rect = self.rect.inflate(-inflation,-inflation)
          
        return result           
    def updatePos(self, Intersecters):
        #tempvel = self.vel.copy()
        #self.vel = self.new_vel
        #if self.vel.x < 0.001:
         #   self.vel.x = 0

        #self.vel += self.addedVel
        self.pos += self.vel +  self.acc * 0.5
        self.inbetweenSolids()
        self.collides_left = False; self.collides_right = False
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
        #pass
        #print(f'player mass: {self.massHOR}')
        if self.can_fall_and_move:
            self.pygamecoll(self.game.group_solid, ignoredSol= self.ignoredSolids)
        self.ignoredSolids = []
        #self.count -= 1
        #if self.count <= 0:
         #   self.solidstrength = 0
        

    def hitsSolid(self, hitObject, hitPosition , relativeHitPos):
        super().hitsSolid(hitObject, hitPosition , relativeHitPos)


# Interactive Field SubClass - Inherits from CustomSprite
class Interactive(CustomSprite):
    def __init__(self, game,  player, facing):
        self.game = game
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
        self.updateRect()
    
    def updateRect(self):
        if not self.colliding:
            self.faceinput = self.player.facing
        #else: 
         #   self.player.solidstrength = 3
          #  self.player.count = 10
            
        self.intUpdate(self.faceinput, "rel")
    
    def resetRects(self):
        self.colliding = False
        self.intUpdate(self.faceinput, "global")

