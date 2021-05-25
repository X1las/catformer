# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# Pickup SubClass - Inherits from CustomSprite
class PickUp(CustomSprite):

    def __init__(self,x,y, type_,  width = 16, height = 16, name = "pickup"): 
        self.width = width; self.height = height
        self.type = type_
        self.pos = vec(x,y)
        self.draw_layer = 10
        self.relativePosition = self.pos.copy()

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_pickups
        pg.sprite.Sprite.__init__(self, self.groups)

        sheet = self.game.spriteSheet

        if self.type == 'health':
            self.image = sheet.image_at((0,101,16,16), colorkey=(0,255,0))
        
        elif self.type == 'catnip':
            self.image = sheet.image_at((0,134,13,16), colorkey=(0,255,0))

        self.image = pg.transform.scale(self.image, (self.width, self.height))  # scale Surface to size
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def update(self):
        self.rect.midbottom = self.pos.realRound().asTuple()