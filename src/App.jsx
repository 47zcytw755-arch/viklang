import { useState, useEffect } from 'react';
import Header from './components/Header.jsx';
import Hero from './components/Hero.jsx';
import CameraDemo from './components/CameraDemo.jsx';
import ConversationModes from './components/ConversationModes.jsx';
import HowItWorks from './components/HowItWorks.jsx';
import Features from './components/Features.jsx';
import Architecture from './components/Architecture.jsx';
import Coverage from './components/Coverage.jsx';
import Impact from './components/Impact.jsx';
import Roadmap from './components/Roadmap.jsx';
import Footer from './components/Footer.jsx';
import { useReveal } from './hooks/useReveal.js';

export default function App() {
  const [route, setRoute] = useState(window.location.hash || '#home');
  useReveal(route);

  useEffect(() => {
    const handleHashChange = () => {
      const currentHash = window.location.hash || '#home';
      setRoute(currentHash);
      
      // Instantly scroll to top when changing pages
      window.scrollTo(0, 0);
    };

    window.addEventListener('hashchange', handleHashChange);
    
    // Normalize initial routing
    if (!window.location.hash) {
      window.location.hash = '#home';
    }

    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  return (
    <>

      <Header currentHash={route} />
      <main id="top" className="page-transition">
        {route === '#home' && (
          <>
            <Hero />
            <CameraDemo />
          </>
        )}
        {route === '#features' && (
          <>
            <HowItWorks />
            <Features />
            <ConversationModes />
          </>
        )}
        {route === '#architecture' && (
          <Architecture />
        )}
        {route === '#mission' && (
          <>
            <Impact />
            <Coverage />
            <Roadmap />
          </>
        )}
      </main>
      <Footer currentHash={route} />
    </>
  );
}
