# Imports
from sys import platform
import pygame as pg
from settings import *
from subSprites import *
from Vector import *

# Level Class
class Level:
    def __init__(self, game):
        self.game = game
    
    # Function to load level files
    def load(self , filename): 

        # Define empty obstacle arrays and default values:   
        self.platforms = []
        self.boxes = []
        self.vases = []
        self.buttons = []
        self.levers = []
        self.goals = []
        self.enemies = []
        self.health = []
        self.water = []

        self.spawn = Vec(0,0)                                # Define a spawnpoint vector as 0,0
        self.musicTrack = "default.mp3"
        self.name = filename

        category = "none"                               # Define a category string as none 

        # Switch function for level loading, using 'regex' to compare dictionary and runs connected function
        def level_switch(regex , args):

            # Defining dictionary to choose from
            switch = {
                "Platforms" : self.setPlatforms,
                "Boxes" : self.setBoxes,
                "Vases" : self.setVases,
                "Buttons" : self.setButtons,
                "Levers" : self.setLevers,
                "Settings" : self.setSettings
            }

            # Sets function equal to function related to the regex and runs it
            setFunc = switch.get(regex)
            if setFunc:
                setFunc(args)


        # Attempt to load level by filename
        try:
            file = open(f"levels/{filename}.txt" , "r")     # Loading level file in levels directory with the given filename
            lines = file.read().splitlines()                # Split the file into an array of string lines
        except:
            print("Error, no level found")
            return False


        # Iterating through the lines of the level file:
        for line in lines:
            header = line.split(" ")

            # Looks for a line starting with H. header indicator, then changes the category to the following word
            if header[0] == "H:":               
                category = header[1]
                print("Reading " + category)
            else:
                if line != "":
                    linesplit = line.split(" , ")
                    level_switch(category,linesplit)

        print("Level loaded successfully!")
        return True

    # Functions for switch
    def setSettings(self,args):
        
        if args[0] == "Spawn":
            self.spawn = Vec(int(args[1]),int(args[2]))
        
        if args[0] == "Length":
            self.length = int(args[1])
        
        if args[0] == "Track":
            self.musicTrack = str(args[1])

    # Switch function to create platforms
    def setPlatforms(self,args):
        self.platforms.append(Platform(self.game, int(args[0]), int(args[1]), int(args[2]), int(args[3]), str(args[4])))
    
    # Switch function to create boxes
    def setBoxes(self,args):
        self.boxes.append(Box(self.game, int(args[0]), int(args[1]), int(args[2]), int(args[3]), str(args[4])))
    
    # Switch function to create buttons
    def setButtons(self,args):
        self.buttons.append(Button(self.game, int(args[0]), int(args[1]), int(args[2]), int(args[3]), str(args[4])))

    # Switch function to create levers
    def setLevers(self,args):
        self.levers.append(Lever(self.game, int(args[0]), int(args[1]), int(args[2]), int(args[3]), str(args[4])))

    # Switch function to create vases
    def setVases(self,args):
        
        for platform in self.platforms:
            if platform.name == str(args[0]):
                plat = platform
                    
        self.vases.append(Vase(self.game, plat, str(args[1]), str(args[2])))