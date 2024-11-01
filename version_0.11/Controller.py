# Controller.py
import subprocess
import sys
from multiprocessing import Process, Queue
import time


def run_snake_game(gesture_queue):
    import Game  # Import the Snake game code here
    Game.game_loop(gesture_queue)


def run_gesture_control(gesture_queue):
    import HandGesture  # Import the gesture detection code here
    HandGesture.detect_gesture(gesture_queue)


def main():
    print("Starting Snake Game with Gesture Controls...")
    print("Press Ctrl+C in this window to quit both programs")

    gesture_queue = Queue()

    game_process = Process(target=run_snake_game, args=(gesture_queue,))
    gesture_process = Process(target=run_gesture_control, args=(gesture_queue,))

    try:
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
        if game_process.is_alive():
            game_process.terminate()
        if gesture_process.is_alive():
            gesture_process.terminate()

        game_process.join()
        gesture_process.join()

        print("Successfully shut down all components")


if __name__ == "__main__":
    main()
