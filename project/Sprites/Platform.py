# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# Platform SubClass - Inherits from CustomSprite
class Platform(CustomSprite):

    game = None
    def __init__(self, x, y, width, height, name = "plat", vel = Vec(), floorplat = False, maxDist = None, leftMaxDist = 1000, rightMaxDist = 1000, upMaxDist = 2, downMaxDist = 2):
        self.height = height; self.width = width; self.name = name; 
        self.pos = vec(x,y); self.vel = vel
        self.originalVel = self.vel.copy()
        self.floorplat = floorplat
        self.isPlatform = True


        if maxDist == None:
            self.leftMaxDist = leftMaxDist
            self.rightMaxDist = rightMaxDist
            self.downMaxDist = downMaxDist
            self.upMaxDist = upMaxDist
        else: 
            self.leftMaxDist  = maxDist
            self.rightMaxDist = maxDist
            self.downMaxDist  = maxDist
            self.upMaxDist    = maxDist

        self.solidstrength = 30
        if floorplat:
            self.solidstrength = 50
        #self.originalsolidstrength = self.solidstrength

        self.relativePosition = self.pos.copy()
        self._layer = 1                                               
        self.draw_layer = 8                                               
        
        self.initX = x
        self.initY = y
        self.x, self.y = x,y
        self.init()
        


        self.prevPos = self.pos.copy()



    def startGame(self, game):
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
        numOfBrownParts_h = math.ceil(self.width/mid.get_width())
        while fill < self.height:
            for i in range(numOfBrownParts_h):
                self.image.blit(brownPiece, (i*end_left.get_width(),fill))
            fill += brownPiece.get_height()

            
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.rect.midbottom = (self.pos.x,self.pos.y)

    # Checking if the enemy is outside it's patrolling area
    def checkDist(self):
        if  self.pos.x -  self.initX >= self.rightMaxDist and self.vel.x > 0: # right boundary
            self.vel.x =  -1 * abs(self.originalVel.x)
        elif self.pos.x - self.initX <= -1*self.leftMaxDist and self.vel.x < 0:
            self.vel.x =  abs(self.originalVel.x)
        elif self.pos.y - self.initY <= -1* abs(self.upMaxDist) and self.vel.y < 0:
            self.vel.y =  abs(self.originalVel.y)
        elif self.pos.y - self.initY >= self.downMaxDist and self.vel.y > 0:
            self.vel.y =  -1* abs(self.originalVel.y)



    def update(self):
        #if self.floorplat:
         #   print(f'in update : {self.pos}')
        if self.vel.x != 0:
            self.massHOR = 29.5
        elif self.vel.y != 0:
            self.massVER = 29.5

        #if self.vel.x != 0 or self.vel.y != 0:
         #   self.originalsolidstrength = 29.5
          #  self.solidstrength = 29.5
           # self.init() # Needs to update massHOR and massVER
        self.checkDist()
       # if self.floorplat:
        #    print(f'aft dist : {self.pos}')
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updatePos(self):
        #if self.floorplat:
         #   print(f'in updPos : {self.pos}')
        #print(f'new iter')

        #if self.originalVel.y == 0:
         #   print(self.vel)
        self.checkDist()
        self.solidCollision() # just moved it up
        super().updatePos()

        self.prevPos = self.pos.copy()

    def resetSprite(self):
        #self.test()

        super().resetSprite()
        #if self.floorplat:
         #   print(f'after reset : {self.pos}')

    def solidCollision(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.x +=self.r(self.vel.x)
        self.rect.y +=self.r(self.vel.y)
        collided_objects = pg.sprite.spritecollide(self, self.game.group_platforms, False)

        if collided_objects:
            for collided in collided_objects:
                if collided != self and self.solidstrength <= collided.solidstrength and not self.floorplat:
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if coll_side == "top":
                        self.vel.y = self.originalVel.y * (-1)
                    if coll_side == "left": # left side of collidedd obj
                        if collided.vel.x == 0: # If collided object is not moving, just turn around
                            self.vel.x = self.originalVel.x * (-1)
                    if coll_side == "right":
                        if collided.vel.x == 0:
                            self.vel.x = self.originalVel.x * (-1)
                    if coll_side == "bot": # left side of collidedd obj
                        self.vel.y = self.originalVel.y * (-1)
                    self.pos = correctedPos
        self.rect.midbottom = self.pos.rounded().asTuple()
