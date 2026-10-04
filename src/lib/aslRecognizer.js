export function normalizeGestureResult(gestureResults, modelId = 'gesture') {
  if (!gestureResults) return null;
  const gestures   = gestureResults.gestures;
  const handedness = gestureResults.handednesses;
  if (!gestures || gestures.length === 0 || gestures[0].length === 0) return null;

  const top        = gestures[0][0];
  const score      = handedness?.[0]?.[0]?.score ?? 1;
  const rawName    = top.categoryName;
  const confidence = Math.min(top.score * score, 0.98);

  if (confidence < 0.45 || !rawName || rawName === 'None') return null;

  const phraseMap = {
    'Open_Palm':   'Hello',
    'Thumb_Up':    'Yes',
    'Thumb_Down':  'No',
    'Victory':     'Peace/V',
    'ILoveYou':    'I Love You',
    'Pointing_Up': 'Up/One',
    'Closed_Fist': 'A',
  };

  const isPhrase = rawName in phraseMap;
  const value    = isPhrase ? phraseMap[rawName] : rawName.toUpperCase();
  if (!value) return null;

  return {
    value,
    confidence,
    type:    isPhrase ? 'phrase' : 'letter',
    display: isPhrase ? value : `ASL ${value}`
  };
}

export const SIGN_SETS = {
  gesture: [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'Hello','Yes','No','Peace/V','I Love You','Up/One'
  ],
  fingerspelling: ['Spell any word — H·E·L·P → "help"'],
  custom: ['Depends on your model']
};
