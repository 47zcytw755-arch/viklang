import SectionHeader from './SectionHeader.jsx';
import { roadmap } from '../data/content.js';

export default function Roadmap() {
  return (
    <section className="section" id="roadmap" aria-labelledby="roadmap-title">
      <div className="wrap">
        <SectionHeader
          kicker="Future vision"
          title="A clear path from prototype to real assistive platform."
        />
        <div className="roadmap">
          {roadmap.map((item) => (
            <article className="roadmap-item" key={item.title}>
              <span className="roadmap-time">{item.time}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </div>
              <span className="tag">{item.tag}</span>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
