import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Luurangi Streets")

# Load background images
start_menu_background = pygame.image.load("menu_background.jpg")
start_menu_background = pygame.transform.scale(start_menu_background, (width, height))

game_background = pygame.image.load("background.jpg")
game_background = pygame.transform.scale(game_background, (width, height))

white = (255, 255, 255)
red = (255, 0, 0)

# Load player, enemy, and bullet images
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (48, 48))

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (48, 48))

bullet_image = pygame.image.load("artifact_bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (15, 15))

player_rect = player_image.get_rect()

projectile_speed = 7
projectile_width = 10
projectile_height = 5
fire_rate = 200

# Initialize projectiles and firing time
projectiles = []
last_fire_time = pygame.time.get_ticks()

enemies = []

score = 0

clock = pygame.time.Clock()

# Define game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

game_state = MENU

def create_enemy():
    enemy_size = 48
    enemy = pygame.Rect(random.randint(0, width - enemy_size), 0, enemy_size, enemy_size)
    return enemy

def show_game_over():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over - Press R to play again or Q to quit", True, red)
    screen.blit(game_over_text, (width // 2 - 300, height // 2))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, red)
    screen.blit(score_text, (width - 150, 20))

def draw_menu():
    # Draw start menu background
    screen.blit(start_menu_background, (0, 0))

    font = pygame.font.Font(None, 48)
    play_text = font.render("Play", True, red)
    quit_text = font.render("Quit", True, red)

    play_rect = play_text.get_rect(center=(width // 2, height // 2 - 50))
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 50))

    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)

def draw_pause():
    font = pygame.font.Font(None, 36)
    pause_text = font.render("Game Paused - Press P to resume, R to restart, or Q to quit", True, red)
    screen.blit(pause_text, (width // 2 - 300, height // 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if game_state == MENU:
        # Menu screen logic
        if keys[pygame.K_DOWN]:
            game_state = GAME_OVER
        elif keys[pygame.K_UP]:
            game_state = PLAYING
    elif game_state == PLAYING:
        # Main game logic

        # Player movement
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.right < width:
            player_rect.x += 5
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= 5
        if keys[pygame.K_DOWN] and player_rect.bottom < height:
            player_rect.y += 5

        # Player attack (shoot up)
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if len(projectiles) < 5 and current_time - last_fire_time > fire_rate:
                projectiles.append(pygame.Rect(player_rect.x + player_rect.width // 2 - projectile_width // 2,
                                               player_rect.y - projectile_height, projectile_width, projectile_height))
                last_fire_time = current_time

        # Move projectiles
        for projectile in projectiles[:]:
            projectile.y -= projectile_speed
            if projectile.y < 0:
                projectiles.remove(projectile)

        # Move enemies
        for enemy in enemies:
            enemy.y += 3
            if enemy.colliderect(player_rect):
                game_state = GAME_OVER
            for projectile in projectiles[:]:
                if enemy.colliderect(projectile):
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    score += 1

        # Create new enemies less often
        if random.randint(0, 100) < 2:
            enemies.append(create_enemy())

        # Pause the game
        if keys[pygame.K_p]:
            game_state = PAUSED
    elif game_state == GAME_OVER:
        # Game over screen logic

        # Check for 'R' key to restart the game or 'Q' to quit
        if keys[pygame.K_r]:
            game_state = PLAYING
            # Reset game state
            player_rect.x = 375
            player_rect.y = 500
            enemies = []
            projectiles = []
            last_fire_time = pygame.time.get_ticks()
            score = 0
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
    elif game_state == PAUSED:
        # Pause screen logic

        # Resume the game
        if keys[pygame.K_p]:
            game_state = PLAYING
        # Restart the game
        elif keys[pygame.K_r]:
            game_state = PLAYING
            # Reset game state
            player_rect.x = 375
            player_rect.y = 500
            enemies = []
            projectiles = []
            last_fire_time = pygame.time.get_ticks()
            score = 0
        # Quit the game
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    # Draw background
    if game_state == MENU:
        draw_menu()
    else:
        screen.blit(game_background, (0, 0))

        if game_state == PLAYING:
            # Draw player
            screen.blit(player_image, player_rect)

            # Draw projectiles (artifacts)
            for projectile in projectiles:
                screen.blit(bullet_image, projectile)

            # Draw enemies
            for enemy in enemies:
                screen.blit(enemy_image, enemy)

            # Draw score
            draw_score()
        elif game_state == GAME_OVER:
            # Show game over screen
            show_game_over()
        elif game_state == PAUSED:
            # Draw pause screen
            draw_pause()

    # Update display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(30)
