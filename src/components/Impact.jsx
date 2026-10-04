import SectionHeader from './SectionHeader.jsx';
import { metrics } from '../data/content.js';

export default function Impact() {
  return (
    <section className="section impact-band" id="impact" aria-labelledby="impact-title">
      <div className="wrap impact-layout">
        <SectionHeader
          kicker="Impact"
          title="Reducing communication barriers where they matter most."
        >
          Communication barriers affect education, healthcare, employment, and everyday independence.
          ALLHANDS is designed to make in-person conversations more immediate, inclusive, and human.
        </SectionHeader>
        <div className="stats reveal">
          {metrics.map((metric) => (
            <div className="stat" key={metric.value}>
              <strong>{metric.value}</strong>
              <span>{metric.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
