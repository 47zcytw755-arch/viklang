import SectionHeader from './SectionHeader.jsx';
import Card from './Card.jsx';
import { features } from '../data/content.js';

export default function Features() {
  return (
    <section className="section" id="features" aria-labelledby="features-title">
      <div className="wrap">
        <SectionHeader
          kicker="Product system"
          title="A maintainable prototype built like a real AI application."
        />
        <div className="features-grid">
          {features.map((feature) => (
            <Card key={feature.title} {...feature} className="feature-card" />
          ))}
        </div>
      </div>
    </section>
  );
}
