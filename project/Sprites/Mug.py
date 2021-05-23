# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *
from Sprites.Platform import Platform

# Case SubClass - Inherits from CustomSprite
class Mug(CustomSprite):
    def __init__(self, plat : Platform, placement, width = 29, height = 26, name = "mug", spawnItem = None, final = False):
        self.spawnPlat = plat
        self.standingon = plat
        self.spawnItem = spawnItem
        self.width  = width; self.height = height
        self.pos = Vec(self.spawnPlat.left_x() + placement, self.spawnPlat.top_y()).rounded() 
        self.final = final
        self.placement = placement
        self.name = name
        self._layer =9
        
        self.broken = False
        self.update_order = 11
        self.fall = False
        self.gravity = GRAVITY
        self.relativePosition = self.pos.copy()
        self.fell_fast_enough = False
        self.init()





    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_mugs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create sub-rectangles to load from water spritesheet
        whole  = pg.Rect(  0,0,29,26)
        broken = pg.Rect( 30,0,29,26)
        bigMug = pg.Rect(104,0,77,72)
        bigMug_broken = pg.Rect(182,0,77,72)
        rects = [whole, broken, bigMug, bigMug_broken]
        # load images from spritesheet
        sheet = self.game.spriteSheet
        self.images = sheet.images_at(rects, (0,255,0))
        # transform aimages to size of sprite
        for img in self.images:
            img = pg.transform.scale(img, (self.width, self.height))
        # set special images for final level
        if self.final:
            self.image_whole = self.images[2]
            self.image_broken = self.images[3]
            self.gravity = GRAVITY/6
        else:
            self.image_whole = self.images[0]
            self.image_broken = self.images[1]
        
        self.image = self.image_whole
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)


    def update(self):
        # Check whether the mug has even fallen yet
        if not self.broken:
            if self.vel.y > 1:
                self.fell_fast_enough = True
            self.touchplat(self.game.group_solid)
        
        self.vel.x = self.addedVel.x
        if self.fall:
            self.applyGrav()
        self.rect.midbottom = self.pos.realRound().asTuple()

    def breaks(self):
        
        self.image = self.image_broken
        if self.standingon:
            self.pos.y = self.standingon.top_y()
        self.pos = self.pos.rounded()
        if self.spawnItem != None:
            self.spawnItem.pos = self.pos.copy()
            self.spawnItem.startGame(self.game)
        if self.final:
            self.game.finished = True
        self.broken = True
        self.fall = False

    # Applies basic gravity
    def applyGrav(self):
        self.acc.y += self.gravity                  # Gravity
        self.vel.y += self.acc.y                              # equations of motion

    def updatePos(self):
        self.standingon = self.on_solid(self.game.group_platforms)
        if self.standingon and not self.fall:
            if self.broken:
                self.pos.y = self.standingon.top_y()
                self.vel.y = self.addedVel.y; self.acc.y = 0
                #self.vel.x = self.addedVel.x
            self.pos.y = self.standingon.top_y()
        self.vel.x = self.addedVel.x
        
        #self.vel.x = self.addedVel.x #here?
        super().updatePos()
        self.rect.midbottom = self.pos.rounded().asTuple()

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
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.y +=self.r(self.vel.y + 4) 
        collided_objects = self.collisionMultipleGroups(group, self.game.group_enemies)
        if collided_objects:
            for collided in collided_objects:
                if collided != self.spawnPlat and self.fell_fast_enough and not self.broken:
                    self.breaks()
        self.rect.midbottom = self.pos.rounded().asTuple()
