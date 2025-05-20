/**
 * CalendarEventForm.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * This React component provides a form for creating calendar events.
 * It is designed to work with a Nextcloud backend, sending event details
 * to an API endpoint for event creation. It supports live validation, error handling,
 * loading state, and success messages.
 */

import React, { useState } from "react";
import axios from "axios";

/**
 * CalendarEventForm component for creating a new calendar event.
 * - Uses controlled form state.
 * - Shows loading, success, and error states.
 * - Sends event details to /api/nextcloud/create-event via POST.
 */
const CalendarEventForm = () => {
    // State for form fields
    const [form, setForm] = useState({
        title: "",
        description: "",
        date: "",
        time: "",
        participant: "",
    });
    // State for success message
    const [message, setMessage] = useState("");
    // State for error message
    const [error, setError] = useState("");
    // State for loading indicator
    const [loading, setLoading] = useState(false);

    /**
     * handleChange updates form state on user input.
     * It also clears error and success messages.
     * @param {React.ChangeEvent<HTMLInputElement|HTMLTextAreaElement>} e
     */
    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
        setError("");
        setMessage("");
    };

    /**
     * handleSubmit sends form data to the backend API.
     * Handles success, error, and loading states.
     * @param {React.FormEvent} e
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");
        setError("");
        try {
            // API call to backend endpoint for Nextcloud event creation
            const res = await axios.post("/api/nextcloud/create-event", {
                ...form,
            });
            setMessage("Event created successfully!");
            setForm({
                title: "",
                description: "",
                date: "",
                time: "",
                participant: "",
            });
        } catch (err) {
            // Error handling: Display API error, network error, or generic error
            if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else if (err.message) {
                setError(err.message);
            } else {
                setError("Unknown error occurred");
            }
        } finally {
            setLoading(false);
        }
    };

    // Render the event creation form UI
    return (
        <div className="bg-white p-4 rounded shadow-md max-w-lg mx-auto">
            <h2 className="text-xl font-semibold mb-4">Create Calendar Event</h2>
            <form className="space-y-3" onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title" className="block font-medium">
                        Title
                    </label>
                    <input
                        id="title"
                        name="title"
                        className="w-full p-2 border rounded"
                        placeholder="Title"
                        value={form.title}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="description" className="block font-medium">
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        className="w-full p-2 border rounded"
                        placeholder="Description"
                        value={form.description}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="date" className="block font-medium">
                        Date
                    </label>
                    <input
                        id="date"
                        name="date"
                        className="w-full p-2 border rounded"
                        type="date"
                        placeholder="Date"
                        value={form.date}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="time" className="block font-medium">
                        Time
                    </label>
                    <input
                        id="time"
                        name="time"
                        className="w-full p-2 border rounded"
                        type="time"
                        placeholder="Time"
                        value={form.time}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="participant" className="block font-medium">
                        Participant Email
                    </label>
                    <input
                        id="participant"
                        name="participant"
                        className="w-full p-2 border rounded"
                        placeholder="Participant Email"
                        value={form.participant}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    type="submit"
                    disabled={loading}
                >
                    {loading ? "Creating..." : "Create Event"}
                </button>
                {message && (
                    <p className="mt-2 text-green-700 text-center" role="status">
                        {message}
                    </p>
                )}
                {error && (
                    <p className="mt-2 text-red-600 text-center" role="alert">
                        {error}
                    </p>
                )}
            </form>
        </div>
    );
};

export default CalendarEventForm;
