// Central registry of all available models.
// To add a new model: add an entry here. Nothing else needs changing.

export const MODEL_REGISTRY = [
  {
    id: 'gesture',
    name: 'MediaPipe Gesture',
    description: 'A–Z alphabet + 6 phrases. Best for static letter signs.',
    badge: 'Built-in',
    type: 'gesture',          // uses GestureRecognizer API
    modelUrl: null,           // uses default MediaPipe hosted model
    supportedSigns: [
      'A','B','C','D','E','F','G','H','I','J','K','L','M',
      'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
      'Hello','Yes','No','Peace/V','I Love You','Up/One'
    ]
  },
  {
    id: 'fingerspelling',
    name: 'Kaggle Fingerspelling',
    description: 'Continuous word spelling — reads full words as you sign letters in motion.',
    badge: 'Advanced',
    type: 'gesture',
    // Uses same GestureRecognizer but tuned for continuous input via AI post-processing
    modelUrl: null,
    supportedSigns: ['Any word spelled letter by letter in ASL']
  },
  {
    id: 'custom',
    name: 'Custom Model',
    description: 'Load your own .task file trained in MediaPipe Studio.',
    badge: 'Custom',
    type: 'custom',
    modelUrl: null,           // set dynamically by user file upload
    supportedSigns: ['Depends on your training data']
  }
];

export function getModel(id) {
  return MODEL_REGISTRY.find(m => m.id === id) ?? MODEL_REGISTRY[0];
}
