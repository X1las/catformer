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

from pygame.constants import KMOD_ALT, KMOD_GUI, KMOD_META, KMOD_MODE

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
    boundary = 600                                                              # default value for lower player boundary
    
    userName = ""                                                               # Used for saving and loading level progress based on given name
    
    
    
    isDamaged = False                                                           # Boolean used for damage HUD after life is lost
    finished = False                                                            # Boolean used for endGame HUD when final level is reached
    paused = False                                                              # Boolean used to pause the game
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
        self.frames                 = 0                                         # variable used for checking performance


            #not needed, old code
        # Reads the player data from file and adds it to self.data
        """self.data = self.getPlayerData()
        if not self.data:
            self.data = []
            self.data.append(DEFAULT_LEVEL)
            self.data.append(PLAYER_LIVES)
            self.data.append(PLAYER_CATNIP)"""

        # load images and sprite sheets
        self.spriteSheet   = ss.Spritesheet('resources/spritesheet_green.png')
        self.dogSheet      = ss.Spritesheet('resources/Hyena_walk.png')
        self.platformSheet = ss.Spritesheet('resources/platforms.png')
        self.wormSheet     = ss.Spritesheet('resources/worm-spritesheet.png')
        # loads background image
        bg = pg.image.load("resources/bg.png")
        self.bg = pg.transform.scale(bg, (WIDTH+400, HEIGHT))

    #create the menus and start main menu
    def start(self):
        self.createMenus()
        self.mainMenu()
    
    # Creates Sprite Groups
    def createSGroups(self):

    
        #self.all_sprites = pg.sprite.LayeredUpdates()                          # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        self.all_sprites = SpriteGroup()                                        # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        
        self.group_platforms          = pg.sprite.Group()                       # Only applied  to platforms
        self.group_boxes              = pg.sprite.Group()                       # Only applied to boxes
        self.group_levers             = pg.sprite.Group()                       # Only applied to the lever 
        self.group_mugs               = pg.sprite.Group()                       # Only applied to mugs
        self.group_pickups            = pg.sprite.Group()                       # All things that can get picked up by player
        self.group_solid              = SpriteGroup()                           # solid objects (formerly rayIntersecters)
        self.group_damager            = pg.sprite.Group()                       # All hostiles
        self.group_enemies            = pg.sprite.Group()
        self.group_pressureActivator  = pg.sprite.Group()                       # Things that can activate a button
        # not necessary?
        self.group_buttons            = pg.sprite.Group()                       # Only applied to button sprite      
        self.group_levelGoals         = pg.sprite.Group()                       # Only applied to the levelGoal sprite
        self.group_movables           = pg.sprite.Group()
        self.group_interactiveFields  = pg.sprite.Group()                       # Only apllies to the interactive field
       
        self.framecount = 0
        self.accumframes = 0

    # Loads all the HUDs default values
    def createHUDs(self):
        resumeText     =  Text("Press P to resume", (300, 250), screen = self.screen)
        quitText       =  Text("Press Q to quit", (300, 350), screen = self.screen)
        self.pauseHUD   = [Text("Game is paused",(300, 150), screen = self.screen), resumeText, quitText]
        self.damageHUD  = [Text("YOU DIED",                   (300, 150), screen = self.screen, displayWay="custom", font = "resources/gypsy-curse.regular.ttf", color = (255, 0, 0), fontsize=80), resumeText, quitText]
        self.endgameHUD = [Text("Congratulations" ,           (300, 150), screen = self.screen, displayWay="custom", font = "resources/action-jackson.regular.ttf", color = (0,200,0)),
                           Text("You have finished the game", (300, 250), screen = self.screen, displayWay="custom", font = "resources/action-jackson.regular.ttf", color = (0,200,0), fontsize = 30)]
        self.scoreHUD   = [Text(f'Lives: {self.player.lives}',(100,50), screen = self.screen), Text(f'Catnip: {self.player.catnip_level}', (500,50), screen = self.screen)]

    #updates the values on HUD that change
    def updateHUD(self):
        self.scoreHUD[0].text = f'Lives: {self.player.lives}'
        self.scoreHUD[1].text = f'Catnip: {self.player.catnip_level}'

    #creating all the menu screens buttons and text
    def createMenus(self):
        quitBTN          = Button("Quit",  trigger = self.quitTrig, screen=self.screen , y=475, textColor = (255,255,255))
        returnBTN        = Button("Return", trigger = self.returnTrig, screen = self.screen, y = 475, textColor = (255,255,255))
        startBTN         = Button("Start", trigger = self.startNewTrig, screen = self.screen, y = 325, textColor = (255,255,255))
        startLoadBTN     = Button("Start", trigger = self.startLoadTrig, screen = self.screen, y = 325, textColor = (255,255,255))
        enterNameTXT     = Text("Please enter a name", (300,100), screen = self.screen, color = (255,255,255))
        enterNameLoadTXT = Text("Please enter a name to load", (300,100), screen = self.screen, color = (255,255,255))

        self.mainmenu = Menu(self.screen,
                        buttons = [Button("New Game", trigger = self.nameStartScreen, screen = self.screen, y = 25, textColor = (255,255,255)), 
                                   Button("Load Game", trigger =self.nameLoadScreen, screen=self.screen , y=175, textColor = (255,255,255)),
                                   Button("Tutorial", trigger = self.tutorialScreen, screen=self.screen , y=325, textColor = (255,255,255)),
                                   quitBTN])

        self.newGamemenu = Menu(self.screen, buttons =  [startBTN, returnBTN], texts = [enterNameTXT]) 
        self.loadGamemenu = Menu(self.screen, buttons =  [startLoadBTN, returnBTN], texts = [enterNameLoadTXT])
            
        self.tutorialmenu = Menu(self.screen,buttons = [returnBTN], texts = [Text("Use arrow keys to move left/right", (300, 50)),
            Text("Press space to jump", (300, 100)),
            Text("Press P to pause", (300, 150)),
            Text("Press Q to quit", (300, 200)),
            Text("Press D to interact",( 300, 250))])
        self.noLivesMenu = Menu(self.screen, buttons = [returnBTN], texts = [
            Text(f'Player has run out of lives', (300, 50)),
            Text("Press Q to quit", (300, 200))])


        self.menus = [self.mainmenu, self.newGamemenu, self.loadGamemenu, self.tutorialmenu, self.noLivesMenu]                          #adding each menu to a list
        for menu in self.menus:
            menu.initTexts()                                #initializing text inside menus
        self.tutorialmenu.initTexts(fontsize = 30)          #making tutorial fontsize smaller



    # Method that creates a new level
    def new(self):
        self.finished = False
        self.createSGroups()                                                    # Creates all the sprite groups
        try:
            self.level
            self.data = self.getPlayerData()                                    #reading playerdata file
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
        
        if not self.level.load(self.level.name):                                #loading default level if it cannot load one
            self.level.load(DEFAULT_LEVEL)
        
        self.player = Player(self.level.spawn)                                  #
        self.player.startGame(self)    
        #
        if self.data:                                                           #set lives and catnip to values from data file
            self.player.lives = self.data[1]
            self.player.catnip_level = self.data[2]    

        # Probably delete!
        try:
            pg.mixer.music.load(self.level.musicTrack)                
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(VOLUME)
        except:
            print("Error loading music!")

        self.paused = False                                                     #reset paused to false incase still active from previous game
        self.createHUDs()

        self.run()                                  # Runs the game


    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     
        while self.playing:                                                     
            self.clock.tick(FPS)                    # Changing our tickrate so that our frames per second will be the same as FPS from settings

            self.framecount += 1                    #section used for checking performance
            self.accumframes += self.clock.get_rawtime()
            self.frames += 1
            if (self.frames >= 60):
                self.frames = 0
            if self.framecount > 60*4:
                print(f'{self.accumframes/self.framecount}')
                self.accumframes = 0
                self.framecount = 0

            # Runs all our methods on loop:
            self.events()  
            if not self.paused:                     #update if not paused
                self.update()
            if self.player.lives <= 0:              #checking if out of lives
                self.playing = False
                self.outOfLives = True
                self.newGamemenu.active = False
                self.loadGamemenu.active = False
                if os.path.exists("playerData/"+self.userName+"Data.txt"):      #deleting data file when out of lives
                    os.remove("playerData/"+self.userName+"Data.txt")
            self.draw()
            

    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    """    ------------------- UPDATE ----------------------------------------------------------------"""
    # Method where we update game processesd
    def update(self):
        self.all_sprites.resetSprites()
        self.all_sprites.update()
        for plat in self.group_solid:
            plat.collisionEffect()
        self.all_sprites.updateAddedvel()
        self.all_sprites.updatePos()
        self.moveScreen()
        self.updateHUD()

      
    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                if os.path.exists("playerData/"+self.userName+"Data.txt"):       #return true/false if file exists/does not
                    self.saveData(levelname = self.level.name, lives = self.player.lives, catnip = self.player.catnip_level)
                self.exitProgram()
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user has any keys pressed down
                if event.key == pg.K_q:                                         # checks if the uses presses q
                    if os.path.exists("playerData/"+self.userName+"Data.txt"):       #return true/false if file exists/does not
                        self.saveData(levelname = self.level.name, lives = self.player.lives, catnip = self.player.catnip_level)  #saves player data
                    if self.playing:                                            #breaking loops to quit to main menu
                        self.playing = False   
                    self.newGamemenu.active = False
                    self.loadGamemenu.active = False                                     
                # restart the level
                if event.key == pg.K_r:                             
                    self.new()
                if event.key  == pg.K_p:                                        #pause/unpause the game
                    self.paused = not self.paused
                    self.isDamaged = False
     
    # Method for drawing everything to the screen           
    def draw(self):                                         
        self.screen.blit(self.bg, (0,0))                    # Draws background image
        self.all_sprites.updateRects()
        self.all_sprites.draw(self.screen)                  # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        self.drawHUDs()     
        pg.display.update()                                 # Updates the drawings to the screen object and flips it
        self.all_sprites.resetRects()
  

        
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
        for sprite in self.all_sprites:                     #reset all sprites position
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()                               #respawn player to spawn position

    #reset camera and pause with damaged to true
    def playerTookDamage(self):
        self.resetCamera()
        self.isDamaged = True
        self.paused = True

    #draw different overlays
    def drawHUDs(self):
        self.drawHUD(self.scoreHUD)
        if self.paused:
            if self.isDamaged:                                  #if life is lost show damage overlay
                self.hud = self.damageHUD
            else:                                               #if paused show pause overlay
                self.hud = self.pauseHUD
            self.drawHUD(self.hud)
        if self.finished:                                       #if game is finished show end game overlay
            self.drawHUD(self.endgameHUD)
    
    #draw HUD on screen
    def drawHUD(self, HUD):
        for text in HUD:
            text.blitText()
    
    #quit out of main menu loop
    def quitTrig(self):
        self.mainmenu.active = False

    #return to main menu
    def returnTrig(self):
        self.newGamemenu.active = False
        self.loadGamemenu.active = False
        self.tutorialmenu.active = False
        self.selectedState = 0

    def startNewTrig(self):
        if not self.userName == "":                              #check if name is not empty
            if not self.checkNameConflict():                     #check if name does not exist already
                self.data = self.saveData()                      #saves new playerdata file with default values
                self.new()                                       #opens the game
            else:
                self.nameError = True                            #give error message
                self.activateSelected = False                    #disable activator (mouse1 or enter)
        else:
            self.nameError = True                                #give error message
            self.activateSelected = False                        #disable activator (mouse1 or enter)
    
    def startLoadTrig(self):
        if self.checkNameConflict():                             #check if name exists already
            self.data = self.getPlayerData()
            self.new()                                           #opens the game
        else:
            self.nameError = True                                #give error message
            self.activateSelected = False                        #disable activator (mouse1 or enter)

    #sets all menus to not active to quit the game
    def exitProgram(self):
        for menu in self.menus:
            menu.active = False
        self.playing = False

    #runs an inputed menu screen
    def runMenu(self, menu, takeUserName = False):
        self.userName = ""                                                  #reseting inputed name
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        menu.active = True
        while menu.active:                                                  #loop while the current menu is active
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            if self.outOfLives:                                             #opening no lives screen if the player runs out of lives
                self.noLivesScreen()
            
            for event in pg.event.get():
                if event.type == (pg.QUIT):                                 #breaks all loops if QUIT is pressed
                    self.exitProgram()
                if takeUserName:                                            #if typing is required call writeName
                    self.userName = menu.writeName(event, self.userName)
                
                menu.menuNavigation(event,takeUserName)                     #events for navitagion through menus
            mx, my = pg.mouse.get_pos()                                     #get mouse position
            for button in menu.buttons:
                if button.rect.collidepoint((mx, my)):                      #checking if mouse position is on a button
                    menu.selectedButton = button                            #set selected button to one colliding with mouse
            menu.currentButton()
            if takeUserName:                                                #if on a screen with typing
                if self.nameError:                                          #error message if invalid name entered
                    Text("Invalid name entered", (300, 300), screen = self.screen, color = (255,255,255)).blitText()
                Text(self.userName, (300, 150), screen = self.screen, color = (255,255,255)).blitText()    #create name input as text object
            menu.blitMenu()                                                 #call function to draw text

            pg.display.update()                                             #update the display

    #used to open main menu
    def mainMenu(self):
        self.runMenu(self.mainmenu)
 
    #used to open new game screen
    def nameStartScreen(self):
        self.runMenu(self.newGamemenu, takeUserName = True)
    
    #used to open load game screen
    def nameLoadScreen(self):
        self.runMenu(self.loadGamemenu, takeUserName = True)
     
    #used to open no lives screen
    def noLivesScreen(self):
        self.outOfLives = False
        self.runMenu(self.noLivesMenu)

    #used to open tutorial screen
    def tutorialScreen(self):
        self.runMenu(self.tutorialmenu)

    def checkNameConflict(self):
        return os.path.exists("playerData/"+self.userName+"Data.txt")       #return true/false if file exists/does not

    #creates or updates a player data save file
    def saveData(self, levelname = 'level1', lives = 9, catnip = 0):
        try:
            file = open("playerData/"+self.userName+"Data.txt","x")          #opening file based on userName
        except:
            file = open("playerData/"+self.userName+"Data.txt","w")
        file.write(f"{levelname},{str(lives)},{str(catnip)}")                #writing text to file
        file.close()
        return [levelname,lives,catnip]                                      #returning values

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

