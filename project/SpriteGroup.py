import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class SpriteGroup(pg.sprite.LayeredUpdates):
    orderedList = None
    massOrdered = None

    def __init__(self):
        pg.sprite.LayeredUpdates.__init__(self)

    #def draw(self):
     #   lis = self.updateOrder()
      #  for i in self:
       #     self.blit()

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
        draw_order = sorted(self.sprites(), key = lambda x: x.draw_layer, reverse = False)
        for spr in draw_order:
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

    def resetRects(self):
        for i in self:
            i.resetRects()

    def updateRects(self):
        for i in self:
            i.updateRect()

    def resetSprites(self):
        for i in self:
            i.resetSprite()

    def updateOrder(self):
        if not self.orderedList:
            self.orderedList = self.createOrderedList()
        self.orderedList.sort(key = lambda x: x.draw_layer, reverse = False)
        return self.orderedList

    def createOrderedList(self):
        self.orderedList = self.sortList()
        return self.orderedList

    def collisionEffects(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.solidstrength, reverse = True)
        for i in lis:
            i.pushEffect()
        
    def massUpdateOrder(self):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        return self.massOrdered


    def massSort(self, key):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        elif key == "massHOR":
            self.massOrdered.sort(key = lambda x: x.massHOR, reverse = True)
        elif key == "massVER":
            self.massOrdered.sort(key = lambda x: x.massVER, reverse = True)
        return self.massOrdered

    def createMassOrdered(self):
        lis = []

        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.solidstrength, reverse = False)
        return lis


    def sortList(self):
        lis = []
        for i in self:
            lis.append(i)
        #lis.sort(key = lambda x: x.update_order, reverse = False)
        lis.sort(key = lambda x: x.draw_layer, reverse = False)
        return lis

    def update(self):
        #lis = self.updateOrder()
        for i in self:
        #for i in lis:
            i.update()

    def update2(self):
        #lis = self.updateOrder()
        #for i in lis:
        for i in self:
            i.update2()


    def updateAddedvel(self):
        #lis = self.updateOrder()

        #for i in lis:
        for i in self:
            i.updateAddedVel()


    def updatePos(self):
        #lis = self.updateOrder()
        #for i in lis:
        for i in self:
            i.updatePos()
            #i.posCorrection()
        """ So, if box is pushing into something and getting pushed out, player is already updated before the box was pushed out, so it vibrates"""
        self.correctPositions()

    def correctPositions(self):
        self.massSort('massVER')
        for i in self.massOrdered:
            i.posCorrection()
        self.massSort("massHOR")
        for i in self.massOrdered:
            i.posCorrection()
        


