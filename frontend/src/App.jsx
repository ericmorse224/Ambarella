// src/App.jsx
import React, { useState ***REMOVED*** from 'react';
import useMeetingState from './hooks/useMeetingState';
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
    ***REMOVED*** = useMeetingState();

    const handleZohoConnect = async () => {
        setZohoError('');
        try {
            const response = await fetch('/api/auth/zoho');
            const result = await response.json();
            if (result.success) {
                alert('Connected to Zoho!');
            ***REMOVED*** else {
                setZohoError('Error fetching Zoho token');
            ***REMOVED***
        ***REMOVED*** catch (err) {
            setZohoError('Error fetching Zoho token');
        ***REMOVED***
    ***REMOVED***;

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
        if (selectedFile.size > 10 * 1024 * 1024) {
            window.alert('File size exceeds 10MB limit');
            return;
        ***REMOVED***
        if (!selectedFile.type.startsWith('audio/')) {
            window.alert('Unsupported file type! Please upload a valid audio file.');
            return;
        ***REMOVED***
        setFile(selectedFile);
    ***REMOVED***;

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        setScheduleError('');
        setScheduleSuccess('');
        const audioSuccess = await processAudio(file);
        if (audioSuccess) {
            await processTranscript();
        ***REMOVED***
    ***REMOVED***;

    const handleDownload = (content, filename) => {
        const blob = new Blob([content], { type: 'text/plain' ***REMOVED***);
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    ***REMOVED***;

    const handleSchedule = async () => {
        setScheduleError('');
        setScheduleSuccess('');
        try {
            const response = await fetch('/api/schedule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' ***REMOVED***,
                body: JSON.stringify({ actions ***REMOVED***),
            ***REMOVED***);
            const data = await response.json();
            if (response.ok) {
                setScheduleSuccess('Events scheduled successfully');
            ***REMOVED*** else {
                setScheduleError(data.error || 'Error scheduling events');
            ***REMOVED***
        ***REMOVED*** catch (err) {
            setScheduleError('Error scheduling events');
        ***REMOVED***
    ***REMOVED***;

    return (
        <div className="p-6 max-w-xl mx-auto font-sans">
            <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer (AssemblyAI + OpenAI)</h1>

            <button
                onClick={handleZohoConnect***REMOVED***
                className="mb-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
                Connect to Zoho
            </button>

            <form onSubmit={handleSubmit***REMOVED*** className="mb-4">
                <label className="block font-medium mb-1" htmlFor="audio-upload">Upload Audio</label>
                <input
                    id="audio-upload"
                    type="file"
                    accept="audio/*"
                    onChange={handleFileChange***REMOVED***
                    className="w-full p-2 border border-gray-300 rounded mb-2"
                />
                <p className="text-sm text-gray-600 mt-1">
                    Selected file: {file ? file.name : 'None'***REMOVED***
                </p>
                <button
                    type="submit"
                    disabled={isLoading || !file***REMOVED***
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 flex items-center gap-2"
                >
                    {isLoading ? 'Processing...' : 'Transcribe Audio'***REMOVED***
                </button>
                {isLoading && (
                    <div className="text-sm text-gray-600 mt-2">Attempt {uploadAttempts + 1***REMOVED*** of 2...</div>
                )***REMOVED***
            </form>

            {/* Error messages */***REMOVED***
            {zohoError && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {zohoError***REMOVED***
                </p>
            )***REMOVED***
            {error && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {error***REMOVED***
                </p>
            )***REMOVED***
            {scheduleError && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    {scheduleError***REMOVED***
                </p>
            )***REMOVED***
            {scheduleSuccess && (
                <p className="mt-2 text-sm text-center text-green-600" role="status">
                    {scheduleSuccess***REMOVED***
                </p>
            )***REMOVED***

            {transcript && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Transcript:</h2>
                    <p className="whitespace-pre-line text-sm mt-1">{transcript***REMOVED***</p>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => handleDownload(transcript, 'transcript.txt')***REMOVED***
                    >
                        Download Transcript
                    </button>
                </div>
            )***REMOVED***

            {summary.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Summary:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {summary.map((s, i) => <li key={i***REMOVED***>{s***REMOVED***</li>)***REMOVED***
                    </ul>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => handleDownload(summary.join('\n'), 'summary.txt')***REMOVED***
                    >
                        Download Summary
                    </button>
                </div>
            )***REMOVED***

            {decisions.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Decisions:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {decisions.map((d, i) => <li key={i***REMOVED***>{d***REMOVED***</li>)***REMOVED***
                    </ul>
                </div>
            )***REMOVED***

            {actions.length > 0 && (
                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
                    <div className="border rounded p-4 mb-4 space-y-2">
                        <ReviewPanel actions={actions***REMOVED*** setActions={setActions***REMOVED*** />
                    </div>
                    <button
                        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                        onClick={handleSchedule***REMOVED***
                    >
                        Schedule Selected
                    </button>
                </div>
            )***REMOVED***
        </div>
    );
***REMOVED***