#class used to represend a text object
class Text():
    def __init__(self, text, position, screen = None, font = 'Comic Sans MS', displayWay = "sysfont", fontsize = 40, bold = False, color = (0,0,0)):
        self.text = text; self.position = position; self.font = font; self.fontsize = fontsize; self.bold = bold; 
        self.color = color
        self.displayWay = displayWay; 
        self.screen = screen
    
    #used to check if default system font or custom font should be rendered
    def rendered(self):
        if self.displayWay == "sysfont":
            font = pg.font.SysFont(self.font, self.fontsize, self.bold, False)
            return font.render(self.text, True, self.color) #returning rendered text surface
        else:
            font = pg.font.Font(self.font, self.fontsize)   #loading custom font
            return font.render(self.text, True, self.color)

    #draws text on the screen
    def blitText(self):
        drawtext = self.rendered()
        textRect = drawtext.get_rect()
        textRect.center = self.position
        self.screen.blit(drawtext, textRect)

#class used to represent a button object
class Button():
    def __init__(self, text, trigger = None, screen = None, x = 190, y = 325, size = (220, 100), color = (0, 125, 255), textColor = (0, 0, 0)):
        self.color = color
        self.rect = pg.Rect((x,y), size)
        self.x, self.y = x,y; self.width = size[0]; self.height = size[1]
        self.screen = screen
        self.text = Text(text, (self.x + round(self.width/2),self.y + 50), screen = self.screen, color= textColor)
        self.trigger_ = trigger

    #draws a rectangle on the screen
    def drawButton(self):
        pg.draw.rect(self.screen, self.color, self.rect)
        self.text.blitText()

    #used to trigger something when button is activated
    def triggers(self):
        self.trigger_()

    #return a string containing the text inside a text object
    def __str__(self):
        return self.text.text

