# game options/settings
TITLE = "Jumpy!"
WIDTH = 600
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

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
PLAYER_SPAWN_X = 0
PLAYER_SPAWN_Y = 500

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 10, 2000, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50, 220, 40),
                 (1000, HEIGHT - 350, 260, 40),
                 (350, 200, 200, 40),
                 (175, 100, 260, 40)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

#Level 1
length = 5000

l1_vases = ()

l1_boxes = [(200, HEIGHT - 50,  40, 40, "box 1")]

