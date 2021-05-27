# Imports
# External Modules:
import pygame as pg

# Class Imports:
from   CustomSprite import CustomSprite
from   Vector       import Vec as vec
from   settings     import GRAVITY

# Box SubClass - Inherits from CustomSprite
class Box(CustomSprite):
    
    # Class variables
    game = None
    
    # Initializer
    def __init__(self, x, y, width = 44, height = 44, name = "box"):
        self.width  = width; self.height = height   # size
        self.name = name
        self.pos = vec(x,y)                         # position
        self._layer = 6
        self.draw_layer = 15                        # layer for drawing
        self.solidstrength = 5                      # lower than for intelligent enemy
        self.initX = x; self.initY = y              # initial position for respawning
        self.has_collided = False                   # tracks collisions
        self.beingHeld = False                      # tracks if being held by player
        self.interacter = None
        self.justreleased = False                   # tracks if player just let go of box
        self.init()                                 # setting mass/strength


    # set game dependent attributes
    def startGame(self, game):
        self.game   = game
        # add to sprite groups
        self.groups = game.all_sprites, game.group_boxes, game.group_pressureActivator , game.group_solid, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        # load image from spritesheet
        sheet = self.game.spriteSheet
        self.img = sheet.image_at((0,34,52,41),(0,255,0))
        # scale image to correct size
        self.image = pg.transform.scale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.initX,self.initY)


    # method for setting box back to initial position
    def respawn(self):
        self = self.__init__(self.initX, self.initY, self.width, self.height, self.name)


    # method for being pulled/pushed by player
    def pickupEffect(self):
        if self.has_collided:
            if self.beingHeld:
                self.new_vel = self.interacter.player.vel.copy()
                self.new_acc = self.interacter.player.acc.copy()
                self.vel.x   = self.new_vel.x
                self.vel.y   = 0
                self.acc.x   = self.new_acc.x
                self.gravity = 0
        else:
            self.beingHeld = False
            if self.justreleased:
                self.pos = self.pos.rounded()
                self.justreleased = False
        if self.beingHeld == False:
            self.gravity = GRAVITY


    # method for updating
    def update(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.applyPhysics()
        self.solidCollisions()
        #self.vel += self.addedVel 
        self.rect.midbottom = self.pos.rounded().asTuple()


    # overwriting inherited method
    def update2(self):
        self.pickupEffect() 


    # method for lifting up the box
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


    # method for updating the position
    def updatePos(self):
        # Only if the box is being picked up, should it get the vel/acc from the interactive field
        if self.vel.x == 0:
            self.pos.x = self.pos.rounded().x
        super().updatePos()
        #self.pos   += self.vel +  self.acc * 0.5
        self.vel.x = self.addedVel.x
        self.has_collided = False
        self.solidCollisions()
        #self.rect.midbottom = self.pos.realRound().asTuple()


    # method for correcting position
    def posCorrection(self):
        if self.beingHeld:
            heldside = self.determineSide(self.interacter.player)
            if heldside == "left":
                self.set_right(self.interacter.player.left_x()-1)
            elif heldside == "right":
                self.set_left(self.interacter.player.right_x()+1)
        self.solidCollisions()
        self.rect.midbottom = self.pos.rounded().asTuple()