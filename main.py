import pygame
import sys
import random
from pygame.locals import *

import config

def init_game():
    pygame.init()
    
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
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 3: # up
                direction = 1
                config.SOUNDS["up"].play()
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 4: # down
                direction = 2
                config.SOUNDS["right"].play()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 1: # left
                direction = 3
                config.SOUNDS["down"].play()
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 2: # right
                direction = 4
                config.SOUNDS["left"].play()
        elif event.type == WINDOWRESIZED:
            actual_resolution = pygame.display.get_window_size()
    return True, direction, actual_resolution

def main():
    screen = init_game()
    clock = pygame.time.Clock()
    actual_resolution = pygame.display.get_window_size()

    cell_size = config.CELL_SIZE
    direction = 0
    score = 0
    base_fps = config.FPS

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
        screen.fill(config.COLORS["background_1"])
        for y in range(0, actual_resolution[1], cell_size):
            for x in range(0, actual_resolution[0], cell_size):
                if (x // cell_size + y // cell_size) % 2 == 0:
                    pygame.draw.rect(screen, config.COLORS["background_2"], (x, y, cell_size, cell_size))

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
            config.SOUNDS["eat"].play()

            if score % 10 == 0:
                base_fps += 2

        if head_x < 0 or head_x >= actual_resolution[0] or head_y < 0 or head_y >= actual_resolution[1] or snake_pos[0] in snake_pos[1:]:
            running = False
            config.SOUNDS["bump"].play()

        draw_snake(screen, snake_pos, cell_size)
        draw_apple(screen, apple_pos, cell_size)
        draw_score(screen, font, score, cell_size)

        pygame.display.flip()
        clock.tick(base_fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()