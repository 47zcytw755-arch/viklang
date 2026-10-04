import { useRef, useState } from 'react';
import { MODEL_REGISTRY } from '../lib/modelRegistry.js';
import { SIGN_SETS } from '../lib/aslRecognizer.js';

export default function ModelSwitcher({ activeId, onSwitch, isSwitching, isLive }) {
  const [open, setOpen]           = useState(false);
  const [customName, setCustomName] = useState('');
  const fileRef                   = useRef(null);

  const active = MODEL_REGISTRY.find(m => m.id === activeId) ?? MODEL_REGISTRY[0];

  const handleSelect = async (model) => {
    if (model.id === activeId) { setOpen(false); return; }
    if (model.id === 'custom') { fileRef.current?.click(); return; }
    setOpen(false);
    onSwitch(model.id, null);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setCustomName(file.name);
    setOpen(false);
    onSwitch('custom', url);
    e.target.value = '';
  };

  return (
    <div className="model-switcher">
      <button
        className="model-switcher-btn"
        onClick={() => setOpen(o => !o)}
        disabled={isSwitching}
        title="Switch recognition model"
      >
        <span className="model-switcher-icon">⚙</span>
        <span className="model-switcher-label">
          {isSwitching ? 'Switching…' : active.name}
        </span>
        <span className={`model-switcher-badge badge-${active.id}`}>
          {active.badge}
        </span>
        <span className="model-switcher-arrow">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="model-dropdown">
          <div className="model-dropdown-header">Choose Recognition Model</div>
          {MODEL_REGISTRY.map(model => (
            <button
              key={model.id}
              className={`model-option ${model.id === activeId ? 'active' : ''}`}
              onClick={() => handleSelect(model)}
            >
              <div className="model-option-top">
                <span className="model-option-name">{model.name}</span>
                <span className={`model-option-badge badge-${model.id}`}>{model.badge}</span>
              </div>
              <div className="model-option-desc">{model.description}</div>
              {model.id === 'custom' && customName && (
                <div className="model-option-file">📄 {customName}</div>
              )}
            </button>
          ))}

          <div className="model-dropdown-signs">
            <strong>Signs in this model:</strong>
            <span>{(SIGN_SETS[activeId] ?? SIGN_SETS.gesture).join(' · ')}</span>
          </div>

          {!isLive && (
            <div className="model-dropdown-note">
              ⚠ Start camera first to switch models live
            </div>
          )}
        </div>
      )}

      {/* hidden file input for custom model upload */}
      <input
        ref={fileRef}
        type="file"
        accept=".task,.tflite,.onnx"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </div>
  );
}
