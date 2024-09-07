# Load images
import pygame

screen_width = 800
screen_height = 600

ship_image = pygame.image.load('./assets/damaged_spaceship.png') 
ship_image = pygame.transform.scale(ship_image, (100, 100))  

# Load the border image
border_image = pygame.image.load('./assets/earth.png')
border_image = pygame.transform.scale(border_image, (screen_width, screen_height))



# Function to draw the ship if in area (0,0)
def draw_ship(screen, currentXArea, currentYArea):
    if currentXArea == 0 and currentYArea == 0:
        screen.blit(ship_image, (screen_width // 2 - ship_image.get_width() // 2, screen_height // 2 - ship_image.get_height() // 2))

def draw_boundary(screen, currentXArea, currentYArea):
    # Right border
    if currentXArea == 4:
        screen.blit(border_image, (screen_width - 150, 0))
    
    # Left border
    if currentXArea == -4:
        screen.blit(border_image, (-screen_width + 10, 0))

    # Bottom border
    if currentYArea == 4:
        screen.blit(border_image, (0, screen_height - 150))
    
    # Top border
    if currentYArea == -4:
        screen.blit(border_image, (0, -screen_height + 150))
