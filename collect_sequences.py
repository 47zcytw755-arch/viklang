# collect_sequences.py (modified)
import cv2
import numpy as np
import os
import time

from mediapipe.python.solutions import holistic as mp_holistic
from mediapipe.python.solutions import drawing_utils as mp_draw

gesture = input("Gesture name: ")

save_dir = os.path.join("lstm_data", gesture)
os.makedirs(save_dir, exist_ok=True)

holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
sequence_id = len(os.listdir(save_dir))

print(f"Gesture: {gesture}")
print("Press S to start recording (3 sec countdown then 30 frames)")
print("Press Q to quit")

def extract_features(results):
    features = []
    if results.left_hand_landmarks:
        for lm in results.left_hand_landmarks.landmark:
            features.extend([lm.x, lm.y, lm.z])
    else:
        features.extend([0] * 63)
    if results.right_hand_landmarks:
        for lm in results.right_hand_landmarks.landmark:
            features.extend([lm.x, lm.y, lm.z])
    else:
        features.extend([0] * 63)
    return features

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(rgb)

    if results.left_hand_landmarks:
        mp_draw.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    if results.right_hand_landmarks:
        mp_draw.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Sequences saved: {sequence_id}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, "Press S to record", (10, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.imshow("LSTM Data Collector", frame)
    key = cv2.waitKey(1)

    if key == ord("s"):
        for countdown in range(3, 0, -1):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, f"Get ready: {countdown}", (180, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            cv2.imshow("LSTM Data Collector", frame)
            cv2.waitKey(1000)

        sequence = []
        print(f"Recording sequence {sequence_id}...")
        for i in range(30):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)
            features = extract_features(results)
            sequence.append(features)
            cv2.putText(frame, f"RECORDING {i+1}/30", (140, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.imshow("LSTM Data Collector", frame)
            cv2.waitKey(1)

        np.save(os.path.join(save_dir, f"{sequence_id}.npy"), np.array(sequence))
        sequence_id += 1
        print(f"✅ Saved sequence {sequence_id-1}")

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()