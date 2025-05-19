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
    if (audioFile.size > 25 * 1024 * 1024) {
        alert("File too large. Max is 25MB");
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

      const data = await res.json();
      if (data.transcript) {
        setTranscript(data.transcript);
        await summarizeTranscript(data.transcript);
      } else {
        alert('Transcription failed');
      }
    } catch (err) {
        console.error('Upload failed:', err);
        alert('Upload failed.');
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

            <button
                onClick={uploadAudio}
                disabled={loading}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                {loading ? 'Processing...' : 'Upload & Transcribe'}
            </button>

            {transcript && (
                <section>
                    <h3 className="text-lg font-medium mt-4">Transcript</h3>
                    <p className="whitespace-pre-wrap">{transcript}</p>
                </section>
            )}

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
