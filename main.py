import pygame
import sys
import random
from pygame.locals import *

import config

def init_game():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((config.WINDOW_RESOLUTION[0], config.WINDOW_RESOLUTION[1]))
    pygame.display.set_caption("Snake Game")
    return screen

def draw_score(screen, font, score):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def main():
    screen = init_game()
    clock = pygame.time.Clock()

    CELL_SIZE = 10
    direction = 1
    update_snake = 0
    score = 0

    snake_pos = [[int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2)]] # head
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + CELL_SIZE]) # body segment
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + CELL_SIZE * 2]) # body segment
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + CELL_SIZE * 3]) # body segment
    apple_pos = [random.randint(0, config.WINDOW_RESOLUTION[0] // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, config.WINDOW_RESOLUTION[1] // CELL_SIZE - 1) * CELL_SIZE]

    font = pygame.font.SysFont(None, 35)

    # pygame.mixer.music.load("background_music.mp3")
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(-1)

    running = True
    while running:
        running = handle_events()
        screen.fill((255, 255, 255))

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()