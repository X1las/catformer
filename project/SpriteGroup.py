import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class SpriteGroup(pg.sprite.LayeredUpdates):


    def __init__(self):
        pg.sprite.LayeredUpdates.__init__(self)
        self._sprite_drawlayers = {}
        self._spritelist_draw = []
        self.massOrdered = None


    def sprites_draw(self):
        return list(self._spritelist_draw)


    """ -------- Small changes/overwriting LayeredUpdate's original methods"""
    # Overwriting add_internal
    def add_internal(self, sprite, layer = None):
        super().add_internal(sprite, layer)

        """ The below is close to equivalent to how sprites are added to LayeredUpdates
            except that it adds it to the draw layer list
        """
        sprites = self._spritelist_draw 
        sprites_drawlayers = self._sprite_drawlayers
        drawlayer = sprite.draw_layer
        sprites_drawlayers[sprite] = drawlayer

        leng = len(sprites)
        low = mid = 0
        high = leng - 1
        while low <= high:
            mid = low + (high - low) // 2
            if sprites_drawlayers[sprites[mid]] <= drawlayer:
                low = mid + 1
            else:
                high = mid - 1
        while mid < leng and sprites_drawlayers[sprites[mid]] <= drawlayer:
            mid += 1
        sprites.insert(mid, sprite)

    # Overwriting remove_internal
    def remove_internal(self, sprite):
        """ Making sure removing the sprite from the group also removes its draw layer
        """
        super().remove_internal(sprite)
        self._spritelist_draw.remove(sprite)
        del self._sprite_drawlayers[sprite]

    # Overwriting draw
    def draw(self, surface):
        """ This method is entirely taken from Pygame's own LayeredUpdates.draw(surface)
            besides the list given as the iterator. Now draws based on draw_layer attr. 
        """
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites_draw(): # Identical besides self.sprites_draw() instead of self.sprites()
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect)
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty




    """ --------- The methods used on the groups in the Game class --------------------------"""
    def resetSprites(self):
        for i in self:
            i.resetSprite()
    
    def update(self):
        for i in self.sprites():
            i.update()

    def collisionEffects(self):
        lis = self.sprites().copy()
        lis.sort(key = lambda x: x.solidstrength, reverse = True)
        for i in lis:
            i.pushEffect()

    def update2(self):
        for i in self.sprites():
            i.update2()

    def updateAddedvel(self):
        for i in self.sprites():
            i.updateAddedVel()

    def updatePos(self):
        for i in self.sprites():
            i.updatePos()
        self.correctPositions()

    def correctPositions(self):
        self.massSort('massVER')
        for i in self.massOrdered:
            i.posCorrection()
        self.massSort("massHOR")
        for i in self.massOrdered:
            i.posCorrection()

    def updateRects(self):
        for i in self:
            i.updateRect()

    def resetRects(self):
        for i in self:
            i.resetRects()

        
    """ ---------- For sorting dependent on mass ---------------------------------------------"""
    def massSort(self, key):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        elif key == "massHOR":
            self.massOrdered.sort(key = lambda x: x.massHOR, reverse = True)
        elif key == "massVER":
            self.massOrdered.sort(key = lambda x: x.massVER, reverse = True)
        return self.massOrdered

    def createMassOrdered(self):
        lis = self.sprites().copy()
        lis.sort(key = lambda x: x.solidstrength, reverse = False)
        return lis


