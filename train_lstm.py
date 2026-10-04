# train_lstm_fixed.py
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import joblib
import os
from collections import Counter

print("="*70)
print("🚀 TRAINING LSTM MODEL (Fixed)")
print("="*70)

# Load data
lstm_path = Path("lstm_data")
X = []
y = []

print("📂 Loading data from lstm_data...")

for sign_folder in lstm_path.iterdir():
    if sign_folder.is_dir():
        npy_files = list(sign_folder.glob("*.npy"))
        for npy_file in npy_files:
            sequence = np.load(npy_file)
            X.append(sequence)
            y.append(sign_folder.name)

if not X:
    print("❌ No .npy files found in lstm_data!")
    exit()

X = np.array(X)
y = np.array(y)

print(f"✅ Loaded {len(X)} sequences")
print(f"✅ Number of signs: {len(set(y))}")
print(f"✅ Sequence shape: {X.shape[1:]}")

# Check class distribution
class_counts = Counter(y)
print("\n📊 Class distribution:")
for sign, count in sorted(class_counts.items())[:10]:
    print(f"   {sign}: {count} sequences")
print("   ... (and more)")

# Identify classes with < 2 samples
low_classes = [sign for sign, count in class_counts.items() if count < 2]
if low_classes:
    print(f"\n⚠️ WARNING: {len(low_classes)} signs have only 1 sequence:")
    for sign in low_classes:
        print(f"   - {sign}")
    print("\n💡 These signs will cause issues with stratification.")
    print("   We'll use a simple random split (no stratification).")
    use_stratify = False
else:
    use_stratify = True

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

num_classes = len(label_encoder.classes_)
print(f"\n✅ Number of classes: {num_classes}")

# Split data - choose stratification based on class counts
if use_stratify:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_categorical, test_size=0.2, random_state=42, stratify=y_encoded
    )
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_categorical, test_size=0.2, random_state=42
    )
    print("⚠️ Using non-stratified split due to low class counts.")

print(f"\n📊 Data split:")
print(f"   Training: {len(X_train)} sequences")
print(f"   Testing: {len(X_test)} sequences")

# Build the model
print("\n🏗️ Building LSTM model...")
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(30, 126)),
    Dropout(0.2),
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Train
print("\n🚀 Training started... (this may take a few minutes)")
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

# Evaluate
print("\n📊 Evaluating model...")
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Test Accuracy: {test_accuracy:.2%}")
print(f"✅ Test Loss: {test_loss:.4f}")

# Save model and encoder
model.save('isl_model.h5')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("\n✅ Model saved as 'isl_model.h5'")
print("✅ Label encoder saved as 'label_encoder.pkl'")

# Show sample predictions
print("\n🔍 Sample predictions on test set:")
y_pred = model.predict(X_test, verbose=0)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

sample_indices = np.random.choice(len(X_test), 5, replace=False)
for idx in sample_indices:
    true_label = label_encoder.inverse_transform([y_true_classes[idx]])[0]
    pred_label = label_encoder.inverse_transform([y_pred_classes[idx]])[0]
    confidence = np.max(y_pred[idx])
    print(f"   True: {true_label:15} | Predicted: {pred_label:15} | Confidence: {confidence:.2%}")

# List low-class signs again for manual action
if low_classes:
    print("\n📝 RECOMMENDATION:")
    print("   The following signs have only 1 sequence. For better accuracy,")
    print("   please record 5-10 more sequences for each:")
    for sign in low_classes:
        print(f"      - {sign}")
    print("   After recording, rerun this script.")