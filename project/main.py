# Description:


''' probably not needed'''

''' just for testing?'''

''' really not sure'''

''' pretty sure is needed'''

''' should be revisited'''

''' in use'''




# Imports
import pygame as pg
import sys

from settings import *
from subSprites import *

from Player import *
from Level2 import Level
from Vector import Vec
from SpriteGroup import *
from levelCreator import *
import os.path


def r(number):
    rounded_num = number
    rounded_num = abs(rounded_num)
    rounded_num = math.floor(rounded_num)
    if number < 0:
        rounded_num *= -1
    return rounded_num

def re(number):
    inte = math.floor(number)
    dec = number - inte
    if dec*10 >= 5:
        result = 1
    else:
        result = 0
    return inte + result



# Game Class
class Game:
    # Class Variables

    # Initializer
    def __init__(self):
        pg.init()                                                               # Initializes the pygame module
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TITLE in settings
        self.clock = pg.time.Clock()                                            # Creates a pygame clock object
        self.running = True                                                     # Creates a boolean for running the game
        self.paused = False
        self.click = False
        self.userName = ""
        self.inNameMenu = False
        self.inNameLoadMenu = False
        self.boundary = 600
        self.isDamaged = False
        self.finished = False
        self.outOfLives = False

        # Reads the player data from file and adds it to self.data
        self.data = self.getPlayerData()
        if not self.data:
            self.data = []
            self.data.append(DEFAULT_LEVEL)
            self.data.append(PLAYER_LIVES)
            self.data.append(PLAYER_CATNIP)

    # Creates Sprite Groups
    def createSGroups(self):
    
        #self.all_sprites = pg.sprite.LayeredUpdates()                           # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        self.all_sprites = SpriteGroup()                           # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        
        self.group_platforms          = pg.sprite.Group() #Only applied  to platforms
        self.group_boxes              = pg.sprite.Group() #Only applied to boxes
        self.group_interactiveFields  = pg.sprite.Group()       # Only apllies to the interactive field
        self.group_buttons            = pg.sprite.Group()  # Only applied to button sprite      
        self.group_levers             = pg.sprite.Group()  # Onlt applied to the lever 
        self.group_levelGoals         = pg.sprite.Group()   # Only applied to the levelGoal sprite
        self.group_mugs              = pg.sprite.Group() #Only applied to mugs
        self.group_solid              = SpriteGroup()          # solid objects (formerly rayIntersecters)
        self.group_pickups            = pg.sprite.Group()       # All things that can get picked up by player
        self.group_damager            = pg.sprite.Group()       # All hostiles
        self.group_enemies            = pg.sprite.Group()
        self.group_pressureActivator  = pg.sprite.Group()        # Things that can activate a button
        self.group_passives           = pg.sprite.Group()

    # Method that creates a new level
    def new(self):
        self.finished = False
        # takshdkawd
        self.createSGroups()                #
        
        try:
            self.level
        except:
            pass
        else:
            self.data = self.getPlayerData()
        
        self.level = Level(self)            #                                     
        
        #
        if self.data:
            #print(self.level.name)
            self.level.name = self.data[0]
            print(self.level.name)
        
        #self.level.load(self.level.name)
        
        if not self.level.load(self.level.name):
            self.level.load(DEFAULT_LEVEL)
            self.finished = True
            print('test')
        
        self.player = Player(self.level.spawn)                         #
        self.player.startGame(self)    
        #
        if self.data:
            self.player.lives = self.data[1]
            self.player.catnip_level = self.data[2]    

        #
        try:
            pg.mixer.music.load(self.level.musicTrack)                
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(VOLUME)
        except:
            print("Error loading music!")
            pass
        #self.movingPlat = Platform(270 , 500 , 150 , 40 , "moving" , vel = Vec(1,0), maxDist = 50)
        #self.movingPlat.startGame(self)
        #self.smalltest = Platform(450 , 550 , 50 , 40 , "small tester" )
        #self.smalltest.startGame(self)
        #self.smalltest = Platform(450 , 550 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        #self.smalltest.startGame(self)
        
        
        #self.tallplat   = Platform(850, 430, 20, 50, "tallplat", upMaxDist= 100, downMaxDist = 200)
        #self.tallplat.startGame(self)
        
        #self.enemy = PatrollingEnemy(350, 550 , 26, 30, 100, name =  "pat1")                       #      
        #self.enemy.startGame(self)
        #self.aienemy = AiEnemy(500, 310,36, 28, 200, name =  "ai1")                       #      
        #self.aienemy.startGame(self)
        #self.level_goal     = LevelGoal(1600 , 550, 20, 100, name = 'end goal')                    # 
        #self.level_goal.startGame(self)
        
        # Matthias level things ----------------------------------------------------------------------------------
        # platform moving up at down if lever is active
        '''
        self.smalltest = Platform(450 , 550 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "conMove" : [{"movespeed"  : Vec(0,-1), "target" : self.smalltest} ]

                                }
        self.button4  = Lever(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.button4.startGame(self)
        '''
        # three platforms going above water
        '''
        self.smalltest = Platform(450 , 550 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        self.smalltest2 = Platform(550 , 550 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest2.startGame(self)
        self.smalltest3 = Platform(650 , 550 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest3.startGame(self)
        dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : self.smalltest} ,
                           {"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : self.smalltest2} ,
                           {"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : self.smalltest3}] 
                }
        self.button4  = Button(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.button4.startGame(self)
        '''
        # top platform
        '''
        self.smalltest = Platform(450 , 550 , 50 , 40, "small tester", leftMaxDist = 100, rightMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "move" : [{"movespeed"  : Vec(-1,0), "deactspeed" : Vec(1,0) , "target" : self.smalltest} ]
                                }
        self.button4  = Button(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.button4.startGame(self)
        '''
        # Matthias level things ----------------------------------------------------------------------------------


        # Stine level things ---------------------------------------------------------------------------------
        # Lever A
        """
        self.smalltest = Platform(450 , 550 , 30 , 100, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        self.smalltest2 = Platform(550 , 350 , 50 , 40, "small tester", leftMaxDist = 0, rightMaxDist= 100, vel = Vec(0,0) )
        self.smalltest2.startGame(self)
        self.smalltest = Platform(450 , 550 , 30 , 100, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : self.smalltest},
                           {"movespeed"  : Vec(1,0), "deactspeed" : Vec(-1,0) , "target" : self.smalltest2} ]
                                }
        self.leverA  = Lever(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.leverA.startGame(self)
        """
        # Lever B
        '''
        self.smalltest = Platform(450 , 550 , 30 , 100, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        #self.smallbox = Box(370 , 200 , 44 , 44 , 'box_1')
        dic = {  "move"  : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : self.smalltest}],
                 "spawn" : [{"target": Box(370 , 200 , 44 , 44 , 'box_1')}] 
                  }
        self.leverA  = Lever(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.leverA.startGame(self)
        '''
        #lever F
        '''
        self.smalltest = Platform(450 , 550 , 30 , 100, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : self.smalltest}]
                               }
        self.leverA  = Lever(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.leverA.startGame(self)
        '''
        # Lever E
        """
        self.smallbox = Box(370 , 200 , 44 , 44 , 'box_1')
        self.smallbox.startGame(self)
        dic = { "respawn" : [{"target": self.smallbox}] 
                  }
        self.leverA  = Lever(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic, autodeactivate=True)                                          #
        self.leverA.startGame(self)
        """
        # button C
        '''
        self.smalltest = Platform(450 , 450 , 30 , 100, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : self.smalltest}]
                         q      }
        self.leverA  = Button(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.leverA.startGame(self)
        '''
        # button D
        '''
        self.smalltest = Platform(450 , 450 , 50 , 40, "small tester", upMaxDist = 100, downMaxDist= 0, vel = Vec(0,0) )
        self.smalltest.startGame(self)
        dic = {  "conMove" : [{"movespeed"  : Vec(0,1), "target" : self.smalltest} ]

                                }
        self.button4  = Button(300 , 410 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        self.button4.startGame(self)
        '''
        # Stine level things ---------------------------------------------------------------------------------
        '''
        dic = { "move"    : [{ "movespeed" : Vec(2,0), "deactspeed" : Vec(-2,0), "target" : self.all_sprites.getObject("p_3")}, 
                             { "movespeed" : Vec(0,-1),"deactspeed" : Vec(0,0), "target" : self.all_sprites.getObject("tallplat")}],
                "respawn" : [{"target" : self.all_sprites.getObject('box_1')}]            }
        #self.button4  = Button(600 , 550 , 30 , 20 , name = "boxbutton", effect = dic)                                          #
        #self.button4.startGame(self)
        self.lever1 = Lever(500 , 550 , 10 , 40 , name = "resparnLever",  effect = "respawn",  target = self.all_sprites.getObject("box_1"))
        self.lever1.startGame(self)
        self.catnip = PickUp(600, 370, 16, 16, 'catnip')   
        self.catnip.startGame(self)

        self.health = PickUp(400, 400, 16, 16, 'health')                                          #
        self.catnip = PickUp(600, 370, 16, 16, 'catnip')   
        self.health.startGame(self)
        self.catnip.startGame(self)
        #self.movingPlat = Platform(self, 300 , 500 , 150 , 40 )
        
        #self.button  = Button(self,400 , 550 , 30 , 20 , name = "boxbutton", effect = ["move"], movespeed = Vec(2,0),  target = self.all_sprites.getObject("p_3"))                                          #
        #self.button2 = Button(self,450 , 550 , 30 , 20 , na me = "boxbutton2", effect = ["move"], movespeed = Vec(-2,0),  target = self.all_sprites.getObject("p_3"))                                          #
        #self.button2 = Button(self,450 , 550 , 30 , 20 , name = "boxbutton3", effect = ["respawn"],  target = self.all_sprites.getObject("box_1"))                                          #
        self.button4  = Button(self,400 , 550 , 30 , 20 , name = "boxbutton", effect = ["move"], movespeed = Vec(0,-2),  target = self.all_sprites.getObject("tallplat"))                                          #

        self.lever1 = Lever(450 , 550 , 10 , 40 , name = "boxlever",  effect = "move", movespeed = 2,  target = self.all_sprites.getObject("p_3"),  autodeactivate = True)
        self.water = Water(500, 400, 10, 10)    
        self.water.startGame(self)     
        ''' 
        
        #
        self.image = pg.Surface((WIDTH,HEIGHT))
        
        self.darkener = self.image.get_rect()

        #self.darkener = pg.Rect(0,0,WIDTH, HEIGHT)
        self.endinglevel = False
        self.sleepcount = 0
        self.refreshedInt_lever     = False                                                       
        self.refreshedInt_box       = False                                                  
        self.interactive_field      = None                                       
        self.frames                 = 0                                                         
        self.refreshCount           = 0                                                        
        self.refreshCount_prev      = 0                                                   
        self.relposx                = 0   
        self.relposp                = 0                                                    
        self.realposp               = 0       
        self.rel_fitToPlayer        = - WIDTH/2 + self.player.pos.x #half screen - pos         
        self.relposx = self.rel_fitToPlayer     
        self.paused = False                                  
        self.run()                                  # Runs the game

    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     
        while self.playing:                                                     
            self.clock.tick(FPS)                    # Changing our tickrate so that our frames per second will be the same as FPS from settings
            
            # Checking frame time for performance (keep commented)
            '''
            self.frames += 1
            if (self.frames >= 60):
                print("new frame")
                self.frames = 0
            print(self.clock.get_rawtime())
            '''
            
            # Runs all our methods on loop:
            #self.new()
            #self.update()
            self.events()  
            
            if self.paused:
                if self.isDamaged:
                    pass
                else:
                    self.displayPauseScreen()
            if not self.paused:                                              
                self.update()
                self.displayHUD()  
            if self.finished:
                self.endGameHUD()        
            if self.player.lives <= 0:
                self.playing = False
                self.outOfLives = True
                self.inNameMenu = False
                self.inNameLoadMenu = False
                #add function to delete playerdata file
            self.draw()  
            
            
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    # Method where we update game processesd
    def update(self):
        self.all_sprites.resetSprites()
        #print(f'NEW RUN')
        
        # I think this should somehow go into CustomSprite/subsprites
        #for sprite in self.group_pressureActivator:
         #   sprite.buttonPress()
        
        #for button in self.group_buttons:
         #   activated_button = button.buttonPress(self.group_pressureActivator)
        
        #self.refreshedInt_lever = self.refreshCount > self.refreshCount_prev      #
        #self.refreshedInt_box = self.refreshCount >= self.refreshCount_prev       #
        
        
        #self.player.touchPickUp(self.group_pickups)
        # Updating Functionsdd
        #
        """
        if self.interactive_field:
            for lever in self.group_levers:
                lever.leverPull(self.group_interactiveFields, self.refreshedInt_lever)
    
            self.interactive_field.pickupSprite(self.group_boxes, self.refreshedInt_box, self.intWasCreated)
            self.interactive_field.knockOver(self.group_mugs, self.intWasCreated)
        #print(f'BEFORE UPDATES')
        """
        """Adds velocity to something when on something moving.
        bad solution. Only works with two stacks :(
        """
        #for plat in self.group_solid:
         #   plat.collisionEffect()
        
        for plat in self.group_solid:
            plat.collisionEffect()
        self.all_sprites.update()
        #self.player.touchEnemy(self.group_damager) # was above update() before. Did this stop the damaging?

        self.all_sprites.updatePos()
        self.moveScreen()
        self.relativePos()

        #self.all_sprites.correctPositions()
        #self.level_goal.endGoal(self.player)
        if (self.player.pos.y > self.boundary):
            self.player.takeDamage()
        # Updating Variables
        #self.intWasCreated = False    
        #self.refreshCount_prev = self.refreshCount

    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                if self.playing:                                                # Sets playing to false if it's running (for safety measures)
                    self.playing = False                                        
                self.running = False                                            # Sets running to false
                self.inMenu = False
                self.inNameMenu = False
                self.inNameLoadMenu = False
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user has any keys pressed down
                if event.key == pg.K_q:                                         # checks if the uses presses the escape key
                    if self.playing:                                            # Does the same as before
                        self.playing = False                                        
                    self.running = False        
                    self.inNameMenu = False
                    self.inNameLoadMenu = False

                if event.key == pg.K_e:                                         # checks if the uses presses the escape key                               
                    self.new()
                if event.key  == pg.K_p:
                    self.paused = not self.paused
                    self.isDamaged = False
            """    
                if event.key == pg.K_d:                                         # Checks if the uses presses 
                    # if not paused?
                    self.refreshCount_prev = self.refreshCount
                    self.interactive_field = Interactive(self,self.player, self.player.facing)
                    self.intWasCreated = True
                    self.refreshCount += 1
                                           
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    if self.interactive_field:
                        self.interactive_field.kill()
                        self.interactive_field = None
            """
    # Method for drawing everything to the screen           
    def draw(self):                                         
        self.screen.fill(BGCOLOR)                           # Sets the background color to default in Settings 
        
        # Loop that updates rectangles?
        for sprite in self.all_sprites:
            sprite.updateRect()
        

        self.all_sprites.draw(self.screen)                  # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        self.group_passives.draw(self.screen)
        self.darkenScreen()
        self.screen.blit(self.lives_display,  (50, 50))
        
        self.screen.blit(self.points_display,  (400, 50))
        if self.paused:
            pauseRect = self.pauseText.get_rect()
            pauseRect.center = (300, 150)
            self.screen.blit(self.pauseText, pauseRect)
            pauseRect2 = self.pauseText2.get_rect()
            pauseRect2.center = (300, 250)
            self.screen.blit(self.pauseText2, pauseRect2)
            pauseRect3 = self.pauseText3.get_rect()
            pauseRect3.center = (300, 350)
            self.screen.blit(self.pauseText3, pauseRect3)
        if self.finished:
            endRect = self.endText.get_rect()
            endRect.center = (300, 150)
            self.screen.blit(self.endText, endRect)
            endRect2 = self.endText2.get_rect()
            endRect2.center = (300, 250)
            self.screen.blit(self.endText2, endRect2)
        
        
        pg.display.update()                                 # Updates the drawings to the screen object and flips it
        
        # Loop that resets rectangles?
        for sprite in self.all_sprites:
            sprite.resetRects()
  
    def darkenScreen(self):

        if self.endinglevel == True:
            self.sleepcount += 1
            if self.sleepcount > 100:
                self.endinglevel = False
                self.sleepcount = 0
            #pg.draw.rect(self.screen, (0,0,0, self.sleepcount), (0,0,WIDTH, HEIGHT))
            #self.image.set_alpha(self.sleepcount)
            #self.darkener = self.image.get_rect()
            #self.screen.blit(self.image, (0,0))
            #pg.display.flip()
            #self.screen.set_alpha(self.sleepcount)

            



    # Method for moving everything on the screen relative to where the player is moving
    def moveScreen(self):
        #if self.player.right_x()>= r(CAMERA_BORDER_R + self.relposx) :                                               # If the player moves to or above the right border of the screen
        if self.player.vel.x + self.player.acc.x * 0.5 > 0:
            self.relposx += self.player.vel.x + self.player.acc.x * 0.5
            self.relposp = 0
        #if self.player.left_x()<= r(CAMERA_BORDER_L+self.relposx):
        if self.player.vel.x + self.player.acc.x * 0.5 < 0:
            self.relposx += self.player.vel.x + self.player.acc.x * 0.5
            self.relposp = 0

        """
        if self.player.right_x()>= r(CAMERA_BORDER_R + self.relposx) :                                               # If the player moves to or above the right border of the screen
            if self.player.vel.x > 0:
                self.relposx += self.player.vel.x+ self.player.acc.x * 0.5
        if self.player.left_x()<= r(CAMERA_BORDER_L+self.relposx):
            if self.player.vel.x < 0:
                self.relposx += self.player.vel.x+ self.player.acc.x * 0.5
                self.relposp = 0
        """
        
   
    # 
    def relativePos(self):
        for sprite in self.all_sprites:
            
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x = sprite.relativePosition.x-self.relposx
            

    # Respawns the player and resets the camera
    def resetCamera(self):
        for sprite in self.all_sprites:
            self.relposx = 0
            self.relposp = 0
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()


    def mainMenu(self):
        self.inMenu = True
        selectedButton  = pg.Rect(75, 50, 50, 50)
        self.selectedState = 0
        self.activateSelected = False
        self.new()
        #while self.inMenu:
        while self.playing:
            #self.events()q
            self.run()
            """
            if self.outOfLives:
                self.noLivesScreen()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()
            mx, my = pg.mouse.get_pos()
            newGameButton   = pg.Rect(190, 25, 220, 100)
            loadGameButton  = pg.Rect(190, 175, 220, 100)
            tutorialButton  = pg.Rect(190, 325, 220, 100)
            exitButton      = pg.Rect(190, 475, 220, 100)


            pg.draw.rect(self.screen, (0, 125, 255), newGameButton)
            pg.draw.rect(self.screen, (0, 125, 255), loadGameButton)
            pg.draw.rect(self.screen, (0, 125, 255), tutorialButton)
            pg.draw.rect(self.screen, (0, 125, 255), exitButton)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if (self.selectedState %4) == 0:
                selectedButton  = pg.Rect(75, 50, 50, 50)
                if self.activateSelected:
                    self.nameInput()
            elif (self.selectedState %4) == 1:
                selectedButton  = pg.Rect(75, 200, 50, 50)
                if self.activateSelected:
                    self.nameLoadScreen()
            elif (self.selectedState %4) == 2:
                selectedButton  = pg.Rect(75, 350, 50, 50)
                if self.activateSelected:
                    self.tutorialScreen()
            else:
                selectedButton  = pg.Rect(75, 500, 50, 50)
                if self.activateSelected:
                    self.inMenu = False
                    self.running = False
            
            if newGameButton.collidepoint((mx, my)):
                self.selectedState = 0
                if self.click:
                    self.nameInput()
            if loadGameButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:
                    self.new()
            if tutorialButton.collidepoint((mx, my)):
                self.selectedState = 2
                if self.click:
                    self.tutorialScreen()
            if exitButton.collidepoint((mx, my)):
                self.selectedState = 3
                if self.click:
                    self.inMenu = False
                    self.running = False
            
            self.activateSelected = False
            self.click = False
            self.drawMenuText("New Game", 300, 75)
            self.drawMenuText("Load Game", 300, 225)
            self.drawMenuText("Tutorial", 300, 375)
            self.drawMenuText("Quit", 300, 525)
            
            pg.display.update()
            """
    def tutorialScreen(self):
        self.inTutorial = True
        self.activateSelected = False
        self.selectedState = 0

        while self.inTutorial:
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()
            mx, my = pg.mouse.get_pos()
            returnButton   = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)

            selectedButton  = pg.Rect(75, 500, 50, 50)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if self.activateSelected:
                self.inTutorial = False

            if self.click:
                if returnButton.collidepoint((mx, my)):
                    self.inTutorial = False
            self.activateSelected = False
            
            self.click = False
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText("Use arrow keys to move left/right", 300, 50, 30)
            self.drawMenuText("Press space to jump", 300, 100, 30)
            self.drawMenuText("Press P to pause", 300, 150, 30)
            self.drawMenuText("Press Q to quit", 300, 200, 30)
            self.drawMenuText("Press D to interact", 300, 250, 30)

            pg.display.update()

    def noLivesScreen(self):
        self.activateSelected = False
        self.selectedState = 0


        while self.outOfLives:
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()
            mx, my = pg.mouse.get_pos()
            returnButton   = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)

            selectedButton  = pg.Rect(75, 500, 50, 50)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if self.activateSelected:
                self.outOfLives = False

            if self.click:
                if returnButton.collidepoint((mx, my)):
                    self.outOfLives = False
            self.activateSelected = False
            
            self.click = False
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText(f'Player '+self.userName+' has run out of lives', 300, 50, 30)
            self.drawMenuText("Press Q to quit", 300, 200, 30)

            pg.display.update()

    def nameInput(self):
        self.inNameMenu = True
        self.userName = ""
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        while self.inNameMenu:
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

            mx, my = pg.mouse.get_pos()
            startButton   = pg.Rect(190, 325, 220, 100)
            returnButton  = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), startButton)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText("Start", 300, 375)
            self.drawMenuText("Please enter a name", 300, 100)
            if self.nameError:
                self.drawMenuText("Invalid name entered", 300, 300)


            if (self.selectedState %2) == 0:
                selectedButton  = pg.Rect(75, 350, 50, 50)
                if self.activateSelected:
                    if not self.userName == "":
                        if not self.checkNameConflict():
                            self.data = self.createPlayerData()
                            self.new()
                        else:
                            self.nameError = True
                            self.activateSelected = False 
                    else:
                        self.nameError = True
                        self.activateSelected = False
            elif (self.selectedState %2) == 1:
                selectedButton  = pg.Rect(75, 500, 50, 50)
                if self.activateSelected:
                    self.inNameMenu = False
                    self.selectedState = 0


            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)
            

            for event in pg.event.get():
                if event.type == pg.QUIT:                                   
                    self.inMenu = False
                    self.running = False
                    self.inTutorial = False  
                    self.inNameMenu = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True 
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.userName = self.userName[:-1]
                    elif event.key == pg.K_RETURN:
                        self.activateSelected = True
                    elif event.key == pg.K_UP:
                        self.selectedState += 1
                    elif event.key == pg.K_DOWN:
                        self.selectedState -= 1
                    else:
                        self.userName += event.unicode
            self.drawMenuText(self.userName, 300, 150)

            
            if returnButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:
                    self.inNameMenu = False
                    self.selectedState = 0
            if startButton.collidepoint((mx, my)):
                self.selectedState = 0
                if self.click:
                    if not self.userName == "":
                        self.new()
                    else:
                        self.nameError = True



            self.click = False
            pg.display.update()

            
    def nameLoadScreen(self):
        self.inNameLoadMenu = True
        self.userName = ""
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        while self.inNameLoadMenu:
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

            mx, my = pg.mouse.get_pos()
            startButton   = pg.Rect(190, 325, 220, 100)
            returnButton  = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), startButton)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText("Start", 300, 375)
            self.drawMenuText("Please enter a name to load", 300, 100)
            if self.nameError:
                self.drawMenuText("Invalid name entered", 300, 300)


            if (self.selectedState %2) == 0:
                selectedButton  = pg.Rect(75, 350, 50, 50)
                if self.activateSelected:
                    if self.checkNameConflict():
                        self.data = self.getPlayerData()
                        print(self.data)
                        self.new()
                    else:
                        self.nameError = True
                        self.activateSelected = False 
                    
            elif (self.selectedState %2) == 1:
                selectedButton  = pg.Rect(75, 500, 50, 50)
                if self.activateSelected:
                    self.inNameLoadMenu = False
                    self.selectedState = 0


            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)
            

            for event in pg.event.get():
                if event.type == pg.QUIT:                                   
                    self.inMenu = False
                    self.running = False
                    self.inTutorial = False  
                    self.inNameLoadMenu = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True 
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.userName = self.userName[:-1]
                    elif event.key == pg.K_RETURN:
                        self.activateSelected = True
                    elif event.key == pg.K_UP:
                        self.selectedState += 1
                    elif event.key == pg.K_DOWN:
                        self.selectedState -= 1
                    else:
                        self.userName += event.unicode
            self.drawMenuText(self.userName, 300, 150)

            
            if returnButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:
                    self.inNameLoadMenu = False
                    self.selectedState = 0
            if startButton.collidepoint((mx, my)):
                self.selectedState = 0
                if self.click:
                    if not self.userName == "":
                        self.new()
                    else:
                        self.nameError = True



            self.click = False
            pg.display.update()

    def checkNameConflict(self):
        result = os.path.exists("playerData/"+self.userName+"Data.txt")
        return result
    
    def menuEvents(self):
        for event in pg.event.get():                                
            
            if event.type == (pg.QUIT):                                   
                self.inMenu = False
                self.running = False
                self.inTutorial = False  
                self.inNameMenu = False
                self.inNameLoadMenu = False
                self.outOfLives = False


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:                                    # checks if the uses presses the escape key
                    self.inMenu = False                                        
                    self.running = False
                    self.inTutorial = False  
                    self.inNameMenu = False
                    self.inNameLoadMenu = False
                    self.outOfLives = False
                if event.key == pg.K_RETURN:
                    self.activateSelected = True
                if event.key == pg.K_DOWN:
                    self.selectedState += 1
                if event.key == pg.K_UP:
                    self.selectedState -= 1
             
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True                                       

    def drawMenuText(self, text, x, y, fontsize = 40):
        drawText = self.textToDisplay(text, fontsize = fontsize)
        textRect = drawText.get_rect()
        textRect.center = (x,y)
        self.screen.blit(drawText, textRect)

    # Gets the current level and player date to save to a player file for saving progress
    def createPlayerData(self):
        try:
            file = open("playerData/"+self.userName+"Data.txt","x")
        except:
            file = open("playerData/"+self.userName+"Data.txt","w")

        newlevelName = "level1"
        newlives = "9"
        newcatnip = "0"

        file.write(f"{newlevelName},{newlives},{newcatnip}")
        file.close()
        print(file)
        return [newlevelName,int(newlives),int(newcatnip)]



    def updateData(self):
        try:
            file = open("playerData/"+self.userName+"Data.txt","x")
        except:
            file = open("playerData/"+self.userName+"Data.txt","w")

        levelName = self.level.name
        lives = str(self.player.lives)
        catnip = str(self.player.catnip_level)

        file.write(f"{levelName},{lives},{catnip}")
        file.close()

        return [levelName,int(lives),int(catnip)]

    # Gets player data from file
    def getPlayerData(self):
        try:
            file = open("playerData/"+self.userName+"Data.txt","r")
            data = file.read().split(",")
            data[1] = int(data[1])
            data[2] = int(data[2])
            return data
        except IOError:
            print("No playerdata found")
            return None

    def displayHUD(self):
        self.lives_display  = self.textToDisplay(f'Lives: {self.player.lives}')
        self.points_display = self.textToDisplay(f'Catnip: {self.player.catnip_level}')

    def endGameHUD(self):
        deathFont = pg.font.Font("resources/gypsy-curse.regular.ttf", 70)
        self.endText = deathFont.render("Congratulations", True, (255, 0 ,0))
        self.endText2 = deathFont.render("You have finished the game", True, (255, 0 ,0))

 
    def displayPauseScreen(self):
        self.pauseText = self.textToDisplay("Game is paused", color= (0,0,0), bold= True)
        self.pauseText2 = self.textToDisplay("Press P to resume", color= (0,0,0), bold= True)
        self.pauseText3 = self.textToDisplay("Press Q to quit", color= (0,0,0), bold= True)

    
    def damageScreen(self):
        deathFont = pg.font.Font("resources/gypsy-curse.regular.ttf", 70)
        self.pauseText = deathFont.render("YOU DIED", True, (255, 0 ,0))
        self.pauseText2 = self.textToDisplay("Press P to resume", color= (0,0,0), bold= True)
        self.pauseText3 = self.textToDisplay("Press Q to quit", color= (0,0,0), bold= True)


    def textToDisplay(self, text, font = 'Comic Sans MS', fontsize = 40, bold = False, italic = False, color = (255,255,255) ):
        font = pg.font.SysFont(font, fontsize, bold, italic)
        return font.render(text, True, color)

# Game Loop
# create objects and dicts
level1 = createLevel1()
level2 = createLevel2()
level3 = createLevel3()

# pickle levels
pickleLevel(level3, 'level1')
pickleLevel(level1, 'level3')
pickleLevel(level2, 'level2')

g = Game()                                                                      # Creates a game instance                                                                                # While loop checking the Game.running boolean
#g.new()                                                                         # Creates a new running process, if broken without stopping the game from running it will restart
g.mainMenu()
#g.run()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
