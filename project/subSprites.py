# Description:

# Imports
import pygame as pg

from settings import *

from CustomSprite import CustomSprite
from Vector import Vec
from random import choice, randrange, uniform

# Variables
vec = Vec

# ------------------------------ collision detection --------------------------------------------------------------------
class Tester(CustomSprite):
    def __init__(self, game,  pos):

        # anchor depends on which way player faces
        pg.sprite.Sprite.__init__(self, game.all_sprites)  
        self.player = player
        width = self.player.width/2 + 50
        height = self.player.height       
        self.facing = facing
        self.image = pg.Surface((width,height)); 
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.image.fill((255,255,255)) 
        self.relativePosition = self.pos.copy()
        self.midbottom = pos

        
    
    #def update(self):
     #   self.midbottom = player.pos.asTuple()





# ---------------- INTERACTIVE ---------------------------------------------------------------------------------------------------------------------------------
class Interactive(CustomSprite):
    def __init__(self, game,  player, facing):

        # anchor depends on which way player faces
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.interactive_boxes)  
        self._layer = 1
        self.player = player
        width = self.player.width/2 + 50
        height = self.player.height       
        self.facing = facing
        self.image = pg.Surface((width,height)); 
        self.image.fill((0,200,0)) 
        self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite 
        self.colliding = False
        self.faceinput = self.player.facing
        self.relativePosition = self.pos.copy()
        self.vel = self.player.vel
        if self.facing == "left":
            self.rect.bottomright = (player.pos.x,player.pos.y)   
        else: 
            self.rect.bottomleft = (player.pos.x,player.pos.y)   

    def intUpdate(self, facing, pos):

        #bob = self.rect.bottomleft
        #bob = self.rect.bottomright

        if facing == "left":
            if pos == "global":
                #bob = (self.player.pos.x,self.player.pos.y)   

                self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
            else:
                #bob = self.player.relativePosition.rounded().asTuple()

                self.rect.bottomright = self.player.relativePosition.rounded().asTuple()
        else: 
            if pos == "global":
                self.rect.bottomleft = (self.player.pos.x,self.player.pos.y)   
            else: 
                self.rect.bottomleft = self.player.relativePosition.rounded().asTuple()
    
    def update(self):
        
        """
        if self.player.facing == "left":
            self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
        else: 
            self.rect.bottomleft = (self.player.pos.x,self.player.pos.y) 
        """  
        self.vel = self.player.vel
    
    def updateRect(self):
        if not self.colliding:
            self.faceinput = self.player.facing
        self.intUpdate(self.faceinput, "rel")

        
    
    def resetRects(self):
        self.intUpdate(self.faceinput, "global")

    #def draw(self):
     #   pass

# ---------------- LEVEL GOAL---------------------------------------------------------------------------------------------------------------------------------

class LevelGoal(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.level_goals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()


    def update(self):
        self.rect.midbottom = self.pos.rounded().asTuple()

    def activate(self):
        # Whatever it does
        self.game.resetCamera()
        """
        for sprite in self.game.all_sprites:
            self.game.relposx = 0
            self.game.relposp = 0
            self.game.player.pos = self.game.level.spawn
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.game.relposx
        """ 
        #self.game.new()
        

# ---------------- PLATFORM ---------------------------------------------------------------------------------------------------------------------------------

# Classes
class Platform(CustomSprite):
    def __init__(self, game, x, y, width, height, name, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        self.solid = True
        self.height = height; self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.non_player, game.platforms, game.obstacles, game.non_moveable, game.rayIntersecters, game.surfaces
        
        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.typed = "platform"    
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
 
    


    def update(self):
        #round(self.pos)
        self.rect.midbottom = self.pos.rounded().asTuple()


# ---------------- BOX ---------------------------------------------------------------------------------------------------------------------------------

class Box(CustomSprite):
    def __init__(self, game, x, y, width, height, name):
        self.game   = game;  self.width  = width; self.height = height; self.name = name
        self._layer = 5
        self.solid = True
        self.moveable = True
        self.groups = game.all_sprites, game.non_player, game.boxes, game.surfaces, game.obstacles, game.interactables, game.weight_act  , game.rayIntersecters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width,height))
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.can_fall_and_move = True
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.friction = 0
   
    def update(self):
        
        if self.has_collided:
            self.vel.x = self.new_vel.x
        else:
            self.vel.x = 0
        self.has_collided = False
        self.applyPhysics(self.game.rayIntersecters)
        #self.pos += self.vel
        self.rect.midbottom = self.pos.rounded().asTuple()

    def pickUp(self, interacter):
        
        self.new_vel.x = interacter.vel.x
       



