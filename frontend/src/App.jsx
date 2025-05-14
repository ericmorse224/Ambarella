import React, { useState, useEffect ***REMOVED*** from 'react';
import axios from 'axios';
import ReviewPanel from './components/ReviewPanel';

function App() {
    const [file, setFile] = useState(null);
    const [transcript, setTranscript] = useState('');
    const [summary, setSummary] = useState([]);
    const [actions, setActions] = useState([]);
    const [decisions, setDecisions] = useState([]);
    const [status, setStatus] = useState('idle');
    const [error, setError] = useState('');
    const [attempt, setAttempt] = useState(0);
    const [processing, setProcessing] = useState(false);

    const downloadTextFile = (filename, content) => {
        const blob = new Blob([content], { type: 'text/plain' ***REMOVED***);
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    ***REMOVED***;

    const handleFileChange = (e) => {
        const uploaded = e.target.files[0];
        if (!uploaded) return;
        if (uploaded.size > 25 * 1024 * 1024) {
            alert('File too large! Max 25MB allowed.');
            return;
        ***REMOVED***
        if (!uploaded.type.startsWith('audio/')) {
            alert('Unsupported file type! Please upload a valid audio file.');
            return;
        ***REMOVED***
        setFile(uploaded);
        setError('');
    ***REMOVED***;

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        setStatus('processing');
        setTranscript('');
        setSummary([]);
        setActions([]);
        setDecisions([]);
        setProcessing(true);
        setError('');
        setAttempt(1);

        const formData = new FormData();
        formData.append('audio', file);

        let success = false;
        try {
            const { data: audioRes ***REMOVED*** = await axios.post('http://localhost:5000/process-audio', formData);
            const { data: nlpRes ***REMOVED*** = await axios.post('http://localhost:5000/process-json', {
                transcript: audioRes.transcript,
                entities: audioRes.entities || [],
            ***REMOVED***);
            setTranscript(audioRes.transcript);
            setSummary(nlpRes.summary);
            setActions(nlpRes.actions);
            setDecisions(nlpRes.decisions);
            success = true;
        ***REMOVED*** catch (err) {
            console.error(err);
            setError(err.message || 'Failed to process.');
        ***REMOVED***
        setProcessing(false);
    ***REMOVED***;

    return (
        <div className="p-6 max-w-xl mx-auto font-sans">
            <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer (AssemblyAI + OpenAI)</h1>
            <button
                onClick={async () => {
                    try {
                        const res = await axios.get('http://localhost:5000/auth-url');
                        if (res.data.url) {
                            window.location.href = res.data.url;
                        ***REMOVED***
                    ***REMOVED*** catch (err) {
                        console.error("Zoho auth failed", err);
                        alert("Failed to connect to Zoho.");
                    ***REMOVED***
                ***REMOVED******REMOVED***
                className="mb-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
                Connect to Zoho
            </button>

            <form onSubmit={handleSubmit***REMOVED*** className="mb-4">
                <label htmlFor="audio-upload" className="block font-medium mb-1">
                    Upload Audio
                </label>
                <input
                    type="file"
                    accept="audio/*"
                    id="audio-upload"
                    onChange={handleFileChange***REMOVED***
                    className="w-full p-2 border border-gray-300 rounded mb-2"
                />
                {file && <p className="text-sm text-gray-600 mt-1">Selected file: {file.name***REMOVED***</p>***REMOVED***
                <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 flex items-center gap-2"
                    disabled={status === 'processing'***REMOVED***
                >
                    {status === 'processing' ? 'Processing...' : 'Transcribe Audio'***REMOVED***
                </button>
                {status === 'processing' && attempt > 0 && (
                    <div className="text-sm text-gray-600 mt-2">Attempt {attempt***REMOVED*** of 2...</div>
                )***REMOVED***
            </form>

            {error && (
                <div role="alert" className="text-red-600 font-semibold mt-2">
                    {error***REMOVED***
                </div>
            )***REMOVED***

            {transcript && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Transcript:</h2>
                    <p className="whitespace-pre-line text-sm mt-1">{transcript***REMOVED***</p>
                </div>
            )***REMOVED***
            {transcript && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Transcript:</h2>
                    <p className="whitespace-pre-line text-sm mt-1">{transcript***REMOVED***</p>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => downloadTextFile('transcript.txt', transcript)***REMOVED***
                    >
                        Download Transcript
                    </button>
                </div>
            )***REMOVED***

            {summary.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Summary:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {summary.map((item, i) => (
                            <li key={i***REMOVED***>{item***REMOVED***</li>
                        ))***REMOVED***
                    </ul>
                </div>
            )***REMOVED***
            {summary.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Summary:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {summary.map((item, i) => <li key={i***REMOVED***>{item***REMOVED***</li>)***REMOVED***
                    </ul>
                    <button
                        className="mt-2 bg-gray-700 text-white px-3 py-1 rounded"
                        onClick={() => downloadTextFile('summary.txt', summary.join('\\n'))***REMOVED***
                    >
                        Download Summary
                    </button>
                </div>
            )***REMOVED***

            {decisions.length > 0 && (
                <div>
                    <h2 className="text-lg font-bold mt-4">Decisions:</h2>
                    <ul className="list-disc list-inside text-sm">
                        {decisions.map((item, i) => (
                            <li key={i***REMOVED***>{item***REMOVED***</li>
                        ))***REMOVED***
                    </ul>
                </div>
            )***REMOVED***
            {actions.length > 0 && (
                <ReviewPanel
                    actions={actions***REMOVED***
                    onSubmit={async (filteredItems) => {
                        try {
                            const res = await axios.post('http://localhost:5000/create-event', {
                                events: filteredItems,
                            ***REMOVED***);
                            alert('Events scheduled successfully!');
                        ***REMOVED*** catch (err) {
                            alert('Failed to schedule events.');
                            console.error(err);
                        ***REMOVED***
                    ***REMOVED******REMOVED***
                />
            )***REMOVED***
        </div>
    );
***REMOVED***

export default App;
