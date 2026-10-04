import Icon from './Icon.jsx';
import { useHeaderScroll } from '../hooks/useHeaderScroll.js';

export default function Header({ currentHash }) {
  const isScrolled = useHeaderScroll();

  return (
    <header className={`site-header ${isScrolled ? 'scrolled' : ''}`}>
      <nav className="nav" aria-label="Primary navigation">
        <a className="brand" href="#home" aria-label="ALLHANDS home">
          <span className="brand-mark" aria-hidden="true">A</span>
          ALLHANDS
        </a>
        <div className="nav-links">
          <a href="#home" className={currentHash === '#home' ? 'active' : ''}>Home</a>
          <a href="#features" className={currentHash === '#features' ? 'active' : ''}>Features</a>
          <a href="#architecture" className={currentHash === '#architecture' ? 'active' : ''}>Tech</a>
          <a href="#mission" className={currentHash === '#mission' ? 'active' : ''}>Our Mission</a>
          <a className="nav-cta" href="#home">
            <Icon name="arrow" />
            Launch Camera
          </a>
        </div>
      </nav>
    </header>
  );
}
