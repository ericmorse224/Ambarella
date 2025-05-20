/**
 * TranscriptPanel.jsx
 * 
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 *   This component displays the transcript section in the AI Meeting Summarizer app.
 *   It shows a formatted transcript and provides a button to download the transcript as a text file.
 *   If no transcript is provided, this panel renders nothing.
 * 
 * Props:
 *   - transcript (string): The transcript text to display.
 *   - onDownload (function): Callback function called when the user clicks the download button.
 *                            Receives the transcript text and file name as arguments.
 * 
 * Usage:
 *   <TranscriptPanel transcript={transcriptText} onDownload={handleDownload} />
 */

export default function TranscriptPanel({ transcript, onDownload }) {
    // Do not render if transcript is missing or blank
    if (!transcript || transcript.trim() === '') return null;
    return (
        <div>
            <h2 className="text-lg font-bold mt-4 dark:text-white">
                Transcript:
            </h2>
            <pre className="whitespace-pre-wrap break-words bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-100 p-2 rounded">
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
