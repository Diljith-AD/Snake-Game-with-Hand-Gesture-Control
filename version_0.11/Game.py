# Game.py
import pygame
import random
import sys
from multiprocessing import Queue

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display dimensions
dis_width = 600
dis_height = 400

# Create display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Clock and speed
clock = pygame.time.Clock()
snake_speed = 10

# Snake
snake_block = 10
snake_list = []
snake_length = 1

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def show_score(score):
    score_text = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(score_text, [0, 0])

def game_loop(gesture_queue):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    global snake_length
    snake_list.clear()
    snake_length = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(blue)
            message = font_style.render("You Lost! Press C-Play Again or Q-Quit", True, red)
            dis.blit(message, [dis_width / 6, dis_height / 3])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(gesture_queue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Handle gestures
        if not gesture_queue.empty():
            gesture = gesture_queue.get()
            if gesture == "LEFT":
                x1_change = -snake_block
                y1_change = 0
            elif gesture == "RIGHT":
                x1_change = snake_block
                y1_change = 0
            elif gesture == "UP":
                y1_change = -snake_block
                x1_change = 0
            elif gesture == "DOWN":
                y1_change = snake_block
                x1_change = 0

        # Check boundaries
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Draw game elements
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list)
        show_score(snake_length - 1)
        pygame.display.update()

        # Check for food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Gesture queue will be initialized in the controller script
    pass
