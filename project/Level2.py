# imports
import pygame as pg
import pickle
from Vector import Vec

# reading from pickle file
def unpickle(filename):
    infile = open(f'levels/{filename}','rb')
    data = pickle.load(infile)
    infile.close()
    return data


class Level:
    def __init__(self, game):
        self.game = game
        self.spawn = Vec()
    
    # Function to load level files
    def load(self , filename):
        
        try:                # try to unpickle file
            print(filename)
            levelData = unpickle(filename)
        except Exception as e: # error if file not found
            print(e)
            print("Error, no level found")
            return False
        
        # set level name and settings
        self.name = levelData['name']                   # set level name
        self.spawn = levelData['settings']['spawn']     # set spawnpoint for player
        #print(type(self.spawn))
        self.musicTrack = "default.mp3"

        # set objects   
        self.platforms = levelData['platforms']
        self.boxes     = levelData['boxes'    ]
        self.mugs      = levelData['mugs'    ]
        self.buttons   = levelData['buttons'  ]
        self.levers    = levelData['levers'   ]
        self.goals     = levelData['goals'    ]
        self.enemies   = levelData['enemies'  ]
        self.health    = levelData['health'   ]
        self.catnip    = levelData['catnip'   ]
        self.water     = levelData['water'    ]
        
        for p in self.platforms:
            p.startGame(self.game)
            if (p.y > self.game.boundary):
                self.game.boundary = p.y
        for p in self.boxes:
            p.startGame(self.game)
        for p in self.mugs:
            p.startGame(self.game)
        for p in self.buttons:
            p.startGame(self.game)
        for p in self.levers:
            p.startGame(self.game)
        for p in self.goals:
            p.startGame(self.game)
        for p in self.enemies:
            p.startGame(self.game)
        for p in self.health:
            p.startGame(self.game)
        for p in self.catnip:
            p.startGame(self.game)
        for p in self.water:
            p.startGame(self.game)
        return True