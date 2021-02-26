import pygame as pg
import main as game
from settings import *
import pygame as pg
from settings import *
from random import choice, randrange, uniform
from os import path
vec = pg.math.Vector2

class Surface(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):

        self.groups = game.all_sprites, game.surfaces
        pg.sprite.Sprite.__init__(self, self.groups)  # Apparently a must, not sure what it does..





class Platform(Surface):                               # The platforms (surprise!)
    def __init__(self, game, x, y, width, height, bot):
        self.bot = bot
        self.width = width
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms, game.surfaces, game.obstacles, game.non_moveable
        pg.sprite.Sprite.__init__(self, self.groups)            # Apparently a must, not sure what it does..
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),                 #Two types of platform, but I only use nr. 2
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]

        self.image = pg.transform.scale(images[0], (width, height))                 # Deciding size of the platform
        #self.image = choice(images)
        self.image.set_colorkey(BLACK)                                              # Removes the black background of the sprite image
        self.rect = self.image.get_rect()                                           # get rekt
        self.rect.x = x                                                             # Put the platform at the given coordinate.
        self.rect.y = y                                                                # \\

class Box(Surface):
    def __init__(self, game, x, y, width, height):
        #super().__init__(game, x, y, width, height)
        self.game   = game
        self.width  = width
        self.height = height
        self.groups = game.all_sprites, game.boxes, game.surfaces, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.image = pg.image.load(path.join(img_dir, 'RTS_Crate.png')).convert()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y