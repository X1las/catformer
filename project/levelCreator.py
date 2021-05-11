# importing modules
from Vector import Vec
import pickle
from subSprites import Box, Button, Lever, PickUp, Platform, Mug, Water, PatrollingEnemy, AiEnemy, LevelGoal

''' template '''
def createLevel():
    # platforms
    # boxes
    # buttons
    # levers
    # mugs
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
        'mugs':      [],
        'goals':     [],
        'enemies':   [],
        'water':     [],
        'health':    [],
        'catnip':    []
    }

    return levelName



''' Level 1 '''
'''
def createLevel1():
    # platforms
    floor   = Platform( 1000, 600 , 2000 , 50 ,'p_floor', floorplat = True )
    fatplat = Platform( 300 , 450 ,  150 , 40 , 'fatplat')
    p_1     = Platform( 500 , 350 ,  150 , 40, "p_1", vel=Vec(-0.7,0), maxDist = 100)
    p_2     = Platform( 500 , 590 ,  150 , 70 , 'p_2')
    p_3     = Platform( 600 , 200 ,  150 , 40 , 'p_3')
    p_4     = Platform( 720 , 450 ,  150 , 40 , 'p_4')
    p_5     = Platform( 1100 , 400 ,  150 , 40 , 'p_5')
    # boxes
    box1 = Box(370 , 200 , 44 , 44 , 'box_1')
    box2 = Box(200 , 400 , 44 , 44 , 'box_2')

    # buttons
    btn1 = Button(600 , 550 , 30 , 20 , 'button1')
    btn2 = Button(500 , 550 , 30 , 20 , 'button2')
    # levers
    lever1 = Lever(650 , 550 , 36 , 26 , 'lever1')
    # mugs
    mug1 = Mug(fatplat , 50 , 'v1')
    # goals
    # enemies
    # water
    water1 = Water(500 , 590 ,  150 , 70)
    # health
    health1 = PickUp(600, 400, 16, 16, 'health')                                          #
    # catnip
    catnip1 = PickUp(400, 370, 16, 16, 'catnip')   

    # create dictionary
    level1 = {
        'name': 'level1',
        'settings': {
            'spawn': Vec(270, 350),
            'length': 5000,
            'track': ''
        },
        'platforms': [floor, fatplat], # , p_1, p_2, p_3, p_4, p_5],
        'boxes':     [], # box1, box2],
        'buttons':   [btn1, btn2],
        'levers':    [],
        'mugs':      [mug1],
        'goals':     [],
        'enemies':   [],
        'water':     [],#water1],
        'health':    [health1],
        'catnip':    [catnip1]
    }
    return level1
'''
''' Level 1 '''
def createLevel1():
    # platforms
    floor     = Platform( 1000, 600 , 3000 , 50 ,'p_floor', floorplat = True )
    startplat = Platform( 300 , 500 ,  120 , 30 , 'startplat')
    p_1       = Platform( 420 , 350 ,  100 , 30, "p_1")
    p_2       = Platform( 540 , 270 ,  65 , 30 , 'p_2')
    mugplat   = Platform( 660 , 270 ,  65 , 30 , 'mugplat', vel = Vec(1,0), maxDist = 50)
    
    waterDiv1 = Platform( 550 , 550 ,  30 , 130 , 'p_3')
    waterDiv2 = Platform( 1100 , 550 ,  30 , 130 , 'p_3')

    moving1     = Platform( 700 , 450 ,  150 , 30 , 'p_4', vel=Vec(-1,0), maxDist = 50)
    moving2     = Platform( 900 , 450 ,  150 , 30 , 'p_4', vel=Vec(-1,0), leftMaxDist=30, rightMaxDist= 70)
    
    endplat     = Platform( 1300 , 500 ,  100 , 30 , 'p_5')
    
    leftboundary = Platform(50, 560, 100, 600, "left bound")
    rightboundary = Platform(1400, 560, 100, 600, "left bound")
    # boxes
    box1 = Box(270 , 200 , 44 , 44 , 'box_1')
    box2 = Box(660 , 200 , 44 , 44 , 'box_1')




    # buttons
    # levers
    # goals
    endgoal = LevelGoal(endplat, 50, name = "end")
    # enemies
    pat1 = PatrollingEnemy(floor, 900, 50)
    pat2 = PatrollingEnemy(floor, 1700, 50)
    # water
    water1 = Water(565 + (1100 - 550 - 30)/2, 600 , 1100 - 550 - 30   , 60)
    # health
    health1 = PickUp(1300, 540, 16, 16, 'health')                                          #
    # catnip
    catnip1 = PickUp(400, 370, 16, 16, 'catnip')   
    # mugs
    mug1 = Mug(mugplat , 50 , 'v1', spawn = catnip1)

    # create dictionary
    level1 = {
        'name': 'level1',
        'settings': {
            'spawn': Vec(320, 350),
            'length': 5000,
            'track': ''
        },
        'platforms': [floor, startplat, p_1, p_2, mugplat, waterDiv1, waterDiv2, moving1, moving2, endplat, leftboundary, rightboundary], # , p_1, p_2, p_3, p_4, p_5],
        'boxes':     [  box1],# box2],
        'buttons':   [],
        'levers':    [],
        'mugs':      [mug1],
        'goals':     [endgoal],
        'enemies':   [pat1, pat2],
        'water':     [water1],
        'health':    [health1],
        'catnip':    [],#catnip1]
    }
    return level1

''' Level 2 '''
def createLevel2():
    # platforms
    floor   = Platform( 1000, 600 , 2000 , 50 ,'p_floor', floorplat = True )
    fatplat = Platform( 300 , 480 ,  150 , 40 , 'fatplat')
    # boxes
    box1 = Box(350 , 400 , 44 , 44 , 'box_1')
    # buttons
    #btn1 = Button(600 , 550 , 30 , 20 , 'button1')
    #btn2 = Button(500 , 550 , 30 , 20 , 'button2')
    # levers
    #lever1 = Lever(450 , 550 , 10 , 40 , 'lever1')
    #lever2 = Lever(500 , 550 , 10 , 40 , 'lever2')
    # mugs
    #mug1 = Mug(fatplat , 50 , 'v1')
    # goals
    # enemies
    # water
    # catnip

    levelName = {
        'name': 'level2',
        'settings': {
            'spawn': Vec(330,350),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        'platforms': [floor, fatplat],
        'boxes':     [box1],
        'buttons':   [],#btn1, btn2],
        'levers':    [],#lever1, lever2],
        'mugs':      [],#mug1],
        'goals':     [],
        'enemies':   [],
        'water':     [],
        'health':    [],
        'catnip':    []
    }

    return levelName

''' End Level '''
def createLevel4():
    # platforms
    floor   = Platform( 1000, 600 , 2000 , 50 ,'p_floor', floorplat = True )

    mug1 = Mug(floor , 50 , 'v1')


    levelName = {
        'name': 'level4',
        'settings': {
            'spawn': Vec(330,550),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        'platforms': [floor],
        'boxes':     [],
        'buttons':   [],
        'levers':    [],
        'mugs':      [mug1],
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
level4 = createLevel4()

# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
pickleLevel(level4, 'level4')
