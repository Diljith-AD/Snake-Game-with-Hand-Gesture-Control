import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand_detector = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Gesture detection variables
gesture = None
swipe_threshold_horizontal = 0.1
swipe_threshold_vertical = 0.1
prev_position = None
last_horizontal_gesture_time = 0
last_vertical_gesture_time = 0
horizontal_cooldown = 1.0
vertical_cooldown = 1.0

# Function to detect swipe gestures
def detect_swipe_gesture(landmarks):
    global gesture, prev_position, last_horizontal_gesture_time, last_vertical_gesture_time

    # Get the coordinates of the index and middle finger tips (landmarks 8 and 12)
    index_tip = landmarks[8]
    middle_tip = landmarks[12]

    # Use the average of index and middle finger tips for swipe detection
    avg_x = (index_tip.x + middle_tip.x) / 2
    avg_y = (index_tip.y + middle_tip.y) / 2
    current_time = time.time()

    if prev_position:
        dx = avg_x - prev_position[0]
        dy = prev_position[1] - avg_y

        # Horizontal swipe detection
        if abs(dx) > abs(dy):
            if (current_time - last_horizontal_gesture_time) > horizontal_cooldown:
                if dx > swipe_threshold_horizontal:
                    gesture = "RIGHT"
                    last_horizontal_gesture_time = current_time
                elif dx < -swipe_threshold_horizontal:
                    gesture = "LEFT"
                    last_horizontal_gesture_time = current_time

        # Vertical swipe detection
        else:
            if (current_time - last_vertical_gesture_time) > vertical_cooldown:
                if dy > swipe_threshold_vertical:
                    gesture = "UP"
                    last_vertical_gesture_time = current_time
                elif dy < -swipe_threshold_vertical:
                    gesture = "DOWN"
                    last_vertical_gesture_time = current_time

    prev_position = (avg_x, avg_y)
    return gesture

# Function to continuously detect gestures
def start_gesture_detection():
    global gesture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hand_detector.process(image)

        if results.multi_hand_landmarks:
            nearest_hand = None
            min_z = float('inf')

            # Find the nearest hand
            for hand_landmarks in results.multi_hand_landmarks:
                wrist_z = hand_landmarks.landmark[0].z
                if wrist_z < min_z:
                    min_z = wrist_z
                    nearest_hand = hand_landmarks

            if nearest_hand:
                detected_gesture = detect_swipe_gesture(nearest_hand.landmark)
                
                # Write the gesture to the file only if it changes
                if detected_gesture:
                    with open('gesture.txt', 'w') as f:
                        f.write(detected_gesture)
                    gesture = None  # Reset only after writing to ensure proper detection

                # Draw landmarks only for the nearest hand
                mp_drawing.draw_landmarks(frame, nearest_hand, mp_hands.HAND_CONNECTIONS)

                if detected_gesture:
                    cv2.putText(frame, f"Gesture: {detected_gesture}", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame
        
        cv2.imshow('Hand Gesture Detection', frame)
        
        # Quit with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
