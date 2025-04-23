import pygame, sys, random
import numpy as np
from pygame.locals import *
from pygame.sndarray import array as sndarray_array, make_sound as sndarray_make

import config

# User event for scheduling full-loop playback
REMAINDER_DONE = pygame.USEREVENT + 1

# 1) Initialize Pygame & Mixer
pygame.mixer.pre_init(frequency=config.BASE_FREQ, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

# 2) Resampling helper
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
    return np.ascontiguousarray(new, dtype=arr.dtype)

# 3) Create a pitched Sound and return it + its sample length
def make_pitched_sound(factor: float, orig_array: np.ndarray):
    arr = resample_array(orig_array, factor)
    return sndarray_make(arr), arr.shape[0]

# 4) Game init
def init_game():
    screen = pygame.display.set_mode(
        (config.WINDOW_RESOLUTION[0], config.WINDOW_RESOLUTION[1]),
        pygame.RESIZABLE | pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Snake Game")
    return screen

# Drawing helpers (unchanged)
def draw_score(screen, font, score, cell_size):
    txt = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(txt, (cell_size, cell_size))

def draw_apple(screen, apple_pos, cell_size):
    pygame.draw.rect(screen, config.COLORS["apple_color"], (*apple_pos, cell_size, cell_size))

def draw_snake(screen, snake_pos, cell_size):
    for i, segment in enumerate(snake_pos):
        outer = config.COLORS["body_outer"]
        inner = config.COLORS["body_inner"] if i>0 else config.COLORS["body_inner"]
        pygame.draw.rect(screen, outer, (*segment, cell_size, cell_size))
        pygame.draw.rect(screen, inner, (segment[0]+1, segment[1]+1, cell_size-2, cell_size-2))

# Event handler unchanged
def handle_events(direction, actual_resolution):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            elif event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            elif event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            elif event.key == pygame.K_LEFT and direction != 2:
                direction = 4
        elif event.type == WINDOWRESIZED:
            actual_resolution = pygame.display.get_window_size()
        elif event.type == REMAINDER_DONE:
            # swap in full-looped pitched sound
            music_chan.play(full_snd, loops=-1)
            pygame.time.set_timer(REMAINDER_DONE, 0)
    return True, direction, actual_resolution

# Main
def main():
    screen = init_game()
    clock = pygame.time.Clock()
    actual_resolution = pygame.display.get_window_size()

    # Load original sound and its PCM array
    orig_sound = pygame.mixer.Sound(config.MUSIC)
    orig_array = sndarray_array(orig_sound)
    music_chan = pygame.mixer.Channel(0)

    # Start playback at normal pitch
    pitch_factor = 1.0
    full_snd, full_length = make_pitched_sound(pitch_factor, orig_array)
    music_chan.play(full_snd, loops=-1)
    start_ms = pygame.time.get_ticks()

    # Game variables
    cell_size = config.CELL_SIZE
    direction = 1
    score = 0
    base_fps = config.FPS

    # Snake & apple setup
    snake_pos = [[config.WINDOW_RESOLUTION[0]//2, config.WINDOW_RESOLUTION[1]//2]
                ] + [[config.WINDOW_RESOLUTION[0]//2,
                      config.WINDOW_RESOLUTION[1]//2 + i*cell_size]
                     for i in range(1,4)]
    apple_pos = [random.randint(0, actual_resolution[0]//cell_size-1)*cell_size,
                 random.randint(0, actual_resolution[1]//cell_size-1)*cell_size]

    font = pygame.font.SysFont(None, 35)
    running = True

    while running:
        ev = handle_events(direction, actual_resolution)
        if ev is False:
            running = False
        else:
            running, direction, actual_resolution = ev

        screen.fill(config.COLORS["background"])

        # Move head
        head_x, head_y = snake_pos[0]
        if direction == 1: head_y -= cell_size
        elif direction == 2: head_x += cell_size
        elif direction == 3: head_y += cell_size
        elif direction == 4: head_x -= cell_size

        snake_pos.insert(0, [head_x, head_y])
        snake_pos.pop()

        # Apple collision
        if snake_pos[0] == apple_pos:
            apple_pos = [random.randint(0, actual_resolution[0]//cell_size-1)*cell_size,
                         random.randint(0, actual_resolution[1]//cell_size-1)*cell_size]
            snake_pos.append(snake_pos[-1])
            score += 1

            if score % 10 == 0:
                # Increase pitch and FPS
                pitch_factor *= 1.25
                base_fps    += 2

                # Compute elapsed samples
                elapsed_ms      = pygame.time.get_ticks() - start_ms
                elapsed_samples = int((elapsed_ms/1000.0) * config.BASE_FREQ)

                # Create new pitched sound & get length
                new_snd, new_length = make_pitched_sound(pitch_factor, orig_array)

                # Slice remainder
                new_start   = int(elapsed_samples / pitch_factor)
                remainder   = resample_array(orig_array, pitch_factor)[new_start:]
                remainder   = np.ascontiguousarray(remainder, dtype=remainder.dtype)
                remainder_snd = sndarray_make(remainder)

                # Play remainder, then schedule full loop
                music_chan.play(remainder_snd, loops=0)
                rem_ms = int((new_length-new_start)/config.BASE_FREQ*1000)
                full_snd = new_snd
                pygame.time.set_timer(REMAINDER_DONE, rem_ms)

                # Re-sync start time
                start_ms = pygame.time.get_ticks() - elapsed_ms

        # Draw everything
        draw_snake(screen, snake_pos, cell_size)
        draw_apple(screen, apple_pos, cell_size)
        draw_score(screen, font, score, cell_size)

        pygame.display.flip()
        clock.tick(base_fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()