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
        super().__init__()
        
        self.width  = width; self.height = height   # size
        self.name = name
        self.pos = vec(x,y)                         # position
        self._layer = 7
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


    # method for setting box back to initial position. Used by Activators
    def respawn(self):
        self = self.__init__(self.initX, self.initY, self.width, self.height, self.name)


    # method for being pulled/pushed by player
    def pickupEffect(self):
        if self.has_collided: # triggered in Player class
            if self.beingHeld: # only true if player is not jumping
                self.vel.x = self.interacter.player.vel.copy()
                self.vel.y   = 0
                self.acc.x   = self.new_acc.x
                self.gravity = 0
        else:
            self.beingHeld = False
            # make sure position is rounded to avoid wobbling
            if self.justreleased:
                self.pos = self.pos.rounded()
                self.justreleased = False
        # only have non-zero gravity if the player isn't lifting the box
        if not self.beingHeld:
            self.gravity = GRAVITY


    # method for updating
    def update(self):
        self.applyPhysics()
        self.solidCollisions()
        self.updateRect()


    # Applying some effects of being lifted
    def update2(self):
        self.pickupEffect() 


    # method for lifting up the box
    def liftedBy(self,interacter):
        # Setting how much box should be lifted
        self.interacter = interacter
        # Only of the player is on a solid or moving downwards should they be able to carry the box
        if not interacter.player.inAir or interacter.player.vel.y > 0:
            self.beingHeld = True
            self.pos.y = interacter.player.pos.y - 3
            # Since box is a solid, it would stop the player when they pick it up and walk towards it.
            # Therefore, if the box is not colliding with another solid, the player's mass is temporarily greater
            #   resulting in the player not being stopped by the box
            if not self.stoppedHOR:
                self.interacter.player.massHOR = self.ori_massHOR - 1
                self.massHOR = self.interacter.player.massHOR - 1
            self.justreleased = True # Meant for rounding position later
        else: 
            self.beingHeld = False
        self.updateRect()


    # method for updating the position
    def updatePos(self):
        # If the pos is not moving screen-wise, the position should be rounded. Otherwise, box "wobbles" when player moves
        if self.vel.x == 0:
            self.pos.x = self.pos.rounded().x
        super().updatePos()
        self.vel.x = self.addedVel.x # Make sure box stands still on anything moving in x direction
        self.has_collided = False
        self.solidCollisions()


    # method for correcting position
    def posCorrection(self):
        if self.beingHeld:
            # Set it such that the pos is always one pixel away from the player with picked up.
            heldside = self.determineSide(self.interacter.player)
            if heldside == "left":
                self.set_right(self.interacter.player.left_x()-1)
            elif heldside == "right":
                self.set_left(self.interacter.player.right_x()+1)
        self.solidCollisions()
        self.updateRect()