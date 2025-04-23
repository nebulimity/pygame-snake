import pygame
import sys
import random
import numpy as np
from pygame.locals import *
from pygame.sndarray import array as sndarray_array, make_sound as sndarray_make

import config

def init_game():
    pygame.mixer.pre_init(frequency=config.BASE_FREQ, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((config.WINDOW_RESOLUTION[0], config.WINDOW_RESOLUTION[1]), pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake Game")
    return screen

def draw_score(screen, font, score, cell_size):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (cell_size, cell_size))

def draw_apple(screen, apple_pos, cell_size):
    pygame.draw.rect(screen, config.COLORS["apple_color"], (apple_pos[0], apple_pos[1], cell_size, cell_size))

def draw_snake(screen, snake_pos, cell_size):
    for i in range(len(snake_pos)):
            segment = snake_pos[i]
            if i == 0: # head
                pygame.draw.rect(screen, config.COLORS["body_outer"], (segment[0], segment[1], cell_size, cell_size))
                pygame.draw.rect(screen, config.COLORS["body_inner"], (segment[0] + 1, segment[1] + 1, cell_size - 2, cell_size - 2))
            else:
                pygame.draw.rect(screen, config.COLORS["body_outer"], (segment[0], segment[1], cell_size, cell_size))
                pygame.draw.rect(screen, config.COLORS["body_inner"], (segment[0] + 1, segment[1] + 1, cell_size - 2, cell_size - 2))

def handle_events(direction, actual_resolution):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3: # up
                direction = 1
            elif event.key == pygame.K_RIGHT and direction != 4: # down
                direction = 2
            elif event.key == pygame.K_DOWN and direction != 1: # left
                direction = 3
            elif event.key == pygame.K_LEFT and direction != 2: # right
                direction = 4
        elif event.type == WINDOWRESIZED:
            actual_resolution = pygame.display.get_window_size()
    return True, direction, actual_resolution

def resample_array(arr: np.ndarray, factor: float) -> np.ndarray:
    old_length = arr.shape[0]
    new_length = int(old_length / factor)
    old_idx = np.arange(old_length)
    new_idx = np.linspace(0, old_length - 1, new_length)
    if arr.ndim == 1:
        new = np.interp(new_idx, old_idx, arr)
    else:
        new = np.vstack([
            np.interp(new_idx, old_idx, arr[:, ch])
            for ch in range(arr.shape[1])
        ]).T
    return new.astype(arr.dtype)

def make_pitched_sound(factor: float, orig_array) -> pygame.mixer.Sound:
    resampled = resample_array(orig_array, factor)
    resampled = np.ascontiguousarray(resampled, dtype=resampled.dtype)
    return sndarray_make(resampled)

def main():
    screen = init_game()
    clock = pygame.time.Clock()
    actual_resolution = pygame.display.get_window_size()

    orig_sound = pygame.mixer.Sound(config.MUSIC)
    orig_array = sndarray_array(orig_sound)
    music_chan = pygame.mixer.Channel(0)
    music_chan.play(orig_sound, loops=-1)

    cell_size = config.CELL_SIZE
    direction = 1
    score = 0
    base_fps = config.FPS
    current_pitch = 1

    snake_pos = [[int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2)]] # head
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + cell_size]) # body segment
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + cell_size * 2]) # body segment
    snake_pos.append([int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + cell_size * 3]) # body segment
    apple_pos = [random.randint(0, config.WINDOW_RESOLUTION[0] // cell_size - 1) * cell_size, random.randint(0, config.WINDOW_RESOLUTION[1] // cell_size - 1) * cell_size]

    font = pygame.font.SysFont(None, 35)

    pygame.mixer.music.load(config.MUSIC)
    pygame.mixer.music.set_volume(config.VOLUME)
    pygame.mixer.music.play(-1)

    running = True
    while running:
        running, direction, actual_resolution = handle_events(direction, actual_resolution)
        screen.fill(config.COLORS["background"])

        head_x, head_y = snake_pos[0]

        if direction == 1:  # up
            head_y -= cell_size
        elif direction == 2:  # right
            head_x += cell_size
        elif direction == 3:  # down
            head_y += cell_size
        elif direction == 4:  # left
            head_x -= cell_size

        snake_pos.insert(0, [head_x, head_y])
        snake_pos.pop()

        if snake_pos[0] == apple_pos:
            apple_pos = [random.randint(0, actual_resolution[0] // cell_size - 1) * cell_size, random.randint(0, actual_resolution[1] // cell_size - 1) * cell_size]
            snake_pos.append(snake_pos[-1])
            score += 1

            if score % 10 == 0:
                current_pitch *= 1.25
                new_snd = make_pitched_sound(current_pitch, orig_array)
                music_chan.fadeout(200)
                music_chan.play(new_snd, loops=-1, fade_ms=200)

                base_fps += 2

        if head_x < 0 or head_x >= actual_resolution[0] or head_y < 0 or head_y >= actual_resolution[1] or snake_pos[0] in snake_pos[1:]:
            running = False

        draw_snake(screen, snake_pos, cell_size)
        draw_apple(screen, apple_pos, cell_size)
        draw_score(screen, font, score, cell_size)

        pygame.display.flip()
        clock.tick(base_fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()