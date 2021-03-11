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
        set = False
        pla = False

        file = open(f"{filename}.txt" , "r")
        file = file.splitlines()
        
        for line in file:
            string1 = line.replace("\n" , "")
            string2 = line.split()
            print(string1)

            if (set and string1!= ""):
                string1 = line.split(" , ")
                print(string1)
                spawn.x = int(line[0])
                spawn.y = int(line[1])

            if (pla and string1!=""):
                string1 = line.split(",")
                print(string1)
                plats[len(plats)] = (int(string1[0]),int(string1[1]),int(string1[2]),int(string1[3]),string1[4])

            if (string2[0] == "Settings"):
                print("true")
                set = True
                pla = False

            if (string2[0] == "Platform"):
                print("true2")
                set = False
                pla = True

        print(plats)
        self.platforms = plats
            

            

            


