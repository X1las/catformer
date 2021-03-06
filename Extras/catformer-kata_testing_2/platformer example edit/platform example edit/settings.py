# game options/settings
TITLE = "Jumpy!"
WIDTH = 1000
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.7
PLAYER_JUMP = 20

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

l1_platforms = [(-400,    HEIGHT - 10,  length, 60, True),
                (300,  HEIGHT / 2,   500,    40, False),
                (1000, HEIGHT - 350, 260,    40, False),
                (1500, HEIGHT - 200, 200,    40, False),
                (600,  HEIGHT - 100, 260,    40, False),
                (800,  HEIGHT - 100, 260,    40, False),
                (1108, HEIGHT - 100, 260,    40, False),
                (750,  HEIGHT - 100, 260,    40, False),
                (450,  HEIGHT - 100, 260,    40, False)]


l1_platforms = [(-400,    HEIGHT - 10,  length, 60, True),
                (300,  HEIGHT / 2,   500,    40, False),
                #(1000, HEIGHT - 350, 260,    40, False),
                #(1500, HEIGHT - 200, 200,    40, False),
                #(600,  HEIGHT - 100, 260,    40, False),
                #(800,  HEIGHT - 100, 260,    40, False),
                (1108, HEIGHT - 100, 260,    40, False),
                (750,  HEIGHT - 100, 260,    40, False),
                (450,  HEIGHT - 100, 260,    40, False)]




l1_boxes = [(400, HEIGHT - 50,  40, 40)]

