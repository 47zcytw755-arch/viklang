const GESTURE_CDN = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm';
const DEFAULT_MODEL = 'https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task';

let recognizer = null;
let currentModelId = null;

export async function createGestureRecognizer(modelUrl = null) {
  try {
    const vision = await import('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/+esm');
    const { GestureRecognizer, FilesetResolver } = vision;
    const fileset = await FilesetResolver.forVisionTasks(GESTURE_CDN);

    recognizer = await GestureRecognizer.createFromOptions(fileset, {
      baseOptions: {
        modelAssetPath: modelUrl || DEFAULT_MODEL,
        delegate: 'GPU'
      },
      runningMode: 'VIDEO',
      numHands: 1,
      minHandDetectionConfidence: 0.6,
      minHandPresenceConfidence: 0.6,
      minTrackingConfidence: 0.5
    });

    return recognizer;
  } catch (err) {
    console.error('GestureRecognizer init failed:', err);
    return null;
  }
}

export async function switchModel(modelId, customUrl = null) {
  if (currentModelId === modelId && modelId !== 'custom') return recognizer;
  if (recognizer) { try { recognizer.close(); } catch (_) {} recognizer = null; }
  const url = modelId === 'custom' ? customUrl : null;
  recognizer = await createGestureRecognizer(url);
  currentModelId = modelId;
  return recognizer;
}

export function runGestureOnFrame(video, lastVideoTime) {
  if (!recognizer || !video) return null;
  if (video.currentTime === lastVideoTime) return null;
  return { results: recognizer.recognizeForVideo(video, performance.now()), time: video.currentTime };
}

export function closeRecognizer() {
  if (recognizer) { try { recognizer.close(); } catch (_) {} recognizer = null; currentModelId = null; }
}
