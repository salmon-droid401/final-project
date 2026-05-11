import pygame
import math

pygame.init()
pygame.display.set_caption("Garden Escape")
resolution = (1920, 1080)
player_vel = 10
screen = pygame.display.set_mode(resolution)


class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    gravity = 1
    sprite = pygame.image.load("Player.png")

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction =  "left"
        self.animation_count = 0
        self.fall_count = 0

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
        # self.y_vel += min(1,  (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = pygame.image.load("Block.png")
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(player_vel)
    if keys[pygame.K_d]:
        player.move_right(player_vel)

def draw(screen, background, player, objects):
    screen.blit(background, (0,0))
    
    for obj in objects:
        obj.draw(screen)
    
    player.draw(screen)

    pygame.display.update()

def main():
    bg = pygame.image.load("Background.png")
    fps = 60
    clock = pygame.time.Clock()
    block_size = 64

    player = Player(100, 100, 64, 64)
    blocks = [Block(0, 1080 - block_size, block_size)]
    running = True

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.loop(fps)
        handle_move(player)
        draw(screen, bg, player, blocks)

    pygame.quit()

if __name__ == "__main__":
    main()