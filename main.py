import pygame
import sys
from pygame.locals import *

pygame.init()

# Finals
WINDOW_SIZE = (960, 640)
FPS_CAP = 60
SKY_COLOR = (146, 244, 255)
TILE_SIZE = 32

clock = pygame.time.Clock()
pygame.display.set_caption("Platformer")
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen.fill((192, 192, 192))

# tiles
grass_image = pygame.image.load("images/Asset 4.png")
sand_image = pygame.image.load("images/Asset 3.png")
brick_image = pygame.image.load("images/Asset 5.png")
dirt_image = pygame.image.load("images/Asset 6.png")

def loadMap(path):
    file = open(path + ".txt", "r")
    data = file.read()
    data = data.splitlines()
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = loadMap("map/map")
true_scroll = [0, 0]


# player
moving_right = False
moving_left = False
jumping = False
sliding = False
player_image = pygame.image.load("images/Asset 2.png")
player_location = [400, 100]
player_vert_momentum = 0
air_time = 0
player_hitbox = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())


def collision_check(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:  # moving right
            rect.right = tile.left
            collision_type['right'] = True
        elif movement[0] < 0:  # moving left
            rect.left = tile.right
            collision_type['left'] = True
    rect.y += movement[1]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:  # moving down
            rect.bottom = tile.top
            collision_type['bottom'] = True
        elif movement[1] < 0:  # moving up
            rect.top = tile.bottom
            collision_type['top'] = True

    return rect, collision_type


# game loop
while True:
    screen.fill(SKY_COLOR)

    true_scroll[0] += (player_hitbox.x - true_scroll[0] - 448)/10
    true_scroll[1] += (player_hitbox.y - true_scroll[1] - 296)/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # initializing the map
    tile_rect = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                screen.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    # player movement
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player_vert_momentum
    player_vert_momentum += 0.5
    if player_vert_momentum > 5: # caps vertical momentum
        player_vert_momentum = 5

    player_hitbox, collisions = move(player_hitbox, player_movement, tile_rect)
    if collisions['bottom']:
        player_vert_momentum = 0
        air_time = 0
    else:
        air_time += 1
    if collisions['top']:
        player_vert_momentum = -player_vert_momentum

    screen.blit(player_image, (player_hitbox.x - scroll[0], player_hitbox.y - scroll[1]))
    # end of player movement

    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                if air_time < 6:
                    jumping = True
                    player_vert_momentum = -10
            if event.key == K_s:
                sliding = True
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                jumping = False
            if event.key == K_s:
                sliding = False


    pygame.display.update()
    clock.tick(FPS_CAP)

