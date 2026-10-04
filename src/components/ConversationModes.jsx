import SectionHeader from './SectionHeader.jsx';
import { conversationModes } from '../data/content.js';

export default function ConversationModes() {
  return (
    <section className="section product-section" aria-labelledby="conversation-title">
      <div className="wrap">
        <SectionHeader
          kicker="Conversation scenarios"
          title="Designed for the moments where communication needs to happen now."
        >
          ALLHANDS is framed as an assistive conversation layer: fast enough for live interaction,
          calm enough for sensitive spaces, and structured enough for future model upgrades.
        </SectionHeader>

        <div className="mode-grid">
          {conversationModes.map((mode) => (
            <article className="mode-card" key={mode.title}>
              <span>{mode.label}</span>
              <h3>{mode.title}</h3>
              <p>{mode.body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
