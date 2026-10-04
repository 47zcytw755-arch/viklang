export function speakText(text, onStatus = () => {}) {
  if (!text || !('speechSynthesis' in window)) {
    onStatus('Speech unavailable');
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.92;
  utterance.pitch = 1;
  utterance.volume = 1;
  utterance.onstart = () => onStatus('Speaking');
  utterance.onend = () => onStatus('Speech ready');
  utterance.onerror = () => onStatus('Speech blocked');
  window.speechSynthesis.speak(utterance);
}

export function stopSpeech() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}
