# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *
from Sprites.Platform import Platform
from threading import Timer

class Activator(CustomSprite):

    hasActivatedTarget = False
    hasDeactivatedTarget = False
    activated = False
    deactivated = True
    auto_deactivate = False
    

    def activeEffect(self):
        doDeactivate = False
        try:
            for e,v in self.effect.items():
                if e == "respawn":
                    for respawn in v:
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            target = respawn['target']
                            #self.hasActivatedTarget = True
                            target.respawn()
                if e == "spawn":
                    for spawn in v:
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            #self.hasActivatedTarget = True
                            target = spawn['target']
                            target.startGame(self.game)
                if e == "move":
                    self.hasDeactivatedTarget = False
                    for move in v:
                        target = move["target"]
                        move['target'].vel = move["movespeed"].copy() + target.originalVel
                if e == "conMove":
                    for conMove in  v:
                        
                        if not self.hasActivatedTarget:
                            doDeactivate = True
                            target = conMove["target"]
                            target.originalVel = conMove['movespeed'].copy()
                            target.vel = target.originalVel.copy()
            if doDeactivate:
                self.hasActivatedTarget = True
        except Exception as e:
            print(f'button activate: {e}') 

    def deactiveEffect(self):
        doActivate = False
        try: # shouldn't be try except, I think
            for e,v in self.effect.items():
                if e == "respawn":
                    self.hasActivatedTarget = False
                if e == "move":
                    if not self.hasDeactivatedTarget:
                        doActivate = True
                        for move in v:
                            target = move["target"]
                            move['target'].vel = move["deactspeed"].copy() + target.originalVel

                if e == "conMove":
                    self.hasActivatedTarget = False
                    for conMove in v:
                        target = conMove["target"]
                        target.originalVel *= 0
                        target.vel = target.originalVel
            if doActivate:
                self.hasDeactivatedTarget = True
        except Exception as e:
            print(f'button deact: {e}') 



    def activate(self):
        if not self.activated:
            self.activated = True
            self.deactivated = False
            self.image = self.image_active
            if self.auto_deactivate:
                t = Timer(1, self.deactivate)
                t.start() 
            #self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
    def deactivate(self):
        if not self.deactivated:
            self.deactivated = True
            self.activated = False
            self.image = self.image_inactive
    def update(self):
        if self.activated:
            self.activeEffect()
        elif self.deactivated:
            self.deactiveEffect()
        self.rect.midbottom = self.pos.realRound().asTuple()

# Lever SubClass - Inherits from CustomSprite
class Lever(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
    def __init__(self, plat, placement, width = 30, height = 20, name = "lever", effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        self.plat = plat
        self.name = name
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement
        self.width = width; self.height = height; self.effect = effect; 
        self.auto_deactivate = autodeactivate
        #self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        
        self.deactivate_counter = 30
        #self.x = x; self.y = y
        '''move to super'''



    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levers, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        #self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from spritesheet
        left  = pg.Rect( 0,87,18,13)
        right = pg.Rect(19,87,18,13)
        rects = [left, right]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     

        #self.image_left  = pg.transform.scale(self.images[0], (self.width, self.height))
        #self.image_right = pg.transform.scale(self.images[1], (self.width, self.height))
        #self.image = self.image_left
        self.image_inactive  = pg.transform.scale(self.images[0], (self.width, self.height))
        self.image_active = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)   

# Button SubClass - Inherits from CustomSprite
class Button(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}): 
    def __init__(self, plat:Platform, placement, width = 30, height = 20, name = "button", effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        self.plat = plat
        self.name = name
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.placement = placement

        self.effect = effect; 
        self.width = width; self.height = height
        #self.pos = vec(x,y)



        ''' probably not needed'''
        #self.x = x; self.y = y
        #self.activated = False
        #self.deactivated = True

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''
        self.relativePosition = self.pos.copy()

        ''' should be revisited'''

        ''' in use'''

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_buttons, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # create surface with correct size
        #self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from spritesheet
        pressed   = pg.Rect( 0,81,18,5)
        unpressed = pg.Rect(18,76,18,10)
        rects = [pressed, unpressed]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        self.images = sheet.images_at(rects, (0,255,0))     
        #self.image_pressed = pg.transform.scale(self.images[0], (self.width, int(self.height/2)))
        #self.image_unpressed = pg.transform.scale(self.images[1], (self.width, self.height))
        #self.image = self.image_unpressed
        self.image_active = pg.transform.scale(self.images[0], (self.width, int(self.height/2)))
        self.image_inactive = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def activate(self):
        super().activate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
    def deactivate(self):
        super().deactivate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height))


    def update(self):
        self.buttonPress()
        super().update()
        self.activated = False # Not sure if needed

    def buttonPress(self):
        collided_list = self.collisionDetection(self.game.group_pressureActivator)
        #collided_list = pg.sprite.spritecollide(self, self.game.group_pressureActivator, False)
        if collided_list:
            for collided in collided_list:
                self.activate()
                self.prevActivated = True
                return self
        else:
            self.deactivate()
            self.activated = False
            self.deactivated = True
            return None