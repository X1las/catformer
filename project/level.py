import pygame as pg
from settings import *
from sprites import *
from os import path

class Level:
    def __init__(self, game, boxes , length):
        self.surfaces = pg.sprite.Group()
        self.boxes = boxes
        self.game = game
        self.length = length

    # --> Just makes the list of platforms in "settings" to actual platforms. creates the objects
    def setPlatforms(self):
        self.plats = []
        for plat in self.platforms:

            self.plats.append(Platform(self.game, *plat))

    def setBoxes(self):
        for plot in self.boxes:
            Box(self.game, *plot)

    def setVases(self):
        Vase(self.game, 100, 100, name = "vase_1")
        Vase.on_platform(self.game, self.plats[1], "left", name = "vase 2")

    def setSurfaces(self):
        #self.surfaces = Surface

        platforms = self.setPlatforms()
        boxes = self.setBoxes()
        vases = self.setVases()
    
    # Function to load level files
    def loadLevel(self , filename): 
        plats = []                                      # Define empty platform array                                           
        spawn = Vec(0,0)                                # Define a spawnpoint vector as 0,0
        category = "none"                               # Define a category string as none 

        file = open(f"levels/{filename}.txt" , "r")     # Loading level file in levels directory with the given filename
        lines = file.read().splitlines()                # Split the file into an array of string lines
        
        # Iterating through the lines:
        for line in lines:
            print(line)                                 # Prints the current line for bugfixing

            if (line == "Settings"):                    # If the header is equal to Settings it will change the category
                category = "Settings"
                print("Reading " + category)

            if (line == "Platforms"):                   # If the header is equal to Platforms it will change the category
                category = "Platforms"
                print("Reading " + category)

            # If the category is Settings, then we check the following lines for settings data we need:
            if (category == "Settings" and line!= "" and line != "Settings"):
                linesplit = line.split(" , ")
                spawn.x = int(line[0])
                spawn.y = int(line[1])

            # If the category is Platforms, then we check the following lines for platform data
            if (category == "Platforms" and line!= "" and line != "Platforms"):
                linesplit = line.split(" , ")
                plats+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]
                print(plats)

        print(plats)
        self.platforms = plats