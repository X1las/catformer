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
from Sprites import *

from player import *
from Level import Level
from Vector import Vec
from SpriteGroup import *
from levelCreator import *
import os
import Spritesheet as ss

# Game Class
class Game:
    # Class Variables
    paused = False
    click = False
    userName = ""                                                               # Used for saving and loading level progress based on given name
    inNameMenu = False                                                          # Boolean used for nameMenu loop
    inNameLoadMenu = False                                                      # Boolean used for nameLoadMenu loop
    boundary = 600                                                              # default value for lower player boundary
    isDamaged = False                                                           # Boolean used for damage HUD after life is lost
    finished = False                                                            # Boolean used for endGame HUD when final level is reached
    outOfLives = False                                                          # Boolean used for outOfLives loop

    # Initializer
    def __init__(self):

        ''' probably not needed'''

        ''' just for testing?'''

        ''' really not sure'''

        ''' pretty sure is needed'''

        ''' should be revisited'''

        ''' in use'''
        pg.init()                                                               # Initializes the pygame module
        pg.mixer.init()
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TITLE in settings
        self.clock = pg.time.Clock()                                            # Creates a pygame clock object
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings
        self.frames                 = 0                                                         

        # Reads the player data from file and adds it to self.data
        self.data = self.getPlayerData()
        if not self.data:
            self.data = []
            self.data.append(DEFAULT_LEVEL)
            self.data.append(PLAYER_LIVES)
            self.data.append(PLAYER_CATNIP)

        # load images and sprite sheets
        self.spriteSheet   = ss.Spritesheet('resources/spritesheet_green.png')
        self.dogSheet      = ss.Spritesheet('resources/Hyena_walk.png')
        self.platformSheet = ss.Spritesheet('resources/platforms.png')
        self.wormSheet     = ss.Spritesheet('resources/worm-spritesheet.png')

        bg = pg.image.load("resources/bg.png")
        self.bg = pg.transform.scale(bg, (WIDTH+400, HEIGHT))

    # Creates Sprite Groups
    def createSGroups(self):

    
        #self.all_sprites = pg.sprite.LayeredUpdates()                          # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        self.all_sprites = SpriteGroup()                                        # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        
        self.group_platforms          = pg.sprite.Group()                       # Only applied  to platforms
        self.group_boxes              = pg.sprite.Group()                       # Only applied to boxes
        self.group_interactiveFields  = pg.sprite.Group()                       # Only apllies to the interactive field
        self.group_buttons            = pg.sprite.Group()                       # Only applied to button sprite      
        self.group_levers             = pg.sprite.Group()                       # Only applied to the lever 
        self.group_levelGoals         = pg.sprite.Group()                       # Only applied to the levelGoal sprite
        self.group_mugs               = pg.sprite.Group()                       # Only applied to mugs
        self.group_solid              = SpriteGroup()                           # solid objects (formerly rayIntersecters)
        self.group_pickups            = pg.sprite.Group()                       # All things that can get picked up by player
        self.group_damager            = pg.sprite.Group()                       # All hostiles
        self.group_enemies            = pg.sprite.Group()
        self.group_pressureActivator  = pg.sprite.Group()                       # Things that can activate a button
        self.group_movables           = pg.sprite.Group()

        self.framecount = 0
        self.accumframes = 0


    # Method that creates a new level
    def new(self):
        self.finished = False
        self.createSGroups()                                                    # Creates all the sprite groups
        
        try:
            self.level
            self.data = self.getPlayerData()
        except:
            pass
        
        self.level = Level(self)            #                                     
        
        # Removes player's save file if all levels are finished
        if self.data:
            self.level.name = self.data[0]
            if self.level.name == "level4":
                #sself.finished = True
                if os.path.exists("playerData/"+self.userName+"Data.txt"):
                    os.remove("playerData/"+self.userName+"Data.txt")
        
        if not self.level.load(self.level.name):
            self.level.load(DEFAULT_LEVEL)
        
        self.player = Player(self.level.spawn)                         #
        self.player.startGame(self)    
        #
        if self.data:
            self.player.lives = self.data[1]
            self.player.catnip_level = self.data[2]    

        # Probably delete!
        try:
            pg.mixer.music.load(self.level.musicTrack)                
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(VOLUME)
        except:
            print("Error loading music!")

        self.paused = False                                  
        self.run()                                  # Runs the game

    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     
        while self.playing:                                                     
            self.clock.tick(FPS)                    # Changing our tickrate so that our frames per second will be the same as FPS from settings
            
            # Checking frame time for performance (keep commented)
            self.framecount += 1
            self.accumframes += self.clock.get_rawtime()
            self.frames += 1
            if (self.frames >= 60):
                #print("new frame")
                self.frames = 0
            if self.framecount > 60*4:
                print(f'{self.accumframes/self.framecount}')
                self.accumframes = 0
                self.framecount = 0
            #print(self.clock.get_rawtime())
            
            
            # Runs all our methods on loop:
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
                if os.path.exists("playerData/"+self.userName+"Data.txt"):
                    os.remove("playerData/"+self.userName+"Data.txt")
                #add function to delete playerdata file
            self.draw()  
            
            
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    # Method where we update game processesd
    def update(self):
        self.all_sprites.resetSprites()
    
        ''' do not delete'''
        #for plat in self.group_solid:
         #   plat.collisionEffect()
        
        for plat in self.group_solid:
            plat.collisionEffect()
        self.all_sprites.update()

        self.all_sprites.updatePos()
        self.moveScreen()

      
    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                if os.path.exists("playerData/"+self.userName+"Data.txt"):       #return true/false if file exists/does not
                    self.saveData(levelname = self.level.name, lives = self.player.lives, catnip = self.player.catnip_level)
                if self.playing:                                                # Sets playing to false if it's running (for safety measures)
                    self.playing = False                                        
                self.inMenu = False
                self.inNameMenu = False
                self.inNameLoadMenu = False
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user has any keys pressed down
                
                if event.key == pg.K_q:                                         # checks if the uses presses the escape key
                    if os.path.exists("playerData/"+self.userName+"Data.txt"):       #return true/false if file exists/does not
                        self.saveData(levelname = self.level.name, lives = self.player.lives, catnip = self.player.catnip_level)
                    if self.playing:                                            # Does the same as before
                        self.playing = False                                        
                    self.inNameMenu = False
                    self.inNameLoadMenu = False

                # restart the level
                if event.key == pg.K_r:                                         # checks if the uses presses the escape key                               
                    self.new()
                if event.key  == pg.K_p:
                    self.paused = not self.paused
                    self.isDamaged = False
     
    # Method for drawing everything to the screen           
    def draw(self):                                         
        self.screen.blit(self.bg, (0,0))                    # Draws background image
        self.all_sprites.updateRects()
        self.all_sprites.draw(self.screen)                  # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        self.drawHUD()
        pg.display.update()                                 # Updates the drawings to the screen object and flips it
        self.all_sprites.resetRects()
  
    def drawHUD(self):
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
        
    # Method for moving everything on the screen relative to where the player is moving
    def moveScreen(self):
        relative = self.player.pos.x - WIDTH/2
        for sprite in self.all_sprites:
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x = sprite.pos.x-relative
            


    # Respawns the player and resets the camera
    def resetCamera(self):
        self.rel_fitToPlayer        = - WIDTH/2 + self.player.pos.x #half screen - pos         
        self.relposx = self.rel_fitToPlayer     
        for sprite in self.all_sprites:
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()

    #creates a main menu for the game
    def mainMenu(self):
        self.inMenu = True
        selectedButton  = pg.Rect(75, 50, 50, 50)
        self.selectedState = 0
        self.activateSelected = False

        while self.inMenu:
            if self.outOfLives:                                              #opening no lives screen if the player runs out of lives
                self.noLivesScreen()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()                                                #getting user input
            mx, my = pg.mouse.get_pos()                                      #getting mouse position
            newGameButton   = pg.Rect(190, 25, 220, 100)                     #creating buttons
            loadGameButton  = pg.Rect(190, 175, 220, 100)
            tutorialButton  = pg.Rect(190, 325, 220, 100)
            exitButton      = pg.Rect(190, 475, 220, 100)

            pg.draw.rect(self.screen, (0, 125, 255), newGameButton)          #drawing buttons on screen
            pg.draw.rect(self.screen, (0, 125, 255), loadGameButton)
            pg.draw.rect(self.screen, (0, 125, 255), tutorialButton)
            pg.draw.rect(self.screen, (0, 125, 255), exitButton)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if (self.selectedState %4) == 0:                                 #getting currently selected item based on arrow key presses
                selectedButton  = pg.Rect(75, 50, 50, 50)                    #setting position of currently selected indicator
                if self.activateSelected:                                    #if enter is pressed call a function
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
                if self.activateSelected:                                    #break out of main menu loop if exit is pressed
                    self.inMenu = False
            
            if newGameButton.collidepoint((mx, my)):                         #checking if mouse position is on a button
                self.selectedState = 0                                       #setting position of currently selected indicator
                if self.click:                                               #if mouse1 is clicked call a function
                    self.nameInput()
            if loadGameButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:
                    self.nameLoadScreen()
            if tutorialButton.collidepoint((mx, my)):
                self.selectedState = 2
                if self.click:
                    self.tutorialScreen()
            if exitButton.collidepoint((mx, my)):
                self.selectedState = 3
                if self.click:                                               #break out of main menu loop if exit is pressed
                    self.inMenu = False
            
            self.activateSelected = False                                    #reset value if enter is pressed
            self.click = False                                               #reset value if mouse1 is pressed
            self.drawMenuText("New Game", 300, 75)                           #drawing text on buttons
            self.drawMenuText("Load Game", 300, 225)
            self.drawMenuText("Tutorial", 300, 375)
            self.drawMenuText("Quit", 300, 525)
            
            pg.display.update()                                              #updating the screen


        #creates tutorial screen
    def tutorialScreen(self):
        self.inTutorial = True
        self.activateSelected = False
        self.selectedState = 0

        while self.inTutorial:                                               #tutorial loop
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()                                                #getting user input
            mx, my = pg.mouse.get_pos()                                      #getting mouse position
            returnButton   = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)

            selectedButton  = pg.Rect(75, 500, 50, 50)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if self.activateSelected:                                        #if return is pressed break tutorial loop
                self.inTutorial = False

            if self.click:
                if returnButton.collidepoint((mx, my)):                      #if return is pressed break tutorial loop
                    self.inTutorial = False
            self.activateSelected = False
            
            self.click = False
            self.drawMenuText("Return", 300, 525)                            #drawing tutorial text
            self.drawMenuText("Use arrow keys to move left/right", 300, 50, 30)
            self.drawMenuText("Press space to jump", 300, 100, 30)
            self.drawMenuText("Press P to pause", 300, 150, 30)
            self.drawMenuText("Press Q to quit", 300, 200, 30)
            self.drawMenuText("Press D to interact", 300, 250, 30)

            pg.display.update()                                              #updating display


        #screen for when player runs out of lives
    def noLivesScreen(self):
        self.activateSelected = False
        self.selectedState = 0


        while self.outOfLives:                                               #no lives menu loop
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            self.menuEvents()                                                #get user input
            mx, my = pg.mouse.get_pos()                                      #get mouse position
            returnButton   = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)

            selectedButton  = pg.Rect(75, 500, 50, 50)
            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)

            if self.activateSelected:                                        #break no lives loop if return is pressed
                self.outOfLives = False

            if self.click:                                                   #break no lives loop if return is pressed
                if returnButton.collidepoint((mx, my)):
                    self.outOfLives = False
            self.activateSelected = False
            
            self.click = False
            self.drawMenuText("Return", 300, 525)                            #drawing text
            self.drawMenuText(f'Player '+self.userName+' has run out of lives', 300, 50, 30)
            self.drawMenuText("Press Q to quit", 300, 200, 30)

            pg.display.update()                                              #updating screen


        #menu for user name input
    def nameInput(self):
        self.inNameMenu = True
        self.userName = ""                                                   #reseting inputed name
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        while self.inNameMenu:                                               #name input loop
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

            mx, my = pg.mouse.get_pos()                                      #get mouse position
            startButton   = pg.Rect(190, 325, 220, 100)
            returnButton  = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), startButton)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText("Start", 300, 375)
            self.drawMenuText("Please enter a name", 300, 100)
            if self.nameError:                                               #error message if invalid name entered
                self.drawMenuText("Invalid name entered", 300, 300)


            if (self.selectedState %2) == 0:
                selectedButton  = pg.Rect(75, 350, 50, 50)
                if self.activateSelected:
                    if not self.userName == "":                              #check if name is not empty
                        if not self.checkNameConflict():                     #check if name does not exist already
                            self.data = self.saveData()
                            #self.createPlayerData()              #creates default playerdata file
                            self.new()                                       #opens the game
                        else:
                            self.nameError = True                            #give error message
                            self.activateSelected = False 
                    else:
                        self.nameError = True                                #give error message
                        self.activateSelected = False
            elif (self.selectedState %2) == 1:
                selectedButton  = pg.Rect(75, 500, 50, 50)
                if self.activateSelected:                                    #breaks name input loop if return
                    self.inNameMenu = False 
                    self.selectedState = 0


            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)
            

            for event in pg.event.get():                                     #custon menu events to allow typing name
                if event.type == pg.QUIT:                                   
                    self.inMenu = False
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
                    elif(pg.K_0 <= event.key <= pg.K_9 or pg.K_a <= event.key <= pg.K_z):
                        if not event.unicode == "*":
                            self.userName += event.unicode
            self.drawMenuText(self.userName, 300, 150)                       #drawing name on screen

            
            if returnButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:
                    self.inNameMenu = False                                  #breaks name input loop if return is pressed
                    self.selectedState = 0
            if startButton.collidepoint((mx, my)):
                self.selectedState = 0
                if self.click:
                    if not self.userName == "":                              #check if name is not empty
                        if not self.checkNameConflict():                     #check if name does not exist already
                            #self.data = self.createPlayerData()              #creates default playerdata file
                            self.data = self.saveData()              #creates default playerdata file
                            self.new()                                       #opens the game
                        else:
                            self.nameError = True                            #give error message
                    else:
                        self.nameError = True                                #gives error message



            self.click = False
            pg.display.update()                                              #updating display

            #menu for loading a game
    def nameLoadScreen(self):
        self.inNameLoadMenu = True
        self.userName = ""
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        while self.inNameLoadMenu:                                           #load screen loop
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

            mx, my = pg.mouse.get_pos()                                      #get mouse position
            startButton   = pg.Rect(190, 325, 220, 100)
            returnButton  = pg.Rect(190, 475, 220, 100)
            pg.draw.rect(self.screen, (0, 125, 255), startButton)
            pg.draw.rect(self.screen, (0, 125, 255), returnButton)
            self.drawMenuText("Return", 300, 525)
            self.drawMenuText("Start", 300, 375)
            self.drawMenuText("Please enter a name to load", 300, 100)
            if self.nameError:                                               #error message
                self.drawMenuText("Invalid name entered", 300, 300)


            if (self.selectedState %2) == 0:
                selectedButton  = pg.Rect(75, 350, 50, 50)
                if self.activateSelected:
                    if self.checkNameConflict():                             #check if name exists
                        self.data = self.getPlayerData()                     #reading data file for that name
                        self.new()                                           #opening the game
                    else:
                        self.nameError = True                                #show error message
                        self.activateSelected = False 
                    
            elif (self.selectedState %2) == 1:
                selectedButton  = pg.Rect(75, 500, 50, 50)
                if self.activateSelected:                                    #break load screen loop
                    self.inNameLoadMenu = False
                    self.selectedState = 0


            pg.draw.rect(self.screen, (255, 125, 0), selectedButton)
            

            for event in pg.event.get():                                     #custom events for typing
                if event.type == pg.QUIT:                                   
                    self.inMenu = False
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
                    elif(pg.K_0 <= event.key <= pg.K_9 or pg.K_a <= event.key <= pg.K_z):
                        if not event.unicode == "*":
                            self.userName += event.unicode
            self.drawMenuText(self.userName, 300, 150)                       #drawing name on screen

            
            if returnButton.collidepoint((mx, my)):
                self.selectedState = 1
                if self.click:                                               #breaking load screen loop if return is pressed
                    self.inNameLoadMenu = False
                    self.selectedState = 0
            if startButton.collidepoint((mx, my)):
                self.selectedState = 0
                if self.click:
                    if self.checkNameConflict():                             #checking if name exists
                        self.data = self.getPlayerData()                     #reading data from file with that name
                        self.new()                                           #loading the game
                    else:
                        self.nameError = True                                #showing error message



            self.click = False
            pg.display.update()                                              #updating the display

        #check for name conflicts
    def checkNameConflict(self):
        return os.path.exists("playerData/"+self.userName+"Data.txt")       #return true/false if file exists/does not

        #getting user input for menu screens
    def menuEvents(self):
        for event in pg.event.get():                                
            
            if event.type == (pg.QUIT):                                      #breaks all loops if QUIT is pressed
                self.inMenu = False
                self.inTutorial = False  
                self.inNameMenu = False
                self.inNameLoadMenu = False
                self.outOfLives = False


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:                                      #breaks all loops if q is pressed
                    #self.saveData(levelname = self.level.name, lives = self.player.lives, catnip = self.player.catnip_level)

                    self.inMenu = False                                        
                    self.inTutorial = False  
                    self.inNameMenu = False
                    self.inNameLoadMenu = False
                    self.outOfLives = False
                if event.key == pg.K_RETURN:                                 #sets value to true if enter is pressed
                    self.activateSelected = True
                if event.key == pg.K_DOWN:                                   #increase value for selection
                    self.selectedState += 1
                if event.key == pg.K_UP:                                     #decrease value for selection
                    self.selectedState -= 1
             
            if event.type == pg.MOUSEBUTTONDOWN:                             #sets value to true if mouse1 is pressed
                if event.button == 1:
                    self.click = True                                       

        #function for drawing text on screen
    def drawMenuText(self, text, x, y, fontsize = 40):
        drawText = self.textToDisplay(text, fontsize = fontsize)             #calls textToDisplay with string and fontsize to get a surface
        textRect = drawText.get_rect()                                       #get rectangle of surface
        textRect.center = (x,y)                                              #centers text based on rectangle position
        self.screen.blit(drawText, textRect)                                 #draws text at rectangle position

     
    def saveData(self, levelname = 'level1', lives = 9, catnip = 0):
        try:
            file = open("playerData/"+self.userName+"Data.txt","x")          #opening file based on userName
        except:
            file = open("playerData/"+self.userName+"Data.txt","w")
        file.write(f"{levelname},{str(lives)},{str(catnip)}")                          #writing text to file
        file.close()
        return [levelname,lives,catnip]                            #returning values

    # Gets player data from file
    def getPlayerData(self):
        try:
            file = open("playerData/"+self.userName+"Data.txt","r")          #opening file based on userName
            data = file.read().split(",")                                    #splitting on , and reading
            data[1] = int(data[1])                                           #converting values to int
            data[2] = int(data[2])
            return data                                                      #returning the data
        except IOError:                                                      #error if data is  found
            print("No playerdata found")
            return None

        #HUD used ingame for displaying lives and catnip
    def displayHUD(self):
        self.lives_display  = self.textToDisplay(f'Lives: {self.player.lives}')
        self.points_display = self.textToDisplay(f'Catnip: {self.player.catnip_level}')

        #HUD used for endgame level 
    def endGameHUD(self):
        endFont = pg.font.Font("resources/action-jackson.regular.ttf", 40)   #loading custom font
        self.endText = endFont.render("Congratulations", True, (0, 200 ,0))
        endFont = pg.font.Font("resources/action-jackson.regular.ttf", 30)
        self.endText2 = endFont.render("You have finished the game", True, (0, 200 ,0))

        #displaying text on screen for pause screen
    def displayPauseScreen(self):
        self.pauseText = self.textToDisplay("Game is paused", color= (0,0,0), bold= True)
        self.pauseText2 = self.textToDisplay("Press P to resume", color= (0,0,0), bold= True)
        self.pauseText3 = self.textToDisplay("Press Q to quit", color= (0,0,0), bold= True)

        #displaying text on screen for damage screen
    def damageScreen(self):
        deathFont = pg.font.Font("resources/gypsy-curse.regular.ttf", 70)    #loading custom font
        self.pauseText = deathFont.render("YOU DIED", True, (255, 0 ,0))
        self.pauseText2 = self.textToDisplay("Press P to resume", color= (0,0,0), bold= True)
        self.pauseText3 = self.textToDisplay("Press Q to quit", color= (0,0,0), bold= True)

        #function used to convert a string into a surface
    def textToDisplay(self, text, font = 'Comic Sans MS', fontsize = 40, bold = False, italic = False, color = (255,255,255) ):
        font = pg.font.SysFont(font, fontsize, bold, italic)
        return font.render(text, True, color)

# Game Loop
# create objects and dicts

''' remove these '''
level1 = createLevel1()
level2 = createLevel2()
level3 = createLevel3()
level4 = createLevel4()

# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
pickleLevel(level3, 'level3')
pickleLevel(level4, 'level4')

g = Game()                                                                      # Creates a game instance                                                                                # While loop checking the Game.running boolean
g.mainMenu()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
