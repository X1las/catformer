# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# Box SubClass - Inherits from CustomSprite
class Box(CustomSprite):
    game = None
    def __init__(self, x, y, width = 44, height = 44, name = "box"):
        self.width  = width; self.height = height; self.name = name
        self.pos = vec(x,y)
                
        ''' probably not needed'''

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''
        self._layer = 15

        ''' should be revisited'''
        self.solidstrength = 5
        self.originalsolidstrength = self.solidstrength
        self.relativePosition = self.pos.copy() # go to init() ?

        ''' in use'''
        self.initX = x; self.initY = y
        self.has_collided = False
        self.beingHeld = False
        self.interacter = None
        self.justreleased = False
        self.update_order = 6
        self.init()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_boxes, game.group_pressureActivator , game.group_solid, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        # load image from spritesheet
        sheet = self.game.spriteSheet
        self.img = sheet.image_at((0,34,52,41),(0,255,0))
        self.image = pg.transform.scale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.initX,self.initY)

    def respawn(self):
        self = self.__init__(self.initX, self.initY, self.width, self.height, self.name)


    def pickupEffect(self):
        if self.has_collided:
            if self.beingHeld:
                self.new_vel = self.interacter.player.vel.copy()
                self.new_acc = self.interacter.player.acc.copy()
                self.vel.x = self.new_vel.x
                self.vel.y = 0
                self.acc.x = self.new_acc.x
                self.gravity = 0
            
        else:
            self.beingHeld = False
            if self.justreleased:
                self.pos = self.pos.rounded()
                self.justreleased = False
        if self.beingHeld == False:
            self.gravity = GRAVITY

    def update(self):
        #self.test()
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.applyPhysics()
        self.solidCollisions()
        #self.vel += self.addedVel 
        self.rect.midbottom = self.pos.rounded().asTuple()


    def update2(self):
        self.pickupEffect() 
        #self.pickupEffect()
        pass


    def liftedBy(self,interacter):

        # Setting how much box should be lifted
        self.interacter = interacter
        if not interacter.player.inAir or interacter.player.vel.y > 0:
            self.beingHeld = True
            self.pos.y = interacter.player.pos.y - 3
            if not self.stoppedHOR:
                self.interacter.player.massHOR = self.ori_massHOR - 1
                self.massHOR = self.interacter.player.massHOR - 1
            self.justreleased = True
        else: 
            self.beingHeld = False
        self.rect.midbottom = self.pos.realRound().asTuple()


    def updatePos(self):
        # Only if the box is being picked up, should it get the vel/acc from the interactive field
        if self.vel.x == 0:
            self.pos = self.pos.rounded()
        super().updatePos()
        #self.pos   += self.vel +  self.acc * 0.5
        self.vel.x = self.addedVel.x
        self.has_collided = False
        self.solidCollisions()
        #self.rect.midbottom = self.pos.realRound().asTuple()



    def posCorrection(self):
        # I am not sure this is needed
        if self.beingHeld:
            heldside = self.determineSide(self.interacter.player)
            if heldside == "left":
                self.set_right(self.interacter.player.left_x()-1)
            elif heldside == "right":
                self.set_left(self.interacter.player.right_x()+1)
        self.solidCollisions()
        self.rect.midbottom = self.pos.rounded().asTuple()