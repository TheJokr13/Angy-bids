import pygame
import sys
import copy
from classes import Birds, Box, HollowBox, PlankFull, FullBox, Enemy, Boss, Blue, Yellow, White

pygame.init()

# Screen setup
width = 1920
height = 1080
game_display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Angy Bids')
clock = pygame.time.Clock()

# Create sprite groups
boxes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
birds_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create structures
# First tower
hollow1 = HollowBox(700, 760)
hollow2 = HollowBox(760, 760)
hollow3 = HollowBox(730, 700)

# Second tower
full1 = FullBox(900, 760)
full2 = FullBox(900, 676)
full3 = FullBox(900, 598)

# Third (rightmost) tower
hollow4 = HollowBox(1050, 760)
hollow5 = HollowBox(1110, 760)
plankFull1 = PlankFull(1030, 700)
hollow6 = HollowBox(1050, 640)
hollow7 = HollowBox(1110, 640)
plankFull2 = PlankFull(1030, 580)
full4 = FullBox(1080, 520)

# Add enemies
enemy1 = Enemy(730, 640, 1)  # Place enemy on top of hollow3
enemy2 = Enemy(900, 525, 1)  # Place enemy on top of full3
enemy3 = Enemy(1080, 460, 1)  # Place enemy on top of full4
boss = Boss(1200, 760, 3)  # King Pig behind the rightmost tower

# Add all objects to their respective groups
boxes.add(hollow1, hollow2, hollow3, full1, full2, full3)
boxes.add(hollow4, hollow5, hollow6, hollow7, plankFull1, plankFull2, full4)
enemies.add(enemy1, enemy2, enemy3, boss)

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
blue_scaled = pygame.transform.scale(blue_img, (51, 49))
yellow_scaled = pygame.transform.scale(yellow_img, (51, 49))
white_scaled = pygame.transform.scale(white_img, (51, 49))

# Define bird types and their corresponding images
bird_types = [
    {"class": Birds, "image": bird_scaled},
    {"class": Blue, "image": blue_scaled},
    {"class": Yellow, "image": yellow_scaled},
    {"class": White, "image": white_scaled}
]

# Initialize the active bird directly
active_bird = bird_types[0]["class"](130, 840, bird_types[0]["image"])
active_bird.launch_pos = (130, 840)  # Set launch position
birds_group.add(active_bird)
all_sprites.add(active_bird)

# Create the waiting birds queue for display
waiting_birds = []
for i in range(1, len(bird_types)):
    bird_class = bird_types[i]["class"]
    bird_image = bird_types[i]["image"]
    waiting_birds.append({"class": bird_class, "image": bird_image})

# Track the current bird type index
current_bird_type_index = 0

# Debug message to confirm bird creation
print(f"Active bird created at {active_bird.rect.center}, class: {active_bird.__class__.__name__}")

# Add all other sprites to main group
all_sprites.add(boxes, enemies)

def draw_trajectory(surface, bird):
    """Draws the predicted trajectory while dragging."""
    if bird and bird.dragging and bird.trajectory_points:
        for point in bird.trajectory_points:
            pygame.draw.circle(surface, (255, 255, 255), point, 3)

def next_bird():
    """Move to the next bird type in the queue, cycling if needed."""
    global active_bird, waiting_birds, current_bird_type_index, bird_types
    
    # Remove the current bird from groups if it exists
    if active_bird:
        active_bird.kill()
    
    # Move to the next bird type
    current_bird_type_index = (current_bird_type_index + 1) % len(bird_types)
    bird_type = bird_types[current_bird_type_index]
    
    # Create new active bird
    active_bird = bird_type["class"](130, 840, bird_type["image"])
    active_bird.launch_pos = (130, 840)
    birds_group.add(active_bird)
    all_sprites.add(active_bird)
    
    # Debug message
    print(f"New active bird created: {active_bird.__class__.__name__} at {active_bird.rect.center}")
    
    # Update waiting birds queue
    waiting_birds = []
    for i in range(1, len(bird_types)):
        idx = (current_bird_type_index + i) % len(bird_types)
        bird_type = bird_types[idx]
        waiting_birds.append({"class": bird_type["class"], "image": bird_type["image"]})

def draw_waiting_birds():
    """Draw birds waiting in the queue."""
    for i, bird in enumerate(waiting_birds[:3]):  # Show up to 3 waiting birds
        # Calculate position (right of slingshot)
        x_pos = 170 + (i * 40)
        y_pos = 860
        
        # Draw the bird image at the calculated position
        temp_rect = pygame.Rect(0, 0, 51, 49)  # Create a temporary rect with the bird's size
        temp_rect.center = (x_pos, y_pos)
        game_display.blit(bird["image"], temp_rect)

def check_level_complete():
    """Check if the level is complete (all enemies defeated)."""
    return len(enemies) == 0

def check_game_over():
    """Check if the game is over (no more birds and enemies still present)."""
    # In this implementation, we never run out of birds since they cycle
    return False

# Game loop
running = True
level_complete = False
game_over = False

while running:
    # Draw background and slingshot
    game_display.blit(background, (0, 0))
    game_display.blit(slingshot, (75, 832))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            # Press Space to activate special ability
            if event.key == pygame.K_SPACE and active_bird and active_bird.launched:
                if hasattr(active_bird, 'special_ability'):
                    active_bird.special_ability()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Only allow dragging if the bird is not launched yet
            if active_bird and not active_bird.launched and active_bird.rect.collidepoint(event.pos):
                active_bird.start_drag()
                print("Bird drag started")

        elif event.type == pygame.MOUSEBUTTONUP:
            if active_bird and active_bird.dragging:
                active_bird.end_drag()
                print("Bird launched")

    if active_bird and active_bird.launched:
        should_switch = active_bird.update(boxes, enemies)
        if should_switch:
            next_bird()
        
    else:
        # Update active bird normally if not launched
        if active_bird:
            active_bird.update(boxes, enemies)
    
    # Verify the active bird exists in the sprite groups
    if active_bird:
        is_in_group = active_bird in birds_group
        print(f"Active bird in group: {is_in_group}, Position: {active_bird.rect.center}")
        
    # Draw a highlight around the active bird if it's not launched
    if active_bird and not active_bird.launched:
        pygame.draw.circle(game_display, (255, 255, 0), active_bird.rect.center, active_bird.rect.width//1.5, 2)
        
    # Update boxes and enemies
    for box in boxes:
        box.update(boxes, [active_bird] if active_bird else [])
    
    for enemy in enemies:
        enemy.update(enemies, [active_bird] if active_bird else [], boxes)
    
    # Draw all sprites
    all_sprites.draw(game_display)
    
    # Draw waiting birds
    draw_waiting_birds()
    
    # Draw trajectory preview
    if active_bird:
        draw_trajectory(game_display, active_bird)
    
    # Check win/lose conditions
    level_complete = check_level_complete()
    game_over = check_game_over()
    
    # Display win/lose messages
    font = pygame.font.SysFont(None, 74)
    if level_complete:
        text = font.render("Level Complete!", True, (0, 255, 0))
        game_display.blit(text, (width//2 - 200, height//2))
    elif game_over:
        text = font.render("Game Over!", True, (255, 0, 0))
        game_display.blit(text, (width//2 - 150, height//2))
    
    # Update display and tick clock
    pygame.display.update()
    clock.tick(60)

pygame.quit()