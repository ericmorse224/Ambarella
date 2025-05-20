/**
 * SummaryPanel.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 *   This React component renders a summary section for meeting summaries.
 *   - Displays a list of summary points (bulleted).
 *   - Provides a button to download the summary as a text file.
 * 
 * Props:
 *   - summary (Array of string): The summary items to display.
 *   - onDownload (function): Handler for downloading the summary. 
 *     Called with the joined summary text and filename when download is clicked.
 * 
 * Usage:
 *   <SummaryPanel summary={['Point 1', 'Point 2']} onDownload={handleDownload} />
 * 
 * If the summary array is empty, the component renders nothing.
 */
export default function SummaryPanel({ summary, onDownload }) {
    // If there are no summary items, render nothing
    if (!summary.length) return null;
    return (
        <div>
            <h2 className="text-lg font-bold mt-4 dark:text-white">
                Summary:
            </h2>
            <ul className="list-disc list-inside text-sm dark:text-gray-100">
                {summary.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
            <button
                className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                onClick={() => onDownload(summary.join('\n'), 'summary.txt')}
            >
                Download Summary
            </button>
        </div>
    );
}
