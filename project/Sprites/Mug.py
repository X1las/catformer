# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *
from Sprites.Platform import Platform

# Case SubClass - Inherits from CustomSprite
class Mug(CustomSprite):
    def __init__(self, plat : Platform, placement, width = 29, height = 26, name = "mug", spawnItem = None):
        self.spawnPlat = plat
        #self.pos = vec()
        self.spawnItem = spawnItem
        self.width  = width; self.height = height
        self.pos = Vec(self.spawnPlat.left_x() + placement, self.spawnPlat.top_y()).rounded() 
        
        self.placement = placement
        self.name = name
        #self.breakable = True
        
        self.broken = False
        self.update_order = 11
        self.fall = False
        self.gravity = GRAVITY
        self.relativePosition = self.pos.copy()
        self.fell_fast_enough = False
        self.init()

        ''' probably not needed'''

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''

        ''' should be revisited'''

        ''' in use'''





    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_mugs, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create sub-rectangles to load from water spritesheet
        whole  = pg.Rect(  0,0,29,26)
        broken = pg.Rect( 30,0,29,26)
        bigMug = pg.Rect(104,0,77,72)
        rects = [whole, broken, bigMug]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     
        self.image_whole = self.images[0]
        self.image_broken = self.images[1]
        image_big = self.images[2]
        
        if self.game.level.name == 'level4':
            self.image = image_big
            self.gravity = GRAVITY/2
        else:
            self.image = self.image_whole
        
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)


    def update(self):
        # Check whether the mug has even fallen yet
        if not self.broken:
            if self.vel.y > 1:
                self.fell_fast_enough = True
            self.touchplat(self.game.group_solid)
        
        self.vel.x = self.addedVel.x
        if self.fall == True:
            self.applyGrav()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def breaks(self):
        if not self.game.level.name == 'level4':
            self.image.blit(self.images[1],(0,0))
        self.pos = self.pos.rounded()
        self.spawnItem.pos = self.pos.copy()
        self.spawnItem.startGame(self.game)
        self.broken = True

    # Applies basic gravity
    def applyGrav(self):
        self.acc.y += self.gravity                  # Gravity
        self.vel.y += self.acc.y                              # equations of motion

    def updatePos(self):
        if self.broken:
        #  self.solidCollisions(self.game.group_solid)
            standingon = self.on_solid(self.game.group_platforms)
            if standingon:
                self.pos.y = standingon.top_y()
                self.vel.y = self.addedVel.y; self.acc.y = 0
                self.vel.x = self.addedVel.x
        self.vel.x = self.addedVel.x
        #self.vel.x = self.addedVel.x #here?
        super().updatePos()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def collisionMultipleGroups(self,*groups):
        collidedObjects = []
        for group in groups:
            collisionsInGroup = pg.sprite.spritecollide(self, group, False)
            for collision in collisionsInGroup:
                collidedObjects.append(collision)
        return collidedObjects

    #def posCorrection(self):
       # self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # When it thouches a platform or other solid
    def touchplat(self, group):
        self.rect.midbottom = self.pos.realRound().asTuple()
        self.rect.y +=self.r(self.vel.y + 4) 
        collided_objects = self.collisionMultipleGroups(group, self.game.group_enemies)
        if collided_objects:
            for collided in collided_objects:
                if collided != self.spawnPlat and self.fell_fast_enough and not self.broken:
                    self.breaks()
