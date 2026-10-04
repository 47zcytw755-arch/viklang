import SectionHeader from './SectionHeader.jsx';
import { coverageRows } from '../data/content.js';

export default function Coverage() {
  return (
    <section className="section coverage-section" aria-labelledby="coverage-title">
      <div className="wrap">
        <SectionHeader
          kicker="Recognition coverage"
          title="Honest prototype today, real model path tomorrow."
        >
          Full sign-language conversation requires trained recognition and language modeling. ALLHANDS now exposes
          the roadmap clearly while keeping the current live pipeline usable.
        </SectionHeader>

        <div className="coverage-table">
          {coverageRows.map((row) => (
            <article className="coverage-row" key={row.stage}>
              <span>{row.stage}</span>
              <strong>{row.coverage}</strong>
              <p>{row.detail}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
