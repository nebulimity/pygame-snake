import pygame
pygame.mixer.init()

WINDOW_RESOLUTION = (800, 600)
FPS = 10
VOLUME = 1
MUSIC = "sounds/mule_bitblaster_mix.wav"
CELL_SIZE = 25
HIGH_SCORE_FILE = "high_score.txt"
try:
    with open(HIGH_SCORE_FILE, "r") as f:
        HIGH_SCORE = int(f.read())
except (FileNotFoundError, ValueError):
    HIGH_SCORE = 0

COLORS = {
    "background_1": (170,215,81),
    "background_2": (162,209,73),
    "red": (255, 0, 0),
    "black": (0, 0, 0),
    "body_inner": (78,124,246),
    "body_outer": (78,124,246),
    "apple_color": (231,71,29)
}
SOUNDS = {
    "up": pygame.mixer.Sound("sounds/sfx/up.wav"),
    "right": pygame.mixer.Sound("sounds/sfx/right.wav"),
    "down": pygame.mixer.Sound("sounds/sfx/down.wav"),
    "left": pygame.mixer.Sound("sounds/sfx/left.wav"),
    "eat": pygame.mixer.Sound("sounds/sfx/eat.wav"),
    "bump": pygame.mixer.Sound("sounds/sfx/bump.wav"),
    "win": pygame.mixer.Sound("sounds/sfx/win.wav"),
}

def save_high_score():
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(HIGH_SCORE))
    except IOError as e:
        print(f"Error saving high score: {e}")