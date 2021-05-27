# Imports
import math
import pygame as pg
from   CustomSprite import CustomSprite
from   Vector       import Vec as vec

# Platform SubClass - Inherits from CustomSprite
class Platform(CustomSprite):

    isPlatform = True
    game = None

    # Initializer
    def __init__(self, x, y, width, height, name = "plat", vel = vec(), floorplat = False, maxDist = None, leftMaxDist = 1000, rightMaxDist = 1000, upMaxDist = 2, downMaxDist = 2):
        super().__init__()
        self.height = height; self.width = width; self.name = name  # size, name
        self.pos = vec(x,y); self.vel = vel                         # position, velocity
        self.originalVel       = self.vel.copy()                    # original velocity
        self.isPlatform        = True
        self.floorplat         = floorplat                          # special properties if platform is the floor
        self.relativePosition  = self.pos.copy()
        self._layer            = 3                                               
        self.draw_layer        = 8                                  # layer for drawing                                        
        self.initX, self.initY = x, y
        self.x,     self.y     = x, y

        # define maximum moving distance in each direction
        if maxDist == None:
            # default values
            self.leftMaxDist  = leftMaxDist
            self.rightMaxDist = rightMaxDist
            self.downMaxDist  = downMaxDist
            self.upMaxDist    = upMaxDist
        else:
            # if given as input
            self.leftMaxDist  = maxDist
            self.rightMaxDist = maxDist
            self.downMaxDist  = maxDist
            self.upMaxDist    = maxDist

        self.solidstrength = 30         # high strength, so it cannot be moved by 'weaker' objects
        if floorplat:
            self.solidstrength = 50     # higher strength if floor, so other platforms cannot move it
        self.init()                     # set mass/strength

    # Method for setting game specific attributes
    def startGame(self, game):
        # adding to sprite groups
        self.game = game
        self.groups = game.all_sprites, game.group_platforms, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get sprite sheet
        sheet = self.game.platformSheet
        # get individual sprites
        end_left   = sheet.image_at((47 ,51, 34,26), colorkey=(0,0,0))
        end_right  = sheet.image_at((175,51, 34,26), colorkey=(0,0,0))
        mid        = sheet.image_at((303,51, 35,26), colorkey=(0,0,0))
        brownPiece = sheet.image_at((303,176,34,32), colorkey=(0,0,0))
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        fill = 0
        # blit left end
        self.image.blit(end_left,(0,0))
        fill += end_left.get_height()
        # blit middle parts depending on platform width
        numOfMidParts = math.ceil(self.width/mid.get_width()-2)
        for i in range(numOfMidParts):
            self.image.blit(mid, ((i+1)*end_left.get_width(),0))
        # blit right end
        self.image.blit(end_right,(self.width-end_right.get_width(),0))
        # blit bottom layers until fully filled
        numOfBrownParts_h = math.ceil(self.width/mid.get_width())+1
        while fill < self.height:
            for i in range(numOfBrownParts_h):
                self.image.blit(brownPiece, (i*end_left.get_width(),fill))
            fill += brownPiece.get_height()
        
        # Making and getting dimensions of the sprite
        self.rect = self.image.get_rect()            
        self.rect.midbottom = (self.pos.x,self.pos.y)
        self.isPlatform = True


    # Checking if the (moving) platform is outside it's moving area
    def checkDist(self):
        if  self.pos.x -  self.initX >= self.rightMaxDist and self.vel.x > 0:
            # if further right than maximum moving distance, move in opposite direction
            self.vel.x =  -1 * abs(self.originalVel.x)
        elif self.pos.x - self.initX <= -1*self.leftMaxDist and self.vel.x < 0:
            # if further left than maximum moving distance, move in opposite direction
            self.vel.x =  abs(self.originalVel.x)
        elif self.pos.y - self.initY <= -1* abs(self.upMaxDist) and self.vel.y < 0:
            # if further up than maximum moving distance, move in opposite direction
            self.vel.y =  abs(self.originalVel.y)
        elif self.pos.y - self.initY >= self.downMaxDist and self.vel.y > 0:
            # if further down than maximum moving distance, move in opposite direction
            self.vel.y =  -1* abs(self.originalVel.y)


    def update(self):
        if self.vel.x != 0:
            self.massHOR = 29.5
        elif self.vel.y != 0:
            self.massVER = 29.5
        self.checkDist()
        self.rect.midbottom = self.pos.realRound().asTuple()

    # Overwriting inherited method
    def updateAddedVel(self):
        pass

    # Method for updating position
    def updatePos(self):
        self.checkDist()
        self.solidCollisions()
        super().updatePos()

    # Method for checking for collisions with other platforms
    def solidCollisions(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.x        += self.r(self.vel.x)
        self.rect.y        += self.r(self.vel.y)
        collided_objects = pg.sprite.spritecollide(self, self.game.group_platforms, False)
        if collided_objects:
            for collided in collided_objects:
                if collided != self and not self.floorplat:
                    coll      = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if (coll_side == "top" or coll_side == "bot") and self.massVER <= collided.massVER:
                        self.vel.y = self.vel.y * (-1)
                        self.pos = correctedPos
                    if (coll_side == "left" or coll_side == "right") and self.massHOR <= collided.massHOR: # left side of collidedd obj
                        self.vel.x = self.vel.x * (-1)
                        self.pos   = correctedPos