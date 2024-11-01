# HandGesture.py
import cv2
import mediapipe as mp
import time
from multiprocessing import Queue

mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

def detect_gesture(gesture_queue):
    prev_position = None
    last_gesture_time = 0
    horizontal_cooldown = 0.5
    vertical_cooldown = 0.2

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

            for hand_landmarks in results.multi_hand_landmarks:
                wrist_z = hand_landmarks.landmark[0].z
                if wrist_z < min_z:
                    min_z = wrist_z
                    nearest_hand = hand_landmarks

            if nearest_hand:
                index_tip = nearest_hand.landmark[8]
                middle_tip = nearest_hand.landmark[12]
                avg_x = (index_tip.x + middle_tip.x) / 2
                avg_y = (index_tip.y + middle_tip.y) / 2
                current_time = time.time()

                if prev_position:
                    dx = avg_x - prev_position[0]
                    dy = prev_position[1] - avg_y

                    if abs(dx) > abs(dy):
                        if (current_time - last_gesture_time) > horizontal_cooldown:
                            if dx > 0.1:
                                gesture_queue.put("RIGHT")
                                last_gesture_time = current_time
                            elif dx < -0.1:
                                gesture_queue.put("LEFT")
                                last_gesture_time = current_time
                    else:
                        if (current_time - last_gesture_time) > vertical_cooldown:
                            if dy > 0.1:
                                gesture_queue.put("DOWN")
                                last_gesture_time = current_time
                            elif dy < -0.1:
                                gesture_queue.put("UP")
                                last_gesture_time = current_time

                prev_position = (avg_x, avg_y)

        cv2.imshow('Hand Gesture Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Gesture queue will be initialized in the controller script
    pass
