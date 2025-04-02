import pygame
import math
import numpy as np  # Needed for sqrt

# Constants
g = 9.81  # Gravity
m = 0.8   # Mass
k = 10    # Spring constant

class Birds(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [0, 0]
        self.dragging = False
        self.launched = False
        self.launch_pos = (x, y)
        self.angle = 0
        self.trajectory_points = []
        self.time_since_stopped = 0
        self.time_y_velocity_zero = 0

    def start_drag(self):
        """Start dragging the bird."""
        self.dragging = True

    def calculate_trajectory(self):
        """Calculate predicted trajectory points."""
        self.trajectory_points = []
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            dx = self.launch_pos[0] - mouse_pos[0]
            dy = self.launch_pos[1] - mouse_pos[1]
            alpha = math.atan2(dy, dx)

            l1 = math.sqrt(dx**2 + dy**2)
            if l1 == 0:
                return
            try:
                v_eject = (l1 * np.sqrt(k / m) * np.sqrt(1 - (m * g * math.sin(alpha) / (k * l1))**2)) / 2
            except ValueError:
                return

            v_x = v_eject * math.cos(alpha)
            v_y = v_eject * math.sin(alpha)

            # Simulate trajectory points
            x, y = self.rect.center
            for t in np.linspace(0, 10, num=20):
                new_x = x + v_x * t
                new_y = y + v_y * t + 0.5 * g * (t ** 2)
                self.trajectory_points.append((int(new_x), int(new_y)))

    def end_drag(self):
        """End drag and launch the bird using computed velocity."""
        self.dragging = False
        self.launched = True
        self.trajectory_points = []

        mouse_pos = pygame.mouse.get_pos()

        # Compute angle alpha
        dx = self.launch_pos[0] - mouse_pos[0]
        dy = self.launch_pos[1] - mouse_pos[1]
        alpha = math.atan2(dy, dx)

        # Compute launch speed using formula
        l1 = math.sqrt(dx**2 + dy**2)
        if l1 == 0:
            return
        try:
            v_eject = (l1 * np.sqrt(k / m) * np.sqrt(1 - (m * g * math.sin(alpha) / (k * l1))**2)) /6
        except ValueError:
            v_eject = 0

        # Apply velocity
        self.velocity = [v_eject * math.cos(alpha), v_eject * math.sin(alpha)]
        self.angle = math.degrees(alpha)

    def handle_collision(self, box):
        """Handle bird collision with a box."""
        if self.rect.right > box.rect.left and self.rect.left < box.rect.left:
            # **Left side collision**
            self.rect.right = box.rect.left
            self.velocity[0] = -abs(self.velocity[0]) * 0.1

        elif self.rect.left < box.rect.right and self.rect.right > box.rect.right:
            # **Right side collision**
            self.rect.left = box.rect.right
            self.velocity[0] = abs(self.velocity[0]) * 0.1

        elif self.rect.bottom > box.rect.top and self.rect.top < box.rect.top:
            # **Top collision**
            self.rect.bottom = box.rect.top
            self.velocity[1] = 0
            self.launched = False

        elif self.rect.top < box.rect.bottom and self.rect.bottom > box.rect.bottom:
            # **Bottom collision**
            self.rect.top = box.rect.bottom
            self.velocity[1] = abs(self.velocity[1]) * 0.4  

    def handle_collision_box(self, box):
        """Handle bird collision with a box."""
        if self.rect.right > box.rect.left and self.rect.left < box.rect.left:
            # **Left side collision**
            self.rect.right = box.rect.left
            self.velocity[0] = -abs(self.velocity[0]) * 0.1

        elif self.rect.left < box.rect.right and self.rect.right > box.rect.right:
            # **Right side collision**
            self.rect.left = box.rect.right
            self.velocity[0] = abs(self.velocity[0]) * 0.1

        elif self.rect.bottom > box.rect.top and self.rect.top < box.rect.top:
            # **Top collision**
            self.rect.bottom = box.rect.top
            self.velocity[1] = 0
            self.launched = False

        elif self.rect.top < box.rect.bottom and self.rect.bottom > box.rect.bottom:
            # **Bottom collision**
            self.rect.top = box.rect.bottom
            self.velocity[1] = abs(self.velocity[1]) * 0.4  

    def handle_collision_enemy(self, Enemy):
        """Handle bird collision with an Enemy."""
        if self.rect.right > Enemy.rect.left and self.rect.left < Enemy.rect.left:
            # **Left side collision**
            self.rect.right = Enemy.rect.left
            self.velocity[0] = -abs(self.velocity[0]) * 0.1

        elif self.rect.left < Enemy.rect.right and self.rect.right > Enemy.rect.right:
            # **Right side collision**
            self.rect.left = Enemy.rect.right
            self.velocity[0] = abs(self.velocity[0]) * 0.1

        elif self.rect.bottom > Enemy.rect.top and self.rect.top < Enemy.rect.top:
            # **Top collision**
            self.rect.bottom = Enemy.rect.top
            self.velocity[1] = 0
            self.launched = False

        elif self.rect.top < Enemy.rect.bottom and self.rect.bottom > Enemy.rect.bottom:
            # **Bottom collision**
            self.rect.top = Enemy.rect.bottom
            self.velocity[1] = abs(self.velocity[1]) * 0.4 

    def update(self, boxes, enemies):
        """Update bird's position based on velocity or dragging."""
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()
            self.calculate_trajectory()
        elif self.launched:
            self.velocity[1] += g * 0.16  
            self.rect.x += int(self.velocity[0])
            self.rect.y += int(self.velocity[1])

            # Rotate sprite based on movement direction
            if self.velocity[0] != 0 or self.velocity[1] != 0:
                self.angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))

            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            original_center = self.rect.center
            self.rect = self.image.get_rect(center=original_center)

            for box in boxes:
                if self.rect.colliderect(box.rect):
                    self.handle_collision_box(box)
                    box.hit()

            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.handle_collision_enemy(enemy)
                    enemy.hit()

            screen_height = pygame.display.get_surface().get_height()
            bounce_y = screen_height - 150
            if self.rect.bottom >= bounce_y:
                self.rect.bottom = bounce_y
                
                # Only bounce if velocity is significant
                if abs(self.velocity[1]) > 3:
                    self.velocity[1] = -self.velocity[1] * 0.5  # Reduce bounce effect
                else:
                    self.velocity[1] = 0
                    # Slow down horizontal movement when on ground
                    self.velocity[0] *= 0.9
                    
                # If both velocities are very low, stop the bird
                if abs(self.velocity[0]) < 0.5 and abs(self.velocity[1]) < 0.5:
                    self.velocity = [0, 0]
                    self.launched = False

        # Check if bird is stationary for too long
        if abs(self.velocity[0]) < 0.1 and abs(self.velocity[1]) < 0.1:
            self.time_since_stopped += 1
        else:
            self.time_since_stopped = 0

        if self.time_since_stopped > 30:
            # Signal to the main game to switch birds instead of respawning
            return True

        if abs(self.velocity[1]) < 0.1: 
            self.time_y_velocity_zero +=1
        else:
            self.time_y_velocity_zero = 0

        if self.time_y_velocity_zero > 30:
            self.velocity[0] = 0

        # Check if bird is out of screen bounds - signal to switch
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0 or self.rect.right > screen_width or self.rect.top < 0:
            return True
            
        return False  # Bird should continue

    def respawn(self):
        """Respawn bird to its initial position."""
        self.rect.center = self.launch_pos
        self.velocity = [0, 0]  # Reset velocity
        self.launched = False  # Stop motion
        self.time_since_stopped = 0  # Reset stop timer
        self.angle = 0  # Reset rotation angle
        self.image = self.original_image

