import React, { useState, useRef, useEffect ***REMOVED*** from 'react';
import axios from 'axios';

const MAX_FILE_SIZE = 25 * 1024 * 1024;
const ALLOWED_TYPES = ['audio/mp3', 'audio/wav', 'audio/flac'];

export default function App() {
    const [audioFile, setAudioFile] = useState(null);
    const [result, setResult] = useState(null);
    const [transcript, setTranscript] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [retryMessage, setRetryMessage] = useState('');

    const resultRef = useRef(null);

    useEffect(() => {
        if (resultRef.current && typeof resultRef.current.scrollIntoView === 'function') {
            resultRef.current.scrollIntoView({ behavior: 'smooth' ***REMOVED***);
        ***REMOVED***
    ***REMOVED***, [result]);


    const handleAudioChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!ALLOWED_TYPES.includes(file.type)) {
            alert('Unsupported file type! Please upload a valid audio file.');
            return;
        ***REMOVED***

        if (file.size > MAX_FILE_SIZE) {
            alert('File too large! Max 25MB allowed.');
            return;
        ***REMOVED***

        setAudioFile(file);
        setResult(null);
        setTranscript('');
        setError('');
    ***REMOVED***;

    const postWithRetry = async (url, data, options = {***REMOVED***, retries = 1, delay = 2000) => {
        for (let attempt = 1; attempt <= retries; attempt++) {
            try {
                setRetryMessage(`Attempt ${attempt***REMOVED*** of ${retries***REMOVED***...`);
                const response = await axios.post(url, data, options);
                setRetryMessage('');
                return response;
            ***REMOVED*** catch (error) {
                if (attempt === retries) {
                    setRetryMessage('');
                    throw error;
                ***REMOVED***
                console.warn(`Retrying ${url***REMOVED*** (attempt ${attempt***REMOVED***/${retries***REMOVED***)...`);
                await new Promise((res) => setTimeout(res, delay));
            ***REMOVED***
        ***REMOVED***
    ***REMOVED***;

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!audioFile && !transcript) {
            alert('Please upload an audio file!');
            return;
        ***REMOVED***

        setLoading(true);
        setError('');
        setResult(null);
        setRetryMessage('');

        try {
            let transcriptText = transcript;

            if (!transcriptText) {
                console.info('Uploading audio to backend for transcription...');
                const formData = new FormData();
                formData.append('audio', audioFile);

                const audioResponse = await postWithRetry('http://localhost:5000/process-audio', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' ***REMOVED***,
                ***REMOVED***);

                if (audioResponse.data.error) {
                    throw new Error(audioResponse.data.error);
                ***REMOVED***

                transcriptText = audioResponse.data.transcript;
                setTranscript(transcriptText);
            ***REMOVED***

            console.info('Sending transcript for analysis...');
            const jsonResponse = await postWithRetry('http://localhost:5000/process-json', {
                transcript: transcriptText,
            ***REMOVED***);

            if (jsonResponse.data.error) {
                throw new Error(jsonResponse.data.error);
            ***REMOVED***

            setResult(jsonResponse.data);
        ***REMOVED*** catch (err) {
            console.error('Processing failed:', err);
            setError(err.message || 'Something went wrong while processing the audio.');
        ***REMOVED*** finally {
            setLoading(false);
            setRetryMessage('');
        ***REMOVED***
    ***REMOVED***;

    return (
        <div className="p-6 max-w-xl mx-auto font-sans">
            <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer (AssemblyAI)</h1>

            <form onSubmit={handleSubmit***REMOVED*** className="mb-4">
                <label htmlFor="audio-upload" className="block font-medium mb-1">
                    Upload Audio
                </label>
                <input
                    id="audio-upload"
                    type="file"
                    accept="audio/*"
                    onChange={handleAudioChange***REMOVED***
                    className="w-full p-2 border border-gray-300 rounded mb-2"
                />

                {audioFile && (
                    <p className="text-sm text-gray-600 mt-1">Selected file: {audioFile.name***REMOVED***</p>
                )***REMOVED***

                <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 flex items-center gap-2"
                    disabled={loading***REMOVED***
                >
                    {loading && (
                        <svg
                            className="animate-spin h-4 w-4 text-white duration-1000"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                className="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="4"
                            ></circle>
                            <path
                                className="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                            ></path>
                        </svg>
                    )***REMOVED***
                    {loading ? 'Processing...' : 'Transcribe Audio'***REMOVED***
                </button>

                {retryMessage && (
                    <div className="text-sm text-gray-600 mt-2">{retryMessage***REMOVED***</div>
                )***REMOVED***
            </form>

            {error && (
                <div className="text-red-600 mb-4 flex items-center space-x-4">
                    <div>
                        <strong>Error:</strong> {error***REMOVED***
                    </div>
                    {audioFile && !loading && (
                        <button
                            onClick={handleSubmit***REMOVED***
                            className="text-sm bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded"
                        >
                            Retry
                        </button>
                    )***REMOVED***
                </div>
            )***REMOVED***

            {transcript && (
                <div className="bg-white p-4 border rounded mb-4">
                    <h2 className="font-semibold mb-2">Transcript:</h2>
                    <p className="text-gray-800 whitespace-pre-line text-sm">{transcript***REMOVED***</p>
                </div>
            )***REMOVED***

            <div ref={resultRef***REMOVED***>
                {result && (
                    <div className="bg-gray-50 p-4 border rounded space-y-4">
                        <div>
                            <h2 className="font-semibold">Summary:</h2>
                            {result.summary?.length ? (
                                <ul className="list-disc ml-6 text-sm">
                                    {result.summary.map((s, i) => <li key={i***REMOVED***>{s***REMOVED***</li>)***REMOVED***
                                </ul>
                            ) : (
                                <p className="text-sm text-gray-500 italic">No summary generated.</p>
                            )***REMOVED***
                        </div>
                        <div>
                            <h2 className="font-semibold">Actions:</h2>
                            {result.actions?.length ? (
                                <ul className="list-disc ml-6 text-sm">
                                    {result.actions.map((a, i) => <li key={i***REMOVED***>{a***REMOVED***</li>)***REMOVED***
                                </ul>
                            ) : (
                                <p className="text-sm text-gray-500 italic">No actions detected.</p>
                            )***REMOVED***
                        </div>
                        <div>
                            <h2 className="font-semibold">Decisions:</h2>
                            {result.decisions?.length ? (
                                <ul className="list-disc ml-6 text-sm">
                                    {result.decisions.map((d, i) => <li key={i***REMOVED***>{d***REMOVED***</li>)***REMOVED***
                                </ul>
                            ) : (
                                <p className="text-sm text-gray-500 italic">No decisions found.</p>
                            )***REMOVED***
                        </div>
                    </div>
                )***REMOVED***
            </div>
        </div>
    );
***REMOVED***
