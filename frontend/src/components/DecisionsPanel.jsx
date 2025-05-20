/**
 * @file DecisionsPanel.jsx
 * @author Eric Morse
 * @date May 11th, 2025
 * @description
 *   This React component displays a list of meeting decisions as a styled panel.
 *   It renders nothing if the decisions array is empty.
 *
 * @param {Object} props
 * @param {string[]} props.decisions - An array of decision strings to display in the list.
 * @returns {JSX.Element|null} Returns a styled decisions panel or null if no decisions.
 */

export default function DecisionsPanel({ decisions }) {
    // If no decisions provided, do not render anything.
    if (!decisions.length) return null;
    // Render the panel with each decision as a list item.
    return (
        <div>
            <h2 className="text-lg font-bold mt-4">Decisions:</h2>
            <ul className="list-disc list-inside text-sm">
                {decisions.map((d, i) => <li key={i}>{d}</li>)}
            </ul>
        </div>
    );
}
