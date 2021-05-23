# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# AI Enemy SubClass 
class IntelligentEnemy(CustomSprite):
    def __init__(self,spawnPlat, placement, width = 36, height = 28, speed = 1.7, name = "enemyai"):
        self.spawnPlat = spawnPlat
        self.pos = Vec(self.spawnPlat.left_x() + placement, self.spawnPlat.top_y()) 
        self.placement = placement
        self.speed = speed
        self.width = width;  self.height = height
        self.name = name
        self.vel = vec(speed,0); self.acc = vec()
        
        #self.relativePosition = self.pos.copy()


        '''just for testing?'''


        ''' pretty sure is needed'''
        #self.target = None # The player



        ''' should be revisited'''
        self.solidstrength = 8
        #self.originalsolidstrength = self.solidstrength


    
        """in use"""
        self.init()
        self.isEnemy = True
        self.active = True
        self.ori_massVER = 8
        self._layer = 25
        self.update_order = 5
        self.currentplat = None


        #self.stopMoving = False
        #self.facing = None
    
    def onSameLevel(self):
        return (abs(self.target.pos.y - self.pos.y) < 125)

    def playerLeft(self):
        return (self.target.pos.x < self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
            
    def onPlayer(self):
        return (abs(self.target.pos.x - self.pos.x) <5)

    def playerRight(self):
        return (self.target.pos.x > self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
    
    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_solid, game.group_enemies, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        sheet = self.game.dogSheet
        # create sub-rectangles to load from spritesheet
        rect1 = pg.Rect(  3, 21, 45, 27)
        rect2 = pg.Rect( 50, 21, 45, 27)
        rect3 = pg.Rect( 99, 21, 45, 27)
        rect4 = pg.Rect(147, 21, 45, 27)
        rect5 = pg.Rect(195, 21, 45, 27)
        rect6 = pg.Rect(243, 21, 45, 27)
        rects = [rect1, rect2, rect3, rect4, rect5, rect6]
        # load images from spritesheet
        self.images_left = sheet.images_at(rects, colorkey=(0,0,0))
        # scale images to correct size
        for img in self.images_left:
            img = pg.transform.scale(img, (self.width, self.height))

        self.images_right = []
        for img in self.images_left:
            self.images_right.append(pg.transform.flip(img,True,False))
        self.imageIndex = 0
        self.image = self.images_left[self.imageIndex]
    
        #self.target = self.game.player
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)

    def detectPlayer(self):
        if self.onSameLevel():
            if self.onPlayer():
                self.vel.x = self.addedVel.x
            elif self.playerRight():
                self.vel.x = self.speed + self.addedVel.x
                self.image = self.images_right[math.floor(self.imageIndex/6)]   # update current image
            elif self.playerLeft(): 
                self.vel.x = - self.speed + self.addedVel.x
                self.image = self.images_left[math.floor(self.imageIndex/6)]   # update current image
            else: 
                self.vel.x = self.addedVel.x
        else:
            self.vel.x = self.addedVel.x


    def updatePos(self): # fix
        self.acc   += vec(0, self.gravity)                  # Gravity
        self.pos +=  self.vel +  self.acc * 0.5
        self.acc = vec(0,0)     


    def update(self):
        self.target = self.game.player
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images_right)*6:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        
        #self.vel += self.addedVel

        #self.solidCollisions()
        self.solidCollisions()
        self.detectPlayer()
        self.checkCliff()
        self.rect.midbottom = self.pos.rounded().asTuple()



    def posCorrection(self):
        self.solidCollisions()

    def checkCliff(self):
        # should it have a max dist?
        possibleplat = self.on_solid(self.game.group_platforms)
        if possibleplat != None:
            self.currentplat = possibleplat
            self.gravity = 0
        else: 
            self.gravity = GRAVITY
        try:
            if self.right_x() >= self.currentplat.right_x() and self.vel.x > 0:
                self.vel = self.addedVel
                self.vel *= 0
                self.set_right(self.currentplat.right_x() ) # Number here must be bigger than 3 lines before. Otherwise dog stands still on edges
            elif self.left_x() <= self.currentplat.left_x()  and self.vel.x < 0: 
                self.vel = self.addedVel
                self.vel *= 0
                self.set_left(self.currentplat.left_x())
        except Exception as e:
            print(f'check cliff: {e}')


    # The part that checks whether to just turn around or be pushed
    # DELETE?
    def solidCollisionsOW(self, group):
        self.rect.midbottom = self.pos.rounded().asTuple()
        self.rect.x +=self.r((self.relativeVel().x)*1.5)
        self.rect.y +=self.r(self.vel.y*1.5)
        collideds = pg.sprite.spritecollide(self, group, False)

        if collideds:
            for collided in collideds:

                if collided != self:
                    if self.ori_massHOR <= collided.massHOR:
                        coll = self.collisionSide_Conditional(collided)
                        coll_side = coll['side']
                        correctedPos = coll['correctedPos']
                        
                        if coll_side == "left" or coll_side == "right": # left side of collidedd obj
                            self.vel.x = self.addedVel.x
                            self.pos = correctedPos
                                
                    """    
                    if self.ori_massVER < collided.massVER:
                        coll_side = self.determineSide(collided)
                            
                        if coll_side == "bot":
                            if  abs(self.right_x() - collided.left_x()) < abs(collided.right_x() - self.left_x() ):
                                self.pos.x = collided.left_x() - self.width/2
                            else: 
                                self.pos.x = collided.right_x() + self.width/2
                            self.massVER = collided.massVER - 1
                    """
