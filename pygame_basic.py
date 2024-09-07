import random
import pygame
import sys
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Random Map Grid')

# Define grid size
GRID_ROWS = 10
GRID_COLS = 10
TILE_SIZE = 64 
x_pos = 0
y_pos = 0

# Arm swing settings
arm_angle = 0
arm_swing_direction = 1  # 1 for swinging forward, -1 for swinging backward

# Movement speed
move_speed = 4

# Direction (1 for right, -1 for left)
direction = 1


plain_moon = pygame.image.load('./assets/plain_moon_ground.png')
water_pond = pygame.image.load('./assets/plain_moon_ground_water_pound.png')
grass = pygame.image.load('./assets/plain_moon_ground_grass.png')

plain_moon = pygame.transform.scale(plain_moon, (TILE_SIZE, TILE_SIZE))
water_pond = pygame.transform.scale(water_pond, (TILE_SIZE, TILE_SIZE))
grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
head_image = pygame.image.load('./assets/head_astronaut.png').convert_alpha()
body_image = pygame.image.load('./assets/astronaut_body.png').convert_alpha()
arm_image = pygame.image.load('./assets/astronaut_arm.png').convert_alpha()

# Scale the head and arm
head_image = pygame.transform.scale(head_image, (head_image.get_width() // 2, head_image.get_height() // 2))
arm_image = pygame.transform.scale(arm_image, (arm_image.get_width() // 2, arm_image.get_height() // 4))


# Create the grid and populate it with random tiles
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

def generate_grid_with_lake_and_grass(rows, cols, lake_size):
    grid = [[0] * cols for _ in range(rows)]  # Start with all plain ground
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    generate_lake_cluster(grid, start_row, start_col, lake_size)

    # Fill the rest with grass randomly
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:  # Only replace plain ground
                grid[row][col] = random.choice([0, 2])  # 0 for ground, 2 for grass

    return grid

# Example usage
grid = generate_grid_with_lake_and_grass(10, 10, lake_size=8)

grid = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)

def transpose_grid(grid):
    return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

inverse_grid = transpose_grid(grid)


# Function to draw the grid
def draw_grid(screen, grid):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            # Determine the x and y position on the screen
            x = col * TILE_SIZE 
            y = row * TILE_SIZE 

            # Get the tile type from the grid
            tile_type = grid[row][col]

            # Blit the correct image based on the tile type
            if tile_type == 0:
                screen.blit(plain_moon, (x, y))
            elif tile_type == 1:
                screen.blit(water_pond, (x, y))
            elif tile_type == 2:
                screen.blit(grass, (x, y))

def draw_grid_overlay(screen, rows, cols, tile_size):
    for row in range(rows + 1):  # +1 to draw the last row line
        pygame.draw.line(screen, (255, 255, 255), (0, row * tile_size), (cols * tile_size, row * tile_size))
    for col in range(cols + 1):  # +1 to draw the last column line
        pygame.draw.line(screen, (255, 255, 255), (col * tile_size, 0), (col * tile_size, rows * tile_size))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False  # Flag to check if astronaut is moving
    

    """ Note X and Y axis are inversed, so we use inversed_grid"""
    out_of_bound = False
    # Horizontal movement
    if keys[pygame.K_LEFT]:

        new_x_pos = x_pos - move_speed
        adj_x = new_x_pos - TILE_SIZE/2
        adj_y = y_pos + TILE_SIZE

        if(adj_x) % TILE_SIZE == 0:
          if (adj_x / TILE_SIZE < 0):
           adj_x = 9 * TILE_SIZE
           grid = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
           inverse_grid = transpose_grid(grid)
           out_of_bound = True
          print("modulo x")
          print(adj_x,adj_y)
          print(int(adj_x/TILE_SIZE),int(math.floor(adj_y/TILE_SIZE)))
          print(inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))])
 
          if inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))]== 0 or inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))] == 2:
            if out_of_bound:
              x_pos = 9* TILE_SIZE;
              out_of_bound = False
            else:
              x_pos -= move_speed
        else:
            x_pos -= move_speed
        direction = 1
        moving = True



    if keys[pygame.K_RIGHT]:
        new_x_pos = x_pos + move_speed
        adj_x = new_x_pos + TILE_SIZE/2
        adj_y = y_pos + TILE_SIZE


        if (adj_x) % TILE_SIZE == 0:
          if (adj_x / TILE_SIZE >= 10):
              adj_x = 0
              grid = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
              inverse_grid = transpose_grid(grid)
              out_of_bound = True

          print("modulo x")
          print(adj_x, adj_y)
          print(int(adj_x/TILE_SIZE),int(math.floor(adj_y/TILE_SIZE)))
          print(inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))])

          if inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))]== 0 or inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))] == 2:
            if out_of_bound:
              x_pos = 0;
              out_of_bound = False
            else:
              x_pos += move_speed
        else:
            x_pos += move_speed
        direction = 1
        moving = True



    # Vertical movement
    if keys[pygame.K_UP]:
        new_y_pos = y_pos - move_speed
        adj_x = x_pos + TILE_SIZE/2
        adj_y = new_y_pos + TILE_SIZE

        if (adj_y % TILE_SIZE)== 0:
          if (adj_y / TILE_SIZE < 0):
              adj_y = 9
              grid = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
              inverse_grid = transpose_grid(grid)
              out_of_bound = True

          print("modulo y")
          print(adj_x,adj_y)
          print(int(math.floor(adj_x/TILE_SIZE)), int(adj_y/TILE_SIZE))
          print(inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1])
          print(inverse_grid)
          if inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1] == 0 or inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1] == 2:
            if out_of_bound:
              y_pos = 9* TILE_SIZE;
              out_of_bound = False
            else:
              y_pos -= move_speed
        else:
            y_pos -= move_speed
        direction = 1
        moving = True



    if keys[pygame.K_DOWN]:
        new_y_pos = y_pos + move_speed
        adj_x = x_pos + TILE_SIZE/2
        adj_y = new_y_pos + TILE_SIZE
        if (adj_y % TILE_SIZE) == 0:
          if (adj_y / TILE_SIZE >= 10):
              adj_y = 0
              grid = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
              inverse_grid = transpose_grid(grid)
              out_of_bound = True
         
          print("modulo y")
          print(adj_x, adj_y)
          print(int(math.floor(adj_x/TILE_SIZE)), int(adj_y/TILE_SIZE))

          if inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)] == 0 or inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)] == 2:
            if out_of_bound:
              y_pos = 0;
              out_of_bound = False
            else:
              y_pos += move_speed
        else:
            y_pos += move_speed
        direction = 1
        moving = True


    # Arm swinging back and forth, only if moving horizontally
    if moving:
        arm_angle += arm_swing_direction * 5  # Adjust the swing speed as needed
        if arm_angle > 35 or arm_angle < -35:  # Swing limits
            arm_swing_direction *= -1
    else:
        arm_angle = 0  # Reset the arm angle when not moving

    # Clear the screen
    screen.fill((0, 0, 0))
    # Draw the grid
    draw_grid(screen, grid)
    draw_grid_overlay(screen, GRID_ROWS, GRID_COLS, TILE_SIZE)


    # Flip images based on direction
    if direction == 1:
        head = head_image
        body = body_image
        arm = pygame.transform.rotate(arm_image, arm_angle)
    else:
        head = pygame.transform.flip(head_image, True, False)
        body = pygame.transform.flip(body_image, True, False)
        arm = pygame.transform.flip(pygame.transform.rotate(arm_image, arm_angle), True, False)

    # Draw the body first, then the head and arm on top
    screen.blit(body, (x_pos, y_pos))
    screen.blit(head, (x_pos + 10, y_pos - 20))  # Adjust head position as needed
    screen.blit(arm, (x_pos + 13, y_pos +12))  # Adjust arm position as needed

    # Frame rate
    pygame.time.Clock().tick(30)


    # Update the display
    pygame.display.flip()

pygame.quit()