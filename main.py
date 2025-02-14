import pygame as pg
from random import randrange

pg.init()
# Size of the game window
window = 1000
tileSize = 30

# Define the range for random positions within the window
range = (tileSize // 2, window - tileSize // 2, tileSize)

# Lambda function to get a random position within the defined range
getRandomPosition = lambda: [randrange(*range), randrange(*range)]

# Create the initial snake segment
snake = pg.rect.Rect([0, 0, tileSize - 2, tileSize - 2])
snake.center = getRandomPosition()

# Initialize the snake length and segments list
length = 1
segments = [snake.copy()]

# Initial direction of the snake (not moving)
snakeDir = (0, 0)

time = 0
timeStep = 110
food = snake.copy()
food.center = getRandomPosition()

# Initialize the score
score = 0

# Set up the Pygame display window
screen = pg.display.set_mode([window] * 2)

# Create a clock object to control the frame rate
clock = pg.time.Clock()

dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Set up font for displaying the score and title
font = pg.font.Font('font//Minecraft.ttf', 50)

# Define the title text
title_text = "Snake Game"

# Main game loop
while True:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snakeDir = (0, -tileSize)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

            elif event.key == pg.K_s and dirs[pg.K_s]:
                snakeDir = (0, tileSize)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

            elif event.key == pg.K_a and dirs[pg.K_a]:
                snakeDir = (-tileSize, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

            elif event.key == pg.K_d and dirs[pg.K_d]:
                snakeDir = (tileSize, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
    
    # Fill the screen with black color
    screen.fill('black')

    # Check border & Self-Eating
    selfEating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or selfEating:
        snake.center, food.center = getRandomPosition(), getRandomPosition()
        length, snakeDir = 1, (0, 0)
        segments = [snake.copy()]
        score = 0  # Reset score on collision

    # Check food
    if snake.center == food.center:
        food.center = getRandomPosition()
        length += 1
        score += 1  # Increase score when food is eaten

    # Draw food as a circle
    pg.draw.circle(screen, 'red', food.center, tileSize // 2)

    # Draw the snake segments
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

    # Move the snake
    timeNow = pg.time.get_ticks()
    if timeNow - time > timeStep:
        time = timeNow
        snake.move_ip(snakeDir)
        segments.append(snake.copy())
        segments = segments[-length:]
    
    # Render the score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Render the title
    title_surface = font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(topright=(window - 10, 10))
    screen.blit(title_surface, title_rect)

    # Update the display
    pg.display.flip()
    
    # Cap the frame rate at 60 frames per second
    clock.tick(60)