import SectionHeader from './SectionHeader.jsx';
import Card from './Card.jsx';
import { processSteps } from '../data/content.js';

export default function HowItWorks() {
  return (
    <section className="section" id="how" aria-labelledby="how-title">
      <div className="wrap">
        <SectionHeader kicker="How it works" title="From natural signing to spoken conversation." />
        <div className="flow">
          {processSteps.map((step) => (
            <Card key={step.title} {...step} />
          ))}
        </div>
      </div>
    </section>
  );
}
