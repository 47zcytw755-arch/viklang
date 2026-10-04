# collect_more_data.py
import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ---- LIST OF SIGNS WITH <15 SEQUENCES ----
SIGNS_TO_RECORD = [
    # 1-2 sequences
    "blue", "brown", "cat", "daughter", "fish", "green",
    "mother", "parent", "son", "yellow",
    # 3-5 sequences
    "doctor", "friday", "hour", "lawyer", "minute", "month",
    "patient", "saturday", "secretary", "student", "sunday",
    "thursday", "today", "tomorrow", "tuesday", "waiter",
    "wednesday", "week", "yesterday", "colours", "people",
    # 7 sequences
    "attack", "bag", "bathroom", "bed", "bedroom", "bill",
    "book", "box", "card", "chair", "door", "dream", "energy",
    "gift", "gun", "key", "kitchen", "letter", "lock", "marriage",
    "medicine", "money", "newspaper", "page", "paper", "peace",
    "pencil", "photograph", "race_ethnicity", "religion", "ring",
    "soap", "table", "team", "technology", "telephone", "tool", "war"
]

# Remove duplicates (if any)
SIGNS_TO_RECORD = list(set(SIGNS_TO_RECORD))
print(f"📋 Total signs to record: {len(SIGNS_TO_RECORD)}")

# ---- MediaPipe Setup ----
# Try different import methods (works with newer MediaPipe)
try:
    from mediapipe.python.solutions import holistic as mp_holistic
    from mediapipe.python.solutions import drawing_utils as mp_draw
    print("✅ Using mediapipe.python.solutions import")
except ImportError:
    # Fallback to standard import
    import mediapipe as mp
    mp_holistic = mp.solutions.holistic
    mp_draw = mp.solutions.drawing_utils
    print("✅ Using mp.solutions import")

# ---- Helper Functions ----
def extract_features(results):
    """Extract hand landmarks into a flat list (126 features)."""
    features = []
    # Left hand
    if results.left_hand_landmarks:
        for lm in results.left_hand_landmarks.landmark:
            features.extend([lm.x, lm.y, lm.z])
    else:
        features.extend([0.0] * 63)
    # Right hand
    if results.right_hand_landmarks:
        for lm in results.right_hand_landmarks.landmark:
            features.extend([lm.x, lm.y, lm.z])
    else:
        features.extend([0.0] * 63)
    return features

def record_sequences(gesture, num_sequences=30):
    """Record 'num_sequences' sequences for the given gesture."""
    save_dir = os.path.join("lstm_data", gesture)
    os.makedirs(save_dir, exist_ok=True)

    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not found!")
        return

    # Start from the next available sequence ID
    existing = [f for f in os.listdir(save_dir) if f.endswith('.npy')]
    sequence_id = len(existing)
    print(f"📂 {gesture}: already has {sequence_id} sequences.")

    print(f"🎬 Recording '{gesture}' – aim for {num_sequences} new sequences.")
    print("Press 'S' to record, 'Q' to finish this sign.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)

        # Draw landmarks
        if results.left_hand_landmarks:
            mp_draw.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        if results.right_hand_landmarks:
            mp_draw.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Display info
        cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Sequences saved: {sequence_id}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        cv2.putText(frame, "Press S to record, Q to quit", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
        cv2.imshow("Record Gestures", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            # Countdown
            for t in range(3, 0, -1):
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                cv2.putText(frame, str(t), (250, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 8)
                cv2.imshow("Record Gestures", frame)
                cv2.waitKey(1000)

            # Record 30 frames
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
                cv2.putText(frame, f"Recording {i+1}/30", (150, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
                cv2.imshow("Record Gestures", frame)
                cv2.waitKey(1)

            # Save .npy
            npy_path = os.path.join(save_dir, f"{sequence_id}.npy")
            np.save(npy_path, np.array(sequence))
            sequence_id += 1
            print(f"✅ Saved {npy_path}")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    holistic.close()
    print(f"✅ Finished '{gesture}'. Total sequences now: {sequence_id}\n")

# ---- Main Loop ----
def main():
    print("="*60)
    print("📹 DATA COLLECTION FOR LOW-COUNT SIGNS")
    print(f"Total signs to record: {len(SIGNS_TO_RECORD)}")
    print("For each sign, record at least 20-30 sequences.")
    print("Press 'S' to record, 'Q' to move to next sign.")
    print("="*60)

    for gesture in SIGNS_TO_RECORD:
        print(f"\n--- Next: {gesture} ---")
        input("Press Enter to start recording (or Ctrl+C to skip)...")
        record_sequences(gesture, num_sequences=30)

    print("\n🎉 All signs recorded! Your dataset is now larger.")

if __name__ == "__main__":
    main()