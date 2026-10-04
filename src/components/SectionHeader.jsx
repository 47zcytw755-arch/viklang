export default function SectionHeader({ kicker, title, children }) {
  return (
    <div className="reveal section-head">
      <p className="section-kicker">{kicker}</p>
      <h2 className="section-title">{title}</h2>
      {children ? <p className="section-copy">{children}</p> : null}
    </div>
  );
}
