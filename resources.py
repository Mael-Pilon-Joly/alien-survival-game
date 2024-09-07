from enum import Enum
import random
import pygame
from utils import display_message

TILE_SIZE = 64

wood_image = pygame.image.load('./assets/wood.png')
water_image = pygame.image.load('./assets/water.png')
oxygen_image = pygame.image.load('./assets/oxygen_tank.png')

wood_image = pygame.transform.scale(wood_image, (TILE_SIZE, TILE_SIZE))
water_image = pygame.transform.scale(water_image, (TILE_SIZE, TILE_SIZE))
oxygen_image = pygame.transform.scale(oxygen_image, (TILE_SIZE, TILE_SIZE))

font = pygame.font.Font(None, 24)

class WaterState(Enum):
    EMPTY = "Empty"
    RADIATED = "Radiated"
    CLEAN = "Clean"

def generate_objects(grid_size):
    objects = []

    # Define the probability and type for each object
    object_types = [
        {"type": "wood", "image": wood_image, "probability": 0.2},
        {"type": "oxygen", "image": oxygen_image, "probability": 0.1}
    ]

    for obj_type in object_types:
        if random.random() < obj_type["probability"]:
            # Random position within the grid
            pos_x = random.randint(0, grid_size - 1) * TILE_SIZE
            pos_y = random.randint(0, grid_size - 1) * TILE_SIZE
            objects.append({"type": obj_type["type"], "image": obj_type["image"], "pos": (pos_x, pos_y), "collected": False, "defeated": False})

    return objects

# Function to check for collisions between character and objects
def check_collision(character_rect, obj_rect):
    return character_rect.colliderect(obj_rect)

# Function to handle interactions
def interact_with_object(character_rect, objects, inventory):
    for obj in objects:
        if not obj.get("collected", False) and not obj.get("defeated", False):
            obj_rect = pygame.Rect(obj["pos"][0], obj["pos"][1], TILE_SIZE, TILE_SIZE)
            if check_collision(character_rect, obj_rect):
                if obj["type"] == "wood":
                    obj["collected"] = True
                    inventory.wood += 1
                    print("Collected wood!")
                elif obj["type"] == "oxygen":
                    obj["collected"] = True
                    inventory.oxygen_tank += 1
                    print("Collected oxygen tank!")
                elif obj["type"] == "alien":
                    obj["defeated"] = True
                    print("Defeated alien!")

def display_inventory(screen, inventory, keys, state ):
    # New panel, slightly lighter color, positioned just above the original panel
    inventory_open = True

    while inventory_open:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Display the inventory items and controls
        wood_text = font.render(f'Wood: {inventory.wood} (press w to burn)', True, (255, 255, 0))
        oxygen_tank_text = font.render(f'Oxygen Tank: {inventory.oxygen_tank} (press o to fill)', True, (255,255,255))
        water_text = font.render(f'Water: {inventory.water.value} (press h to drink)', True, (0, 0, 255))
        exit_text = font.render('Release i to exit inventory', True, (255, 255, 255))  # Exit message
        
        # Draw the inventory panel
        pygame.draw.rect(screen, (80, 80, 80), (550, 300, 250, 150))  
        screen.blit(wood_text, (560, 310))  # Position for wood
        screen.blit(oxygen_tank_text, (560, 340))  # Position for oxygen tank
        screen.blit(water_text, (560, 370))  # Position for water
        screen.blit(exit_text, (560, 410))  # Position for exit text

        # Handle consuming items
        if keys[pygame.K_w] and inventory.wood > 0:
            inventory.wood -= 1

        if keys[pygame.K_o] and inventory.oxygen_tank > 0:
            inventory.oxygen_tank -= 1
            state.thirst = min(state.thirst + 50, 100) 


        if keys[pygame.K_h]:
            if (inventory.water == WaterState.EMPTY or inventory.water == WaterState.RADIATED):
                display_message(screen, "You do not have any clean water!")
            else:
                inventory.water -= WaterState.EMPTY
                state.thirst = min(state.thirst + 50, 100) 

        # Check if 'i' is pressed to exit inventory
        if keys[pygame.K_i]:
            inventory_open = False

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(30)


# Function to fill the bottle with radiated water
def fill_bottle_with_radiated_water(inventory):
    if inventory.water == WaterState.EMPTY:
        inventory.water = WaterState.RADIATED
        return("Bottle filled with radiated water.")
    else:
        return("Bottle is already filled.")

# Function to cook the water to make it clean
def cook_water(inventory):
    if inventory.water == WaterState.RADIATED:
        inventory.water = WaterState.CLEAN
        return("Water is now clean.")
    else:
        return("You need to fill the bottle with radiated water first.")
