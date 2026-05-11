import pygame

def main():
    pygame.init()
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Garden Escape")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()