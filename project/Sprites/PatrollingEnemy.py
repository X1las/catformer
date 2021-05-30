# Imports
import pygame as pg
import math
from   CustomSprite     import CustomSprite
from   Sprites.Platform import Platform
from   Vector           import Vec as vec

# Patrolling Enemy SubClass - Inherits from CustomSprite
class PatrollingEnemy(CustomSprite):

    def __init__(self,plat : Platform, placement, maxDist, width = 23, height = 29, vel = vec(1.2,0), name = "enemy"):
        super().__init__()
        
        self.plat             = plat                        # the platform the enemy spawns on
        self.placement        = placement                   # placement relative to the spawn platform
        self.pos              = vec(self.plat.left_x() + placement, self.plat.top_y()) # position
        self.width            = width; self.height = height # size
        self.vel              = vel; self.acc = vec(0, 0)   # velocity and acceleration
        self.maxDist          = maxDist                     # maximum walking distance
        self.name             = name
        self.isEnemy          = True                        # used in CustomSprite.collisionEffect
        self.originalVel      = vel.copy()
        self.relativePosition = self.pos.copy()
        self.solidstrength    = 3
        self.initX            = self.pos.x
        self.currentplat      = None                        # The platform it stands on
        self.aboveground      = True
        self.wasunderground   = False                       # Only true when worm *just* popped up
        self.draw_layer       = 4                           # specifies when to draw
        self.damagesPlayer    = True

        self.init()     # setting mass/strength

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_enemies, game.group_movables #, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        sheet = self.game.wormSheet
        # create sub-rectangles to load from spritesheet
        walk = []
        walk.append(pg.Rect(  4, 36, 28, 28))
        walk.append(pg.Rect( 36, 36, 28, 28))
        walk.append(pg.Rect( 68, 36, 28, 28))
        walk.append(pg.Rect(100, 36, 28, 28))
        walk.append(pg.Rect(132, 36, 28, 28))
        walk.append(pg.Rect(164, 36, 28, 28))
        popup = []
        popup.append(pg.Rect(  4, 4, 28, 28))
        popup.append(pg.Rect( 36, 4, 28, 28))
        popup.append(pg.Rect( 68, 4, 28, 28))
        popup.append(pg.Rect(100, 4, 28, 28))
        popup.append(pg.Rect(132, 4, 28, 28))
        popup.append(pg.Rect(164, 4, 28, 28))
        # load images from spritesheet
        images_walk  = sheet.images_at(walk,  colorkey=(0,0,0))
        images_popup = sheet.images_at(popup, colorkey=(0,0,0))
        # scale image to correct size
        images_walk  = [pg.transform.scale(img, (self.width, self.height)) for img in images_walk]
        images_popup = [pg.transform.scale(img, (self.width, self.height)) for img in images_popup]
        images_hide  = []
        for img in reversed(images_popup):
            images_hide.append(img)
        # define and flip images        
        self.images  = {
            'walk' : {'right': images_walk,  'left': [pg.transform.flip(i, True, False) for i in images_walk ]},
            'popup': {'right': images_popup, 'left': [pg.transform.flip(i, True, False) for i in images_popup]},
            'hide' : {'right': images_hide,  'left': [pg.transform.flip(i, True, False) for i in images_hide ]}
        }
        # set initial image
        self.facing     = 'right'
        self.activity   = 'walk'
        self.imageIndex = 0
        self.image      = self.images[self.activity][self.facing][self.imageIndex]
    
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)


    # method for checking if the enemy is outside its patrolling area or at the edge of a platform
    def checkDist(self):
        if  self.right_x() >= self.currentplat.right_x() - 2:   # at right edge of platform turn around
            self.vel.x = (-1) * abs(self.originalVel.x)
            self.set_right(self.currentplat.right_x() - 3)
        elif self.left_x() <= self.currentplat.left_x() + 2:    # at left edge of platform turn around
            self.vel.x = abs(self.originalVel.x)
            self.set_left(self.currentplat.left_x() + 3)
        elif self.pos.x - self.initX >= self.maxDist:           # if further right than maximum patrolling distance, turn around
            self.vel.x = (-1) * abs(self.originalVel.x)
        elif self.pos.x - self.initX <= -1*self.maxDist:        # if further left than maximum patrolling distance, turn around
            self.vel.x = abs(self.originalVel.x)

    # method for updating the current image
    def updateAnimation(self):
        if self.activity == "hide" or self.activity == "popup":
            walkTime = 5                                                    # hide/popup image changes every 5th frame
        elif self.activity == "walk":
            walkTime = 10                                                   # walk image changes every 10th frame
        self.imageIndex += 1                                                # increment image index every update
        if self.imageIndex >= len(self.images['walk']['right'])*walkTime:   # reset image index to 0 when running out of images
            self.imageIndex = 0
        # set facing direction based on moving direction (velocity)
        if self.vel.x < 0:
            self.facing = 'left'
        elif self.vel.x > 0:
            self.facing = 'right'
        # get image based on activity and facing direction
        self.image = self.images[self.activity][self.facing][math.floor(self.imageIndex/walkTime)]
        # change back to walking animation after last frame of hide/popup animation
        if self.activity == "popup" and self.image == self.images['popup'][self.facing][-1]:
            self.activity = 'walk'
        if self.activity == "hide" and self.image == self.images['hide'][self.facing][-1]:
            self.activity = 'walk'
            self.aboveground = False

    # method for updating
    def update(self):
        try:
            self.hide()
        except Exception as e:
            print(f'touchbox: {e}')
        self.damagesPlayer = self.aboveground # only deals damage when above ground
        # stop walking when hiding/popping up
        if self.activity == "popup":
            self.vel.x = 0
        elif self.activity == "hide":
            self.vel.x = 0
        elif self.activity == "walk":
            # set moving direction (velocity) based on facing direction
            if self.facing == 'left':
                self.vel.x = abs(self.originalVel.x) * (-1)
            elif self.facing == 'right':
                self.vel.x = abs(self.originalVel.x)
        if self.aboveground:
            self.pos.y = self.plat.top_y()
        self.checkDist()                      # turn around if at the edge of platform or patrolling area
        self.updateAnimation()                # update current image
        self.updateRect()
    
    # method for hiding underground
    def hide(self):
        self.updateRect()
        if self.aboveground:
            # if above ground, get which platform it's on
            possibleplat = self.on_solid(self.game.group_platforms)
            if possibleplat != None:
                self.currentplat = possibleplat
        else: 
            # else if it is inside a plat (self.aboveground = False), move enemies rect up for collision detection
            self.rect.bottom = self.currentplat.rect.top - 1
        
        # collision detection
        collided_list = pg.sprite.spritecollide(self, self.game.group_solid, False)
        self.updateRect()
        if collided_list:
            # if enemy collides with any objects, update activity
            for collided in collided_list:
                if collided != self.currentplat:
                    if self.aboveground:
                        self.activity = "hide"
                        self.imageIndex = 0
                        self.aboveground = False
                    if self.activity == "walk":
                        self.addedVel = self.currentplat.vel
                        self.pos.y = self.currentplat.pos.y - 1
                        self.aboveground = False
                        self.wasunderground = True
        else:
            # if no collisions, walk above ground or pop up
            self.pos.y = self.currentplat.top_y()
            self.aboveground = True
            if self.wasunderground:
                self.activity = 'popup'
                self.imageIndex = 0
            self.wasunderground = False
        self.updateRect()
