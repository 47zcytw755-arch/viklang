import { useState, useEffect } from 'react';
import SectionHeader from './SectionHeader.jsx';
import ModelSwitcher from './ModelSwitcher.jsx';

export default function CameraDemo() {
  const [activeModelId, setActiveModelId] = useState('gesture');
  const [isLive, setIsLive] = useState(false);
  const [isSwitching, setIsSwitching] = useState(false);
  
  // Simulated state
  const [cameraStatus, setCameraStatus] = useState('Camera offline (Demo mode)');
  const [modelStatus, setModelStatus] = useState('No model loaded');
  const [helper, setHelper] = useState('Backend disabled. Click Start Demo to see a simulation.');
  const [detected, setDetected] = useState(null);
  const [transcript, setTranscript] = useState([]);
  const [aiSentence, setAiSentence] = useState('');
  const [aiStatus, setAiStatus] = useState('');

  const handleSwitch = (modelId) => {
    setActiveModelId(modelId);
    setIsSwitching(true);
    setTimeout(() => {
      setIsSwitching(false);
      if (isLive) {
        setModelStatus(`${modelId} model live`);
      }
    }, 600);
  };

  const startDemo = () => {
    setIsLive(true);
    setCameraStatus('Simulation running');
    setModelStatus(`${activeModelId} model live`);
    setHelper('Simulating sign detection in real-time...');
    setTranscript([]);
    setAiSentence('');
    setAiStatus('Waiting for signs...');
  };

  const clearTranscript = () => {
    setTranscript([]);
    setAiSentence('');
    setDetected(null);
    setAiStatus('Waiting for signs...');
  };

  // Run a fake simulation sequence when live
  useEffect(() => {
    if (!isLive) return;
    
    const sequence = [
      { text: 'HELLO', wait: 1500 },
      { text: 'WORLD', wait: 3000 },
      { text: 'HOW', wait: 4500 },
      { text: 'ARE', wait: 5500 },
      { text: 'YOU', wait: 6500 },
      { ai: 'Hello world, how are you today?', wait: 8000 }
    ];
    
    const timeouts = sequence.map(item => {
      return setTimeout(() => {
        if (item.text) {
          setDetected({ display: 'Detected sign', value: item.text, confidence: 0.95 });
          setTranscript(prev => [...prev, { 
            id: Math.random(), 
            text: item.text, 
            confidence: 0.95, 
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
          }]);
        }
        if (item.ai) {
          setDetected(null);
          setAiStatus('AI thinking...');
          setTimeout(() => {
            setAiSentence(item.ai);
            setAiStatus('AI translated successfully');
            setHelper('Simulation complete. Try clicking Reset to run again.');
          }, 800);
        }
      }, item.wait);
    });
    
    return () => timeouts.forEach(clearTimeout);
  }, [isLive]);

  const rawText = transcript.length
    ? transcript.map(i => i.text).join(' ')
    : 'Show me some signs to get started!';

  return (
    <section className="section camera-section" id="demo" aria-labelledby="demo-title">
      <div className="wrap">
        <SectionHeader
          kicker="Let's sign together!"
          title="Let's translate your hands into natural speech."
        >
          Select a gesture model, wake up the camera, and start signing! ALLHANDS will read your hand movements
          and translate them into full, natural English sentences that are spoken out loud.
        </SectionHeader>

        <div className="model-switcher-row">
          <ModelSwitcher
            activeId={activeModelId}
            onSwitch={handleSwitch}
            isSwitching={isSwitching}
            isLive={isLive}
          />
        </div>

        <div className="camera-stage">
          <div className={`camera-frame ${isLive ? 'live' : ''}`}>
            
            {/* Fake video background */}
            <div className="camera-video" style={{ 
              backgroundColor: '#13151b', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              width: '100%',
              height: '100%'
            }}>
              {isLive ? (
                <div style={{ color: 'rgba(240,160,48,0.4)', fontSize: '1.2rem', animation: 'pulse 2s infinite' }}>
                  [ Simulating Camera Feed ]
                </div>
              ) : null}
            </div>

            {!isLive && (
              <div className="ai-empty">
                <div>
                  <div className="companion-avatar" aria-hidden="true" style={{ fontSize: '3.5rem', marginBottom: '1.2rem', animation: 'float 3s ease-in-out infinite' }}>👋</div>
                  <strong>I'm ready to simulate!</strong>
                  Backend processing is currently disabled. Click "Start Demo" to see a simulated UI walk-through of the detection process.
                </div>
              </div>
            )}

            <div className="scanline" aria-hidden="true" />
            <div className="camera-topbar">
              <span className="status-pill">
                <span className="pulse-dot" aria-hidden="true" />
                {cameraStatus}
              </span>
              <span className="status-pill">{modelStatus}</span>
            </div>

            <span className="corner c1" aria-hidden="true" />
            <span className="corner c2" aria-hidden="true" />
            <span className="corner c3" aria-hidden="true" />
            <span className="corner c4" aria-hidden="true" />

            <aside className="model-note">
              <strong>Signs I know</strong>
              <span>A · B · C · D · E · F · G · H · I · J · K · L …</span>
            </aside>

            <aside className="translation-panel" aria-label="Live translation output">
              <div className="translation-label">
                <span>{detected?.display || 'What I see'}</span>
                <span>{detected ? `${Math.round(detected.confidence * 100)}%` : '--'}</span>
              </div>
              <div className="translation-text" aria-live="polite">
                {detected?.value || 'Show me a sign! ✋'}
              </div>
              <p className="translation-helper">{helper}</p>

              <div className="sentence-output" aria-live="polite">{rawText}</div>

              <div className="ai-sentence-panel">
                <div className="ai-sentence-label">
                  <span>✦ AI Translated Sentence</span>
                  <span className="ai-status-tag">{aiStatus || 'waiting for signs…'}</span>
                </div>
                <div className="ai-sentence-text" aria-live="polite">
                  {aiSentence || 'Sign 3 gestures, and I\'ll stitch them into a human sentence here.'}
                </div>
              </div>

              <div className="transcript-list" aria-label="Recent transcript">
                <span>Words recorded</span>
                {transcript.length ? (
                  transcript.slice(-4).map(item => (
                    <div className="transcript-item" key={item.id}>
                      <strong>{item.text}</strong>
                      <em>{item.time} / {Math.round(item.confidence * 100)}%</em>
                    </div>
                  ))
                ) : <p>No signs captured yet.</p>}
              </div>

              <div className="speech-row">
                <div className="wave" aria-hidden="true">
                  {Array.from({ length: 10 }).map((_, i) => <span key={i} />)}
                </div>
                <span className="confidence">Speech muted in demo</span>
              </div>

              <div className="control-row">
                <button className="ai-button" type="button" onClick={startDemo}
                  disabled={isLive}>
                  {isLive ? 'Simulation Live' : 'Start Demo'}
                </button>
                <button className="ai-button secondary" type="button" disabled={true}>Translate Now</button>
                <button className="ai-button secondary" type="button" disabled={true}>Speak Sentence</button>
                <button className="ai-button secondary" type="button" disabled={true}>Speak Words</button>
                <button className="ai-button secondary" type="button" disabled={true}>Copy Text</button>
                <button className="ai-button secondary" type="button" onClick={clearTranscript}
                  disabled={!transcript.length && !aiSentence}>Reset</button>
              </div>
            </aside>
          </div>
        </div>
      </div>
    </section>
  );
}
