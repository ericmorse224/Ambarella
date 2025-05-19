import React, { useState } from 'react';
import useMeetingState from './hooks/UseMeetingState';
import NextcloudConnect from './components/NextcloudConnect';
import AudioUploadForm from './components/AudioUploadForm';
import TranscriptPanel from './components/TranscriptPanel';
import SummaryPanel from './components/SummaryPanel';
import DecisionsPanel from './components/DecisionsPanel';
import ReviewPanel from './components/ReviewPanel';

export default function App() {
    const [file, setFile] = useState(null);
    const [scheduleError, setScheduleError] = useState('');
    const [scheduleSuccess, setScheduleSuccess] = useState('');
    const {
        transcript, summary, actions, decisions,
        isLoading, uploadAttempts, processAudio,
        processTranscript, setActions, error
    } = useMeetingState();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;
        if (selectedFile.size > 25 * 1024 * 1024) {
            window.alert('File size exceeds 25MB limit');
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
        setScheduleError('');
        setScheduleSuccess('');
        if (file) {
            const audioSuccess = await processAudio(file);
            if (audioSuccess) await processTranscript();
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
            const response = await fetch('http://localhost:5000/schedule', {
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
            <NextcloudConnect />
            <AudioUploadForm
                file={file}
                onFileChange={handleFileChange}
                onSubmit={handleSubmit}
                isLoading={isLoading}
                uploadAttempts={uploadAttempts}
            />
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
            <TranscriptPanel transcript={transcript} onDownload={handleDownload} />
            <SummaryPanel summary={summary} onDownload={handleDownload} />
            <DecisionsPanel decisions={decisions} />
            {actions.length > 0 && (
                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
                    <div className="border rounded p-4 mb-4 space-y-2">
                        <ReviewPanel actions={actions} setActions={setActions} />
                    </div>
                    <button
                        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                        onClick={handleSchedule}
                        data-testid="schedule-actions"
                    >
                        Schedule Selected
                    </button>

                </div>
            )}
        </div>
    );
}
