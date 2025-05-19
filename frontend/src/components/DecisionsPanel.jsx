// src/components/DecisionsPanel.jsx
export default function DecisionsPanel({ decisions }) {
    if (!decisions.length) return null;
    return (
        <div>
            <h2 className="text-lg font-bold mt-4">Decisions:</h2>
            <ul className="list-disc list-inside text-sm">
                {decisions.map((d, i) => <li key={i}>{d}</li>)}
            </ul>
        </div>
    );
}
