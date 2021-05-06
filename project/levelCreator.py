# importing modules
from Vector import Vec
import pickle
from subSprites import Box, Button, Lever, Platform, Vase, Water

''' template '''
def createLevel():
    # platforms
    # boxes
    # buttons
    # levers
    # vases
    # goals
    # enemies
    # water
    # catnip

    levelName = {
        'name': '',
        'settings': {
            'spawn': (),
            'length': 0,
            'track': ''
        },
        'platforms': [],
        'boxes':     [],
        'buttons':   [],
        'levers':    [],
        'vases':     [],
        'goals':     [],
        'enemies':   [],
        'water':     [],
        'health':    [],
        'catnip':    []
    }

    return levelName



''' Level 1 '''
def createLevel1():
    # platforms
    floor   = Platform(-200 , 600 , 6000 , 50 , 'p_floor')
    fatplat = Platform( 100 , 500 ,  150 , 40 , 'fatplat')
    p_2     = Platform( 300 , 590 ,  150 , 70 , 'p_2')
    p_3     = Platform( 500 , 300 ,  150 , 40 , 'p_3')
    p_4     = Platform( 700 , 450 ,  150 , 40 , 'p_4')
    p_5     = Platform( 900 , 400 ,  150 , 40 , 'p_5')
    # boxes
    box1 = Box(200 , 400 , 44 , 44 , 'box_1')
    box2 = Box(130 , 500 , 44 , 44 , 'box_2')

    # buttons
    btn1 = Button(400 , 550 , 30 , 20 , 'button1')
    btn2 = Button(300 , 550 , 30 , 20 , 'button2')
    # levers
    lever1 = Lever(450 , 550 , 10 , 40 , 'lever1')
    # vases
    # goals
    # enemies
    # water
    water1 = Water(300 , 590 ,  150 , 70)
    # catnip
    # create dictionary
    level1 = {
        'name': 'level1',
        'settings': {
            'spawn': Vec(170, 350),
            'length': 5000,
            'track': ''
        },
        'platforms': [floor, fatplat, p_3, p_4, p_5],
        'boxes':     [box1, box2],
        'buttons':   [btn1, btn2],
        'levers':    [lever1],
        'vases':     [],
        'goals':     [],
        'enemies':   [],
        'water':     [water1],
        'health':    [],
        'catnip':    []
    }
    return level1

''' Level 2 '''
def createLevel2():
    # platforms
    floor   = Platform(-200 , 600 , 6000 , 50 , 'p_floor')
    fatplat = Platform( 100 , 500 ,  150 , 40 , 'fatplat')
    # boxes
    box1 = Box(150 , 400 , 44 , 44 , 'box_1')
    # buttons
    btn1 = Button(400 , 550 , 30 , 20 , 'button1')
    btn2 = Button(300 , 550 , 30 , 20 , 'button2')
    # levers
    lever1 = Lever(450 , 550 , 10 , 40 , 'lever1')
    lever2 = Lever(500 , 550 , 10 , 40 , 'lever2')
    # vases
    vase1 = Vase(fatplat , 'left' , 'v1')
    # goals
    # enemies
    # water
    # catnip

    levelName = {
        'name': 'level2',
        'settings': {
            'spawn': Vec(370,350),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        'platforms': [floor, fatplat],
        'boxes':     [box1],
        'buttons':   [btn1, btn2],
        'levers':    [lever1, lever2],
        'vases':     [vase1],
        'goals':     [],
        'enemies':   [],
        'water':     [],
        'health':    [],
        'catnip':    []
    }

    return levelName


# pickling method
def pickleLevel(level, filename):
    outfile = open(f'levels/{filename}','wb')   # 'wb' means write binary
    pickle.dump(level, outfile)
    outfile.close()

# create objects and dicts
level1 = createLevel1()
level2 = createLevel2()

# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
