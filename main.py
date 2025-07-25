import pygame
import random
import math
import sys

# Initialize
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion")

# Load sounds
laser_sound = pygame.mixer.Sound("laser.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Load player image
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Multiple aliens (SLOWER)
alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alien_img.append(pygame.image.load('alien.png'))
    alien_x.append(random.randint(0, 736))
    alien_y.append(random.randint(30, 150))
    alien_x_change.append(2)    # SLOWER horizontal speed
    alien_y_change.append(20)   # SLOWER vertical drop

# Bullet setup
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"  # "ready" means bullet can be fired

# Score and font
score = 0
font = pygame.font.Font(None, 36)

# Game Over
game_over_font = pygame.font.Font(None, 64)
game_over_played = False

def show_score():
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

def game_over_text():
    global game_over_played
    if not game_over_played:
        gameover_sound.play()
        game_over_played = True
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (280, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(ax, ay, bx, by):
    distance = math.hypot(ax - bx, ay - by)
    return distance < 27

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x  # align bullet with player
                laser_sound.play()
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0

    # Move player
    player_x += player_x_change
    player_x = max(0, min(player_x, 736))

    # Game over check
    game_active = True
    for i in range(num_of_aliens):
        if alien_y[i] > 440:
            for j in range(num_of_aliens):
                alien_y[j] = 2000  # hide all aliens
            game_active = False
            break

    if game_active:
        # Alien logic
        for i in range(num_of_aliens):
            alien_x[i] += alien_x_change[i]
            if alien_x[i] <= 0 or alien_x[i] >= 736:
                alien_x_change[i] *= -1
                alien_y[i] += alien_y_change[i]

            if is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y):
                bullet_y = 480
                bullet_state = "ready"
                hit_sound.play()
                score += 1
                alien_x[i] = random.randint(0, 736)
                alien_y[i] = random.randint(30, 150)

            alien(alien_x[i], alien_y[i], i)

    else:
        game_over_text()

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    # Draw player and score
    player(player_x, player_y)
    show_score()
    pygame.display.update()
