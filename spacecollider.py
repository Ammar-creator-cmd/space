import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window setup
window_width, window_height = 400, 300
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Collider")

# Load and scale background
background = pygame.image.load("spacebg.jpg").convert()
background = pygame.transform.scale(background, (window_width, window_height))

# Load and scale spaceship
spaceship_img = pygame.image.load("spaceship-removebg-preview.png").convert_alpha()
spaceship_img = pygame.transform.scale(spaceship_img, (int(spaceship_img.get_width() * 0.15), int(spaceship_img.get_height() * 0.15)))
spaceship_width, spaceship_height = spaceship_img.get_size()
spaceship_x = window_width // 2 - spaceship_width // 2
spaceship_y = window_height - 50
spaceship_speed = 3

# Load asteroid
asteroid_img = pygame.image.load("asteroid-removebg-preview.png").convert_alpha()
asteroid_width, asteroid_height = asteroid_img.get_size()

# Asteroid class
class Asteroid:
    def __init__(self, x, y, image, scale):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

    def move(self, speed):
        self.y += speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

# Game variables
asteroids = []
clock = pygame.time.Clock()
game_running = True
background_y1 = 0
background_y2 = -window_height
lives = 3
score = 0
font = pygame.font.Font(None, 36)
score_timer = 0  # Track time for score increment

# Functions
def close_game():
    pygame.quit()
    sys.exit()

def update_background():
    global background_y1, background_y2
    background_y1 += 1
    background_y2 += 1
    if background_y1 >= window_height:
        background_y1 = -window_height
    if background_y2 >= window_height:
        background_y2 = -window_height
    window.blit(background, (0, background_y1))
    window.blit(background, (0, background_y2))

def draw_lives():
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (window_width - 120, 10))

def lose_life():
    global lives
    lives -= 1
    if lives <= 0:
        close_game()

# Intro screen
intro_running = True
while intro_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            intro_running = False

    window.fill((0, 0, 0))
    intro_text = font.render("Welcome to Space Collider!", True, (255, 255, 255))
    instructions_text = font.render("Press Enter to start.", True, (255, 255, 255))
    controls_text = font.render("Use arrows to move.", True, (255, 255, 255))
    window.blit(intro_text, (50, 100))
    window.blit(instructions_text, (30, 150))
    window.blit(controls_text, (30, 200))
    pygame.display.update()
    clock.tick(60)

# Main game loop
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_x = max(spaceship_x - spaceship_speed, 0)
    if keys[pygame.K_RIGHT]:
        spaceship_x = min(spaceship_x + spaceship_speed, window_width - spaceship_width)

    update_background()
    window.blit(spaceship_img, (spaceship_x, spaceship_y))

    # Spawn asteroids
    if random.randint(0, 100) < 2:
        asteroid_x = random.randint(30, window_width - 30)
        asteroid_scale = random.uniform(0.05, 0.15)
        asteroid = Asteroid(asteroid_x, -int(asteroid_height * asteroid_scale), asteroid_img, asteroid_scale)
        asteroids.append(asteroid)

    # Move and draw asteroids
    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)
    for asteroid in asteroids[:]:
        asteroid.move(1)
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.image.get_width(), asteroid.image.get_height())
        asteroid.draw(window)

        if spaceship_rect.colliderect(asteroid_rect):
            asteroids.remove(asteroid)
            lose_life()

    # Remove off-screen asteroids
    asteroids = [a for a in asteroids if a.y < window_height]

    # Score increases every second
    score_timer += clock.get_time()
    if score_timer >= 1000:  # 1000 milliseconds = 1 second
        score += 1
        score_timer = 0

    draw_lives()
    draw_score()
    pygame.display.update()
    clock.tick(60)
pygame.quit()