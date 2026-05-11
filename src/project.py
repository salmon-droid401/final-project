import pygame
import math

pygame.init()
pygame.display.set_caption("Garden Escape")
resolution = (1920, 1080)
player_vel = 10
screen = pygame.display.set_mode(resolution)

class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction =  "left"
        self.animation_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(player_vel)
    if keys[pygame.K_d]:
        player.move_right(player_vel)

def main():
    bg = pygame.image.load("Background.png")
    fps = 60
    clock = pygame.time.Clock()
    player = Player(100, 100, 64, 64)
    running = True

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg, (0,0))

        player.loop(fps)
        handle_move(player)
        player.draw(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()