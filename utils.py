import pygame

font = pygame.font.Font(None, 36)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def display_message(screen, message, duration=5000):
    start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    displaying_message = True

    duration_not_filling_water = 3000

    while displaying_message:
        # Calculate the elapsed time
        elapsed_time = pygame.time.get_ticks() - start_time
        
        # Render the message text
        text_surface = font.render(message, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))  # Centered horizontally, near the bottom
        
         # Clear only the bottom part of the screen or redraw the previous frame
        pygame.draw.rect(screen, (0, 0, 0), (0, SCREEN_HEIGHT + 50, SCREEN_WIDTH, 50))  # Draw background for the message area
        
        # Display the message
        screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

        if elapsed_time >= duration_not_filling_water and message != "Filling bottle with radiated water.":
            displaying_message = False

        # Check if the specified duration has passed
        if elapsed_time >= duration:
            displaying_message = False

        # Handle events so the window doesn't freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()