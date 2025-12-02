export default function PreviewPanels() {
  return (
    <section className="pp" aria-label="Previews">
      <div className="pp-left" aria-label="Top API Matches">
        <div className="pp-header">Top API Matches</div>
        <ul className="pp-list">
          <li className="pp-item">Result card placeholder #1</li>
          <li className="pp-item">Result card placeholder #2</li>
          <li className="pp-item">Result card placeholder #3</li>
        </ul>
      </div>

      <div className="pp-right" aria-label="Code Snippet">
        <div className="pp-header">Code Snippet</div>
        <pre className="pp-code">
{`// example (placeholder)
fetch("https://api.example.com/endpoint?city=Seattle", {
  headers: { "x-api-key": "YOUR_KEY" }
}).then(r => r.json());`}
        </pre>
      </div>
    </section>
  );
}