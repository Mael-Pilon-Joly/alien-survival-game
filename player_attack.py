import pygame

TILE_SIZE = 64

slash_image = pygame.image.load('./assets/slash.png')
slash_image = pygame.transform.scale(slash_image, (TILE_SIZE, TILE_SIZE))


def display_slash(screen, target_rect, slash_image):
    # Display the slash at the target's position
    screen.blit(slash_image, target_rect.topleft)
    pygame.display.flip()
    pygame.time.wait(200)  

def character_attack(screen, character_rect, aliens, attack_power):
    for alien in aliens:
        if character_rect.colliderect(alien.rect):
            display_slash(screen, alien.rect, slash_image)  # Show the slash effect
            alien.take_damage(attack_power)
            print(f"Alien {alien.__class__.__name__} takes {attack_power} damage! Remaining health: {alien.health}")
            if alien.health <= 0:
                alien.die()
                aliens.remove(alien) 