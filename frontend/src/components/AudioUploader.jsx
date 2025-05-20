/**
 * File: AudioUploader.jsx
 * Date: May 11th, 2025
 * Author: Eric Morse
 * Description:
 *   - React component to upload, transcribe, and summarize meeting audio files.
 *   - Handles file selection, size validation, server upload, error messaging, and result rendering.
 *   - Communicates with backend endpoints for transcription and NLP processing.
 */

import React, { useState } from 'react';

/**
 * AudioUploader component
 * Provides a UI for uploading an audio file, transcribing it, and displaying summary, actions, and decisions.
 */
function AudioUploader() {
    // React state hooks for managing UI and data.
    const [audioFile, setAudioFile] = useState(null);        // Selected file
    const [transcript, setTranscript] = useState('');        // Transcript result
    const [summary, setSummary] = useState([]);              // Summary array
    const [actions, setActions] = useState([]);              // Action items
    const [decisions, setDecisions] = useState([]);          // Decisions
    const [loading, setLoading] = useState(false);           // Loading state
    const [error, setError] = useState('');                  // Error message

    /**
     * Handler for file input changes.
     * Sets the audioFile state and clears any previous errors.
     * @param {Event} e - File input change event
     */
    const handleFileChange = (e) => {
        setAudioFile(e.target.files[0]);
        setError('');
    };

    /**
     * Uploads the selected audio file to the backend for transcription.
     * Handles file size validation, displays errors, and updates state.
     * On success, triggers summarization of the transcript.
     */
    const uploadAudio = async () => {
        setError('');
        if (!audioFile) return;
        // Validate file size (max 25MB)
        if (audioFile.size > 25 * 1024 * 1024) {
            setError("File too large. Max is 25MB");
            window.alert("File too large. Max is 25MB");
            return;
        }
        setLoading(true);
        const formData = new FormData();
        formData.append('audio', audioFile);

        try {
            const res = await fetch('http://localhost:5000/process-audio', {
                method: 'POST',
                body: formData,
            });

            // Check for server error (non-2xx)
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                const message = errData.error || "Transcription failed (server error)";
                setError(message);
                window.alert(message);
                setLoading(false);
                return;
            }

            const data = await res.json();
            if (data.transcript) {
                setTranscript(data.transcript);
                await summarizeTranscript(data.transcript);
            } else {
                const message = data.error || 'Transcription failed';
                setError(message);
                window.alert(message);
            }
        } catch (err) {
            setError('Upload failed.');
            window.alert("Upload failed.");
        }
        setLoading(false);
    };

    /**
     * Sends transcript text to the backend for summarization and entity extraction.
     * Updates summary, actions, and decisions states.
     * @param {string} text - Transcript to summarize
     */
    const summarizeTranscript = async (text) => {
        if (!text || typeof text !== "string" || !text.trim()) {
            setError("Transcript is missing or invalid.");
            window.alert("Transcript is missing or invalid.");
            return;
        }
        try {
            const res = await fetch('http://localhost:5000/process-json', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript: text }),
            });
            const data = await res.json();
            setSummary(data.summary || []);
            setActions(data.actions || []);
            setDecisions(data.decisions || []);
        } catch (err) {
            setError('Summarization failed');
            window.alert("Summarization failed");
        }
    };

    // Render the uploader UI and results
    return (
        <div className="p-4 max-w-2xl mx-auto space-y-6">
            <h2 className="text-xl font-semibold">Upload Meeting Audio</h2>
            <label htmlFor="audio-upload" className="block font-medium mb-1">
                Upload Audio
            </label>
            <input
                id="audio-upload"
                name="audio"
                type="file"
                accept="audio/*"
                onChange={handleFileChange}
                className="border p-2 rounded w-full"
            />

            {/* Upload & Transcribe button */}
            <button
                onClick={uploadAudio}
                disabled={loading}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                {loading ? 'Processing...' : 'Upload & Transcribe'}
            </button>

            {/* Error Message */}
            {error && (
                <p className="mt-2 text-red-600 text-center" role="alert">
                    {error}
                </p>
            )}

            {/* Transcript Section */}
            {transcript && (
                <section>
                    <h3 className="text-lg font-medium mt-4">Transcript</h3>
                    <p className="whitespace-pre-wrap">{transcript}</p>
                </section>
            )}

            {/* Summary Section */}
            {summary?.length > 0 && (
                <section>
                    <h3 className="text-lg font-medium mt-4">Summary</h3>
                    <ul className="list-disc ml-5">
                        {summary.map((s, i) => (
                            <li key={i}>{s}</li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Action Items Section */}
            {actions?.length > 0 && (
                <section>
                    <h3 className="text-lg font-medium mt-4">Action Items</h3>
                    <ul className="list-disc ml-5">
                        {actions.map((a, i) => (
                            <li key={i}>{a}</li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Decisions Section */}
            {decisions?.length > 0 && (
                <section>
                    <h3 className="text-lg font-medium mt-4">Decisions</h3>
                    <ul className="list-disc ml-5">
                        {decisions.map((d, i) => (
                            <li key={i}>{d}</li>
                        ))}
                    </ul>
                </section>
            )}
        </div>
    );
}

export default AudioUploader;
