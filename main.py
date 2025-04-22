import pygame
import sys
import config

def init_game():
    pygame.init()
    
    screen = pygame.display.set_mode((config.WINDOW_RESOLUTION[0], config.WINDOW_RESOLUTION[1]))
    pygame.display.set_caption("Pygame Template")
    return screen

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