# Sprites classes
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill((150,0,0))
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0

    def update(self):
        self.vx = 0
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.vx -= 5
        
        if keys[pg.K_RIGHT]:
            self.vx += 5
        
        self.rect.x += self.vx
        self.rect.y += self.vy

        