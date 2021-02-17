import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Level:
    def __init__(self, game, platforms, boxes , length):
        self.surfaces = pg.sprite.Group()
        self.platforms = platforms
        self.boxes = boxes
        self.game = game
        self.length = length

    # --> Just makes the list of platforms in "settings" to actual platforms. creates the objects
    def setPlatforms(self):
        for plat in self.platforms:
            Platform(self.game, *plat)

    def setBoxes(self):
        for plot in self.boxes:
            Box(self.game, *plot)

    def setSurfaces(self):
        #self.surfaces = Surface

        platforms = self.setPlatforms()
        boxes = self.setBoxes()

