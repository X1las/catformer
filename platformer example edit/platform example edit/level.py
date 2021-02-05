
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Level:
    def __init__(self, game, platforms, length):
        self.platforms = platforms
        self.game = game
        self.length = length

    def setPlatforms(self):
        for plat in self.platforms:
            Platform(self.game, *plat)




