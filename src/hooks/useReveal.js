import { useEffect } from 'react';

export function useReveal(route) {
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.12 }
    );

    // Small delay to let React render the new page DOM
    const timer = setTimeout(() => {
      const elements = document.querySelectorAll('.reveal, .card, .roadmap-item');
      elements.forEach((element, index) => {
        element.style.transitionDelay = `${Math.min(index * 40, 240)}ms`;
        observer.observe(element);
      });
    }, 60);

    return () => {
      clearTimeout(timer);
      observer.disconnect();
    };
  }, [route]);
}
