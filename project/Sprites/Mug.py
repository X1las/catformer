# Imports
# External Imports:
import pygame as pg
from Sprites.Platform import Platform

# Project Imports:
from CustomSprite import CustomSprite
from settings import *

# Mug Class - Inherits from CustomSprite class
class Mug(CustomSprite):

    # Initializer
    def __init__(self, plat : Platform, placement, width = 29, height = 26, name = "mug", spawnItem = None, final = False):
        
        super().__init__()
        self.spawnPlat        = plat               # the platform tht the mug spawns on
        self.standingon       = plat
        self.spawnItem        = spawnItem          # what the mug should spwan when broken
        self.width = width; self.height = height   # size
        self.pos = Vec(self.spawnPlat.left_x() + placement, self.spawnPlat.top_y()).rounded() # position
        self.final            = final
        self.placement        = placement          # placement relative to spawn platform
        self.name             = name
        self.draw_layer       = 7                  # layer for drawing
        self._layer           = 9
        self.broken           = False              # initially mugs are not broken
        self.fall             = False              # initially mugs have not fallen
        self.fell_fast_enough = False
        self.gravity          = GRAVITY
        self.relativePosition = self.pos.copy()
        self.init()                                # setting weight/strength

    # Includes the Game class in the object after it has been loaded onto a level
    def startGame(self, game):
        # adding to sprite groups
        self.game   = game
        self.groups = game.all_sprites, game.group_mugs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create sub-rectangles to load from spritesheet
        whole         = pg.Rect(  0,0,29,26)
        broken        = pg.Rect( 30,0,29,26)
        bigMug        = pg.Rect(104,0,77,72)
        bigMug_broken = pg.Rect(182,0,77,72)
        rects = [whole, broken, bigMug, bigMug_broken]
        # load images from spritesheet
        sheet       = self.game.spriteSheet
        self.images = sheet.images_at(rects, (0,255,0))
        # transforms images to size of sprite
        for img in self.images:
            img = pg.transform.scale(img, (self.width, self.height))
        # set special images for final level
        if self.final:
            self.image_whole  = self.images[2]
            self.image_broken = self.images[3]
            self.gravity      = GRAVITY/6
        else:
            self.image_whole  = self.images[0]
            self.image_broken = self.images[1]
        # set initial image
        self.image = self.image_whole

        self.rect           = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    # Object Update
    def update(self):
        # Check whether the mug has fallen yet/is broken
        if not self.broken:                                                 
            if self.vel.y > 1:                                              
                self.fell_fast_enough = True
            self.touchplat(self.game.group_solid)
        self.vel.x = self.addedVel.x
        # only apply gravity if knocked over, i.e. falling
        if self.fall:
            self.applyGrav()
        self.rect.midbottom = self.pos.rounded().asTuple()

    # Method that breaks the mug
    def breaks(self, collidedwith):
        self.image = self.image_broken      # switch to image of broken mug
        self.pos = self.pos.rounded()
        # potentially spawn items
        if self.spawnItem != None:
            self.spawnItem.pos = self.pos.copy()
            self.spawnItem.startGame(self.game)
        elif self.final:
            # in final level, end game when mug breaks
            self.game.finished = True
        # set mug to top of the lower platform
        if collidedwith.isPlatform:
            self.pos.y = collidedwith.top_y()
            self.vel.y = 0
        # update broken and fall trackers
        self.broken = True
        self.fall   = False

    # Applies basic gravity
    def applyGrav(self):
        self.acc.y += self.gravity                                          # Gravity
        self.vel.y += self.acc.y                                            # Equations of motion


    # Updates position of the object
    def updatePos(self):
        self.standingon = self.on_solid(self.game.group_platforms)  # get current platform
        if self.standingon and not self.fall:
            self.pos.y = self.standingon.top_y()                    # update position
            if self.broken:
                self.vel.y = self.addedVel.y; self.acc.y = 0        # update y-velocity and acceleration
        self.vel.x = self.addedVel.x
        super().updatePos()
        self.rect.midbottom = self.pos.rounded().asTuple()


    # Checks for multiple collisions between the objects
    def collisionMultipleGroups(self,*groups):
        collidedObjects = []
        for group in groups:
            collisionsInGroup = pg.sprite.spritecollide(self, group, False)
            for collision in collisionsInGroup:
                collidedObjects.append(collision)
        return collidedObjects


    # When it touches a platform or other solids
    def touchplat(self, group):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.y        += self.r(self.relativeVel().y) 
        collided_objects    = self.collisionMultipleGroups(group, self.game.group_enemies)
        if collided_objects:
            for collided in collided_objects:
                if collided != self.spawnPlat and self.fell_fast_enough:
                    # only break if fell fast enough on another solid/enemy
                    self.breaks(collided)
                    return collided
        self.rect.midbottom = self.pos.rounded().asTuple()
