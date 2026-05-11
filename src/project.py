import pygame

pygame.init()
pygame.display.set_caption("Garden Escape")
resolution = (1920, 1080)
screen = pygame.display.set_mode(resolution)

class Player():

    def __init__(self):
        pass

def main():
    bg = pygame.image.load("Background.png")
    fps = 60
    clock = pygame.time.Clock()
    running = True

    while running:

        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()