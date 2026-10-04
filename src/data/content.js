export const processSteps = [
  {
    icon: 'hand',
    title: 'User signs',
    body: 'A signer communicates naturally in front of the camera with no special hardware.'
  },
  {
    icon: 'scan',
    title: 'AI vision detection',
    body: 'MediaPipe extracts hand landmarks and the recognition layer interprets shape and motion.'
  },
  {
    icon: 'text',
    title: 'Conversation translation',
    body: 'Stable detections become transcript entries that can be reviewed, spoken, or copied.'
  },
  {
    icon: 'wave',
    title: 'Speech output',
    body: 'The browser voice engine speaks recognized phrases in real time for face-to-face conversation.'
  }
];

export const features = [
  {
    icon: 'bolt',
    title: 'Real-time camera pipeline',
    body: 'Native webcam access starts first, then the AI layer attaches when the hand model is ready.'
  },
  {
    icon: 'spark',
    title: 'Expandable ASL recognizer',
    body: 'A starter rule engine handles common handshapes and can be replaced by a trained model.'
  },
  {
    icon: 'caption',
    title: 'Live transcript',
    body: 'Recognized signs are saved as a readable conversation stream instead of disappearing.'
  },
  {
    icon: 'voice',
    title: 'Audio output',
    body: 'Text is spoken aloud using browser speech synthesis with repeat and clear controls.'
  },
  {
    icon: 'shield',
    title: 'Privacy-first prototype',
    body: 'Camera frames are processed in the browser for this demo; no video is uploaded by default.'
  },
  {
    icon: 'cpu',
    title: 'Model-ready architecture',
    body: 'The AI module is isolated in src/lib so a dataset-trained recognizer can be plugged in later.'
  },
  {
    icon: 'scan',
    title: 'Confidence-aware UI',
    body: 'Detections include confidence feedback so the app can avoid speaking uncertain signs too quickly.'
  },
  {
    icon: 'text',
    title: 'Correction-ready transcript',
    body: 'The transcript surface is prepared for future edit, delete, confirmation, and phrase repair controls.'
  },
  {
    icon: 'hand',
    title: 'In-person conversation mode',
    body: 'The camera cockpit is optimized for a signer standing in front of a listener in real time.'
  }
];

export const conversationModes = [
  {
    label: 'Face-to-face',
    title: 'Live conversation assist',
    body: 'A signer stands in front of the camera while ALLHANDS builds a spoken response stream for the listener.'
  },
  {
    label: 'Classroom',
    title: 'Education support',
    body: 'Teachers and classmates can follow recognized signs as text and audio during learning sessions.'
  },
  {
    label: 'Healthcare',
    title: 'High-clarity moments',
    body: 'A privacy-first interface can help reduce communication friction during appointments and intake.'
  },
  {
    label: 'Public services',
    title: 'Accessible front desks',
    body: 'Kiosks, help desks, and service counters can use the same pipeline for quick assisted conversations.'
  }
];

export const architectureLayers = [
  {
    title: 'Camera stream',
    body: 'Secure browser camera access starts immediately and keeps the live preview visible even if the AI model is still loading.'
  },
  {
    title: 'Landmark engine',
    body: 'MediaPipe Hands converts each frame into 21 hand landmarks that are stable enough for shape and motion analysis.'
  },
  {
    title: 'Recognition layer',
    body: 'The current rules engine recognizes a starter sign set. The file boundary is ready for a TensorFlow or ONNX model later.'
  },
  {
    title: 'Conversation layer',
    body: 'Stable detections become transcript entries, spoken output, correction opportunities, and future phrase-level context.'
  }
];

export const coverageRows = [
  {
    stage: 'Now',
    coverage: 'Starter static signs plus simple motion',
    detail: 'A, B, C, D, I, L, O, V, Y, Hello, Yes'
  },
  {
    stage: 'Next',
    coverage: 'Alphabet and common phrase pack',
    detail: 'More letters, numbers, greetings, needs, emotions, directions'
  },
  {
    stage: 'Model',
    coverage: 'Continuous ASL classifier',
    detail: 'Dataset-trained recognition across signer variation, speed, angle, and lighting'
  },
  {
    stage: 'Conversation',
    coverage: 'Full assisted dialogue',
    detail: 'Phrase segmentation, intent repair, confidence prompts, and voice synthesis'
  }
];

export const metrics = [
  { value: '70M+', label: 'people worldwide use sign language to communicate.' },
  { value: '300+', label: 'sign languages exist across global communities.' },
  { value: '<1s', label: 'target response time for real-time assistive conversation.' }
];

export const roadmap = [
  {
    time: 'Prototype',
    title: 'Live landmark recognizer',
    body: 'Current app supports camera input, hand landmarks, starter ASL rules, transcript, and speech.',
    tag: 'Now'
  },
  {
    time: 'Model',
    title: 'Dataset-trained ASL classifier',
    body: 'Replace the rule engine with a real trained model for larger vocabulary and signer variation.',
    tag: 'Next'
  },
  {
    time: 'Conversation',
    title: 'Phrase and grammar engine',
    body: 'Move beyond letters into continuous sign-language phrases, context, correction, and intent.',
    tag: 'Soon'
  },
  {
    time: 'Platform',
    title: 'Mobile and smart glasses',
    body: 'Bring ALLHANDS to everyday communication, classrooms, meetings, healthcare, and public services.',
    tag: 'Vision'
  }
];
