# Description:

# Imports
import pygame as pg

from settings import *

from CustomSprite import CustomSprite
from Vector import Vec
from random import choice, randrange, uniform

# Variables
vec = Vec

class Interactive(CustomSprite):
    def __init__(self, game,  player, facing):

        # anchor depends on which way player faces
        self.player = player
        width = self.player.width/2 + 50
        height = self.player.height       
        self.facing = facing
        self.image = pg.Surface((width,height)); 
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.image.fill((0,200,0)) 
        if self.facing == "left":
            self.rect.bottomright = (player.pos.x,player.pos.y)   
        else: 
            self.rect.bottomleft = (player.pos.x,player.pos.y)   

        pg.sprite.Sprite.__init__(self, game.all_sprites)  
    
    def update(self):
        if self.player.facing == "left":

            self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
        else: 
            self.rect.bottomleft = (self.player.pos.x,self.player.pos.y)   

    def draw(self):
        pass
       




# Classes
class Platform(CustomSprite):
    def __init__(self, game, x, y, width, height, name, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        self.solid = True
        self.height = height; self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.non_player, game.platforms, game.surfaces, game.obstacles, game.non_moveable, game.rayIntersecters

        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.typed = "platform"    
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
    


    def update(self):
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()

class Box(CustomSprite):
    def __init__(self, game, x, y, width, height, name):
        self.game   = game;  self.width  = width; self.height = height; self.name = name
        self.solid = True
        self.groups = game.all_sprites, game.non_player, game.boxes, game.surfaces, game.obstacles, game.rayIntersecters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width,height))
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y

        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        #self.rect.x = x                                                                       # Put the platform at the given coordinate.
        #self.rect.y = y
                                                                           # \\


    def update(self):
        self.pos += self.vel
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()

class Vase(CustomSprite):
    def __init__(self,game,x,y, name = None):
        self.broken = False; self.name = name
        self.width = 10
        self.height = 10
        self.game = game
        self.groups = game.all_sprites, game.vases, game.non_player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)

    def update(self):
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()
    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str , name = None):
        try:
            if placement == "left":
                pos = plat.rect.topleft
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos = plat.rect.midtop
            return cls(game = game, x = pos[0] + push, y = pos[1])
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1])

    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True

class PickUp(CustomSprite):
    def __init__(self,game,x,y, type, name = None): 
        pass
    # Catnip
    # Health (fish)
    # Zoomies (yarn)


class Hostile(CustomSprite):
    pass

class PatrollingEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass

class Water(Hostile):
    def __init__(self,game,x,y, name = None):
        pass

class AiEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass






