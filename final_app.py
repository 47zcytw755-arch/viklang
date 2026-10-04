import cv2
import mediapipe as mp
import pyttsx3
import threading
import numpy as np
import pickle
from openai import OpenAI

# --- API Setup ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# --- Load ISL Model ---
with open("isl_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5
)

# --- Emotion Detection using Face Mesh ---
def detect_emotion(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(frame_rgb)

    if not result.multi_face_landmarks:
        return "neutral"

    landmarks = result.multi_face_landmarks[0].landmark

    # Key points
    left_mouth  = landmarks[61]
    right_mouth = landmarks[291]
    top_lip     = landmarks[13]
    bottom_lip  = landmarks[14]
    left_eye_top    = landmarks[159]
    left_eye_bottom = landmarks[145]
    left_brow   = landmarks[70]
    left_eye_center = landmarks[33]

    mouth_width = abs(right_mouth.x - left_mouth.x)
    mouth_open  = abs(bottom_lip.y - top_lip.y)
    eye_open    = abs(left_eye_top.y - left_eye_bottom.y)
    brow_height = abs(left_brow.y - left_eye_center.y)

    # Emotion rules
    if mouth_width > 0.45 and mouth_open < 0.02:
        return "happy"
    elif mouth_open > 0.05:
        return "surprised"
    elif brow_height < 0.02:
        return "angry"
    elif eye_open < 0.008:
        return "sad"
    else:
        return "neutral"

# --- Emotion Display ---
emotion_hindi = {
    "happy":     "Khush 😊",
    "sad":       "Udaas 😢",
    "angry":     "Gussa 😠",
    "surprised": "Hairaan 😲",
    "neutral":   "Theek hai 😐"
}

emotion_colors = {
    "happy":     (0, 255, 0),
    "sad":       (255, 100, 100),
    "angry":     (0, 0, 255),
    "surprised": (0, 255, 255),
    "neutral":   (200, 200, 200)
}

# --- ISL to Hindi ---
isl_to_speech = {
    "namaste":  "Namaste",
    "help":     "Mujhe madad chahiye",
    "water":    "Mujhe paani chahiye",
    "food":     "Mujhe khana chahiye",
    "yes":      "Haan",
    "no":       "Nahi",
    "pain":     "Mujhe dard ho raha hai",
    "toilet":   "Mujhe bathroom jaana hai",
    "thankyou": "Dhanyavaad",
    "please":   "Kripya"
}

# --- TTS ---
is_speaking = False

def speak(text):
    global is_speaking
    if is_speaking:
        return
    def run():
        global is_speaking
        is_speaking = True
        eng = pyttsx3.init()
        eng.setProperty('rate', 150)
        eng.setProperty('volume', 1.0)
        eng.say(text)
        eng.runAndWait()
        eng.stop()
        is_speaking = False
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# --- AI Sentence Generator ---
ai_sentence = ""

def generate_ai_sentence(gesture, emotion):
    global ai_sentence
    def run():
        global ai_sentence
        try:
            prompt = f"""A mute person just made the ISL sign for "{gesture}".
Their face shows they feel "{emotion}".
Write one natural Hindi sentence combining both.
Maximum 10 words. Reply with ONLY the Hindi sentence."""
            response = client.chat.completions.create(
                model="openrouter/owl-alpha",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60
            )
            ai_sentence = response.choices[0].message.content.strip()
            print(f"AI: {ai_sentence}")
        except:
            ai_sentence = isl_to_speech.get(gesture, gesture)
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# --- Gesture Prediction ---
def predict_gesture(hand_landmarks):
    landmarks = []
    for lm in hand_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])
    data = np.array(landmarks).reshape(1, -1)
    prediction = model.predict(data)
    confidence = max(model.predict_proba(data)[0])
    gesture = le.inverse_transform(prediction)[0]
    if confidence > 0.80:
        return gesture, confidence
    return "", 0.0

# --- Main Loop ---
cap = cv2.VideoCapture(0)
gesture = ""
last_gesture = ""
frame_count = 0
confidence_score = 0.0
current_emotion = "neutral"
last_spoken = ""
emotion_frame = 0

print("✅ SignSpeak Started!")
print("Show ISL gesture to camera")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # --- Hand Detection ---
    hand_result = hands.process(frame_rgb)

    if hand_result.multi_hand_landmarks:
        for hand in hand_result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS)
            detected, confidence_score = predict_gesture(hand)
            if detected:
                gesture = detected
    else:
        gesture = ""
        frame_count = 0
        last_gesture = ""

    # --- Emotion Detection every 15 frames ---
    emotion_frame += 1
    if emotion_frame % 15 == 0:
        current_emotion = detect_emotion(frame)

    # --- Speak on gesture hold ---
    if gesture == last_gesture and gesture != "":
        frame_count += 1
        if frame_count == 30:
            speech_text = isl_to_speech.get(gesture, gesture)
            speak(speech_text)
            if gesture != last_spoken:
                generate_ai_sentence(gesture, current_emotion)
                last_spoken = gesture
    else:
        frame_count = 0
        last_gesture = gesture

    # --- UI ---
    cv2.rectangle(frame, (0, 0), (640, 210), (15, 15, 15), -1)

    # Gesture name
    display = gesture.upper() if gesture else "No hand detected"
    cv2.putText(frame, display, (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                (0, 255, 0) if gesture else (100, 100, 100), 3)

    # Hindi translation
    if gesture and gesture in isl_to_speech:
        cv2.putText(frame, isl_to_speech[gesture], (10, 88),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2)

    # Emotion
    emo_color = emotion_colors.get(current_emotion, (200, 200, 200))
    emo_hindi = emotion_hindi.get(current_emotion, current_emotion)
    cv2.putText(frame, f"Mood: {emo_hindi}", (10, 128),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, emo_color, 2)

    # AI sentence
    if ai_sentence:
        cv2.putText(frame, f"AI: {ai_sentence}", (10, 165),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 165, 0), 1)

    # Confidence
    if confidence_score > 0:
        cv2.putText(frame, f"Confidence: {confidence_score*100:.1f}%",
                    (10, 190), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (150, 150, 150), 1)

    # Progress bar
    if gesture != "":
        bar_width = int((frame_count / 30) * 300)
        cv2.rectangle(frame, (10, 198), (310, 208), (50, 50, 50), -1)
        cv2.rectangle(frame, (10, 198), (10 + bar_width, 208),
                      (0, 255, 0), -1)

    cv2.imshow("SignSpeak - ISL + Emotion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()