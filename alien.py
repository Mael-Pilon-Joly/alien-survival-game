import time
import pygame
import random

TILE_SIZE = 64

class Alien:
    def __init__(self, health, attack_power, image, size, speed, is_hostile):
        self.health = health
        self.attack_power = attack_power
        self.image = pygame.transform.scale(image, (size, size))  # Scale image based on size
        self.size = size
        self.speed = speed
        self.is_hostile = is_hostile
        self.rect = pygame.Rect(0, 0, size, size)  
        self.attack_cooldown = 2  # Cooldown in seconds
        self.last_attack_time = 0 

    def move(self, target_position):
      if self.is_hostile:
        direction = pygame.math.Vector2(target_position) - pygame.math.Vector2(self.rect.center)
        
        if direction.length() > 0:  # Check if the vector is non-zero
            direction = direction.normalize() * self.speed
            self.rect.move_ip(direction)

    def take_damage(self, amount):
        """Reduce the alien's health by the given amount."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Handle the alien's death."""
        print(f"Alien defeated!")

    def attack(self, target):
        current_time = time.time()
        if self.is_hostile and (current_time - self.last_attack_time) >= self.attack_cooldown:
            target.health -= self.attack_power
            print(f"Alien attacks for {self.attack_power} damage!")
            self.last_attack_time = current_time  

    def draw(self, screen):
        """Draw the alien on the screen."""
        screen.blit(self.image, self.rect.topleft)

    def loot(self):
        """Calculate loot when alien is killed."""
        loot = {'meat': 0, 'material': 0}
        if random.random() < self.meat_chance:
            loot['meat'] = 1
        if random.random() < self.material_chance:
            loot['material'] = 1
        return loot

# Load images for aliens
red_alien_img = pygame.image.load('./assets/red_alien.png')
green_alien_img = pygame.image.load('./assets/green_alien.png')
blue_alien_img = pygame.image.load('./assets/blue_alien.png')
black_alien_img = pygame.image.load('./assets/black_alien.webp')

class SmallAlien(Alien):
    def __init__(self):
        super().__init__(health=50, attack_power=5, image=blue_alien_img, size=30, speed=4, is_hostile=True)
        self.meat_chance = 0.1
        self.material_chance = 0.1

class GreenAlien(Alien):
    def __init__(self):
        super().__init__(health=100, attack_power=10, image=green_alien_img, size=50, speed=3, is_hostile=True)
        self.meat_chance = 0.2
        self.material_chance = 0.2

class BigAlien(Alien):
    def __init__(self):
        super().__init__(health=150, attack_power=20, image=red_alien_img, size=70, speed=2, is_hostile=True)
        self.meat_chance = 0.2
        self.material_chance = 0.5

class RareAlien(Alien):
    def __init__(self):
        super().__init__(health=200, attack_power=33, image=black_alien_img, size=90, speed=1, is_hostile=True)
        self.meat_chance = 0.2
        self.material_chance = 1.0

    def loot(self):
        """Special loot for RareAlien: Always drops double material."""
        loot = super().loot()
        loot['material'] *= 2
        return loot

