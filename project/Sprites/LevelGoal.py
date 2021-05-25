# Imports
import Spritesheet as ss
import pygame as pg

from CustomSprite import CustomSprite
from Vector import Vec as vec
from settings import *

# LevelGoal SubClass - Inherits from CustomSprite
class LevelGoal(CustomSprite):
    def __init__(self,plat, placement, name = "Goal"): 
        self.pos = Vec(plat.left_x() + placement, plat.top_y()) 
        self.width = 55; self.height = 20
        self.name = name
        self.relativePosition = self.pos.copy()
        self.sleepcount = 0

    def startGame(self, game):
        self.game = game
        self.groups = game.all_sprites, game.group_levelGoals, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        # load image from spritesheet
        sheet = self.game.spriteSheet
        self.image = sheet.image_at((0,280,55,20),(0,255,0))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x,self.pos.y)

    def update(self):
        self.rect.midbottom = self.pos.realRound().asTuple()


    def update2(self):
        self.endGoal(self.game.player)


    # Function that gets called whenever the player reaches a goal
    def nextLevel(self):
       
        self.game.resetCamera()
        current = self.game.level.name
        level = int(current[5:6])
        level+=1
        self.game.level.name = f"level{level}"
        self.game.data[0] = self.game.level.name
        self.game.new()

    def endGoal(self, player):
        has_collided = pg.sprite.collide_rect(self, player)
        if has_collided:
            self.game.endinglevel = True
            #self.game.player.image = self.game.player.images['sleep']
            player.image = player.images['sleep']
            self.sleepcount += 1
            if self.sleepcount > 100:
                self.nextLevel()
                self.sleepcount = 0
        else:
            self.sleepcount = 0
            
