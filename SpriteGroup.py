#Description:

# Imports
# External Iports:
import pygame as pg

class SpriteGroup(pg.sprite.LayeredUpdates):

    # Initializor
    def __init__(self):
        self._sprite_drawlayers = {}
        self._spritelist_draw = []
        self.massOrdered = None
        pg.sprite.LayeredUpdates.__init__(self)


    # Returns the list sorted by draw_layer
    def sprites_draw(self):
        return self._spritelist_draw


    """ Overwriting LayeredUpdates methods """
    # Extending add_internal from pygame's spritegroup
    def add_internal(self, sprite, layer = None):
        super().add_internal(sprite, layer)

        # The below is close to equivalent to how sprites are added to LayeredUpdates
        # except that it adds it to the draw layer list
        
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
        #Making sure removing the sprite from the group also removes its draw layer
        super().remove_internal(sprite)
        self._spritelist_draw.remove(sprite)
        del self._sprite_drawlayers[sprite]


    # Overwriting draw
    def draw(self, surface):
        # This method is entirely taken from Pygame's own LayeredUpdates.draw(surface)
        # besides the list given as the iterator. Now draws based on draw_layer attr. 
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


    """ Methods iterating through the sprites calling methods from CustomSprite"""
    def resetSprites(self):
        for sprite in self:
            sprite.resetSprite()
    
    def update(self):
        for sprite in self.sprites():
            sprite.update()

    def dragAlongSprites(self):
        lis = self.sprites().copy()
        lis.sort(key = lambda x: x.solidstrength, reverse = True)
        for sprite in lis:
            sprite.pushEffect()

    def update2(self):
        for sprite in self.sprites():
            sprite.update2()

    def updateAddedvel(self):
        for sprite in self:
            sprite.updateAddedVel()

    def updatePos(self):
        for sprite in self.sprites():
            sprite.updatePos()
        self.correctPositions()

    def correctPositions(self):
        self.massSort('massVER')
        for sprite in self.massOrdered:
            sprite.posCorrection()
        self.massSort("massHOR")
        for sprite in self.massOrdered:
            sprite.posCorrection()

    def toRelativeRects(self):
        for sprite in self:
            sprite.toRelativeRect()

    def resetRects(self):
        for sprite in self:
            sprite.resetRects()

    
    """ Sorting methods"""
    # Sort method for sorting by object mass
    def massSort(self, key):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        elif key == "massHOR":
            self.massOrdered.sort(key = lambda x: x.massHOR, reverse = True)
        elif key == "massVER":
            self.massOrdered.sort(key = lambda x: x.massVER, reverse = True)
        return self.massOrdered

    # sorts such that sprites further down on the screen are first in the list
    def heightSort(self):
        lis = self.sprites().copy()
        lis.sort(key = lambda x: x.pos.y, reverse = False)
        return lis


    # Sort list based on solidstrength
    def createMassOrdered(self):
        lis = self.sprites().copy()
        lis.sort(key = lambda x: x.solidstrength, reverse = False)
        return lis


