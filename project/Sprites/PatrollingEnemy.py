# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *
from Sprites.Platform import Platform


# Patrolling Enemy SubClass - Inherits from Hostile
class PatrollingEnemy(CustomSprite):

    #def __init__(self,x,y, width, height, maxDist, vel = vec(1,0), name = "enemy"):
    def __init__(self,plat : Platform, placement, maxDist, width = 23, height = 29, vel = vec(1.2,0), name = "enemy"):
        self.plat = plat
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement
        self.width  = width;      self.height = height;   self.name = name
        #self.pos    = vec(x,y);   
        self.vel =  vel;        self.acc = vec(0, 0)
        self.maxDist = maxDist

        ''' probably not needed'''
        self.dontmove = False
        #self.x = x
        self.collides_right = False
        self.collides_left = False
        
        '''just for testing?'''
        
        ''' really not sure'''
        self.isEnemy = True

        ''' pretty sure is needed'''
        self.justpoppedup = False
        self.originalVel = vel.copy()
        self.relativePosition = self.pos.copy()
        
        ''' should be revisited'''
        self.solidstrength = 3
        self.originalsolidstrength = self.solidstrength
        
        '''in use'''
        self.initX = self.pos.x
        self.currentplat = None # The platform it stands on/
        self.aboveground = True
        self.wasunderground = False # Only true when worm *just* popped up
        self._layer = 4
        self.active = True

        self.init()



        #self.stopMoving = False
        #self.facing = None

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_damager, game.group_enemies, game.group_movables #, game.group_solid
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        sheet = self.game.wormSheet
        # create sub-rectangles to load from spritesheet
        walk = []
        walk.append(pg.Rect(  4, 36, 28, 28))
        walk.append(pg.Rect( 36, 36, 28, 28))
        walk.append(pg.Rect( 68, 36, 28, 28))
        walk.append(pg.Rect(100, 36, 28, 28))
        walk.append(pg.Rect(132, 36, 28, 28))
        walk.append(pg.Rect(164, 36, 28, 28))
        popup = []
        popup.append(pg.Rect(  4, 4, 28, 28))
        popup.append(pg.Rect( 36, 4, 28, 28))
        popup.append(pg.Rect( 68, 4, 28, 28))
        popup.append(pg.Rect(100, 4, 28, 28))
        popup.append(pg.Rect(132, 4, 28, 28))
        popup.append(pg.Rect(164, 4, 28, 28))
        #hide = popup.copy()
        #hide.reverse()
        # load images from spritesheet
        images_walk  = sheet.images_at(walk,  colorkey=(0,0,0))
        images_popup = sheet.images_at(popup, colorkey=(0,0,0))
        # scale image to correct size
        images_walk  = [pg.transform.scale(img, (self.width, self.height)) for img in images_walk]
        images_popup = [pg.transform.scale(img, (self.width, self.height)) for img in images_popup]
        images_hide = []
        for img in reversed(images_popup):
            images_hide.append(img)
        #images_hide = images_popup.copy()
        #images_hide.reverse()
        # define and flip images        
        self.images  = {
            'walk':  {'right': images_walk,  'left': [pg.transform.flip(i, True, False) for i in images_walk]},
            'popup': {'right': images_popup, 'left': [pg.transform.flip(i, True, False) for i in images_popup]},
            'hide': {'right': images_hide, 'left': [pg.transform.flip(i, True, False) for i in images_hide]}
        }
        # set initial image
        self.facing = 'right'
        self.activity = 'walk'
        self.imageIndex = 0
        self.image = self.images[self.activity][self.facing][self.imageIndex]
    
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)


    # Checking if the enemy is outside its patrolling area
    def checkDist(self):
        if   self.right_x() >= self.currentplat.right_x()  -2:
            self.vel.x = (-1) * abs(self.originalVel.x)# + self.addedVel.x
            self.set_right(self.currentplat.right_x() - 3)
        elif self.left_x() <= self.currentplat.left_x() + 2:
            self.vel.x = abs(self.originalVel.x)# + self.addedVel.x
            self.set_left(self.currentplat.left_x() + 3)

        elif self.pos.x - self.initX >= self.maxDist: # right boundary
            self.vel.x = (-1) * abs(self.originalVel.x)# + self.addedVel.x
        elif self.pos.x - self.initX <= -1*self.maxDist:
            self.vel.x = abs(self.originalVel.x)# + self.addedVel.x

    #def updatePos(self, group):
     #   self.pos +=  self.vel +  self.acc * 0.5



    def updateAnimation(self):
        #walkTime = 10
        if self.activity == "hide" or self.activity == "popup":
            walkTime = 5
        elif self.activity == "walk":
            walkTime = 10
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images['walk']['right'])*walkTime:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        #self.area = "mid" #Doesn't matter rn, but maybe later?
        if self.vel.x < 0:
            self.facing = 'left'
        elif self.vel.x > 0:
            self.facing = 'right'

        self.image = self.images[self.activity][self.facing][math.floor(self.imageIndex/walkTime)]
        if self.activity == "popup" and self.image == self.images['popup'][self.facing][-1]:
            self.activity = 'walk'
        if self.activity == "hide" and self.image == self.images['hide'][self.facing][-1]:
            self.activity = 'walk'
            self.aboveground = False
                


    def update(self):

        #self.stopMoving = self.inbetweenSolids()
        #self.acc = vec(0,0)    
        try:
            self.hide()
        except Exception as e:
            print(f'touchbox: {e}')
        #self.vel += self.addedVel
        self.active = self.aboveground # Whether it should deal damage'
        if self.activity == "popup":
            self.vel.x = 0
        elif self.activity == "hide":
            self.vel.x = 0
        elif self.activity == "walk":
            if self.facing == 'left':
                self.vel.x = abs(self.originalVel.x) * (-1)
            elif self.facing == 'right':
                self.vel.x = abs(self.originalVel.x)
        if self.aboveground:
            self.pos.y = self.plat.top_y()
        self.checkDist()
        self.updateAnimation()
        #self.solidCollision()
        self.rect.midbottom = self.pos.rounded().asTuple()
    
    
    """
    -> Checks whether aboveground bool is true. If it is, reset the currentplat the worm is on
    -> Move rect above platform to check it is it "free" for boxes.
    -> Checks collisions. If true, set pos to platform bot (inside plat). 
        -> else: set pos to top of current platform.
    """
    def hide(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        if self.aboveground:
            possibleplat = self.on_solid(self.game.group_platforms)
            if possibleplat != None:
                self.currentplat = possibleplat
        # else if it is inside a plat (self.abovegroun = False), move enemies rect up
        else: 
            self.rect.bottom = self.currentplat.rect.top - 1
        
        collideds = pg.sprite.spritecollide(self, self.game.group_solid, False)
        self.rect.midbottom = self.pos.rounded().asTuple()
        if collideds:
            for collided in collideds:
                if collided != self.currentplat:
                    if self.aboveground:
                        self.activity = "hide"
                        self.imageIndex = 0
                        self.aboveground = False
                    if self.activity == "walk":
                        self.addedVel = self.currentplat.vel
                        self.pos.y = self.currentplat.pos.y - 1
                        self.aboveground = False
                        self.wasunderground = True
        else: 
            self.pos.y = self.currentplat.top_y()
            self.aboveground = True
            if self.wasunderground:
                self.justpoppedup = True
                # go to dirt pile animations
                self.activity = 'popup'
                self.imageIndex = 0
            self.wasunderground = False
        self.rect.midbottom = self.pos.rounded().asTuple()
    # Currently doesn't matter. The worm just hides. so?
    def solidCollision(self):
        self.rect.midbottom = self.pos.rounded().asTuple()
        collideds = pg.sprite.spritecollide(self, self.game.group_platforms, False)

        if collideds:
            for collided in collideds:
                # handle floor plat better
                if collided != self and collided != self.currentplat: #and collided.name != "p_floor" and self.lessMassThan(collided) :
                    
                    #coll_side = self.determineSide(collided)
                    coll = self.collisionSide_Conditional(collided)
                    coll_side = coll['side']
                    correctedPos = coll['correctedPos']
                    if coll_side == "left": # left side of collidedd obj
                        self.vel.x *= -1
                            
                    if coll_side == "right":
                        self.vel.x *= -1
                    self.pos = correctedPos
                            
                    """    
                    if coll_side == "bot":
                        if  abs(self.right_x() - collided.left_x()) < abs(collided.right_x() - self.left_x() ):
                            self.pos.x = collided.left_x() - self.width/2
                        else: 
                            self.pos.x = collided.right_x() + self.width/2
                        #self.count = 5
                    """

    # DEL?
    def posCorrection(self):
        #self.collidingWithWall()
        pass


    # Will make the enemy stand still if inbetween solids (instead of vibrating)
    

        
    # DEL?
    def collidingWithWall(self):
        #self.pygamecolls(self.game.group_solid)

        self.collides_left = False
        self.collides_right = False
