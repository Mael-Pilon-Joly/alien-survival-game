# Load images
import pygame
from resources import WaterState

screen_width = 800
screen_height = 600

ship_image = pygame.image.load('./assets/damaged_spaceship.png') 
ship_image = pygame.transform.scale(ship_image, (100, 100))  

# Load the border image
border_image = pygame.image.load('./assets/earth.png')
border_image = pygame.transform.scale(border_image, (screen_width, screen_height))

class Ship:
    def __init__(self):
        self.damage = 100  # The ship starts with 100% damage
        self.repaired = False
        self.rect = None

    def repair(self, amount):
        self.damage -= amount
        if self.damage <= 0:
            self.damage = 0
            self.repaired = True
            print("The ship is fully repaired!")

    def is_fully_repaired(self):
        return self.damage == 0



# Function to draw the ship if in area (0,0)
def draw_ship(screen, currentXArea, currentYArea):
    if currentXArea == 0 and currentYArea == 0:
        ship_x = screen_width // 2 - ship_image.get_width() // 2
        ship_y = screen_height // 2 - ship_image.get_height() // 2
        ship_rect = pygame.Rect(ship_x, ship_y, ship_image.get_width(), ship_image.get_height())
        screen.blit(ship_image, ship_rect)
        return ship_rect
    return None

def draw_boundary(screen, currentXArea, currentYArea):
    # Right border
    if currentXArea == 4:
        screen.blit(border_image, (screen_width - 150, 0))
    
    # Left border
    if currentXArea == -4:
        screen.blit(border_image, (-screen_width + 10, 0))

    # Bottom border
    if currentYArea == 4:
        screen.blit(border_image, (0, screen_height - 10))
    
    # Top border
    if currentYArea == -4:
        screen.blit(border_image, (0, -screen_height + 10))

def interact_with_ship(character_rect, ship, inventory, state, screen):
    if ship and character_rect.colliderect(ship.rect):
        # Draw the interaction menu
        draw_interaction_menu(screen)
        

        # Check for key presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if inventory.water == WaterState.RADIATED and inventory.wood > 0:
                inventory.water = WaterState.CLEAN
                return("Water is now clean.")
            else:
                return("Not enough water or wood.")
            
        if keys[pygame.K_m]:
            if inventory.meat > 0:
                inventory.meat -= 1
                state.health += 10
                if state.health > 100:
                    state.health = 100
                return("Meat is cooked and consumed. Health increased.")
        
        if keys[pygame.K_r]:
            if inventory.material >= 1:  # Assume repairing requires 5 units of wood
                inventory.material -= 1
                ship.repair(5)  # Assume each repair reduces damage by 20%
                return ("Ship repaired by 5%.")
        
        # Handle sleep logic
        for num in range(1, 10):
            if keys[getattr(pygame, f'K_{num}')]:
                sleep_hours = num
                state.health += 10 * sleep_hours
                if state.health > 100:
                    state.health = 100
                return(f"Player slept for {sleep_hours} hours and regained health.")
        
        if keys[pygame.K_e]:
            print("Exiting interaction with the ship.")
            return  # Exit interaction

# Function to draw the interaction menu
def draw_interaction_menu(screen):
    # Define the menu's appearance
    menu_width = 400
    menu_height = 200
    menu_x = screen.get_width() // 2 - menu_width // 2
    menu_y = screen.get_height() // 2 - menu_height // 2

    # Draw the menu background
    pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))

    # Create and render the text
    font = pygame.font.Font(None, 30)
    options = [
        "Press W to cook water",
        "Press M to cook meat",
        "Press R to repair",
        "Press a number to sleep that number of hours",
        "Press E to exit interaction"
    ]
    for i, option in enumerate(options):
        text_surface = font.render(option, True, (255, 255, 255))
        screen.blit(text_surface, (menu_x + 20, menu_y + 20 + i * 30))

    # Update the display
    pygame.display.flip()

