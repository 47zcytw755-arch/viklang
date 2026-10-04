const fallbackConnections = [
  [0, 1], [1, 2], [2, 3], [3, 4],
  [0, 5], [5, 6], [6, 7], [7, 8],
  [5, 9], [9, 10], [10, 11], [11, 12],
  [9, 13], [13, 14], [14, 15], [15, 16],
  [13, 17], [17, 18], [18, 19], [19, 20],
  [0, 17]
];

export function resizeCanvas(canvas, frame) {
  const rect = frame.getBoundingClientRect();
  canvas.width = Math.max(1, Math.round(rect.width));
  canvas.height = Math.max(1, Math.round(rect.height));
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;
  return rect;
}

export function clearCanvas(canvas, context) {
  context.clearRect(0, 0, canvas.width, canvas.height);
}

export function drawHand(canvas, context, landmarks) {
  if (window.drawConnectors && window.drawLandmarks && window.HAND_CONNECTIONS) {
    window.drawConnectors(context, landmarks, window.HAND_CONNECTIONS, {
      color: 'rgba(240, 160, 48, 0.92)',
      lineWidth: 3
    });
    window.drawLandmarks(context, landmarks, {
      color: '#ffffff',
      fillColor: '#f0a030',
      lineWidth: 1,
      radius: 4
    });
    return;
  }

  context.lineWidth = 3;
  context.strokeStyle = 'rgba(240, 160, 48, 0.92)';
  context.beginPath();
  fallbackConnections.forEach(([from, to]) => {
    context.moveTo(landmarks[from].x * canvas.width, landmarks[from].y * canvas.height);
    context.lineTo(landmarks[to].x * canvas.width, landmarks[to].y * canvas.height);
  });
  context.stroke();

  landmarks.forEach((point) => {
    context.beginPath();
    context.arc(point.x * canvas.width, point.y * canvas.height, 4, 0, Math.PI * 2);
    context.fillStyle = '#f0a030';
    context.fill();
    context.strokeStyle = '#ffffff';
    context.lineWidth = 1;
    context.stroke();
  });
}
