import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class Sprites(pg.sprite.LayeredUpdates):

    def update(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort()
        for i in lis:
            i.update()





