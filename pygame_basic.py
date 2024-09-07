import random
import pygame
import time
import sys
import math
from intro import intro_screen
from ship import draw_boundary, draw_ship, interact_with_ship, Ship
from resources import generate_objects, interact_with_object, interact_with_lake, display_inventory, WaterState, fill_bottle_with_radiated_water
from utils import display_message
from grid_generator import generate_grid_with_lake_and_grass, generate_aliens, generate_aliens_attacks
from player_attack import character_attack

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Random Map Grid')

# Define clock for controlling the frame rate
clock = pygame.time.Clock()
# Create game state
class GameState:
    def __init__(self):
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.oxygen = 100
        self.game_over = False

class Inventory:
    def __init__(self):
        self.wood = 0
        self.oxygen_tank = 1
        self.water = WaterState.EMPTY
        self.material = 0
        self.meat = 0

# Create game state
state = GameState()
inventory = Inventory()
ship = Ship()

# Font for displaying stats
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Time management variables
game_minutes_passed = 0  # Define this outside the function
last_update_time = time.time()  

def update_resources(state):
    global game_minutes_passed, last_update_time
    current_time = time.time()
    
    # Check if a real second has passed
    if current_time - last_update_time >= 1:
        # Increase in-game time by 1 minute
        game_minutes_passed += 1
        last_update_time = current_time

        # Deplete resources every in-game hour
        if game_minutes_passed % 60 == 0:  # Every 60 minutes, i.e., 1 in-game hour
            state.hunger -= 5
            state.thirst -= 7
            state.oxygen -= 3
        
        if state.hunger == 0:
            state.health -= 10

        if state.thirst == 0:
            state.health -= 20

        if state.oxygen == 0:
            state.health -=100

        if state.health == 0:
            state.game_over = True

            # Ensure values don't go below zero
            state.hunger = max(state.hunger, 0)
            state.thirst = max(state.thirst, 0)
            state.oxygen = max(state.oxygen, 0)
            state.health = max(state.health, 0)



def draw_stats(screen, state, font):
    if state.game_over:
        return
    
    # Display the current in-game time and resource stats in a square in the bottom right
    health_text = font.render(f'Health: {int(state.health)}', True, (255, 0, 0))
    hunger_text = font.render(f'Hunger: {int(state.hunger)}', True, (0, 255, 0))
    thirst_text = font.render(f'Thirst: {int(state.thirst)}', True, (0, 0, 255))
    oxygen_text = font.render(f'Oxygen: {int(state.oxygen)}', True, (255, 255, 0))

    pygame.draw.rect(screen, (50, 50, 50), (600, 450, 200, 150))  # Background square
    screen.blit(health_text, (610, 460))
    screen.blit(hunger_text, (610, 490))
    screen.blit(thirst_text, (610, 520))
    screen.blit(oxygen_text, (610, 550))

    # Calculate the in-game time in hours and minutes
    hours = game_minutes_passed // 60
    minutes = game_minutes_passed % 60
    time_text = font.render(f'Time: {hours:02}:{minutes:02}', True, (255, 255, 255))
    
    # Display the time in the upper right corner
    screen.blit(time_text, (screen.get_width() - time_text.get_width() - 10, 10))
    
    # Display the time in the upper right corner
    screen.blit(time_text, (screen.get_width() - time_text.get_width() - 10, 10))

def display_game_over(screen):
    screen.fill((0, 0, 0))  # Black background
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()


# Define grid size
GRID_ROWS = 10
GRID_COLS = 10
TILE_SIZE = 64 
x_pos = 0
y_pos = 0
aliens = []

currentXArea = 0
currentYArea = 0

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

grid, lakes = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
objects = generate_objects(GRID_COLS)
print(objects)

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
intro = True


