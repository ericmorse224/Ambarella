// src/App.jsx
import React, { useState } from 'react';
import useMeetingState from './hooks/UseMeetingState';
import ReviewPanel from './components/ReviewPanel';
export default function App() {
    const [file, setFile] = useState(null);
    const [zohoError, setZohoError] = useState('');
    const [scheduleError, setScheduleError] = useState('');
    const [scheduleSuccess, setScheduleSuccess] = useState('');
    const {
        transcript,
        summary,
        actions,
        decisions,
        isLoading,
        uploadAttempts,
        processAudio,
        processTranscript,
        setTranscript,
        setActions,
        error, // from useMeetingState, for audio/transcript errors
    } = useMeetingState();

    const handleZohoConnect = async () => {
        setZohoError('');
        try {
            const response = await fetch('/api/zoho-token');
            const result = await response.json();
            if (response.ok && result.access_token) {
                alert('Connected to Zoho!');
            } else {
                console.error("Zoho token error:", result);
                setZohoError(result.message || 'Error fetching Zoho token');
            }
        } catch (err) {
            console.error("Fetch error:", err);
            setZohoError('Error fetching Zoho token');
        }
    };


    const handleFileChange = (e) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;
        if (selectedFile.size > 10 * 1024 * 1024) {
            window.alert('File size exceeds 10MB limit');
            return;
        }
        if (!selectedFile.type.startsWith('audio/')) {
            window.alert('Unsupported file type! Please upload a valid audio file.');
            return;
        }
        setFile(selectedFile);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        setScheduleError('');
        setScheduleSuccess('');
        const audioSuccess = await processAudio(file);
        if (audioSuccess) {
            await processTranscript();
        }
    };

    const handleDownload = (content, filename) => {
        const blob = new Blob([content], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    };

    const handleSchedule = async () => {
        setScheduleError('');
        setScheduleSuccess('');
        try {
            const response = await fetch('/api/schedule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ actions }),
            });
            const data = await response.json();
            if (response.ok) {
                setScheduleSuccess('Events scheduled successfully');
            } else {
                setScheduleError(data.error || 'Error scheduling events');
            }
        } catch (err) {
            setScheduleError('Error scheduling events');
        }
    };

    return (
        <div className="p-6 max-w-xl mx-auto font-sans">
            <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer (AssemblyAI + OpenAI)</h1>

            <button
                onClick={handleZohoConnect}
                className="mb-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
                Connect to Zoho
            </button>

            <form onSubmit={handleSubmit} className="mb-4">
                <label className="block font-medium mb-1" htmlFor="audio-upload">Upload Audio</label>
                <input
                    data-testid="audio-upload"
                    id="audio-upload"
                    type="file"
                    accept="audio/*"
                    onChange={handleFileChange}
                    className="w-full p-2 border border-gray-300 rounded mb-2"
                />
                <p className="text-sm text-gray-600 mt-1">
                    Selected file: {file ? file.name : 'None'}
                </p>
                <button
                    type="submit"
                    disabled={isLoading || !file} // disable if loading OR no file selected!
                    aria-label="Transcribe Audio"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                >
                    {isLoading ? (
                        <span>
                            <span className="sr-only">Transcribe Audio</span>
                            Processing...
                        </span>
                    ) : (
                        'Transcribe Audio'
                    )}
                </button>

                {isLoading && (
                    <div className="text-sm text-gray-600 mt-2">Attempt {uploadAttempts + 1} of 2...</div>
                )}
            </form>

            {/* Error messages */}
            {zohoError && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {zohoError}
                </p>
            )}

            {error && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {error}
                </p>
            )}
            {scheduleError && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {scheduleError}
                </p>
            )}
            {scheduleSuccess && (
                <p className="mt-2 text-sm text-center text-green-600" role="status">
                    {scheduleSuccess}
                </p>
            )}

            {transcript && transcript.trim() != '' && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Transcript:</h2>
                    <pre className="whitespace-pre-wrap break-words bg-gray-100 p-2 rounded">
                        {transcript}
                    </pre>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => handleDownload(transcript, 'transcript.txt')}
                    >
                        Download Transcript
                    </button>
                </div>
            )}


            {summary.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Summary:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {summary.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => handleDownload(summary.join('\n'), 'summary.txt')}
                    >
                        Download Summary
                    </button>
                </div>
            )}

            {decisions.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Decisions:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {decisions.map((d, i) => <li key={i}>{d}</li>)}
                    </ul>
                </div>
            )}

            {actions.length > 0 && (
                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
                    <div className="border rounded p-4 mb-4 space-y-2">
                        <ReviewPanel actions={actions} setActions={setActions} />
                    </div>
                    <button
                        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                        onClick={handleSchedule}
                    >
                        Schedule Selected
                    </button>
                </div>
            )}
        </div>
    );
}

