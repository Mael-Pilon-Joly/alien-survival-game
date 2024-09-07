import pygame

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

intro_image = pygame.image.load('./assets/intro.png')
intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def display_intro(screen):
    screen.blit(intro_image, (0, 0))  # Draw the image on the screen at position (0, 0)
    pygame.display.flip()  
    
# Function to handle the intro screen
def intro_screen(screen):

    intro_active = True
    while intro_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Check if "S" key is pressed
                    intro_active = False  # Exit the intro screen

        display_intro(screen)