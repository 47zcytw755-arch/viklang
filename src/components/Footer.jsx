export default function Footer({ currentHash }) {
  return (
    <footer className="footer">
      <div className="footer-grid">
        <div>
          <a className="brand" href="#home" aria-label="ALLHANDS home">
            <span className="brand-mark" aria-hidden="true">A</span>
            ALLHANDS
          </a>
          <p>AI-powered accessibility for real-time sign language communication.</p>
        </div>
        <nav className="footer-links" aria-label="Footer navigation">
          <a href="#mission">About</a>
          <a href="mailto:hello@allhands.ai">Contact</a>
          <a href="#mission">Roadmap</a>
          <a href="#features">Accessibility</a>
          <a href="#home">Home</a>
          <a href="#home">Privacy</a>
        </nav>
      </div>
    </footer>
  );
}
