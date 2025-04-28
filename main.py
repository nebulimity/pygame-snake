import pygame
import sys
import random
import config

def draw_snake(screen, snake_pos):
    index = 0
    for segment in snake_pos:
        pygame.draw.rect(screen, config.COLORS["body_inner"], (segment[0], segment[1], config.CELL_SIZE, config.CELL_SIZE))
        pygame.draw.rect(screen, config.COLORS["body_inner"], (segment[0] + 1, segment[1] + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
        index += 1

def draw_apple(screen, apple_pos):
    pygame.draw.rect(screen, config.COLORS["apple_color"], (apple_pos[0], apple_pos[1], config.CELL_SIZE, config.CELL_SIZE))

def draw_text(screen, score, font, fps):
    score_text = font.render(f"Score: {score}", True, config.COLORS["black"])
    high_score_text = font.render(f"High Score: {config.HIGH_SCORE}", True, config.COLORS["black"])
    speed_text = font.render(f"Speed: {fps / 10}", True, config.COLORS["black"])
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(speed_text, (10, 70))

def draw_checkers(screen):
    for x in range(0, config.WINDOW_RESOLUTION[0], config.CELL_SIZE):
        for y in range(0, config.WINDOW_RESOLUTION[1], config.CELL_SIZE):
            if (x // config.CELL_SIZE + y // config.CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, config.COLORS["background_1"], (x, y, config.CELL_SIZE, config.CELL_SIZE))
            else:
                pygame.draw.rect(screen, config.COLORS["background_2"], (x, y, config.CELL_SIZE, config.CELL_SIZE))

def spawn_apple(snake_pos):
    max_x = (config.WINDOW_RESOLUTION[0] - config.CELL_SIZE) // config.CELL_SIZE
    max_y = (config.WINDOW_RESOLUTION[1] - config.CELL_SIZE) // config.CELL_SIZE
    x = random.randint(0, max_x) * config.CELL_SIZE
    y = random.randint(0, max_y) * config.CELL_SIZE
    apple = [x, y]
    if apple in snake_pos:
        return spawn_apple(snake_pos)
    return apple

def run_snake_game():
    screen = pygame.display.set_mode(config.WINDOW_RESOLUTION, pygame.RESIZABLE)
    pygame.display.set_caption("Snake - Game")
    clock = pygame.time.Clock()

    direction = 1
    score = 0
    snake_pos = [[int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2)]]
    snake_pos.extend([[int(config.WINDOW_RESOLUTION[0] / 2), int(config.WINDOW_RESOLUTION[1] / 2) + config.CELL_SIZE * i] for i in range(1, 4)])
    apple_pos = [random.randint(0, (config.WINDOW_RESOLUTION[0] - config.CELL_SIZE) // config.CELL_SIZE) * config.CELL_SIZE,
                 random.randint(0, (config.WINDOW_RESOLUTION[1] - config.CELL_SIZE) // config.CELL_SIZE) * config.CELL_SIZE]
    font = pygame.font.SysFont(None, 35)
    fps = config.FPS

    running_game = True
    while running_game:
        draw_checkers(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save_high_score()
                running_game = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                new_direction = direction
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 3:
                    new_direction = 1
                    config.SOUNDS["up"].play()
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 4:
                    new_direction = 2
                    config.SOUNDS["right"].play()
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 1:
                    new_direction = 3
                    config.SOUNDS["down"].play()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 2:
                    new_direction = 4
                    config.SOUNDS["left"].play()

                direction = new_direction

        head_x, head_y = snake_pos[0]
        if direction == 1: head_y -= config.CELL_SIZE
        elif direction == 2: head_x += config.CELL_SIZE
        elif direction == 3: head_y += config.CELL_SIZE
        elif direction == 4: head_x -= config.CELL_SIZE

        snake_pos.insert(0, [head_x, head_y])

        if snake_pos[0] == apple_pos:
            score += 1
            if score > config.HIGH_SCORE:
                config.HIGH_SCORE = score
            if score % 10 == 0 and fps < 30:
                fps += 2
            apple_pos = spawn_apple(snake_pos)
            pygame.mixer.Sound.play(config.SOUNDS["eat"])
        else:
            snake_pos.pop()

        if (snake_pos[0][0] < 0 or snake_pos[0][0] >= config.WINDOW_RESOLUTION[0] or
            snake_pos[0][1] < 0 or snake_pos[0][1] >= config.WINDOW_RESOLUTION[1] or
            snake_pos[0] in snake_pos[1:]):
            pygame.mixer.Sound.play(config.SOUNDS["bump"])
            running_game = False

        draw_apple(screen, apple_pos)
        draw_snake(screen, snake_pos)
        draw_text(screen, score, font, fps)

        pygame.display.flip()
        clock.tick(fps)

    config.save_high_score()

def main_menu():
    screen = pygame.display.set_mode(config.WINDOW_RESOLUTION, pygame.RESIZABLE)
    pygame.display.set_caption("Snake - Main Menu")
    font = pygame.font.SysFont(None, 40)
    snake_font = pygame.font.SysFont(None, 100)
    button_color = (87, 138, 52)
    text_color = (255, 255, 255)

    pygame.mixer.music.load(config.MUSIC)
    pygame.mixer.music.set_volume(config.VOLUME)
    pygame.mixer.music.play(-1)

    snake_text = snake_font.render("Snake Game", True, text_color)
    snake_text_rect = snake_text.get_rect(center=(config.WINDOW_RESOLUTION[0] // 2, config.WINDOW_RESOLUTION[1] // 4))

    play_button_rect = pygame.Rect(0, config.WINDOW_RESOLUTION[1] // 3, 200, 50)
    play_button_rect.centerx = config.WINDOW_RESOLUTION[0] // 2
    play_button_rect.y = config.WINDOW_RESOLUTION[1] // 2
    play_text = font.render("Play Game", True, text_color)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)

    exit_button_rect = pygame.Rect(0, config.WINDOW_RESOLUTION[1] // 2, 200, 50)
    exit_button_rect.centerx = config.WINDOW_RESOLUTION[0] // 2
    exit_button_rect.y = config.WINDOW_RESOLUTION[1] // 2 + 60
    exit_text = font.render("Exit Game", True, text_color)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)

    running_menu = True
    while running_menu:
        draw_checkers(screen)

        pygame.draw.rect(screen, button_color, play_button_rect)
        screen.blit(play_text, play_text_rect)

        pygame.draw.rect(screen, button_color, exit_button_rect)
        screen.blit(exit_text, exit_text_rect)

        screen.blit(snake_text, snake_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save_high_score()
                running_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    run_snake_game()
                elif exit_button_rect.collidepoint(event.pos):
                    running_menu = False
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    main_menu()