#class used to represent a menu object
class Menu():

    def __init__(self,  screen, buttons = [], texts = []):
        self.screen = screen
        self.buttons = buttons
        self.texts = texts
        for button in self.buttons:
            button.screen = self.screen
        self.selectedButton = self.buttons[0]
        self.selectedState = 0
        self.activateSelected = False
        self.active = False

    #used to initialize values of text
    def initTexts(self, fontsize = 40, color = (255,255,255)):
        for text in self.texts:
            text.color = color; text.fontsize = fontsize; text.screen = self.screen

    #function for currently selected button
    def currentButton(self):
        orangeRect     = pg.Rect(75, self.selectedButton.y + 25, 50, 50)
        pg.draw.rect(self.screen, (255, 125, 0), orangeRect)                #draws indicator for currently selected button
        if self.activateSelected:                                           #if selected activate trigger
            self.selectedButton.triggers()
            self.activateSelected = False
    
    #draws menus
    def blitMenu(self):
        for button in self.buttons:
            button.drawButton()                                             #calling draw on each button
        for text in self.texts:
            text.blitText()                                                 #calling draw on each text

    #getting user input for menu screens
    def menuNavigation(self, event, takeUserName = False):
        #for event in pg.event.get():                                
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_RETURN) or (event.key == pg.K_KP_ENTER):  #sets value to true if enter is pressed
                self.activateSelected = True
            if event.key == pg.K_q and not takeUserName:                 #quit if not in a typing menu
                self.active = False
            if event.key == pg.K_DOWN:                                   #increase value for selection
                self.selectedState += 1
                self.selectedButton = self.selectedState % len(self.buttons)
                self.selectedButton = self.buttons[self.selectedButton]
            if event.key == pg.K_UP:                                     #decrease value for selection
                self.selectedState -= 1
                self.selectedButton = self.selectedState % len(self.buttons)
                self.selectedButton = self.buttons[self.selectedButton]
            
        if event.type == pg.MOUSEBUTTONDOWN:                             #sets value to true if mouse1 is pressed
            if event.button == 1:       
                self.activateSelected = True                                

    # events used to type in the menu
    def writeName(self, event, username):
        self.userName = username
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:                              #backspace for removing unwanted text
                self.userName = self.userName[:-1]
            elif(pg.K_0 <= event.key <= pg.K_9):                         #checking correct key range and no modifiers are pressed
                if not ((event.mod & pg.KMOD_SHIFT) or (event.mod & pg.KMOD_CTRL) or (event.mod & pg.KMOD_ALT) or (event.mod & KMOD_MODE) or (event.mod & KMOD_META) or (event.mod & KMOD_GUI)):
                    self.userName += event.unicode
            elif(pg.K_a <= event.key <= pg.K_z):                         #checking correct key range and no modifiers are pressed
                if not ((event.mod & pg.KMOD_CTRL) or (event.mod & pg.KMOD_ALT) or (event.mod & KMOD_MODE) or (event.mod & KMOD_META) or (event.mod & KMOD_GUI)):
                    self.userName += event.unicode
        return self.userName


# Game Loop
# create objects and dicts

''' remove these 
level1 = createLevel1()
level2 = createLevel2()
level3 = createLevel3()
level4 = createLevel4()
level4 = createLevel5()
# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
pickleLevel(level3, 'level3')
pickleLevel(level4, 'level4')
pickleLevel(level4, 'level1')
'''
testLevel = createTestLevel()
pickleLevel(testLevel, 'level1')



g = Game()                                                                      # Creates a game instance                                                                                # While loop checking the Game.running boolean
g.start()
#g.mainMenu()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
