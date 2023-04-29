import os.path

import pygame as pg
import random


# define colors, colors work in a (RGB) format.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0,175,255)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PINK = (255,0,255)
ORANGE = (255,127,0)
DARK_GRAY = (64,64,64)
LIGHT_GRAY = (192,192,192)
GRAY_BLUE = (92,192,194)

BG_COLOR = LIGHT_BLUE
colors = (WHITE,BLUE,BLACK,RED,GREEN,YELLOW,TEAL,PINK,ORANGE)



#Game Title
TITLE = "JumpBug"




# Window Settings
WIDTH = 500
HEIGHT = 750
DEFAULT_COLOR = BLACK
TILE_SIZEX = WIDTH/10
TILE_SIZEY = HEIGHT/10


# camera settings
FPS = 60
FONT_NAME = "comic_sans"

# file locations
#gets location of file on computer
game_folder = os.path.dirname(__file__)
game_folder = game_folder.replace("\scripts","")
sprites_folder = os.path.join(game_folder,"sprites")
backgroundSprites = os.path.join(sprites_folder,"Backgrounds")


scripts_folder = os.path.join(game_folder,"scripts")
HS_FILE = os.path.join(scripts_folder,"highscore.txt")

spriteSheets = os.path.join(sprites_folder,"Spritesheets")
SPRITESHEET = os.path.join(spriteSheets, "spritesheet_jumper.png")

snd_folder = os.path.join(game_folder, "snds")
jump_sound_effect = os.path.join(snd_folder, "Jump33.wav") #bfxr is good sound generator
default_music = os.path.join(snd_folder, "HappyTuneReal.wav")
title_music = os.path.join(snd_folder, "Yippee.wav")



# player Settings
PLAYER_STILL = (614,1063,120,191)



PLAYER_ACC = 0.75
PLAYER_FRICTION = -0.12 #teeny tiny number
PLAYER_GRAV = 0.7
PLAYER_JUMP = 18
PLAYER_LAYER = 2


#Powerup Settings
BOOST_POWER = 60
POW_SPAWN_PCT = 4
boost_sound_effect = os.path.join(snd_folder, "Boost16.wav")
POW_LAYER = 1

#Starting Platforms
PLATFORM_IMG = (534,1063)
PLATFORM_LIST = [(0, HEIGHT-60),
                (WIDTH/2-50, HEIGHT*3/4),
                 (125, HEIGHT-350),
                 (350,200),
                 (175,100)]
PLATFORM_LAYER = 1

# Enemy Settings
MOB_FREQ = 5000
MOB_LAYER = 2


#Clouds
CLOUD_LAYER = 0



