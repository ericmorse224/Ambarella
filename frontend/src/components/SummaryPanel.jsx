export default function SummaryPanel({ summary, onDownload }) {
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
