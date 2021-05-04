# importing modules
import pickle
from subSprites import Box, Button, Lever, Platform
from spritesheet import Spritesheet

''' template '''
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
        'length': 0
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



''' Level 1 '''
# create objects
# platforms

floor   = Platform(-200 , 600 , 6000 , 50 , 'p_floor')
fatplat = Platform( 100 , 500 ,  150 , 40 , 'fatplat')
p_2     = Platform( 300 , 590 ,  150 , 70 , 'p_2')
p_3     = Platform( 500 , 300 ,  150 , 40 , 'p_3')
p_4     = Platform( 700 , 450 ,  150 , 40 , 'p_4')
p_5     = Platform( 900 , 400 ,  150 , 40 , 'p_5')

# boxes
box1 = Box(150 , 400 , 44 , 44 , 'box_1')

# buttons
btn1 = Button(400 , 550 , 30 , 20 , 'button1')
btn2 = Button(300 , 550 , 30 , 20 , 'button2')

# levers
lever1 = Lever(450 , 550 , 10 , 40 , 'lever1')

# create dictionary
level1 = {
    'name': 'level1',
    'settings': {
        'spawn': (170, 350),
        'length': 5000
    },
    'platforms': [floor, fatplat, p_2, p_3, p_4, p_5],
    'boxes':     [box1],
    'buttons':   [btn1, btn2],
    'levers':    [lever1],
    'vases':     [],
    'goals':     [],
    'enemies':   [],
    'water':     [],
    'health':    [],
    'catnip':    []
}

# pickling
filename = 'level1'
outfile = open(f'levels/{filename}','wb')   # 'wb' means write binary
pickle.dump(level1, outfile)
outfile.close()