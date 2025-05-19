// src/components/TranscriptPanel.jsx
export default function TranscriptPanel({ transcript, onDownload }) {
    if (!transcript || transcript.trim() === '') return null;
    return (
        <div>
            <h2 className="text-lg font-bold mt-4">Transcript:</h2>
            <pre className="whitespace-pre-wrap break-words bg-gray-100 p-2 rounded">
                {transcript}
            </pre>
            <button
                className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                onClick={() => onDownload(transcript, 'transcript.txt')}
            >
                Download Transcript
            </button>
        </div>
    );
}
