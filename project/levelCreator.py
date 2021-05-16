# importing modules
from Vector import Vec
import pickle

from Sprites.Platform import Platform
from Sprites.Box import Box
from Sprites.activator import Lever, Button
from Sprites.IntelligentEnemy import IntelligentEnemy
from Sprites.PatrollingEnemy import PatrollingEnemy
from Sprites.LevelGoal import LevelGoal
from Sprites.Pickup import PickUp
from Sprites.Water import Water
from Sprites.Mug import Mug

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
    left = -200

    ceil      = Platform( 1000 - left, 0 , 3000 - left, 50 )
    floor     = Platform( 1000, 600 , 3000 , 50, floorplat = True  )
    startplat = Platform( 300 , 400 ,  120 , 30)
    p_1       = Platform( 420 , 350 ,  100 , 30)
    p_2       = Platform( 540 , 270 ,   65 , 30)
    mugplat   = Platform( 660 , 270 ,   65 , 30, vel = Vec(1,0), maxDist = 50)
    
    waterDiv1 = Platform( 550 , 550 ,  30 , 130)
    waterDiv2 = Platform( 1100, 550 ,  30 , 130)

    moving1     = Platform( 700 , 450 ,  150 , 30 , vel=Vec(-1,0), maxDist = 50)
    moving2     = Platform( 900 , 450 ,  150 , 30 , vel=Vec(-1,0), leftMaxDist=30, rightMaxDist= 70)
    
    endplat     = Platform( 1300 , 500 ,  100 , 30)
    
    leftboundary = Platform(50, 550, 100, 550)
    rightboundary = Platform(1400, 550, 100, 550)
    # boxes
    box1 = Box(270 , 200 , 44 , 44 )
    box2 = Box(660 , 200 , 44 , 44 )




    # buttons
    # levers
    # goals
    endgoal = LevelGoal(endplat, 50)
    # enemies
    pat1 = PatrollingEnemy(floor, 900, 50)
    pat2 = PatrollingEnemy(floor, 1700, 50)
    # water
    water1 = Water(565 + (1100 - 550 - 30)/2, 600 , 1100 - 550 - 30   , 60)
    # health
    health1 = PickUp(1300, 540, 'health')                                          #
    # catnip
    catnip1 = PickUp(400, 370, 'catnip')   
    # mugs
    mug1 = Mug(mugplat , 50 , spawnItem = catnip1)

    # create dictionary
    level1 = {
        'name': 'level1',
        'settings': {
            'spawn': Vec(endplat.right_x(), 350),
            'length': 5000,
            'track': ''
        },
        'platforms': [ceil, floor, startplat, p_1, p_2, mugplat, waterDiv1, waterDiv2, moving1, moving2, endplat, leftboundary, rightboundary], # , p_1, p_2, p_3, p_4, p_5],
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
    bottom = 550
    left = -200
    # platforms
    ceil   = Platform( 1000 - left, 0 , 3000 - left, 50 )
    floor   = Platform( 1000 - left, 600 , 3000 - left, 50 ,floorplat = True )
    rightboundary = Platform(1800 - left, bottom, 100, bottom)
    
    water1width = 200
    waterdiv1 = Platform( 400 - left , bottom ,  20 , 40 )
    midwater  = Platform( waterdiv1.right_x() + water1width/2 , 530 ,     50 , 30)
    waterdiv2 = Platform( waterdiv1.right_x() + water1width + 10 , bottom ,  20 , 40)

    # height 1
    plat1     = Platform(1200 - left, 500    , 500 , 30 )
    blocker   = Platform(plat1.x - 30, plat1.top_y() - 50   , 44 , 154 ) 
    vert      = Platform(plat1.x - plat1.width/2 + 15, plat1.y - plat1.height   , 30 , 100)
    #jumphelp  = Platform(plat1.right_x() + 200, bottom    , 30 , 30, "plat1" )
    #jumphelp2 = Platform(plat1.left_x() + 30 + 15, plat1.top_y()    , 30 , 30, "plat1" )
    plat2     = Platform(vert.left_x()  - 50/2, vert.top_y() + 30    , 50 , 30)
    vert2     = Platform(plat2.left_x() - 30/2, vert.top_y()+vert.height/2 + 40, 30, vert.height/2 + 40 ) 
    plat5     = Platform(vert2.left_x()  - 50, vert2.bot_y()    , 100 , 30)
    vert3     = Platform(plat5.left_x() - 30/2, vert.top_y()+vert.height/2 + 40, 30, vert.height/2 ) 


    #height 2 part 1
    plat3     = Platform(plat1.right_x() -(plat1.right_x()-blocker.right_x())/2, blocker.top_y() + 30, plat1.right_x()-blocker.right_x() , 30)
    moving1   = Platform(plat1.right_x() + 50, plat1.bot_y()    , 100 , 30, downMaxDist = 0, upMaxDist = plat1.pos.y - plat3.pos.y, name = "moving1")
    underwater= Platform(blocker.left_x()  - 200, blocker.top_y() + 60, 400 , 20)
    boxstop   = Platform(blocker.left_x() + 5, blocker.top_y()    , 10 , 10 )
    waterplat1 = Platform(underwater.left_x() + underwater.width*3/4, underwater.top_y(), 50, 20, downMaxDist = 0, upMaxDist = 40)
    waterplat2 = Platform(underwater.left_x() + underwater.width*2/4, underwater.top_y(), 50, 20,  downMaxDist = 0, upMaxDist = waterplat1.upMaxDist)
    waterplat3 = Platform(underwater.left_x() + underwater.width*1/4, underwater.top_y(), 50, 20, downMaxDist = 0, upMaxDist = waterplat1.upMaxDist)
    rightwat  = Platform(underwater.left_x() , underwater.top_y(), 50, 30)
    
    
    
    #height 2 part 2
    jumper1    = Platform(rightwat.left_x() - 100, rightwat.bot_y() + 20, 50, 30)
    jumper2    = Platform(jumper1.left_x() - 100, jumper1.bot_y(), 50, 30)
    jumper3    = Platform(jumper2.left_x() - 100, jumper1.bot_y(), 50, 30)
    jumper4    = Platform(jumper3.left_x() - 100, jumper1.bot_y() - 40, 100, 30)
    smallleft  = Platform(jumper4.left_x() + 15, jumper4.top_y() - 55, 30, 30)
    
    #height 3
    plat4      = Platform(smallleft.right_x() + 50 + 60, smallleft.top_y() - 20, 100, 30)
    rightmov  = Platform(plat4.right_x() + 300, plat4.bot_y(), 80, 30)
    moving2   = Platform(rightmov.left_x() - 30, plat4.bot_y(), 60 , 30, leftMaxDist = rightmov.left_x() - plat4.right_x(), rightMaxDist = 0)
    longplat = Platform(rightmov.right_x() + 250, rightmov.bot_y() - 10, 300, 30)
    enemyplat = Platform(longplat.right_x() + 200, longplat.bot_y(), 200, 30)
    enemsafe  = Platform(enemyplat.mid().x, enemyplat.top_y(), 20, 40)
    #plat5  = Platform(enemyplat.right_x() + 150, enemyplat.bot_y(), 200, 30)
    goalplat  = Platform(enemyplat.right_x() + 150, enemyplat.bot_y(), 150, 30)

    leftboundary = Platform(jumper4.left_x() - 50, bottom, 100, bottom)

    plats = [floor, leftboundary, rightboundary, waterdiv1, midwater ,waterdiv2,
             plat1, blocker, vert,  plat2, moving1, rightwat, plat5, vert2, vert3,#jumphelp, jumphelp2,
             plat3, underwater, boxstop, waterplat1, waterplat2, waterplat3,
             jumper1, jumper2, jumper3, jumper4, smallleft, 
             plat4, moving2, rightmov, longplat, enemyplat,  goalplat #enemsafe,
             ]
    # boxes
    box1 = Box( moving1.pos.x , plat1.top_y() , 44 , 44 )
    #box1 = Box( blocker.pos.x , plat1.top_y() , 44 , 44 )
    # buttons
    btn1eff = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : waterplat1} ,
                {"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : waterplat2} ,
                {"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1), "target" : waterplat3}] }
    
    waters1btn = Button(plat3, 40, effect = btn1eff)
    mov2btneff = {  "move" : [{"movespeed"  : Vec(-1,0), "deactspeed" : Vec(1,0) , "target" : moving2} ]}
    mov2btn = Button(plat4, 20, effect = mov2btneff)
    #btn1 = Button(600 , 550 , 30 , 20 , 'button1')
    #btn2 = Button(500 , 550 , 30 , 20 , 'button2')
    # levers
    lev1eff = {  "conMove" : [{"movespeed"  : Vec(0,-1), "target" : moving1} ]
                        }
    #mov1lev = Lever(plat5, 40, effect = lev1eff)
    mov1lev = Lever(plat1, 400, effect = lev1eff)
    # pickups
    health1 = PickUp(1300, 540, 'health')                                          #
    catnip1 = PickUp(400, 370, 'catnip')   
    # mugs
    mug1 = Mug(longplat , 220, spawnItem = catnip1)
    mug2 = Mug(jumper2 , 40, spawnItem = health1)
    # goals
    goal = LevelGoal(goalplat, 60)
    # enemies
    pat1 = PatrollingEnemy(enemyplat, 70, maxDist = 100)
    detect1 = IntelligentEnemy(floor, 1400)
    # water
    water1 = Water(waterdiv1.right_x() + water1width/2, bottom , water1width, 36 )
    water2 = Water(underwater.mid().x  + rightwat.width/2 - 13, underwater.top_y() , underwater.width - rightwat.width/2, plat2.height - 5)
    # catnip

    levelName = {
        'name': 'level2',
        'settings': {
            'spawn': Vec(goalplat.right_x(),100),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        #'platforms': [floor, leftboundary, rightboundary, waterdiv1, midwater ,waterdiv2, plat1],
        'platforms': plats,
        'boxes':     [box1],
        'buttons':   [waters1btn, mov2btn],#btn1, btn2],
        'levers':    [mov1lev],#lever1, lever2],
        'mugs':      [mug1, mug2],
        'goals':     [goal],
        'enemies':   [pat1, detect1],
        'water':     [water1, water2],
        'health':    [],
        'catnip':    []
    }

    return levelName


''' level3 '''
def createLevel3():
    # platforms
    bottom = 550
    left = -200
    # platforms
    ceil   = Platform( 1000 - left, 0 , 3000 - left, 50 )
    floor   = Platform( 1000 - left, 600 , 3000 - left, 50 , floorplat = True)

    leftboundary = Platform(20 - left, bottom, 100, bottom)
    rightboundary = Platform(1800 - left, bottom, 100, bottom)

    startplat = Platform(600 - left, bottom, 150, 100)
    hiddenwaterplat1 = Platform(startplat.left_x() - 120, bottom, 60, 20, downMaxDist = 0, upMaxDist = 60)
    hiddenlevplat1 = Platform(startplat.left_x() - 210, bottom, 60, 60)
    hiddenwaterplat2 = Platform(startplat.left_x() - 350, bottom, 60, 20, downMaxDist = 0, upMaxDist = hiddenwaterplat1.upMaxDist)
    hiddenlevplat2 = Platform(startplat.left_x() - 420, bottom, 60, 60)

    tinyhiddenplat = Platform(startplat.left_x() - 50, bottom, 60, 2)

    plat1 = Platform(startplat.right_x() + 100, startplat.top_y() - 50, 80, 30)
    movingd = Platform(plat1.right_x() + 100, plat1.bot_y() + 30, 80, 30, upMaxDist =  10, downMaxDist = 30)

    mugplat = Platform(movingd.right_x() + 100, movingd.top_y() - 50, 80, 30)
    boxrespplat = Platform(mugplat.left_x()-100, mugplat.top_y() - 50, 80, 30)
    befend  = Platform(boxrespplat.right_x() + 100, boxrespplat.top_y() - 30, 80, 30)
    endplat  = Platform(befend.right_x() + 150, befend.top_y() - 30, 150, 30)
    enddoor  = Platform(endplat.left_x() + 10, endplat.top_y(), 20, 200, downMaxDist = 0, upMaxDist = 80)
    plat2  = Platform(boxrespplat.left_x() - 100, boxrespplat.top_y() - 30, 80, 30)
    #plat3  = Platform(plat2.left_x() - 100, plat2.top_y() - 30, 80, 30)
    btnmugplat = Platform(plat2.left_x() - 100, plat2.top_y() - 30, 80, 30)
    movinga = Platform(leftboundary.right_x() + 50, btnmugplat.bot_y() + 60, 100, 30, leftMaxDist = 0, rightMaxDist =  btnmugplat.left_x() - 120 - leftboundary.right_x())


    topleft = Platform(leftboundary.right_x() + 360/2, movinga.top_y() - 30, 360, 30)
    topleftdoor = Platform(topleft.right_x() - 10, topleft.top_y(), 20, topleft.top_y(), downMaxDist = 0, upMaxDist = 100)
    hiddendoor = Platform(topleft.left_x() + 100, topleft.top_y(), 20, topleft.top_y(), downMaxDist = 0, upMaxDist = 100)




    plats = [floor, leftboundary, rightboundary, startplat, 
            hiddenlevplat1, hiddenlevplat2, hiddenwaterplat1, hiddenwaterplat2, tinyhiddenplat,
            plat1, movingd, mugplat, boxrespplat, btnmugplat, movinga,
            plat2, topleftdoor, hiddendoor,
            topleft,
            befend, endplat, enddoor]


    ''' BOXES '''
    box1 = Box(startplat.right_x() - 22, startplat.top_y() - 40)

    ''' LEVERS '''
    dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : topleftdoor},
                       {"movespeed"  : Vec(1,0),  "deactspeed" : Vec(-1,0) , "target" : movinga}]}
    leverA = Lever(hiddenlevplat1, 20, effect = dic)
    
    dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : hiddendoor}]}            
    leverF = Lever(hiddenlevplat2, 40, effect = dic)
    
    dic = {  "move"  : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : enddoor}],
             "spawn" : [{"target": Box(370 , 200 , 44 , 44 , 'box_1')},
                        {"target" : PickUp(hiddendoor.left_x() - 40, topleft.top_y() - 30, "catnip")},
                        {"target" : leverF}]}
    leverB = Lever(topleft, 200, effect = dic)

    dic = { "respawn" : [{"target": box1}]
                  }
    leverE = Lever(boxrespplat, 40, effect = dic, autodeactivate = True)


    ''' BUTTONS '''
    dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : topleftdoor}]
                               }
    btnC = Button(btnmugplat, 40, effect = dic)

    dic = {  "move" : [{"movespeed"  : Vec(0,-1), "deactspeed" : Vec(0,1) , "target" : hiddenwaterplat1}]
                               }
    btnG = Button(tinyhiddenplat, 20, width = 60, effect = dic)

    dic = {  "conMove" : [{"movespeed"  : Vec(0,0.5), "target" : movingd} ]
                                }
    btnD = Button(plat1, 40, effect = dic)

    '''WATER '''
    water1 = Water(leftboundary.right_x() + round((startplat.left_x() - leftboundary.right_x())/2) - 2, bottom, startplat.left_x() - leftboundary.right_x() + 4, 40)


    '''PICKUPS'''
    mug1spawn = PickUp(0,0, "catnip")
    mug2spawn = PickUp(0,0, "health")


    ''' MUGS '''
    mug1 = Mug(btnmugplat , 50, spawnItem = mug1spawn)
    mug2 = Mug(mugplat , 50, spawnItem = mug2spawn)

    '''ENEMIES'''

    pat1 = PatrollingEnemy(floor, 1400 - left, 300)
    detect1 = IntelligentEnemy(floor, 1300)
    detect2 = IntelligentEnemy(floor, 1600)


    '''GOAL'''
    goal = LevelGoal(endplat, 100)


    levelName = {
        'name': 'level3',
        'settings': {
            'spawn': Vec(endplat.right_x(),100),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        'platforms': plats,
        'boxes':     [box1],
        'buttons':   [btnC, btnD, btnG],
        'levers':    [ leverB, leverE, leverA],
        'mugs':      [mug1, mug2],
        'goals':     [goal],
        'enemies':   [pat1, detect1, detect2],
        'water':     [water1],
        'health':    [],
        'catnip':    []
    }

    return levelName



''' End Level '''
def createLevel4():
    # platforms
    left = -200

    ceil   = Platform( 1000 - left, 0 , 3000 - left, 50 )
    floor   = Platform( 1000, 600 , 2000 , 50 , floorplat = True )
    WINPLAT = Platform( 400, 500, 400, 30)
    win = PickUp(0,0,"health")
    mug1 = Mug(WINPLAT , 50 , spawnItem = win, width = 100, height = 100, final = True)

    levelName = {
        'name': 'level4',
        'settings': {
            'spawn': Vec(330,550),
            'length': 5000,
            'track': 'nyan.mp3'
        },
        'platforms': [WINPLAT, floor],
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
level3 = createLevel3()
level4 = createLevel4()

# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
pickleLevel(level3, 'level3')
pickleLevel(level4, 'level4')
