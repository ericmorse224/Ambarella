import React, { useState } from 'react';

function AudioUploader() {
  const [audioFile, setAudioFile] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState([]);
  const [actions, setActions] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
  };

  const uploadAudio = async () => {
    if (!audioFile) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
      const res = await fetch('http://localhost:5000/process-audio', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      if (data.transcript) {
        setTranscript(data.transcript);
        await summarizeTranscript(data.transcript);
      } else {
        alert('Transcription failed');
      }
    } catch (err) {
      console.error(err);
      alert('Upload failed');
    }

    setLoading(false);
  };

  const summarizeTranscript = async (text) => {
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
      console.error(err);
      alert('Summarization failed');
    }
  };

  return (
    <div>
      <h2>Upload Meeting Audio</h2>
      <input type="file" accept="audio/*" onChange={handleFileChange} />
      <button onClick={uploadAudio} disabled={loading}>
        {loading ? 'Processing...' : 'Upload & Transcribe'}
      </button>

      {transcript && (
        <>
          <h3>Transcript</h3>
          <p>{transcript}</p>
        </>
      )}

      {summary.length > 0 && (
        <>
          <h3>Summary</h3>
          <ul>{summary.map((s, i) => <li key={i}>{s}</li>)}</ul>
        </>
      )}

      {actions.length > 0 && (
        <>
          <h3>Action Items</h3>
          <ul>{actions.map((a, i) => <li key={i}>{a}</li>)}</ul>
        </>
      )}

      {decisions.length > 0 && (
        <>
          <h3>Decisions</h3>
          <ul>{decisions.map((d, i) => <li key={i}>{d}</li>)}</ul>
        </>
      )}
    </div>
  );
}

export default AudioUploader;

