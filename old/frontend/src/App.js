import React, { useState ***REMOVED*** from 'react';
import axios from 'axios';

export default function App() {
    const [transcript, setTranscript] = useState('');
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.info('Submitting transcript:', transcript);
            const response = await axios.post('http://localhost:5000/process-json', {
                transcript: [
                    { speaker: 'User', text: transcript ***REMOVED***
                ]
            ***REMOVED***);
            console.info('Response received:', response.data);
            setResult(response.data);
        ***REMOVED*** catch (error) {
            console.error('Error during submission:', error);
        ***REMOVED***
    ***REMOVED***;

    return (
        <div className="p-6 max-w-xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">AI Meeting Summarizer</h1>
            <form onSubmit={handleSubmit***REMOVED*** className="mb-4">
                <textarea
                    className="w-full p-2 border rounded mb-2"
                    rows={5***REMOVED***
                    placeholder="Paste transcript text here..."
                    value={transcript***REMOVED***
                    onChange={(e) => setTranscript(e.target.value)***REMOVED***
                />
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Summarize</button>
            </form>
            {result && (
                <div className="bg-gray-100 p-4 rounded">
                    <h2 className="font-semibold">Summary:</h2>
                    <ul className="list-disc ml-6">
                        {result.summary && result.summary.map((s, i) => <li key={`summary-${i***REMOVED***`***REMOVED***>{s***REMOVED***</li>)***REMOVED***
                    </ul>
                    <h2 className="font-semibold mt-4">Actions:</h2>
                    <ul className="list-disc ml-6">
                        {result.actions && result.actions.map((a, i) => <li key={`action-${i***REMOVED***`***REMOVED***>{a***REMOVED***</li>)***REMOVED***
                    </ul>
                    <h2 className="font-semibold mt-4">Decisions:</h2>
                    <ul className="list-disc ml-6">
                        {result.decisions && result.decisions.map((d, i) => <li key={`decision-${i***REMOVED***`***REMOVED***>{d***REMOVED***</li>)***REMOVED***
                    </ul>
                </div>
            )***REMOVED***
        </div>
    );
***REMOVED***
