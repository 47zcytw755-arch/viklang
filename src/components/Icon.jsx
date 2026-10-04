const paths = {
  hand: <path d="M8 11V6a2 2 0 1 1 4 0v5m0-3V5a2 2 0 1 1 4 0v7m0-3a2 2 0 1 1 4 0v3c0 5-3 8-8 8h-1a7 7 0 0 1-7-7V9a2 2 0 1 1 4 0v4" />,
  scan: <path d="M4 7V5a1 1 0 0 1 1-1h2m10 0h2a1 1 0 0 1 1 1v2M4 17v2a1 1 0 0 0 1 1h2m10 0h2a1 1 0 0 0 1-1v-2M8 12h8M12 8v8" />,
  text: <path d="M4 5h16M6 5v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V5M9 10h6M9 14h4" />,
  wave: <path d="M4 10v4m4-7v10m4-13v16m4-11v6m4-8v10" />,
  bolt: <path d="M13 2 4 14h7l-1 8 10-13h-7l1-7Z" />,
  spark: <path d="M12 3v18M3 12h18M6 6l12 12M18 6 6 18" />,
  caption: <path d="M4 5h16v14H4zM8 9h8M8 13h5" />,
  voice: <path d="M12 3a5 5 0 0 1 5 5v3a5 5 0 0 1-10 0V8a5 5 0 0 1 5-5Zm-7 9a7 7 0 0 0 14 0M12 19v2" />,
  shield: <path d="M12 21s8-4.5 8-11V5l-8-3-8 3v5c0 6.5 8 11 8 11Z" />,
  cpu: <path d="M8 8h8v8H8zM4 9h2m-2 6h2m12-6h2m-2 6h2M9 4v2m6-2v2M9 18v2m6-2v2" />,
  play: <path d="m8 5 11 7-11 7V5Z" fill="currentColor" stroke="none" />,
  arrow: <path d="M5 12h14m-6-6 6 6-6 6" />,
  plus: <path d="M4 12h16M12 4v16" />
};

export default function Icon({ name }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <g stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
        {paths[name]}
      </g>
    </svg>
  );
}
