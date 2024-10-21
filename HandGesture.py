import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)  # Allow detection of multiple hands

# Gesture detection variables
gesture = None
swipe_threshold_horizontal = 0.2
swipe_threshold_vertical = 0.1
diagonal_threshold = 0.05  # A smaller threshold to detect diagonal gestures
prev_position = None
last_gesture_time = 0  # To store the time of the last detected gesture
horizontal_cooldown = 0.5  # Cooldown time in seconds to prevent rapid left/right gesture detection
vertical_cooldown = 0.2  # Cooldown time in seconds to prevent rapid up/down gesture detection

def detect_swipe_gesture(landmarks):
    global gesture, prev_position, last_gesture_time

    # Get the coordinates of the index and middle finger tips (landmarks 8 and 12)
    index_tip = landmarks[8]
    middle_tip = landmarks[12]

    # Use average of index and middle finger tips for swipe detection
    avg_x = (index_tip.x + middle_tip.x) / 2
    avg_y = (index_tip.y + middle_tip.y) / 2
    current_time = time.time()

    # Calculate movement from previous position
    if prev_position:
        dx = avg_x - prev_position[0]  # Horizontal movement
        dy = prev_position[1] - avg_y  # Vertical movement (y-axis inverted)

        # Detect gesture only when it surpasses the cooldown period
        if abs(dx) > abs(dy):  # Primarily horizontal movement
            if (current_time - last_gesture_time) > horizontal_cooldown:
                if dx > swipe_threshold_horizontal:
                    if dy < -diagonal_threshold:  # Diagonal down-right (Right + Down)
                        gesture = "RIGHT"
                    else:
                        gesture = "RIGHT"
                elif dx < -swipe_threshold_horizontal:
                    if dy < -diagonal_threshold:  # Diagonal down-left (Left + Down)
                        gesture = "LEFT"
                    else:
                        gesture = "LEFT"
                if gesture:
                    last_gesture_time = current_time
        else:  # Primarily vertical movement
            if (current_time - last_gesture_time) > vertical_cooldown:
                if dy > swipe_threshold_vertical:
                    if abs(dx) > diagonal_threshold:  # Detect diagonal up movement
                        if dx > 0:
                            gesture = "UP"
                        else:
                            gesture = "UP"
                    else:
                        gesture = "UP"
                elif dy < -swipe_threshold_vertical:
                    if abs(dx) > diagonal_threshold:  # Detect diagonal down movement
                        if dx > 0:
                            gesture = "DOWN"
                            gesture = "RIGHT"  # Diagonal down-right
                        else:
                            gesture = "DOWN"
                            gesture = "LEFT"  # Diagonal down-left
                    else:
                        gesture = "DOWN"
                if gesture:
                    last_gesture_time = current_time

    # Update previous position
    prev_position = (avg_x, avg_y)
    return gesture

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame to avoid mirrored view
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hand_detector.process(image)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        nearest_hand = None
        min_z = float('inf')  # Initialize with a large value to find the nearest hand

        # Loop through detected hands to find the nearest one
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_z = hand_landmarks.landmark[0].z  # Z coordinate of the wrist (landmark 0)
            if wrist_z < min_z:  # A smaller Z value means the hand is closer
                min_z = wrist_z
                nearest_hand = hand_landmarks

        # If a nearest hand is found, process its gesture
        if nearest_hand:
            gesture = detect_swipe_gesture(nearest_hand.landmark)

            # Print the detected gesture to the console if a gesture was detected
            if gesture:
                print(gesture)
                gesture = None  # Reset gesture after displaying in the console

    # Display the frame for visual reference (optional)
    cv2.imshow('Hand Gesture Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
