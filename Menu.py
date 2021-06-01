# External Imports:
import pygame as pg
from pygame.constants import KMOD_ALT, KMOD_GUI, KMOD_META, KMOD_MODE

# Menu Class
class Menu:

    # Initializor
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

    
    # Functions
    # Used to initialize values of text
    def initTexts(self, fontsize = 40, color = (255,255,255)):
        for text in self.texts:
            text.color = color; text.fontsize = fontsize; text.screen = self.screen


    # Function for currently selected button
    def currentButton(self):
        orangeRect     = pg.Rect(75, self.selectedButton.y + 25, 50, 50)
        pg.draw.rect(self.screen, (255, 125, 0), orangeRect)                #draws indicator for currently selected button
        if self.activateSelected:                                           #if selected activate trigger
            self.selectedButton.triggers()
            self.activateSelected = False
    

    # Draws menus
    def blitMenu(self):
        for button in self.buttons:
            button.drawButton()                                             #calling draw on each button
        for text in self.texts:
            text.blitText()                                                 #calling draw on each text


    # Getting user input for menu screens
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


    # Events used to type in the menu
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


    # Inner Classes
    # Class used to represend a text object
    class Text:

        # Text Initializor
        def __init__(self, text, position, screen = None, font = 'Comic Sans MS', displayWay = "sysfont", fontsize = 40, bold = False, color = (0,0,0)):
            self.text = text; self.position = position; self.font = font; self.fontsize = fontsize; self.bold = bold; 
            self.color = color
            self.displayWay = displayWay; 
            self.screen = screen
        

        # Used to check if default system font or custom font should be rendered
        def rendered(self):
            if self.displayWay == "sysfont":
                font = pg.font.SysFont(self.font, self.fontsize, self.bold, False)
                return font.render(self.text, True, self.color) #returning rendered text surface
            else:
                font = pg.font.Font(self.font, self.fontsize)   #loading custom font
                return font.render(self.text, True, self.color)


        # Draws text on the screen
        def blitText(self):
            drawtext = self.rendered()
            textRect = drawtext.get_rect()
            textRect.center = self.position
            self.screen.blit(drawtext, textRect)

    # Class used to represent a button object
    class Button:

        # Button Initializor
        def __init__(self, text, trigger = None, screen = None, x = 190, y = 325, size = (220, 100), color = (0, 125, 255), textColor = (0, 0, 0)):
            self.color = color
            self.rect = pg.Rect((x,y), size)
            self.x, self.y = x,y; self.width = size[0]; self.height = size[1]
            self.screen = screen
            self.text = Menu.Text(text, (self.x + round(self.width/2),self.y + 50), screen = self.screen, color= textColor)
            self.trigger_ = trigger


        # Draws a rectangle on the screen
        def drawButton(self):
            pg.draw.rect(self.screen, self.color, self.rect)
            self.text.blitText()


        # Used to trigger something when button is activated
        def triggers(self):
            self.trigger_()


        # Return a string containing the text inside a text object
        def __str__(self):
            return self.text.text