import cv2
import mediapipe as mp

# -----------------------
# MediaPipe Setup
# -----------------------

mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    refine_face_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------
# Webcam
# -----------------------

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = holistic.process(rgb)

    # -----------------------
    # Face Mesh
    # -----------------------

    if results.face_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_draw.DrawingSpec(
                color=(0, 255, 255),
                thickness=1,
                circle_radius=1
            )
        )

        cv2.putText(
            frame,
            "FACE DETECTED",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    # -----------------------
    # Left Hand
    # -----------------------

    if results.left_hand_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            mp_draw.DrawingSpec(
                color=(0, 255, 0),
                thickness=2,
                circle_radius=2
            ),
            mp_draw.DrawingSpec(
                color=(0, 200, 255),
                thickness=2,
                circle_radius=2
            )
        )

        cv2.putText(
            frame,
            "LEFT HAND",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # -----------------------
    # Right Hand
    # -----------------------

    if results.right_hand_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            mp_draw.DrawingSpec(
                color=(255, 0, 0),
                thickness=2,
                circle_radius=2
            ),
            mp_draw.DrawingSpec(
                color=(255, 255, 0),
                thickness=2,
                circle_radius=2
            )
        )

        cv2.putText(
            frame,
            "RIGHT HAND",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

    # -----------------------
    # Landmark Counts
    # -----------------------

    face_count = 0
    left_count = 0
    right_count = 0

    if results.face_landmarks:
        face_count = len(results.face_landmarks.landmark)

    if results.left_hand_landmarks:
        left_count = len(results.left_hand_landmarks.landmark)

    if results.right_hand_landmarks:
        right_count = len(results.right_hand_landmarks.landmark)

    cv2.putText(
        frame,
        f"Face: {face_count}",
        (10, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Left Hand: {left_count}",
        (10, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Right Hand: {right_count}",
        (10, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow("SignSpeak Holistic Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()