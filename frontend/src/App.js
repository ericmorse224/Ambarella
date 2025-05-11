import React, { useState ***REMOVED*** from 'react';
import axios from 'axios';

export default function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [result, setResult] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  console.log('App.js is loaded!');

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 25 * 1024 * 1024) {
      alert('File too large! Max 25MB allowed.');
      return;
    ***REMOVED***

    setAudioFile(file);
    setResult(null);
    setTranscript('');
    setError('');
  ***REMOVED***;

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!audioFile) {
      alert('Please upload an audio file!');
      return;
    ***REMOVED***

    const formData = new FormData();
    formData.append('audio', audioFile);

    setLoading(true);
    setError('');
    setResult(null);
    setTranscript('');

    try {
      console.info('Uploading audio to backend for transcription...');
      const audioResponse = await axios.post('http://localhost:5000/process-audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        ***REMOVED***,
      ***REMOVED***);

      if (audioResponse.data.error) {
        throw new Error(audioResponse.data.error);
      ***REMOVED***

      const transcriptText = audioResponse.data.transcript;
      setTranscript(transcriptText);

      console.info('Sending transcript for analysis...');
      const jsonResponse = await axios.post('http://localhost:5000/process-json', {
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
    ***REMOVED***
  ***REMOVED***;

  return (
    <div className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer (AssemblyAI)</h1>

      <form onSubmit={handleSubmit***REMOVED*** className="mb-4">
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioChange***REMOVED***
          className="w-full p-2 border border-gray-300 rounded mb-2"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading***REMOVED***
        >
          {loading ? 'Processing...' : 'Transcribe Audio'***REMOVED***
        </button>
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

      {result && (
        <div className="bg-gray-50 p-4 border rounded space-y-4">
          <div>
            <h2 className="font-semibold">Summary:</h2>
            <ul className="list-disc ml-6 text-sm">
              {result.summary?.map((s, i) => <li key={i***REMOVED***>{s***REMOVED***</li>)***REMOVED***
            </ul>
          </div>
          <div>
            <h2 className="font-semibold">Actions:</h2>
            <ul className="list-disc ml-6 text-sm">
              {result.actions?.map((a, i) => <li key={i***REMOVED***>{a***REMOVED***</li>)***REMOVED***
            </ul>
          </div>
          <div>
            <h2 className="font-semibold">Decisions:</h2>
            <ul className="list-disc ml-6 text-sm">
              {result.decisions?.map((d, i) => <li key={i***REMOVED***>{d***REMOVED***</li>)***REMOVED***
            </ul>
          </div>
        </div>
      )***REMOVED***
    </div>
  );
***REMOVED***
