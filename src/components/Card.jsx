import Icon from './Icon.jsx';

export default function Card({ icon, title, body, className = '' }) {
  return (
    <article className={`card ${className}`}>
      <div className="icon-box">
        <Icon name={icon} />
      </div>
      <h3>{title}</h3>
      <p>{body}</p>
    </article>
  );
}