class Blue(Birds): 
    def __init__(self, x, y, image): 
        super().__init__(x, y, image)
        self.x = x
        self.y = y 
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(x, y))
        
    def special_ability(self):
        # Blue bird can split into three birds
        print("Blue bird special ability activated")
        # Implementation would go here
        pass
        
class Yellow(Birds): 
    def __init__(self, x, y, image): 
        super().__init__(x, y, image)
        self.x = x
        self.y = y 
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(x, y))
        
    def special_ability(self):
        # Yellow bird can speed up
        print("Yellow bird special ability activated")
        # Implementation would boost speed
        self.velocity[0] *= 2.5
        pass
        
class White(Birds): 
    def __init__(self, x, y, image): 
        super().__init__(x, y, image)
        self.x = x
        self.y = y 
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(x, y))
        
    def special_ability(self):
        # White bird can drop eggs
        print("White bird special ability activated")
        # Implementation would go here
        pass

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health=1):
        super().__init__()
        self.width = width
        self.height = height
        self.health = health
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load('hollow_box.png')
        self.image = pygame.transform.scale(self.image, (60, 60))  # Scaling the box image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocity = [0, 0]
        self.gravity = g  # Gravity force
        self.on_ground = False  # Used to check if the box is on the ground
        self.grounded_cooldown = 0  # Cooldown to prevent vibration
        
        # Add a small offset to prevent boxes from overlapping exactly
        self.collision_offset = 2

    def hit(self):
        """Reduce health on impact and remove if broken."""
        print(f"Box hit, health before: {self.health}")
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def apply_gravity(self, boxes):
        """Apply gravity to the box and handle collisions with other boxes."""
        if self.grounded_cooldown > 0:
            self.grounded_cooldown -= 1
            return
            
        # Apply gravity to the box
        if not self.on_ground:
            self.velocity[1] += self.gravity * 0.1
        
        # Move the box down based on its velocity
        self.rect.y += int(self.velocity[1])

        screen_height = pygame.display.get_surface().get_height()
        ground_level = screen_height - 150
        
        # Check ground collision first - more definitive grounding
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity[1] = 0
            self.on_ground = True
            self.grounded_cooldown = 10
            return

        # Check for collisions with other boxes
        box_list = sorted([box for box in boxes if box != self], key=lambda box: box.rect.y)
        
        collision_occurred = False
        for box in box_list:
            if box == self:
                continue
            
            # Only check for meaningful top-bottom collisions
            if (self.rect.bottom > box.rect.top and 
                self.rect.top < box.rect.top and 
                self.rect.bottom - box.rect.top > 2 and
                abs(self.rect.centerx - box.rect.centerx) < (self.rect.width + box.rect.width) / 3):
                
                self.rect.bottom = box.rect.top - self.collision_offset
                self.velocity[1] = 0
                self.on_ground = True
                self.grounded_cooldown = 5
                collision_occurred = True
                break
        
        if not collision_occurred:
            self.on_ground = False
            
            collision_occurred = False
            for box in box_list:
                if box == self:
                    continue  # Skip self-collision
                
                # Only check for top-bottom collisions with sufficient horizontal overlap
                if (self.rect.bottom > box.rect.top and 
                    self.rect.top < box.rect.top and 
                    self.rect.bottom - box.rect.top > 2 and  # Ensure meaningful overlap
                    abs(self.rect.centerx - box.rect.centerx) < (self.rect.width + box.rect.width) / 3):
                    
                    # Place this box on top
                    self.rect.bottom = box.rect.top - self.collision_offset
                    self.velocity[1] = 0
                    self.on_ground = True
                    self.grounded_cooldown = 5  # Set cooldown after landing on another box
                    collision_occurred = True
                    break
            
            if not collision_occurred:
                self.on_ground = False

    def update(self, boxes, birds):
        """Update box's position and check for collisions with birds."""
        # Apply gravity and check for collisions
        self.apply_gravity(boxes)
        
        # Check if the box collides with any birds
        for bird in birds:
            if bird and isinstance(bird, Birds) and self.rect.colliderect(bird.rect):
                self.hit()  # Handle box being hit by the bird

