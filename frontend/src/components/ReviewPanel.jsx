/**
 * ReviewPanel.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * This component provides a UI for reviewing, editing, and scheduling action items
 * detected from a meeting transcript. It is a key part of the AI Meeting Summarizer
 * workflow, allowing the user to confirm, modify, or exclude action items, adjust
 * scheduling metadata, and send selected actions to the calendar integration.
 *
 * Key Features:
 * - Displays a list of action items, each with editable owner, date, time, and duration.
 * - Allows users to include or exclude actions from scheduling via checkbox.
 * - Supports per-action editing for ownership and scheduling.
 * - Presents a "Schedule Selected" button to trigger scheduling for checked items.
 * - Shows loading state and error messages for scheduling.
 * - Handles validation for empty action lists and at least one action selected.
 *
 * Props:
 * - actions (array): List of action objects, each with text, owner, datetime, duration, include.
 * - setActions (func): Callback to update the actions state.
 * - onSchedule (func): Callback invoked when the user schedules actions.
 * - loading (bool): If true, disables scheduling UI.
 * - error (string): Optional error message for scheduling failures.
 *
 * Usage:
 * <ReviewPanel
 *   actions={actions}
 *   setActions={setActions}
 *   onSchedule={scheduleActions}
 *   loading={loading}
 *   error={errorMsg}
 * />
 *
 * Dependencies: React, PropTypes, Tailwind CSS for styling
 */


import React, { useState } from "react";
import axios from "axios";

const ReviewPanel = ({ actions, setActions }) => {
    // State for success/error UI and loading spinner
    const [scheduleStatus, setScheduleStatus] = useState(""); // "", "success", "error"
    const [loading, setLoading] = useState(false);

    /**
     * Ensure every action has required fields on mount.
     * This prevents missing owner/date/time/duration/include fields.
     */
    React.useEffect(() => {
        const updated = actions.map(a => ({
            ...a,
            include: a.include !== undefined ? a.include : true,
            owner: a.owner || "",
            date: a.date || "",
            time: a.time || "",
            duration: a.duration || 60
        }));
        if (JSON.stringify(updated) !== JSON.stringify(actions)) setActions(updated);
        // eslint-disable-next-line
    }, []); // Run only once on mount

    /**
     * Handler for field changes (owner, date, time, duration, include).
     * Updates a single action within the array.
     */
    const handleActionChange = (idx, field, value) => {
        const updated = actions.map((action, i) =>
            i === idx ? { ...action, [field]: value } : action
        );
        setActions(updated);
    };

    /**
     * Schedule handler.
     * - Filters for included actions with all required fields.
     * - Converts local date/time+duration to ISO start/end.
     * - Sends POST to backend /api/schedule-actions.
     * - Updates UI for success/error.
     */
    const handleSchedule = async () => {
        setLoading(true);
        setScheduleStatus("");
        try {
            // Prepare actions for scheduling (filter + build ISO times)
            const toSchedule = actions
                .filter(a => a.include && a.owner && a.date && a.time)
                .map(a => {
                    const localDateTime = `${a.date}T${a.time}`;
                    const isoStart = new Date(localDateTime);
                    const durationMinutes = parseInt(a.duration, 10) || 60;
                    const isoEnd = new Date(isoStart.getTime() + durationMinutes * 60000);
                    return {
                        include: true,
                        datetime: isoStart.toISOString(),
                        end: isoEnd.toISOString(),
                        text: a.text,
                        owner: a.owner,
                    };
                });
            // Send to backend API
            const res = await axios.post("http://localhost:5000/api/schedule-actions", { actions: toSchedule });
            if (res.data && res.data.success) {
                setScheduleStatus("success");
            } else {
                setScheduleStatus("error");
            }
        } catch (err) {
            setScheduleStatus("error");
        } finally {
            setLoading(false);
        }
    };

    // Show a placeholder if there are no actions to review
    if (!actions || actions.length === 0) {
        return (
            <div className="bg-white rounded-2xl shadow-md p-6 text-center text-gray-500 mt-6">
                No actions detected. Please transcribe audio or add an action.
            </div>
        );
    }

    return (
        <div>
            {scheduleStatus === "success" && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded mb-4 text-center font-semibold" role="status">
                    Events scheduled successfully!
                </div>
            )}
            {scheduleStatus === "error" && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4 text-center font-semibold" role="alert">
                    Error scheduling events
                </div>
            )}
            <div className="space-y-6">
                {actions.map((action, idx) => {
                    const ownerId = `owner-${idx}`;
                    const dateId = `date-${idx}`;
                    const timeId = `time-${idx}`;
                    const durationId = `duration-${idx}`;
                    return (
                        <div key={idx} className="bg-white rounded-2xl shadow-md p-6">
                            {/* Centered, multi-line action text */}
                            <div className="font-bold text-lg text-blue-700 mb-4 text-center break-words whitespace-pre-line leading-snug">
                                {action.text}
                            </div>
                            <div className="mb-3">
                                <label htmlFor={ownerId} className="block font-medium mb-1 text-gray-700">Owner</label>
                                <input
                                    id={ownerId}
                                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150"
                                    placeholder="Owner"
                                    type="text"
                                    value={action.owner || ""}
                                    onChange={e => handleActionChange(idx, "owner", e.target.value)}
                                />
                            </div>
                            <div className="flex gap-3 mb-3">
                                <div className="flex-1">
                                    <label htmlFor={dateId} className="block font-medium mb-1 text-gray-700">Date</label>
                                    <input
                                        id={dateId}
                                        className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        type="date"
                                        value={action.date || ""}
                                        onChange={e => handleActionChange(idx, "date", e.target.value)}
                                    />
                                </div>
                                <div className="flex-1">
                                    <label htmlFor={timeId} className="block font-medium mb-1 text-gray-700">Time</label>
                                    <input
                                        id={timeId}
                                        className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        type="time"
                                        value={action.time || ""}
                                        onChange={e => handleActionChange(idx, "time", e.target.value)}
                                    />
                                </div>
                                <div className="flex-1">
                                    <label htmlFor={durationId} className="block font-medium mb-1 text-gray-700">Duration (min)</label>
                                    <input
                                        id={durationId}
                                        className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        type="number"
                                        min={5}
                                        max={480}
                                        step={5}
                                        value={action.duration || 60}
                                        onChange={e => handleActionChange(idx, "duration", e.target.value)}
                                        placeholder="Duration (minutes)"
                                        title="Duration (minutes)"
                                    />
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <input
                                    aria-label="Include this action"
                                    type="checkbox"
                                    className="accent-blue-600 h-4 w-4"
                                    checked={action.include !== undefined ? action.include : true}
                                    onChange={e => handleActionChange(idx, "include", e.target.checked)}
                                />
                                <span className="text-gray-600">Include this action</span>
                            </div>
                        </div>
                    );
                })}
            </div>
            <button
                className="mt-8 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl px-4 py-3 shadow-lg transition-all duration-150 disabled:opacity-60 disabled:cursor-wait"
                onClick={handleSchedule}
                disabled={loading}
            >
                {loading ? "Scheduling..." : "Schedule Selected"}
            </button>
        </div>
    );
};

export default ReviewPanel;
