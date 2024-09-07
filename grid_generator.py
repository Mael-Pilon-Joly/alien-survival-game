import random

import pygame

from alien import Alien, BigAlien, GreenAlien, RareAlien, SmallAlien

class Lake:
    def __init__(self, tiles):
        self.tiles = tiles

def generate_lake_cluster(grid, start_row, start_col, size):
    """Generate a lake cluster starting from a given tile."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    lake_tiles = [(start_row, start_col)]
    grid[start_row][start_col] = 1  # 1 for water

    for _ in range(size - 1):
        # Choose a random existing lake tile
        r, c = random.choice(lake_tiles)

        # Try to expand the lake to an adjacent tile
        possible_directions = random.sample(directions, len(directions))  # Shuffle directions
        for dr, dc in possible_directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 1:
                grid[nr][nc] = 1
                lake_tiles.append((nr, nc))
                break

    return Lake(lake_tiles)  # Return a Lake object containing the tiles

def generate_grid_with_lake_and_grass(rows, cols, lake_size):
    grid = [[0] * cols for _ in range(rows)]  # Start with all plain ground
    lakes = []
    
    # Generate lake and store its object
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    lake = generate_lake_cluster(grid, start_row, start_col, lake_size)
    lakes.append(lake)  # Store the lake object

    # Fill the rest with grass randomly
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:  # Only replace plain ground
                grid[row][col] = random.choice([0, 2])  # 0 for ground, 2 for grass

    return grid, lakes

def generate_aliens_attacks(screen, player_pos_x, player_pos_y, body, state, aliens):
   for alien in aliens:
    player_pos = (player_pos_x, player_pos_y)
    player_rect = pygame.Rect(player_pos_x, player_pos_y, body.get_width(), body.get_height())
    alien.move(player_pos)
    if player_rect.colliderect(alien.rect):
        alien.attack(state)
    alien.draw(screen)

def generate_aliens():
   aliens = []
   aliens_qty = random.randint(0, 5)

   alien_types = [
        (SmallAlien, 50),  
        (GreenAlien, 30),  
        (BigAlien, 15),    
        (RareAlien, 5)     
    ]
   
   for _ in range(aliens_qty):
        alien_type = random.choices(
            [atype for atype, _ in alien_types],  # Alien classes
            weights=[prob for _, prob in alien_types],  # Probabilities
            k=1
        )[0]
        aliens.append(alien_type())

   return aliens
  
