import pygame
from classes import Birds, Box, HollowBox, PlankFull, FullBox, Enemy, Boss, Blue, Yellow, White

pygame.init()

# Screen setup
width = 1920
height = 1080
game_display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Angy Bids')
clock = pygame.time.Clock()
boxes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
KingPig = pygame.sprite.Group()

hollow1 = HollowBox(700,760)
hollow2 = HollowBox(760,760)
hollow3 = HollowBox(730,700)

full1 = FullBox(900, 760)
full2 = FullBox(900, 676)
full3 = FullBox(900, 598)

# hollow4 = ()
# hollow5 = ()
# plankFull1 = ()
# hollow6 = ()
# hollow7 = ()
# plankFull2 = ()
# full4 = ()

# enemy1 = ()
# enemy2 = ()
# enemy3 = ()
# enemy4 = ()

# hollow4, hollow5, hollow6, hollow7, full1, full2, full3, full4, plankFull1, plankFull2
# enemy1, enemy2, enemy3, enemy4
boxes.add(hollow1, hollow2, hollow3, full1, full2, full3)
enemies.add()
# Load images
background_img = pygame.image.load('volcano.png')
slingshot_img = pygame.image.load('slingshot.png')
bird_img = pygame.image.load('red.png')
blue_img = pygame.image.load('blue.png')
yellow_img = pygame.image.load('yellow.png')
white_img = pygame.image.load('white.png')

# Resize images
background = pygame.transform.scale(background_img, (width, height))
slingshot = pygame.transform.scale(slingshot_img, (110, 100))
bird_scaled = pygame.transform.scale(bird_img, (51, 49))
blue_scaled = pygame.transform.scale(blue_img,(51, 49))
yellow_scaled = pygame.transform.scale(yellow_img,(51, 49))
white_scaled = pygame.transform.scale(white_img,(51, 49))

# Create Bird instance (spawns on slingshot)
player_bird = Birds(130, 840, bird_scaled)
player_blue = Blue(130, 840, blue_scaled)
player_yellow = Yellow(130, 840, yellow_scaled)
player_white = White(130, 840, white_scaled)
all_sprites = pygame.sprite.Group(player_bird, player_blue, player_yellow, player_white)

birds = []
current_bird = None

def draw_trajectory(surface, bird):
    """Draws the predicted trajectory while dragging."""
    if bird.dragging:
        for point in bird.trajectory_points:
            pygame.draw.circle(surface, (255, 255, 255), point, 5) 

# Game loop
running = True
while running:
    game_display.blit(background, (0, 0))
    game_display.blit(slingshot, (75, 832))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_bird.rect.collidepoint(event.pos):
                player_bird.start_drag()

        elif event.type == pygame.MOUSEBUTTONUP:
            if player_bird.dragging:
                player_bird.end_drag()

    all_sprites.update(boxes, enemies)
    birds = [sprite for sprite in all_sprites if isinstance(sprite, Birds)]
    boxes.update(boxes, birds)
    enemies.update(enemies, birds)

    box_hits = pygame.sprite.spritecollide(player_bird, boxes, False)
    for box in box_hits:
        box.hit()
        player_bird.velocity[0] *= 0.6
        player_bird.velocity[1] *= 0.6

    draw_trajectory(game_display, player_bird)
    all_sprites.draw(game_display)
    boxes.draw(game_display)
    enemies.draw(game_display)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
