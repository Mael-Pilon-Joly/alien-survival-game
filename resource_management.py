import pygame

class GameState:
    def __init__(self):
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.oxygen = 100

def update_resources(state, elapsed_time, real_seconds_per_game_hour, time):
    global game_hours_passed, last_update_time
    current_time = time.time()
    elapsed_time = current_time - last_update_time
    
    # Convert elapsed real time to game hours
    game_hours = int(elapsed_time / real_seconds_per_game_hour)
    
    if game_hours > 0:
        # Deplete resources based on how many game hours have passed
        state.hunger -= game_hours * 5  # Example: Decrease hunger by 5 units per hour
        state.thirst -= game_hours * 7  # Example: Decrease thirst by 7 units per hour
        state.oxygen -= game_hours * 3  # Example: Decrease oxygen by 3 units per hour
        
        # Ensure values don't go below zero
        state.hunger = max(state.hunger, 0)
        state.thirst = max(state.thirst, 0)
        state.oxygen = max(state.oxygen, 0)
        
        # Update game hours passed and reset timer
        game_hours_passed += game_hours
        last_update_time = current_time

def draw_stats(screen, state, font):
    # Display the current in-game time and resource stats in a square in the bottom right
    health_text = font.render(f'Health: {int(state.health)}', True, (255, 0, 0))
    hunger_text = font.render(f'Hunger: {int(state.hunger)}', True, (0, 255, 0))
    thirst_text = font.render(f'Thirst: {int(state.thirst)}', True, (0, 0, 255))
    oxygen_text = font.render(f'Oxygen: {int(state.oxygen)}', True, (255, 255, 0))

    # Draw the stats in a square at the bottom right
    pygame.draw.rect(screen, (50, 50, 50), (600, 450, 200, 150))  # Background square

    screen.blit(health_text, (610, 460))
    screen.blit(hunger_text, (610, 490))
    screen.blit(thirst_text, (610, 520))
    screen.blit(oxygen_text, (610, 550))