while running:
    if (intro):
      intro_screen(screen)
      intro = False
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
           if currentXArea > -4:
              grid, lakes = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)  
              objects = generate_objects(GRID_COLS)
              print(objects)
              inverse_grid = transpose_grid(grid)
           out_of_bound = True
          print("modulo x")
          print(adj_x,adj_y)
          print(int(adj_x/TILE_SIZE),int(math.floor(adj_y/TILE_SIZE)))
          print(inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))])
 
          if inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))]== 0 or inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))] == 2:
            if out_of_bound:
              if currentXArea >-4:
                aliens = generate_aliens()
                x_pos = 9* TILE_SIZE;
                currentXArea -= 1
              out_of_bound = False
            else:
              x_pos -= move_speed
        else:
            x_pos -= move_speed
        direction = -1
        moving = True



    if keys[pygame.K_RIGHT]:
        new_x_pos = x_pos + move_speed
        adj_x = new_x_pos + TILE_SIZE/2
        adj_y = y_pos + TILE_SIZE


        if (adj_x) % TILE_SIZE == 0:
          if (adj_x / TILE_SIZE >= 10):
              adj_x = 0
              if currentXArea < 4:
                grid, lakes = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
                objects = generate_objects(GRID_COLS)
                print(objects)
                inverse_grid = transpose_grid(grid)
              out_of_bound = True

          print("modulo x")
          print(adj_x, adj_y)
          print(int(adj_x/TILE_SIZE),int(math.floor(adj_y/TILE_SIZE)))
          print(inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))])

          if inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))]== 0 or inverse_grid[int(adj_x/TILE_SIZE)][int(math.floor(adj_y/TILE_SIZE))] == 2:
            if out_of_bound:
              if currentXArea < 4:
                aliens = generate_aliens()
                x_pos = 0;
                currentXArea += 1
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
              if currentYArea > -4:
                grid, lakes = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
                objects = generate_objects(GRID_COLS)
                print(objects)
                inverse_grid = transpose_grid(grid)
              out_of_bound = True

          print("modulo y")
          print(adj_x,adj_y)
          print(int(math.floor(adj_x/TILE_SIZE)), int(adj_y/TILE_SIZE))
          print(inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1])
          print(inverse_grid)
          if inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1] == 0 or inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)-1] == 2:
            if out_of_bound:
              if currentYArea > -4:
                y_pos = 9* TILE_SIZE;
                aliens = generate_aliens()
                print("currentYArea:",currentYArea)
                currentYArea -= 1
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
              if currentYArea < 4:
                grid, lakes = generate_grid_with_lake_and_grass(GRID_ROWS, GRID_COLS, lake_size=8)
                objects = generate_objects(GRID_COLS)
                print(objects)
                inverse_grid = transpose_grid(grid)
              out_of_bound = True
         
          print("modulo y")
          print(adj_x, adj_y)
          print(int(math.floor(adj_x/TILE_SIZE)), int(adj_y/TILE_SIZE))

          if inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)] == 0 or inverse_grid[int(math.floor(adj_x/TILE_SIZE))][int(adj_y/TILE_SIZE)] == 2:
            if out_of_bound:
              if currentYArea<4:
                aliens = generate_aliens()
                y_pos = 0;
                currentYArea += 1
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
    if not state.game_over:
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
        character_rect = screen.blit(body, (x_pos, y_pos))
        screen.blit(head, (x_pos + 10, y_pos - 20))  # Adjust head position as needed
        screen.blit(arm, (x_pos + 13, y_pos +12))  # Adjust arm position as needed

        # Frame rate
        pygame.time.Clock().tick(30)

        #elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        update_resources(state)

         # Draw the boundary if at the edge of the world
        draw_boundary(screen, currentXArea, currentYArea)
        
        # Draw the resource stats
        draw_stats(screen, state, font)

         # Draw the ship if in (0,0)
        ship.rect  = draw_ship(screen, currentXArea, currentYArea)

        for obj in objects:
            if not obj["collected"] and not obj["defeated"]:
                screen.blit(obj["image"], obj["pos"])

        generate_aliens_attacks(screen, x_pos, y_pos, body, state, aliens)

        if keys[pygame.K_SPACE]:
            character_attack(screen, character_rect, aliens, 10)
            interact_with_object(character_rect, objects, inventory)
            lake_message = interact_with_lake(character_rect, lakes, inventory)
            print(lake_message)
            if lake_message:
               display_message(screen, lake_message)
            if ship.rect:
               message= interact_with_ship(character_rect, ship, inventory, state, screen)
               if (message):
                 display_message(screen, message)
            
        
        if keys[pygame.K_i]:
          display_inventory(screen, inventory, keys, state)

        # Update the display
        pygame.display.flip()
    else:
        display_game_over(screen)


pygame.quit()