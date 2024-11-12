import pygame
import random
import threading
import HandGesture
import os

# Initialize Pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

# Load sound effect
eat_sound = pygame.mixer.Sound(os.path.join('assets', 'eat_sound.wav'))

# Game display dimensions
DIS_WIDTH = 800
DIS_HEIGHT = 600
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Enhanced Snake Game with Hand Gestures')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Game clock
clock = pygame.time.Clock()
SNAKE_BLOCK = 20
SNAKE_SPEED = 5

# Font settings
font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load assets
food_size = 50
try:
    apple_image = pygame.image.load(os.path.join('assets', 'apple.png'))
    apple_image = pygame.transform.scale(apple_image, (food_size, food_size))
except pygame.error:
    apple_image = None
    print("Error loading apple image")

background_image = pygame.image.load('game_background.png')
background_image = pygame.transform.scale(background_image, (DIS_WIDTH, DIS_HEIGHT))

# Start gesture detection in a separate thread
gesture_thread = threading.Thread(target=HandGesture.start_gesture_detection, daemon=True)
gesture_thread.start()

# Function to read hand gestures from file
def read_gesture():
    try:
        with open('gesture.txt', 'r+') as f:
            gesture = f.read().strip()
            if gesture:
                f.seek(0)
                f.truncate()
            return gesture
    except FileNotFoundError:
        return ''

# Display score
def show_score(score):
    # Render the score on the screen
    value = score_font.render(f"Score: {score}", True, YELLOW)
    dis.blit(value, [0, 0])

    # Write the score to 'high_scores.txt'
    with open('high_scores.txt', 'w') as file:
        file.write(f" {score}\n")

# Draw snake on the screen
def draw_snake(snake_blocks):
    for i, block in enumerate(snake_blocks):
        x, y = block
        if i == 0:  # Draw the head
            pygame.draw.rect(dis, GREEN, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])
        else:  # Draw the body
            pygame.draw.rect(dis, BLUE, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])

# Function to show messages
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])

# Draw button with text
def draw_button(screen, msg, color, font, button_rect):
    pygame.draw.rect(screen, WHITE, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    text_surface = font.render(msg, True, color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# Game over screen with option to return to the menu
def game_over_menu():
    while True:
        dis.fill(BLACK)
        message("Game Over!", RED, DIS_WIDTH // 3, DIS_HEIGHT // 4)
        
        # Define buttons
        play_again_button = pygame.Rect(DIS_WIDTH // 3, DIS_HEIGHT // 2 - 80, 200, 50)
        menu_button = pygame.Rect(DIS_WIDTH // 3, DIS_HEIGHT // 2, 200, 50)
        quit_button = pygame.Rect(DIS_WIDTH // 3, DIS_HEIGHT // 2 + 80, 200, 50)

        draw_button(dis, "Play Again", BLACK, font_style, play_again_button)
        draw_button(dis, "Menu", BLACK, font_style, menu_button)
        draw_button(dis, "Quit", BLACK, font_style, quit_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return 'play_again'
                elif menu_button.collidepoint(event.pos):
                    return 'menu'
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Game Loop
def game_loop():
    global SNAKE_SPEED
    while True:
        x, y = DIS_WIDTH // 2, DIS_HEIGHT // 2
        x_change, y_change = 0, 0

        snake_blocks = []
        snake_length = 1

        foodx = round(random.randrange(0, DIS_WIDTH - food_size) / 10.0) * 10.0
        foody = round(random.randrange(0, DIS_HEIGHT - food_size) / 10.0) * 10.0

        direction = 'RIGHT'
        gesture_cooldown = 3
        gesture_timer = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Handle hand gestures
            if gesture_timer == 0:
                gesture = read_gesture()
                if gesture == "LEFT" and direction != 'RIGHT':
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                    direction = 'LEFT'
                elif gesture == "RIGHT" and direction != 'LEFT':
                    x_change = SNAKE_BLOCK
                    y_change = 0
                    direction = 'RIGHT'
                elif gesture == "UP" and direction != 'DOWN':
                    x_change = 0
                    y_change = -SNAKE_BLOCK
                    direction = 'UP'
                elif gesture == "DOWN" and direction != 'UP':
                    x_change = 0
                    y_change = SNAKE_BLOCK
                    direction = 'DOWN'
                gesture_timer = gesture_cooldown
            else:
                gesture_timer -= 1

            # Update snake position
            x += x_change
            y += y_change

            # Check for collisions with walls or itself
            if x >= DIS_WIDTH or x < 0 or y >= DIS_HEIGHT or y < 0:
                break

            dis.blit(background_image, (0, 0))
            if apple_image:
                dis.blit(apple_image, (foodx, foody))
            else:
                pygame.draw.rect(dis, RED, [foodx, foody, food_size, food_size])

            snake_head = [x, y]
            snake_blocks.append(snake_head)
            if len(snake_blocks) > snake_length:
                del snake_blocks[0]

            for block in snake_blocks[:-1]:
                if block == snake_head:
                    break

            draw_snake(snake_blocks)
            show_score(snake_length - 1)
            pygame.display.update()

            # Check if snake eats the food
            if (x >= foodx and x < foodx + food_size) and (y >= foody and y < foody + food_size):
                foodx = round(random.randrange(0, DIS_WIDTH - food_size) / 10.0) * 10.0
                foody = round(random.randrange(0, DIS_HEIGHT - food_size) / 10.0) * 10.0
                snake_length += 1
                eat_sound.play()
                SNAKE_SPEED = min(SNAKE_SPEED + 0.2, 15)

            clock.tick(SNAKE_SPEED)

        # Handle game over menu
        choice = game_over_menu()
        if choice == 'play_again':
            continue  # Restart the game loop
        elif choice == 'menu':
            return 'menu'

if __name__ == "__main__":
    while game_loop() != 'menu':
        pass
