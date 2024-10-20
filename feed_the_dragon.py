import pygame
import random

# Initialize the game
pygame.init()

# Set up the screen
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Feed the Dragon')

# Set fps and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 1
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARKGREEN = (10, 100, 0)
BLACK = (0, 0, 0)

# Set fonts
font = pygame.font.Font('AttackGraffiti.ttf', 32)

# Set text
score_text = font.render('Score: ' + str(score), True, GREEN, DARKGREEN)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

title_text = font.render('Feed the Dragon', True, GREEN, WHITE)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WINDOW_WIDTH // 2
title_text_rect.y = 10

lives_text = font.render('Lives: ' + str(player_lives), True, GREEN, DARKGREEN)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render('Game Over', True, GREEN, DARKGREEN)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render('Press any key to continue', True, GREEN, DARKGREEN)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)

# Set sounds
coin_sound = pygame.mixer.Sound('coin_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
miss_sound.set_volume(0.1)
pygame.mixer.music.load('ftd_background_music.wav')

# Set images
player_image = pygame.image.load('dragon_right.png')
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# Main game loop
pygame.mixer.music.play(-1)
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # Move the coin
    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        coin_rect.x -= coin_velocity

    # Check for collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    # Update the text
    score_text = font.render('Score: ' + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render('Lives: ' + str(player_lives), True, GREEN, DARKGREEN)

    # Check for game over
    if player_lives <= 0:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(continue_text, continue_text_rect)
        pygame.display.update()

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT // 2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    #Fill the screen
    display_surface.fill(BLACK)

    #Blit the HUD
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(lives_text, lives_text_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    #Blit assets
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()
