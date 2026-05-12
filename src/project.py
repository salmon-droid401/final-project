import pygame
import math

pygame.init()
pygame.display.set_caption("Garden Escape")
resolution = (1920, 1080)
player_vel = 10
screen = pygame.display.set_mode(resolution)


class Player(pygame.sprite.Sprite):
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
        self.jump_count = 0
    
    def jump(self):
        self.y_vel = -self.gravity * 6
        self.jump_count += 1

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
        self.y_vel += min(1,  (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self, screen, offset_x):
        screen.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, screen, offset_x):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = pygame.image.load("Block.png")
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        
        collided_objects.append(obj)

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    collide_left = collide(player, objects, -player_vel)
    collide_right = collide(player, objects, player_vel)

    player.x_vel = 0
    if keys[pygame.K_a] and not collide_left:
        player.move_left(player_vel)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(player_vel)

    handle_vertical_collision(player, objects, player.y_vel)

def draw(screen, background, player, objects, offset_x):
    screen.blit(background, (0,0))
    
    for obj in objects:
        obj.draw(screen, offset_x)
    
    player.draw(screen, offset_x)

    pygame.display.update()

def main():
    bg = pygame.image.load("Background.png")
    fps = 60
    clock = pygame.time.Clock()
    block_size = 64

    player = Player(400, 800, 64, 64)
    # floor = [Block(i* block_size, 1080 - block_size, block_size) 
    #         for i in range(-1920 // block_size * 2, block_size)]
    blocks = [Block(400, 1080 - block_size * 3, block_size), 
              Block(400 + block_size * 6, 1080 - block_size * 4, block_size),
              Block(400 + block_size * 7, 1080 - block_size * 4, block_size),
              Block(400 + block_size * 12, 1080 - block_size * 5, block_size),
              Block(400 + block_size * 17, 1080 - block_size * 6, block_size)]
    offset_x = 0
    scroll_area_width = 200
    running = True

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 1:
                    player.jump()
        
        player.loop(fps)
        handle_move(player, blocks)
        draw(screen, bg, player, blocks, offset_x)

        if ((player.rect.right - offset_x >= 1920 - scroll_area_width and player.x_vel > 0) or (
            player.rect.right - offset_x <= 1920 - scroll_area_width and player.x_vel < 0)):
            offset_x += player.x_vel

    pygame.quit()

if __name__ == "__main__":
    main()