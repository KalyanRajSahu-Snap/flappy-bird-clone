import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
BIRD_X, BIRD_Y = 100, SCREEN_HEIGHT // 2
BIRD_RADIUS = 20
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 4

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 250)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# Load images
bird_img = pygame.image.load("assets/bird.png")
pipe_img = pygame.image.load("assets/pipe.png")
bg_img = pygame.image.load("assets/background.png")

# Resize images
bird_img = pygame.transform.scale(bird_img, (40, 30))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, 300))
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Variables
bird_y = BIRD_Y
velocity = 0
pipes = []
score = 0
font = pygame.font.Font(None, 36)

# Function to create new pipes
def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return top_pipe, bottom_pipe

# Add initial pipes
pipes.append(create_pipe())

# Game Loop
running = True
while running:
    screen.fill(BLUE)
    screen.blit(bg_img, (0, 0))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = JUMP_STRENGTH

    # Bird Physics
    velocity += GRAVITY
    bird_y += velocity
    screen.blit(bird_img, (BIRD_X, bird_y))

    # Move and Draw Pipes
    for pipe in pipes:
        pipe[0].x -= PIPE_SPEED
        pipe[1].x -= PIPE_SPEED
        pygame.draw.rect(screen, GREEN, pipe[0])  # Top Pipe
        pygame.draw.rect(screen, GREEN, pipe[1])  # Bottom Pipe

    # Check for Pipe Collision
    for pipe in pipes:
        if pipe[0].colliderect((BIRD_X, bird_y, 40, 30)) or pipe[1].colliderect((BIRD_X, bird_y, 40, 30)):
            running = False  # Game Over

    # Check if pipes go off screen & add new pipes
    if pipes[0][0].x < -PIPE_WIDTH:
        pipes.pop(0)
        pipes.append(create_pipe())
        score += 1

    # Display Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update Display
    pygame.display.update()
    clock.tick(30)

pygame.quit()
