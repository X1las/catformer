import pygame as pg
from settings import *
from sprites import *
from os import path

class Level:
    def __init__(self, game):
        self.surfaces = pg.sprite.Group()
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
    def load(self , filename): 

        # Define empty obstacle arrays:   
        plats = []                                      
        boxes = []                                      
        vases = []   

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
                    if header[0] == "Spawn:":
                        linesplit = line.replace("Spawn: " , "").split(" , ")
                        spawn.x = int(linesplit[0])
                        spawn.y = int(linesplit[1])
                    if header[0] == "Length:":
                        length = header[1]

                # If the category is Platforms, then we check the following lines for platform data
                if category == "Platforms" and line!= "":
                    linesplit = line.split(" , ")
                    plats+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]
                
                if category == "Boxes" and line!= "":
                    linesplit = line.split(" , ")
                    boxes+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]

        self.platforms = plats
        self.spawn = spawn
        self.boxes = boxes
        self.length = length
        print("Level loaded successfully!")