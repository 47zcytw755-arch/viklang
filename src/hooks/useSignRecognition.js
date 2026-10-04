import { useCallback, useEffect, useRef, useState } from 'react';
import { normalizeGestureResult } from '../lib/aslRecognizer.js';
import { createGestureRecognizer, switchModel, runGestureOnFrame, closeRecognizer } from '../lib/mediaPipe.js';
import { speakText, stopSpeech } from '../lib/speech.js';
import { buildSentence } from '../lib/sentenceBuilder.js';
import { drawHand, clearCanvas } from '../lib/handDrawing.js';

const STABLE_FRAMES   = 14;
const REPEAT_COOLDOWN = 3000;
const AI_EVERY_N      = 3;

export function useSignRecognition(activeModelId = 'gesture') {
  const videoRef       = useRef(null);
  const canvasRef      = useRef(null);
  const frameRef       = useRef(null);
  const recognizerRef  = useRef(null);
  const streamRef      = useRef(null);
  const loopRef        = useRef(null);
  const candidateRef   = useRef({ sign: null, frames: 0 });
  const lastCommitRef  = useRef({ sign: null, at: 0 });
  const lastVideoTime  = useRef(-1);
  const detectedRef    = useRef(null);
  const signsBufferRef = useRef([]);
  const aiCountRef     = useRef(0);
  const modelIdRef     = useRef(activeModelId);

  const [isLive,        setIsLive]        = useState(false);
  const [isStarting,    setIsStarting]    = useState(false);
  const [isSwitching,   setIsSwitching]   = useState(false);
  const [cameraStatus,  setCameraStatus]  = useState('Camera idle');
  const [modelStatus,   setModelStatus]   = useState('No model loaded');
  const [helper,        setHelper]        = useState('Press Start and allow camera access.');
  const [detected,      setDetected]      = useState(null);
  const [transcript,    setTranscript]    = useState([]);
  const [speechStatus,  setSpeechStatus]  = useState('Speech ready');
  const [aiSentence,    setAiSentence]    = useState('');
  const [aiStatus,      setAiStatus]      = useState('');

  const publishDetected = useCallback((next) => {
    const prev = detectedRef.current;
    if (!prev && !next) return;
    if (prev && next && prev.value === next.value &&
        Math.abs(prev.confidence - next.confidence) < 0.03) return;
    detectedRef.current = next;
    setDetected(next);
  }, []);

  const resize = useCallback(() => {
    const c = canvasRef.current, f = frameRef.current;
    if (c && f) { c.width = f.offsetWidth; c.height = f.offsetHeight; }
  }, []);

  const triggerAI = useCallback(async (signs) => {
    if (!signs.length) return;
    setAiStatus('AI thinking…');
    const sentence = await buildSentence(signs);
    if (sentence) { setAiSentence(sentence); setAiStatus('AI ready'); speakText(sentence, setSpeechStatus); }
    else setAiStatus('AI unavailable');
  }, []);

  const commitSign = useCallback((result) => {
    const now = Date.now(), last = lastCommitRef.current;
    if (result.value === last.sign && now - last.at < REPEAT_COOLDOWN) return;
    const entry = { id: `${now}-${result.value}`, text: result.value,
      confidence: result.confidence,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setTranscript(items => [...items, entry]);
    lastCommitRef.current = { sign: result.value, at: now };
    speakText(result.type === 'letter' ? `Letter ${result.value}` : result.value, setSpeechStatus);
    signsBufferRef.current.push(result.value);
    aiCountRef.current += 1;
    if (aiCountRef.current >= AI_EVERY_N) {
      aiCountRef.current = 0;
      triggerAI([...signsBufferRef.current]);
    }
  }, [triggerAI]);

  const startLoop = useCallback(() => {
    if (loopRef.current) cancelAnimationFrame(loopRef.current);
    const run = () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (video && video.readyState >= 2 && recognizerRef.current) {
        const out = runGestureOnFrame(video, lastVideoTime.current);
        if (out) {
          lastVideoTime.current = out.time;
          
          if (canvas) {
            const ctx = canvas.getContext('2d');
            clearCanvas(canvas, ctx);
            if (out.results.landmarks) {
              out.results.landmarks.forEach(l => drawHand(canvas, ctx, l));
            }
          }

          const result = normalizeGestureResult(out.results, modelIdRef.current);
          if (!result) {
            candidateRef.current = { sign: null, frames: 0 };
            publishDetected(null);
            setCameraStatus('Searching');
            setHelper('Place your hand in the frame and hold an ASL sign.');
          } else {
            publishDetected(result);
            setCameraStatus('Detecting');
            setHelper('Hold steady ~1 s to commit. Every 3 signs → AI builds a sentence.');
            if (candidateRef.current.sign === result.value) candidateRef.current.frames += 1;
            else candidateRef.current = { sign: result.value, frames: 1 };
            if (candidateRef.current.frames === STABLE_FRAMES) commitSign(result);
          }
        }
      }
      loopRef.current = requestAnimationFrame(run);
    };
    loopRef.current = requestAnimationFrame(run);
  }, [commitSign, publishDetected]);

  // ── Switch model while live ───────────────────────────────────────────────
  const handleModelSwitch = useCallback(async (modelId, customUrl = null) => {
    if (!isLive) { modelIdRef.current = modelId; return; }
    setIsSwitching(true);
    setModelStatus(`Loading ${modelId} model…`);
    if (loopRef.current) { cancelAnimationFrame(loopRef.current); loopRef.current = null; }
    try {
      const rec = await switchModel(modelId, customUrl);
      if (rec) {
        recognizerRef.current = rec;
        modelIdRef.current    = modelId;
        candidateRef.current  = { sign: null, frames: 0 };
        lastVideoTime.current = -1;
        setModelStatus(`${modelId} model live`);
        setCameraStatus('AI running');
        startLoop();
      } else {
        setModelStatus('Model failed — using previous');
      }
    } catch (err) {
      console.error(err);
      setModelStatus('Switch failed');
    } finally {
      setIsSwitching(false);
    }
  }, [isLive, startLoop]);

  const start = useCallback(async () => {
    setIsStarting(true);
    setCameraStatus('Starting');
    setHelper('Requesting camera…');
    try {
      if (!streamRef.current) {
        streamRef.current = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false
        });
      }
      videoRef.current.srcObject = streamRef.current;
      await videoRef.current.play();
      setIsLive(true); resize();
    } catch (err) {
      setIsLive(false);
      setCameraStatus(err.name === 'NotFoundError' ? 'No camera found' : 'Camera blocked');
      setHelper('Allow camera access then try again.');
      setIsStarting(false); return;
    }
    setCameraStatus('Loading model…');
    setHelper('Downloading model (first run ~25 MB)…');
    try {
      let rec;
      if (modelIdRef.current === 'gesture') {
        rec = await createGestureRecognizer();
      } else {
        rec = await switchModel(modelIdRef.current);
      }
      
      if (rec) {
        recognizerRef.current = rec;
        setModelStatus(modelIdRef.current === 'gesture' ? 'Gesture Recognizer – A to Z live' : `${modelIdRef.current} model live`);
        setCameraStatus('AI running');
        setHelper('Full A–Z ASL active. Hold any sign ~1 s to capture it.');
        startLoop();
      } else {
        setModelStatus('Model failed — check internet');
        setHelper('Refresh and try again.');
      }
    } catch (err) {
      console.error(err); setModelStatus('Model error');
    } finally { setIsStarting(false); }
  }, [resize, startLoop]);

  const speakTranscript = useCallback(() =>
    speakText(transcript.map(i => i.text).join(' '), setSpeechStatus), [transcript]);
  const speakAiSentence = useCallback(() =>
    { if (aiSentence) speakText(aiSentence, setSpeechStatus); }, [aiSentence]);
  const buildAiNow = useCallback(() =>
    triggerAI(transcript.map(i => i.text)), [transcript, triggerAI]);
  const copyTranscript = useCallback(async () => {
    const text = aiSentence || transcript.map(i => i.text).join(' ');
    if (text && navigator.clipboard) { await navigator.clipboard.writeText(text); setSpeechStatus('Copied'); }
  }, [transcript, aiSentence]);
  const clearTranscript = useCallback(() => {
    stopSpeech(); setTranscript([]); setAiSentence(''); setAiStatus('');
    signsBufferRef.current = []; aiCountRef.current = 0;
    detectedRef.current = null; setDetected(null); setSpeechStatus('Speech ready');
    candidateRef.current = { sign: null, frames: 0 };
    lastCommitRef.current = { sign: null, at: 0 };
  }, []);

  useEffect(() => {
    window.addEventListener('resize', resize);
    return () => {
      window.removeEventListener('resize', resize);
      if (loopRef.current) cancelAnimationFrame(loopRef.current);
      streamRef.current?.getTracks().forEach(t => t.stop());
      stopSpeech(); closeRecognizer();
    };
  }, [resize]);

  return {
    videoRef, canvasRef, frameRef,
    isLive, isStarting, isSwitching,
    cameraStatus, modelStatus, helper,
    detected, transcript, speechStatus,
    aiSentence, aiStatus,
    start, handleModelSwitch,
    speakTranscript, speakAiSentence,
    buildAiNow, copyTranscript, clearTranscript
  };
}
