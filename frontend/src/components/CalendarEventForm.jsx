import React, { useState } from 'react';
import axios from 'axios';

export default function CalendarEventForm() {
    const [form, setForm] = useState({
        title: '',
        description: '',
        date: '',
        time: '',
        participant: ''
    });
    const [status, setStatus] = useState('');

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('Creating event...');

        try {
            const res = await axios.post('http://localhost:5000/create-event', form);
            setStatus(res.data.message || 'Event created!');
        } catch (err) {
            console.error(err);
            setStatus('Failed to create event.');
        }
    };

    return (
        <div className="bg-white p-4 rounded shadow-md max-w-lg mx-auto">
            <h2 className="text-xl font-semibold mb-4">Create Calendar Event</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
                <input name="title" value={form.title} onChange={handleChange} placeholder="Title" className="w-full p-2 border rounded" required />
                <textarea name="description" value={form.description} onChange={handleChange} placeholder="Description" className="w-full p-2 border rounded" required />
                <input name="date" type="date" value={form.date} onChange={handleChange} className="w-full p-2 border rounded" required />
                <input name="time" type="time" value={form.time} onChange={handleChange} className="w-full p-2 border rounded" required />
                <input name="participant" value={form.participant} onChange={handleChange} placeholder="Participant Email" className="w-full p-2 border rounded" required />
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Create Event</button>
            </form>
            {status && <p className="text-sm mt-3">{status}</p>}
        </div>
    );
}