class HollowBox(Box):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(x, y, width, height, health=1)
        self.image = pygame.image.load('hollow_box.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))

class PlankFull(Box):
    def __init__(self, x, y):
        super().__init__(x, y, 205, 22, health=2)
        self.image = pygame.image.load('plank_100.png')
        self.image = pygame.transform.scale(self.image, (205, 22))
        self.rect = self.image.get_rect(topleft=(x, y))

class FullBox(Box):
    def __init__(self, x, y, width=60, height=63):
        super().__init__(x, y, width, height, health=1)
        self.image = pygame.image.load('full_box.png')
        self.image = pygame.transform.scale(self.image, (60, 63))
        self.rect = self.image.get_rect(topleft=(x, y))
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=1, width=60, height=60):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (60, 60))  # Scaling the enemy image
        self.rect = self.image.get_rect(center=(x,y))
        self.velocity = [0, 0]
        self.gravity = g  # Gravity force
        self.on_ground = False  # Used to check if the enemy is on the ground
        self.health = health 
        self.collision_offset = 2  # Small offset to prevent pixel-perfect collisions
        self.grounded_cooldown = 0  # Cooldown to prevent vibration

    def hit(self):
        """Reduce health on impact and remove if killed."""
        print(f"Enemy hit, health before: {self.health}")
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def apply_gravity(self, enemies, boxes):
        """Apply gravity to the enemy and handle collisions with boxes and other enemies."""
        if self.grounded_cooldown > 0:
            self.grounded_cooldown -= 1
            return
            
        # Apply gravity to the enemy
        self.velocity[1] += self.gravity * 0.1  # Reduced gravity for stability
        
        # Move the enemy down based on its velocity
        self.rect.y += int(self.velocity[1])

        screen_height = pygame.display.get_surface().get_height()
        ground_level = screen_height - 150  # Define the ground level
        
        # Ground collision
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity[1] = 0
            self.on_ground = True
            self.grounded_cooldown = 10  # Set cooldown after touching ground
            return

        # Check collisions with boxes and other enemies
        collision_occurred = False
        
        # Check collisions with boxes - prioritize these
        box_list = sorted(boxes, key=lambda box: box.rect.y)
        for box in box_list:
            # Only check for top-bottom collision with good horizontal overlap
            if (self.rect.bottom > box.rect.top and 
                self.rect.top < box.rect.top and
                self.rect.bottom - box.rect.top > 2 and  # Ensure meaningful overlap
                abs(self.rect.centerx - box.rect.centerx) < (self.rect.width + box.rect.width) / 3):
                
                # Place enemy on top of box
                self.rect.bottom = box.rect.top - self.collision_offset
                self.velocity[1] = 0
                self.on_ground = True
                self.grounded_cooldown = 5  # Set cooldown after landing on a box
                collision_occurred = True
                break
        
        if not collision_occurred:
            # Sort other enemies by y position for accurate stacking
            enemy_list = sorted([enemy for enemy in enemies if enemy != self], 
                              key=lambda enemy: enemy.rect.y)
            
            # Check collisions with other enemies
            for enemy in enemy_list:
                if enemy == self:
                    continue  # Skip self-collision

                # Only check for top-bottom collision with good horizontal overlap
                if (self.rect.bottom > enemy.rect.top and 
                    self.rect.top < enemy.rect.top and
                    self.rect.bottom - enemy.rect.top > 2 and  # Ensure meaningful overlap
                    abs(self.rect.centerx - enemy.rect.centerx) < (self.rect.width + enemy.rect.width) / 3):
                    
                    # Place this enemy on top
                    self.rect.bottom = enemy.rect.top - self.collision_offset
                    self.velocity[1] = 0
                    self.on_ground = True
                    self.grounded_cooldown = 5  # Set cooldown after landing on another enemy
                    collision_occurred = True
                    break
        
        if not collision_occurred:
            self.on_ground = False

    def update(self, enemies, birds, boxes):
        """Update enemy's position and check for collisions."""
        # Apply gravity and handle collisions
        self.apply_gravity(enemies, boxes)

        # Check if the enemy collides with any birds
        for bird in birds:
            if bird and isinstance(bird, Birds) and self.rect.colliderect(bird.rect):
                self.hit()  # Handle enemy being hit by the bird

class Boss(Enemy):
    def __init__(self, x, y, health=3):
        super().__init__(x, y, health, width=100, height=150)
        self.image = pygame.image.load('KingPig.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.action = action