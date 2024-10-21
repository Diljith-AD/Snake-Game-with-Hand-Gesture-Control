import subprocess
import sys
import os
import time
from multiprocessing import Process


def run_snake_game():
    try:
        subprocess.run([sys.executable, "Game.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Snake game crashed with error: {e}")
    except KeyboardInterrupt:
        print("Snake game stopped by user")


def run_gesture_control():
    try:
        subprocess.run([sys.executable, "HandGesture.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Gesture control crashed with error: {e}")
    except KeyboardInterrupt:
        print("Gesture control stopped by user")


def create_gesture_file():
    # Create the gesture file if it doesn't exist
    with open('gesture.txt', 'w') as f:
        f.write('')


def main():
    print("Starting Snake Game with Gesture Controls...")
    print("Press Ctrl+C in this window to quit both programs")

    # Create the gesture file for communication
    create_gesture_file()

    # Create processes for both programs
    game_process = Process(target=run_snake_game)
    gesture_process = Process(target=run_gesture_control)

    try:
        # Start both processes
        game_process.start()
        time.sleep(2)  # Give the game a moment to start
        gesture_process.start()

        # Keep the main process running
        while True:
            if not game_process.is_alive() and not gesture_process.is_alive():
                print("Both programs have ended")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up processes
        if game_process.is_alive():
            game_process.terminate()
        if gesture_process.is_alive():
            gesture_process.terminate()

        # Clean up the gesture file
        try:
            os.remove('gesture.txt')
        except:
            pass

        # Wait for processes to finish
        game_process.join()
        gesture_process.join()

        print("Successfully shut down all components")


if __name__ == "__main__":
    main()