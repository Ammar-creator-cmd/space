#module
import pygame
import random
import sys

#initialize pygame libraries
pygame.init()

#set up window
window_width, window_height = 400, 300
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Collider")

#load bg image and scale it
background1 = pygame.image.load("space/spacebg.jpg").convert()
background1 = pygame.transform.scale(background1, (window_width, window_height))
background2 = pygame.transform.scale(background1, (window_width, window_height))

#load spaceship
spaceship_img = pygame.image.load("space/spaceship-removebg-preview.png").convert_alpha()
spaceship_width, spaceship_height = spaceship_img.get_size()
spaceship_scale = 0.15
spaceship_img = pygame.transform.scale(spaceship_img, (int(spaceship_width * spaceship_scale), int(spaceship_height * spaceship_scale)))
spaceship_width, spaceship_height = spaceship_img.get_size()

#spaceship position
spaceship_x = window_width // 2 - spaceship_width // 2
spaceship_y = window_height - 50
spaceship_speed = 3

class Asteroid:
    def __init__(self, x, y, image, scale):
        self.x = x
        self.y = y
        self.image = image
        self.scale = scale
        #resize the asteorid image based on the scale
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))

    def move(self, speed=1):  # <-- Add default value
        self.y += speed
        
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


asteroid_img = pygame.image.load("space/asteroid-removebg-preview.png").convert_alpha()
asteroid_width, asteroid_height = asteroid_img.get_size()

max_asteroid_scale = 0.15
min_asteroid_scale = 0.05

asteroids = []
clock = pygame.time.Clock()
game_running = True

# Initialize background positions for scrolling
background1_y = 0
background2_y = window_height

def close_game():
    pygame.quit()
    sys.exit()

# Function to update the background position for scrolling
def update_background():
    global background1_y, background2_y
    
    # Update positions
    background1_y += 1
    background2_y += 1
    
    # Reset positions when backgrounds move off screen
    if background1_y >= window_height:
        background1_y = -window_height
    if background2_y >= window_height:
        background2_y = -window_height
        
    # Draw backgrounds at their current positions
    window.blit(background1, (0, background1_y))
    window.blit(background2, (0, background2_y))


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            close_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_x -= spaceship_speed
        if spaceship_x < 0:
            spaceship_x = 0

    if keys[pygame.K_RIGHT]:
        spaceship_x += spaceship_speed
        if spaceship_x > window_width - spaceship_width:
            spaceship_x = window_width - spaceship_width
    
    window.fill((0, 0, 0))
    update_background()
    window.blit(spaceship_img, (spaceship_x, spaceship_y)) 

    #asteroid spawn
    if random.randint(0,100) < 2:
        asteroid_x = random.randint(30, window_width - 30)
        asteroid_scale = random.uniform(min_asteroid_scale, max_asteroid_scale)
        asteroid = Asteroid(asteroid_x, -int(asteroid_height * asteroid_scale), asteroid_img, asteroid_scale)
        asteroids.append(asteroid)

    #rectangles to represent collisions
    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)

    #move and draw asteroids
    for asteroid in asteroids:
        asteroid.move(1)
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.image.get_width(), asteroid.image.get_height())
        asteroid.draw(window)

        if spaceship_rect.colliderect(asteroid_rect):
            game_running = False
            close_game()

    #remove asteroids that have gone off screen
    asteroids = [asteroid for asteroid in asteroids if asteroid.y < window_height]

    pygame.display.update()
    clock.tick(60)
    
    









pygame.quit()
sys.exit()