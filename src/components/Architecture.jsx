import SectionHeader from './SectionHeader.jsx';
import { architectureLayers } from '../data/content.js';

export default function Architecture() {
  return (
    <section className="section architecture-section" aria-labelledby="architecture-title">
      <div className="wrap architecture-layout">
        <SectionHeader
          kicker="System architecture"
          title="A clean AI stack your team can actually keep improving."
        >
          The app is split into visible product components and replaceable AI modules, so the prototype can grow
          without becoming a tangled demo file.
        </SectionHeader>

        <div className="architecture-stack">
          {architectureLayers.map((layer, index) => (
            <article className="architecture-row" key={layer.title}>
              <strong>{String(index + 1).padStart(2, '0')}</strong>
              <div>
                <h3>{layer.title}</h3>
                <p>{layer.body}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
