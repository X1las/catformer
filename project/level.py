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
    
    def loadLevel(self , filename):
        plats = []
        spawn = Vec(0,0)
        category = "none"
        counter = 0

        file = open(f"{filename}.txt" , "r")
        lines = file.read().splitlines()
        
        for line in lines:
            print(line)

            if (line == "Settings"):
                category = "Settings"
                print("Reading " + category)

            if (line == "Platforms"):
                category = "Platforms"
                print("Reading " + category)

            if (category == "Settings" and line!= "" and line != "Settings"):
                linesplit = line.split(" , ")
                spawn.x = int(line[0])
                spawn.y = int(line[1])

            if (category == "Platforms" and line!= "" and line != "Platforms"):
                linesplit = line.split(" , ")
                plats+= [(int(linesplit[0]),int(linesplit[1]),int(linesplit[2]),int(linesplit[3]),linesplit[4])]
                print(plats)

        print(plats)
        self.platforms = plats