from Vector import *

# Description: 

# game options/settings
TITLE = "Catformer!"
WIDTH = 600
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
DEFAULT_LEVEL = "level1"

# Camera Options
CAMERA_BORDER_R = WIDTH * 2/3
CAMERA_BORDER_L = WIDTH / 3

#Platform types
bot_plat = 1
basic_plat = 2
moving_plat = 3

# Player properties
PLAYER_ACC = 0.4
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.7
PLAYER_JUMP = 13
PLAYER_LIVES = 9
PLAYER_CATNIP = 0
PLAYER_SPAWN = Vec()

# Game properties
GRAVITY = 0.7
FRICTION = -0.12
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0
VOLUME = 0.0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE


