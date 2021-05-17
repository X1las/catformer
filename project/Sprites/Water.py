# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# Water SubClass - Inherits from Hostile
class Water(CustomSprite):
    def __init__(self,x,y, width, height, name = "water"): 
        self.active = True
        self.name = name
        self.width = width; self.height = height
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self._layer = 15

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        rect1 = pg.Rect( 0,117,16,16)
        rect2 = pg.Rect(16,117,16,16)
        rect3 = pg.Rect(32,117,16,16)
        rect4 = pg.Rect(48,117,16,16)
        blue  = pg.Rect( 0,121,16,10)
        rects = [rect1, rect2, rect3, rect4, blue]
        # load images from spritesheet
        sheet = self.game.spriteSheet
        self.images = sheet.images_at(rects, colorkey=(0,255,0))

        fill_h = 0      # for tracking how much was filled horizontally
        fill_v = 0      # for tracking how much was filled vertically
        # filling horizontally
        numOfWaveParts = math.ceil(self.width/self.images[0].get_width())
        while fill_h < self.width:
            for i in range(len(self.images)-1):
                self.image.blit(self.images[i], (fill_h,0))
                fill_h += self.images[i].get_width()
        fill_v += self.images[0].get_height()
        # filling vertically
        while fill_v < self.height:
            for i in range(numOfWaveParts):
                self.image.blit(self.images[4], (self.images[4].get_width()*i,fill_v))
            fill_v += self.images[4].get_height()
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

        
    # Catnip
    # Health (fish)
