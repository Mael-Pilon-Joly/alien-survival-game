import pygame

font = pygame.font.Font(None, 36)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def display_message(screen, message):
    text_surface = font.render(message, True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))  # Centered horizontally, near the bottom
    pygame.draw.rect(screen, (0, 0, 0), text_rect)  # Draw background for the message
    screen.blit(text_surface, text_rect)