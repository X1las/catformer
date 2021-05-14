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

    """
    def update(self):
        '''
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images)*10:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        self.image = self.images[math.floor(self.imageIndex/10)]
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        '''
        #round(self.pos) 
        self.rect.midbottom = self.pos.realRound().asTuple()
    """

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
        waterSheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = waterSheet.images_at(rects, colorkey=(0,255,0))
        self.imageIndex = 0
        #self.image = self.images[self.imageIndex]

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