# ---------------- VASE ---------------------------------------------------------------------------------------------------------------------------------

class Vase(CustomSprite):
    def __init__(self,game,x,y, name = None):
        self.broken = False; self.name = name
        self.breakable = True
        self.width = 20
        self.height = 30
        self.game = game
        self.groups = game.all_sprites, game.vases, game.non_player, game.interactables, game.rayIntersecters
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.fall = False
        self.gravity = PLAYER_GRAV
        #self.can_fall_and_move = True
        self.relativePosition = self.pos.copy()
        self.isVase = True

    def update(self):
        
        #round(self.pos)
        

        if self.fall == True:
            print("should fall")
            self.inAir = True
            self.applyPhysics(self.game.rayIntersecters)
        if self.on_solid(self.game.rayIntersecters) != self.ignoreSol:
            self.breaks()
        self.rect.midbottom = self.pos.rounded().asTuple()
    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str , name = None):
        try:
            if placement == "left":
                pos = plat.topleft()
             
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos.x, pos.y = plat.rect.midtop.x, plat.rect.midtop.y 
            return cls(game = game, x = pos.x+ push, y = pos.y, name = name)
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1], ignoreSol = plat)
        self.ignoreSol = plat

    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True



# ---------------- LEVER ---------------------------------------------------------------------------------------------------------------------------------

class Lever(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.interactables, game.levers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,200,200))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

        self.activated = False
        self.deactivated = True
        

    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.image.fill((255,255,255))
        # whatever else it needs to activate
     
            
        
        

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
          
            self.image.fill((0,200,200))
        # whatever else it needs to deactivate
            
    

    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


# ---------------- BUTTON ---------------------------------------------------------------------------------------------------------------------------------

class Button(CustomSprite):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.activator, game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((200,0,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        self.activated = False
        self.deactivated = True

    def activate(self):
        if self.activated != True:
            self.activated = True
            self.deactivated = False
            self.rect.update(self.pos.asTuple(), (self.width, self.height/2))
        # whatever else it needs to activate
        

    def deactivate(self):
        if self.deactivated != True:
            self.deactivated = True
            self.activated = False
            #if self.prevActivated:
          
            self.rect.update(self.pos.asTuple(), (self.width, self.height))
            #    self.prevActivated = False
        # whatever else it needs to deactivate

    def update(self):
       
            
        self.activated = False

        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()



# ---------------- PICKUP ---------------------------------------------------------------------------------------------------------------------------------

class PickUp(CustomSprite):

    def __init__(self,game,x,y, width, height, type_, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.pickups
        self.type = type_
        self.pickup = True
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        if self.type == 'health':
            self.image.fill((255,0, 200))
        
        if self.type == 'catnip':
            self.image.fill((165, 42, 42))

        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()

    def update(self):
        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


# ---------------- HOStiLE ---------------------------------------------------------------------------------------------------------------------------------

class Hostile(CustomSprite):
    pass

# ---------------- WATER ---------------------------------------------------------------------------------------------------------------------------------

class Water(Hostile):
    def __init__(self,game,x,y, width, height, name = None): 
        self.game = game
        self.width = width; self.height = height
        self.groups = game.all_sprites, game.damager
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((0,0,200))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        self.relativePosition = self.pos.copy()
        
    def update(self):

        #round(self.pos) 
        self.rect.midbottom = self.pos.rounded().asTuple()


        
    # Catnip
    # Health (fish)
    # Zoomies (yarn)




# ---------------- PATrOLLING ENEMY ---------------------------------------------------------------------------------------------------------------------------------

class PatrollingEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass


class AiEnemy(Hostile):
    def __init__(self,game,x,y, name = None):
        pass






