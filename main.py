import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merry Christmas")

COLORS = [
    (0, 0, 0),
    (255, 255, 255),
    (139, 0, 0),
    (255, 165, 0),
    (255, 0, 0),
    (0, 255, 0)
]
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (139, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTS = [ORANGE, WHITE, (255, 255, 0), (135, 206, 250), (255, 99, 71)]  # Blinking colors

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
snowman_img = pygame.image.load("snowman.png")
snowman_img = pygame.transform.scale(snowman_img, (150, 200))

tree_img = pygame.image.load("image.png")
tree_img = pygame.transform.scale(tree_img, (200, 300))

# Load gift image
gift_img = pygame.image.load("gift.png")
gift_img = pygame.transform.scale(gift_img, (50, 50))  # Adjust size of gift

# Draw a blinking star
def draw_star(surface, x, y, size, color):
    points = []
    for i in range(10):
        angle = math.radians(i * 36)
        radius = size if i % 2 == 0 else size / 2.5
        points.append((x + radius * math.cos(angle), y - radius * math.sin(angle)))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, WHITE, points, 2)

# Draw snowflakes
snowflakes = [[random.randint(0, WIDTH), random.randint(-HEIGHT, HEIGHT), random.randint(2, 5)] for _ in range(200)]

def draw_snow(surface):
    for snowflake in snowflakes:
        x, y, size = snowflake
        pygame.draw.circle(surface, WHITE, (x, y), size)

def update_snow():
    for snowflake in snowflakes:
        snowflake[1] += snowflake[2]  # Fall speed
        if snowflake[1] > HEIGHT:
            snowflake[1] = random.randint(-50, -10)
            snowflake[0] = random.randint(0, WIDTH)

# Draw snow ground
def draw_snow_ground(surface):
    pygame.draw.rect(surface, WHITE, (0, HEIGHT - 100, WIDTH, 100))

# Draw gifts
def draw_gifts(surface, tree_x, tree_y):
    gift_positions = [
        (tree_x - 75, tree_y + 250),  # Left gift
        (tree_x - 45, tree_y + 250),  # Center-left gift
        (tree_x - 20, tree_y + 260),
        (tree_x + 25, tree_y + 250),  # Center-right gift
    ]
    for pos in gift_positions:
        surface.blit(gift_img, pos)

# Main loop
running = True
last_blink_time = time.time()
current_star_color = ORANGE
text_x = -200  # Start off-screen to the left
text_blink = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw snow ground
    draw_snow_ground(screen)

    # Draw tree image
    tree_x = WIDTH // 2 - tree_img.get_width() // 2
    tree_y = HEIGHT - tree_img.get_height() - 100 + 20  # Adjust to remove gap
    screen.blit(tree_img, (tree_x, tree_y))

    # Blink the star
    if time.time() - last_blink_time > 0.5:  # Change color every 0.5 seconds
        current_star_color = random.choice(LIGHTS)
        text_blink = not text_blink  # Toggle text blinking
        last_blink_time = time.time()

    # Draw blinking star on top of the tree
    star_x = WIDTH // 2
    star_y = tree_y - 20  # Adjust star to overlap with the tree
    draw_star(screen, star_x, star_y, 30, current_star_color)

    # Draw snowman images
    snowman_left_x = tree_x - 150
    snowman_left_y = HEIGHT - snowman_img.get_height() - 100 + 20  # Adjust to remove gap
    screen.blit(snowman_img, (snowman_left_x, snowman_left_y))

    snowman_right_x = tree_x + tree_img.get_width() + 50
    snowman_right_y = HEIGHT - snowman_img.get_height() - 100 + 20  # Adjust to remove gap
    screen.blit(snowman_img, (snowman_right_x, snowman_right_y))

    # Draw gifts
    draw_gifts(screen, tree_x + tree_img.get_width() // 2, tree_y)

    # Draw snowflakes
    draw_snow(screen)
    update_snow()

    # Display moving and blinking text
    font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    text_surface = font.render("Merry Christmas", True, WHITE)
    text_outline = font.render("Merry Christmas", True, RED)

    # Draw outline
    screen.blit(text_outline, (text_x - 2, 48))  # Slight offset for outline
    screen.blit(text_outline, (text_x + 2, 48))
    screen.blit(text_outline, (text_x, 46))
    screen.blit(text_outline, (text_x, 50))

    # Draw main text
    screen.blit(text_surface, (text_x, 48))

    text_x += 2  # Move text to the right
    if text_x > WIDTH:
        text_x = -200  # Reset position to the left

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
