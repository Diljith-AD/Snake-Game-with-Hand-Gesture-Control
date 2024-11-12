import pygame
import sys
import os
import game
from PIL import Image

# Initialize Pygame
pygame.init()
pygame.mixer.init() 

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (0, 128, 0)
HOVER_COLOR = (0, 200, 0)

# Fonts
font = pygame.font.SysFont('Arial', 40)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 30

# Load and scale the background image
background_image = pygame.image.load('menu_background.png')  # Use the path to your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

background_music_path = 'assets/background_music.mp3'
background_music_enabled = True

def play_background_music():
    if background_music_enabled:
        pygame.mixer.music.load(background_music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Loop indefinitely

def stop_background_music():
    pygame.mixer.music.stop()

# Toggle music state
def toggle_music():
    global background_music_enabled
    background_music_enabled = not background_music_enabled
    if background_music_enabled:
        play_background_music()
    else:
        stop_background_music()

# File to store high scores
HIGH_SCORES_FILE = 'high_scores.txt'
MAX_HIGH_SCORES = 10

# Game States
MENU = 'menu'
GAME = 'game'
INSTRUCTIONS = 'instructions'
SETTINGS = 'settings'
HIGHSCORE = 'highscore'
EXIT = 'exit'
current_state = MENU

# Read and write high scores
def load_high_scores():
    """Load high scores from the file."""
    scores = []
    if not os.path.exists(HIGH_SCORES_FILE):  # Create file if it doesn't exist
        with open(HIGH_SCORES_FILE, 'w') as file:
            file.write("")  # Write empty content to create the file
    else:
        with open(HIGH_SCORES_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Only process non-empty lines
                    print(f"Processing line: {line}")  # Debugging: see the content of the line
                    try:
                        score = int(line)  # Only store the score as a number
                        scores.append(score)  # Add valid score to the list
                    except ValueError:
                        # Handle lines that don't match the expected format
                        print(f"Skipping invalid line: {line}")  # Debugging statement
    # Sort scores in descending order and return the top scores
    if scores:
        scores = sorted(scores, reverse=True)  # Sort by score, descending
        return scores  # Return the sorted list of scores
    else:
        return []  # Return an empty list if no scores exist




def save_high_scores(scores):
    """Save high scores to the file."""
    with open(HIGH_SCORES_FILE, 'w') as file:
        for score in scores:
            file.write(f"{score}\n")  # Save only the score, no player name



def update_high_scores(new_score, player_name):
    """Update the list of high scores with a new score."""
    scores = load_high_scores()
    scores.append((player_name, new_score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:MAX_HIGH_SCORES]
    save_high_scores(scores)


def draw_text(text, font, color, surface, x, y):
    """Draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def draw_button(text, x, y, width, height, color, hover_color):
    """Draw a button and check if the mouse is hovering over it."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Change button color when hovered
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:  # Left mouse button click
            return True
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Draw button text
    draw_text(text, font, WHITE, screen, x + width // 2, y + height // 2)

    return False


def menu_screen():
    """Display the main menu with buttons."""
    print("Entering menu screen...")  # Debugging statement
    while True:
        screen.fill(BLACK)

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw menu buttons
        if draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            print("Start Game clicked!")
            return GAME  # Update the game state to start the game
        if draw_button("Instructions", WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            print("Instructions clicked!")  # Debugging statement
            return INSTRUCTIONS

        if draw_button("Settings", WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            print("Settings clicked!")  # Debugging statement
            return SETTINGS

        if draw_button("High Scores", WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            print("High Scores clicked!")  # Debugging statement
            return HIGHSCORE

        if draw_button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            print("Exit clicked!")  # Debugging statement
            return EXIT

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def game_screen():
    """The game screen logic, where the actual gameplay happens."""
    while True:
        screen.fill(BLACK)
        # Your game logic here (e.g., displaying the snake and handling movements)

        # Example condition to check if the game is over
        if game_is_over():  # Replace with your actual game over condition
            print("Game Over!")  # Debugging statement
            return MENU  # Transition back to the menu once the game ends

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)       


def settings_screen():
    global background_music_enabled
    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Toggle music ON/OFF button
        music_button_text = "Music: ON" if background_music_enabled else "Music: OFF"
        if draw_button(music_button_text, WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            toggle_music()

        # Back button to the bottom right corner
        back_button_x = WIDTH - 250  # Position it 50 pixels from the right edge
        back_button_y = HEIGHT - 100  # Position it 50 pixels from the bottom edge
        if draw_button("Back", back_button_x, back_button_y, 200, 50, BUTTON_COLOR, HOVER_COLOR):
            pygame.event.clear()  # Clear all mouse events before returning to the menu
            return MENU

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

def high_score_screen():
    """Display the top high scores from the game."""
    scores = load_high_scores()

    # If no scores are loaded, show a message
    if not scores:
        scores = ["No high scores yet!"]

    while True:
        screen.fill(BLACK)
        
        # Display the title at the top of the screen
        draw_text("High Scores", font, GREEN, screen, WIDTH // 2, 100)

        # Display the top scores or a message if no scores exist
        y_position = 200
        if scores:
            for i, score in enumerate(scores[:10]):  # Display the top 10 scores
                draw_text(f"{i + 1}. {score}", font, WHITE, screen, WIDTH // 2, y_position)
                y_position += 40  # Adjust space between scores
        else:
            draw_text("No high scores yet!", font, WHITE, screen, WIDTH // 2, y_position)

        # Display the "Press ESC to return to Menu" message at the bottom
        draw_text("Press ESC to return to Menu", font, RED, screen, WIDTH // 2, HEIGHT - 50)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MENU  # Return to the main menu when ESC is pressed

        pygame.display.update()
        clock.tick(FPS)






def display_gif(gif_path, x, y, width, height):
    """Display a GIF by showing each frame in a loop."""
    gif = Image.open(gif_path)
    gif_frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = pygame.image.fromstring(gif.convert("RGBA").tobytes(), gif.size, 'RGBA')
        gif_frames.append(frame_image)
    
    frame_count = len(gif_frames)
    frame_index = 0
    return gif_frames, frame_count


def instructions_screen():
    """Display the instructions screen with GIFs side by side."""
    swipe_gif_path = 'assets/swipe.gif'  # Path to swipe.gif
    scroll_gif_path = 'assets/scroll.gif'  # Path to scroll.gif
    
    # Load GIFs
    swipe_gif_frames, swipe_frame_count = display_gif(swipe_gif_path, WIDTH // 4 - 100, HEIGHT // 8, 200, 200)
    scroll_gif_frames, scroll_frame_count = display_gif(scroll_gif_path, 3 * WIDTH // 4 - 100, HEIGHT // 8, 200, 200)

    swipe_frame_index = 0
    scroll_frame_index = 0
    swipe_frame_delay = 5  # Adjust this to control speed of the swipe gif
    scroll_frame_delay = 5  # Adjust this to control speed of the scroll gif
    swipe_frame_counter = 0
    scroll_frame_counter = 0

    # Scale GIFs to fit within the window (800x600)
    max_width = 400  # Max width for each GIF
    max_height = 300  # Max height for each GIF

    def scale_image(image, max_width, max_height):
        """Scale the image to fit within the max width and height."""
        width, height = image.get_width(), image.get_height()
        aspect_ratio = width / height
        if width > height:
            new_width = min(width, max_width)
            new_height = new_width / aspect_ratio
        else:
            new_height = min(height, max_height)
            new_width = new_height * aspect_ratio
        return pygame.transform.scale(image, (int(new_width), int(new_height)))

    # Scale images to fit the window
    swipe_gif_frames = [scale_image(frame, max_width, max_height) for frame in swipe_gif_frames]
    scroll_gif_frames = [scale_image(frame, max_width, max_height) for frame in scroll_gif_frames]

    while True:
        screen.fill(BLACK)
        
        # Draw the swipe GIF frame at the top
        screen.blit(swipe_gif_frames[swipe_frame_index], (WIDTH // 4 - swipe_gif_frames[swipe_frame_index].get_width() // 2, 50))

        # Draw the scroll GIF frame at the top
        screen.blit(scroll_gif_frames[scroll_frame_index], (3 * WIDTH // 4 - scroll_gif_frames[scroll_frame_index].get_width() // 2, 50))

        # Display instructions text slightly higher
        draw_text("Instructions:", font, GREEN, screen, WIDTH // 2, HEIGHT // 2 + 120)
        draw_text("Use hand gestures to control the snake", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 150)
        draw_text("Swipe to change direction", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 180)
        draw_text("Make sure swipe gestures occur within the camera", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 210)

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MENU  # Return to the menu when ESC is pressed

        # Cycle through the swipe GIF frames with a delay
        swipe_frame_counter += 1
        if swipe_frame_counter >= swipe_frame_delay:
            swipe_frame_index = (swipe_frame_index + 1) % swipe_frame_count
            swipe_frame_counter = 0
        
        # Cycle through the scroll GIF frames with a delay
        scroll_frame_counter += 1
        if scroll_frame_counter >= scroll_frame_delay:
            scroll_frame_index = (scroll_frame_index + 1) % scroll_frame_count
            scroll_frame_counter = 0

        pygame.display.update()
        clock.tick(FPS)

# Main loop
# Main loop in menu.py
def main():
    global current_state
    play_background_music()

    while True:
        if current_state == MENU:
            current_state = menu_screen()
        elif current_state == GAME:
            current_state = game.game_loop()
            if current_state == 'menu':
                continue  # Go back to the menu if the game loop returns 'menu'
        elif current_state == INSTRUCTIONS:
            current_state = instructions_screen()
        elif current_state == SETTINGS:
            current_state = settings_screen()    
        elif current_state == HIGHSCORE:
            current_state = high_score_screen()
        elif current_state == EXIT:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
