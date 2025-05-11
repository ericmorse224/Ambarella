import React, { useState ***REMOVED*** from 'react';

function AudioUploader() {
  const [audioFile, setAudioFile] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState([]);
  const [actions, setActions] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
  ***REMOVED***;

  const uploadAudio = async () => {
    if (!audioFile) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
      const res = await fetch('http://localhost:5000/process-audio', {
        method: 'POST',
        body: formData,
      ***REMOVED***);

      const data = await res.json();
      if (data.transcript) {
        setTranscript(data.transcript);
        await summarizeTranscript(data.transcript);
      ***REMOVED*** else {
        alert('Transcription failed');
      ***REMOVED***
    ***REMOVED*** catch (err) {
      console.error(err);
      alert('Upload failed');
    ***REMOVED***

    setLoading(false);
  ***REMOVED***;

  const summarizeTranscript = async (text) => {
    try {
      const res = await fetch('http://localhost:5000/process-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        ***REMOVED***,
        body: JSON.stringify({ transcript: text ***REMOVED***),
      ***REMOVED***);

      const data = await res.json();
      setSummary(data.summary || []);
      setActions(data.actions || []);
      setDecisions(data.decisions || []);
    ***REMOVED*** catch (err) {
      console.error(err);
      alert('Summarization failed');
    ***REMOVED***
  ***REMOVED***;

  return (
    <div>
      <h2>Upload Meeting Audio</h2>
      <input type="file" accept="audio/*" onChange={handleFileChange***REMOVED*** />
      <button onClick={uploadAudio***REMOVED*** disabled={loading***REMOVED***>
        {loading ? 'Processing...' : 'Upload & Transcribe'***REMOVED***
      </button>

      {transcript && (
        <>
          <h3>Transcript</h3>
          <p>{transcript***REMOVED***</p>
        </>
      )***REMOVED***

      {summary.length > 0 && (
        <>
          <h3>Summary</h3>
          <ul>{summary.map((s, i) => <li key={i***REMOVED***>{s***REMOVED***</li>)***REMOVED***</ul>
        </>
      )***REMOVED***

      {actions.length > 0 && (
        <>
          <h3>Action Items</h3>
          <ul>{actions.map((a, i) => <li key={i***REMOVED***>{a***REMOVED***</li>)***REMOVED***</ul>
        </>
      )***REMOVED***

      {decisions.length > 0 && (
        <>
          <h3>Decisions</h3>
          <ul>{decisions.map((d, i) => <li key={i***REMOVED***>{d***REMOVED***</li>)***REMOVED***</ul>
        </>
      )***REMOVED***
    </div>
  );
***REMOVED***

export default AudioUploader;
