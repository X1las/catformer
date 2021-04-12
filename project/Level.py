# Imports
import pygame as pg
from settings import *
from subSprites import *

# Classes
class Level:
    def __init__(self, game):
        self.surfaces = pg.sprite.Group()
        self.game = game

    # --> Just makes the list of platforms in "settings" to actual platforms. creates the objects
    def setPlatforms(self):
        self.plats = []
        for plat in self.platforms:

            self.plats.append(Platform(self.game, *plat))

    def setBoxes(self):
        for plot in self.boxes:
            Box(self.game, *plot).name = "box1"

    def setVases(self):
        #Vase(self.game, 100, 100, name = "vase_1")
        vase = Vase.on_platform(self.game, self.plats[1], "left", name = "vase 2")
        

    def setLevers(self):
        for lever in self.levers:
            Lever(self.game, *lever)

    def setButtons(self):
        for button in self.buttons:
            Button(self.game, *button)

    def setSurfaces(self):
        #self.surfaces = Surface

        platforms = self.setPlatforms()
        boxes = self.setBoxes()
        vases = self.setVases()
        buttons = self.setButtons()
        levers = self.setLevers()
    
    # Function to load level files
    def load(self , filename): 

        # Define empty obstacle arrays:   
        plats = []                                      
        boxes = []                                      
        vases = []  
        buttons = [] 
        levers = []

        spawn = Vec(0,0)                                # Define a spawnpoint vector as 0,0
        category = "none"                               # Define a category string as none 

        file = open(f"levels/{filename}.txt" , "r")     # Loading level file in levels directory with the given filename
        lines = file.read().splitlines()                # Split the file into an array of string lines
        
        # Iterating through the lines:
        for line in lines:
            #print(line)                                # Prints the current line for bugfixing
            header = line.split(" ")

            # Looks for a line starting with H. header indicator, then changes the category to the following word
            if header[0] == "H:":               
                category = header[1]
                print("Reading " + category)
            else:
                # If the category is Settings, then we check the following lines for settings data we need:
                if category == "Settings" and line!= "":
                    # Using the header to check if it's a spawn point option
                    if header[0] == "Spawn:":
                        linesplit = line.replace("Spawn: " , "").split(" , ")
                        spawn.x = int(linesplit[0])
                        spawn.y = int(linesplit[1])
                    # Using the header to check if it's a level lenght option
                    if header[0] == "Length:":
                        length = header[1]
                    if header[0] == "Track:":
                        track = "resources/"+header[1]
                    else:
                        track = "resources/default.mp3"

                # If the category is Platforms, then we check the following lines for platform data
                if category == "Platforms" and line!= "":
                    linesplit = line.split(" , ")
                    plats+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]
                
                if category == "Boxes" and line!= "":
                    linesplit = line.split(" , ")
                    boxes+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]

                if category == "Buttons" and line!= "":
                    linesplit = line.split(" , ")
                    buttons+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]

                if category == "Levers" and line!= "":
                    linesplit = line.split(" , ")
                    levers+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]



        self.platforms = plats
        self.spawn = spawn
        self.boxes = boxes
        self.buttons = buttons
        self.levers = levers
        self.length = length
        self.musicTrack = track
        self.name = filename
        print("Level loaded successfully!")