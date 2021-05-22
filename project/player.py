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
    lockFacing          = False
    can_fall_and_move   = True

    width               = 47 
    height              = 42
    dist_from_right     = 0
    dslopest_from_left  = 0
    dist_from_top       = 0
    dist_from_bottom    = 0
    collides_left = False; collides_right = False

    canjump = True
    jumpcounter = 0
    liftedBefore = False

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
        self.refreshedInt_lever     = False                                                       
        self.refreshedInt_box       = False                                                  
        self.interactive_field      = None                                       
        self.refreshCount           = 0                                                        
        self.refreshCount_prev      = 0         
        self.imageIndex = 0 

        


    def startGame(self, game):    
        self.game       = game
        self.groups = game.all_sprites, game.group_pressureActivator, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        sit        = pg.Rect(  0,155,47,42)
        walk1      = pg.Rect( 48,155,47,42)
        walk2      = pg.Rect( 65,112,47,42)
        walk3      = pg.Rect( 96,155,47,42)
        walk4      = pg.Rect(113,112,47,42)
        jump       = pg.Rect(  0,198,47,42)
        interact1  = pg.Rect( 48,198,47,42)
        interact2  = pg.Rect( 96,198,47,42)
        sleep      = pg.Rect(  0,241,42,38)
        rects = [sit, walk1, walk2, walk3, walk4, jump, interact1, interact2, sleep]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        images = sheet.images_at(rects,(0,255,0))
        # scaling images to correct size
        for img in images:
            img = pg.transform.scale(img, (self.width, self.height))
        # define and flip images
        self.images = {
            'sit' :     {'right': images[0],   'left':  pg.transform.flip(images[0], True, False)},
            'walk':     {'right': images[1:5], 'left': [pg.transform.flip(i, True, False) for i in images[1:5]]},
            'jump':     {'right': images[5],   'left':  pg.transform.flip(images[5], True, False)},
            'interact': {'right': images[6:8], 'left': [pg.transform.flip(i, True, False) for i in images[6:8]]},
            'sleep':    images[8]
        }
        
        # set starting image
        self.facing = 'right'
        self.image = self.images['sit'][self.facing]

        self.rect = self.image.get_rect()
        self.rect.midbottom         = (self.spawn.x,self.spawn.y)

    def respawn(self):
        self.pos        = self.spawn

    def setSpawn(self,spawn):
        self.spawn      = spawn

    def takeDamage(self):
        self.lives -= 1
        self.respawn()
        self.game.playerTookDamage()

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
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images['walk']['right'])*15:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        self.image = self.images['sit'][self.facing]
        if not self.inAir:
            self.jumpcounter += 1
        else:
            self.jumpcounter = 0
            self.image = self.images['jump'][self.facing]
        if self.jumpcounter > 8:
            self.canjump = True
        else:
            self.canjump = False
        self.move()
        self.determineGravity()
        self.applyPhysics() 
        #self.checkDamage()
        self.touchPickUp()
        self.solidCollisions()
        self.liftArm()
        self.rect.midbottom = self.pos.rounded().asTuple()

    def updatePos(self):
        self.pos += self.vel +  self.acc * 0.5
        self.collides_left = False; self.collides_right = False

    def determineGravity(self):
        if self.on_solid(self.game.group_solid):
            self.inAir = False
            self.gravity = 0
        else:
            self.inAir = True
            self.gravity = GRAVITY

    def posCorrection(self):
        self.solidCollisions()
        self.rect.midbottom = self.pos.rounded().asTuple()


    def outOfBounds(self):
          if (self.pos.y > self.game.boundary):
            self.takeDamage()


    def checkDamage(self):
        self.inbetweenSolids()
        self.outOfBounds()
        self.touchEnemy()

    def touchEnemy(self):
        damager = self.game.group_damager
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect = self.rect.inflate(4,4)
        collided = pg.sprite.spritecollide(self, damager, False)
        self.rect = self.rect.inflate(-4,-4)
        if collided: 
            for collided_obj in collided:
                if collided_obj.active:
                    self.takeDamage()         
        self.rect.midbottom = self.pos.rounded().asTuple()


    def interactUpdate(self):
        self.image = self.images['interact'][self.facing][math.floor(self.imageIndex/30)]
        self.refreshedInt_lever = self.refreshCount > self.refreshCount_prev      #
        self.refreshedInt_box   = self.refreshCount >= self.refreshCount_prev       #
        self.interactive_field.leverPull()
        self.interactive_field.pickupSprite()
        self.interactive_field.knockOver()

        self.refreshCount_prev = self.refreshCount


    def liftArm(self):
        self.lockFacing = False
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.isInteracting = True
            if not self.liftedBefore:
                self.interactive_field = Interactive(self.game,self, self.facing)
                self.liftedBefore = True
                self.intJustCreated = True
                self.refreshCount += 1
            self.interactUpdate()

        else:
            self.isInteracting = False
            try:
                self.interactive_field.kill()
                self.liftedBefore = False
            except:
                pass
        self.intJustCreated = False    
        
    def update2(self):
        self.checkDamage()

    # ---> Checks for pressed keys to move left/right and jump
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT]:                                             # If it's left arrow
            if not self.lockFacing:
                self.facing = "left"
            if not self.inAir and not self.isInteracting:
                self.image = self.images['walk'][self.facing][math.floor(self.imageIndex/15)]
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT]:
            if not self.lockFacing:
                self.facing = "right"
            self.acc.x = PLAYER_ACC                                          
            if not self.inAir and not self.isInteracting:
                self.image = self.images['walk'][self.facing][math.floor(self.imageIndex/15)]
        if keys[pg.K_SPACE] and not self.inAir and self.canjump:                                                 
            self.inAir = True                                                    
            self.vel.y = -PLAYER_JUMP


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


    def inbetweenSolids(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        inflation = 2
        self.rect = self.rect.inflate(inflation,inflation)
        collideds = pg.sprite.spritecollide(self, self.game.group_solid, False)
        result = False
        movingVER = False
        movingHOR = False
        collides_top = False; collides_bot = False
        collides_left = False; collides_right = False
        if collideds:
            for collided in collideds:
                if collided != self:
                    coll_side = self.determineSide(collided)
                    if coll_side == "left": # left side of collidedd obj
                        if collided.vel.x + collided.addedVel.x < 0:
                            movingHOR = True
                        if self.collides_left and movingHOR:
                            self.takeDamage()
                            result = True
                        self.collides_right = True
                    if coll_side == "right":
                        if collided.vel.x + collided.addedVel.x > 0:
                            movingHOR = True
                        if self.collides_right and movingHOR:
                            self.takeDamage()
                            #self.vel.x *= 0
                        self.collides_left = True
                    if coll_side == "top": # left side of collidedd obj
                        if collided.vel.y < 0:
                            movingVER = True
                        if collides_top and movingVER:
                            self.takeDamage()
                            result = True
                        collides_bot = True
                    if coll_side == "bot":
                        if collided.vel.y > 0:
                            movingVER = True
                        if collides_bot and movingVER:
                            self.takeDamage()
                            result = True
                        collides_top = True

        self.rect = self.rect.inflate(-inflation,-inflation)
          
        return result           


# Interactive Field SubClass - Inherits from CustomSprite
class Interactive(CustomSprite):
    def __init__(self, game,  player, facing):
        self.game = game
        self.name = "interactive"
        # anchor depends on which way player faces
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.group_interactiveFields)  
        self._layer = 2
        self.update_order = 3
        self.player = player
        width = 30#self.player.width/2 + 5
        height = self.player.height     
        self.facing = facing
        
        # create surface with correct size
        self.image = pg.Surface((width,height),pg.SRCALPHA)
        # load image from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        img = sheet.image_at((144,198,30,42),(0,255,0))
        image = pg.transform.scale(img, (int(width), int(height)))
        pg.Surface.fill(self.image, (0,255,0))
        
        self.images = {'right': image, 'left': pg.transform.flip(image, True, False)}
        self.image = self.images[self.facing]

        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.width = image.get_width()/2; self.height = image.get_height()/2
        
        self.colliding = False
        self.faceinput = self.player.facing
        self.relativePosition = self.pos.copy()
        self.vel = self.player.vel
        if self.facing == "left":
            self.rect.bottomright = (player.pos.x,player.pos.y)   
        else: 
            self.rect.bottomleft = (player.pos.x,player.pos.y)   

        

    def intUpdate(self, facing, pos):
        if facing == "left":
            print(f'left')
            if pos == "global":
                self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
            else:
                self.rect.bottomright = self.player.relativePosition.rounded().asTuple()
        elif facing == "right": 
            print(f'right')
            if pos == "global":
                self.rect.bottomleft = (self.player.pos.x,self.player.pos.y)   
            else: 
                self.rect.bottomleft = self.player.relativePosition.rounded().asTuple()
    
    def update(self):
        self.image = self.images[self.player.facing]
        if self.player.facing == "left":
            self.pos = Vec(self.player.left_x(), self.player.mid().y)
        if self.player.facing == "right":
            self.pos = Vec(self.player.right_x(), self.player.mid().y)
        self.vel = self.player.vel
        self.acc = self.player.acc
        self.updateRect()
    
    def updateRect(self):
        self.image = self.images[self.player.facing]
        self.intUpdate(self.player.facing, "rel")
        #self.intUpdate(self.faceinput, "rel")
    
    def resetRects(self):
        self.colliding = False
        self.intUpdate(self.player.facing, "global")

    def knockOver(self):
        collided_list = pg.sprite.spritecollide(self, self.game.group_mugs, False)
        if collided_list: 
            for collided in collided_list:
                if self.player.intJustCreated and not collided.broken:
                    collided.fall = True
                    #collided.gravity = PLAYER_GRAV
                    #collided.fall = True

    def pickupSprite(self):
        justPickedUp = self.player.intJustCreated
        self.colliding = False
        canpickup = True
        collided_list = pg.sprite.spritecollide(self,  self.game.group_boxes, False)
        if collided_list: 
            if self.player.refreshedInt_box:
                for collided in collided_list:
                    collided.rect.midbottom = collided.pos.realRound().asTuple()
                
                    collided.rect.y -= 2
                    # Kind of bad solution. removed from the group, because otherwise it detects collision with itself
                    testcol = pg.sprite.spritecollide(collided, self.game.group_solid, False)
                    collided.rect.midbottom = collided.pos.realRound().asTuple()
                    for i in testcol:
                        if i != collided:
                            side = i.determineSide(collided)
                            if side == "top":
                                canpickup = False

                    if canpickup:
                
                        self.colliding = True
                        if justPickedUp:
                            collided.pickupStarted = True
                        collided.has_collided = True
                        #collided.beingheld = True
                        self.vel = self.player.vel.copy()
                        self.acc = self.player.acc.copy()
                        collided.liftedBy(self)
                        self.player.lockFacing = True
            else:
                self.colliding = False # remove?

    def leverPull(self):
        collided_list = pg.sprite.spritecollide(self, self.game.group_levers, False)
        if collided_list: 
            for collided in collided_list:
                if self.player.refreshedInt_lever:
                    if not collided.activated:
                        collided.activate()
                    else:
                        collided.deactivate()
                collided.prevActivated = True
                return collided # del?