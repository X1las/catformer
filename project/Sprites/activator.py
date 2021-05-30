# Imports
import pygame as pg

from CustomSprite import CustomSprite
from settings import *
from Sprites.Platform import Platform
from threading import Timer

class Activator(CustomSprite):

    # Initial booleans representing an inactive Activator
    hasActivatedTargets  = False
    hasDeactivatedTarget = False
    activated            = False
    deactivated          = True
    auto_deactivate      = False

    # Draw/update layers
    _layer = 0  # update layer
    draw_layer = 3

    # When Activator is activated
    def activeEffect(self):
        hasActivated = False
        try:
            # Traversing through the given event dictionary
            for e,v in self.effect.items():
                # Respawns an already existing sprite
                if e == "respawn":
                    if not self.hasActivatedTargets: # Only happens the first iterations of it active state
                        hasActivated = True          # Sets the self.hasActivatedTargets afterwards
                        for respawn in v:
                            target = respawn['target']
                            target.respawn()
                # Spawns a new item
                if e == "spawn":
                    if not self.hasActivatedTargets:
                        hasActivated = True
                        for spawn in v:
                            target = spawn['target']
                            target.startGame(self.game)
                # Causes target to move with given velocity until it cannot anymore
                if e == "move":
                    self.hasDeactivatedTarget = False
                    for move in v:
                        target = move["target"]
                        move['target'].vel = move["movespeed"].copy() + target.originalVel
                # Causes target to move back and forth within it's area of movement
                if e == "conMove":
                    if not self.hasActivatedTargets:
                        hasActivated = True
                        for conMove in  v:
                            target = conMove["target"]
                            target.originalVel = conMove['movespeed'].copy()
                            target.vel = target.originalVel.copy()
            if hasActivated:
                self.hasActivatedTargets = True
        except Exception as e:
            print(f'button activate: {e}') 

    # When Activator is deactivated
    def deactiveEffect(self):
        hasDeactivated = False
        try: 
            for e,v in self.effect.items():
                # Just making it possible to respawn target again upon activating again
                if e == "respawn":
                    self.hasActivatedTargets = False
                # Moves target in the deactivate velocity given as event input
                if e == "move":
                    if not self.hasDeactivatedTarget:
                        hasDeactivated = True
                        for move in v:
                            target = move["target"]
                            move['target'].vel = move["deactspeed"].copy() + target.originalVel
                # Stops the platform from moving
                if e == "conMove":
                    self.hasActivatedTargets = False
                    for conMove in v:
                        target = conMove["target"]
                        target.originalVel *= 0
                        target.vel = target.originalVel.copy()
            if hasDeactivated:
                self.hasDeactivatedTarget = True
        except Exception as e:
            print(f'button deact: {e}') 


    # The function called outside to set state to activated
    def activate(self):
        if not self.activated:
            self.activated = True
            self.deactivated = False
            self.image = self.image_active
            if self.auto_deactivate:
                t = Timer(1, self.deactivate)
                t.start() 
    
    # The function called outside to set state to deactivated
    def deactivate(self):
        if not self.deactivated:
            self.deactivated = True
            self.activated = False
            self.image = self.image_inactive

    # Runs events based on state
    def update(self):
        if self.activated:
            self.activeEffect()
        elif self.deactivated:
            self.deactiveEffect()
        self.updateRect()

    def updatePos(self):
        super().updatePos()
        self.pos.y = self.plat.top_y() # Should always just stay on top of the platform


# Lever SubClass - Inherits from CustomSprite
class Lever(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
    def __init__(self, plat, placement, width = 30, height = 20, name = "lever", effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        super().__init__()
        self.plat = plat;   self.name = name;     self.placement = placement
        self.width = width; self.height = height; self.effect = effect; 
        
        # start positions
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.relativePosition = self.pos.copy()
        
        self._layer = 1
        # Automatically deactive lever
        self.auto_deactivate = autodeactivate
        self.deactivate_counter = 30

    # Set game-specific variables
    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levers
        pg.sprite.Sprite.__init__(self, self.groups)

        # create sub-rectangles to load from spritesheet
        left  = pg.Rect( 0,87,18,13)
        right = pg.Rect(19,87,18,13)
        rects = [left, right]
        # load images from spritesheet
        sheet = self.game.spriteSheet
        self.images = sheet.images_at(rects, (0,255,0))     

        self.image_inactive  = pg.transform.scale(self.images[0], (self.width, self.height))
        self.image_active = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)   

# Button SubClass - Inherits from CustomSprite
class Button(Activator):
    #def __init__(self,x,y, width, height, name = None, effect = {}): 
    def __init__(self, plat:Platform, placement, width = 30, height = 20, name = "button", effect = {}, autodeactivate = False):#None, movespeed = None, target = None, autodeactivate = None): 
        super().__init__()
        
        self.plat = plat;   self.placement = placement; self.name = name
        self.width = width; self.height = height;       self.effect = effect; 
        self.pos = Vec(self.plat.left_x() + placement, self.plat.top_y()) 
        self.relativePosition = self.pos.copy()

    # Set game-specific variables
    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # create sub-rectangles to load from spritesheet
        pressed   = pg.Rect( 0,81,18,5)
        unpressed = pg.Rect(18,76,18,10)
        rects = [pressed, unpressed]
        # load images from spritesheet
        sheet = self.game.spriteSheet
        self.images = sheet.images_at(rects, (0,255,0))     
        self.image_active   = pg.transform.scale(self.images[0], (self.width, int(self.height/2)))
        self.image_inactive = pg.transform.scale(self.images[1], (self.width, self.height))
        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    # Activator's adtivate() and deactivate() should also change side of button (so it looks pressed)
    def activate(self):
        super().activate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
    def deactivate(self):
        super().deactivate()
        self.rect.update(self.pos.asTuple(), (self.width, self.height))

    def update(self):
        self.buttonPress()

    # deciding whether the button is activated or deactivated
    def buttonPress(self):
        # Check if any pressure activators are on the button
        collided_list = pg.sprite.spritecollide(self, self.game.group_pressureActivator, False)
        if collided_list:
            self.activate()
        else:
            self.deactivate()