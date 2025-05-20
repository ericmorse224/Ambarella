import React, { useState } from "react";
import axios from "axios";

/**
 * ReviewPanel component for reviewing and scheduling action items with duration.
 *
 * @param {Object[]} actions - Array of action objects.
 * @param {Function} setActions - Function to update actions.
 */
const ReviewPanel = ({ actions, setActions }) => {
    const [scheduleStatus, setScheduleStatus] = useState(""); // "", "success", "error"
    const [loading, setLoading] = useState(false);

    // Ensure all actions have include, owner, date, time, duration fields (avoid uncontrolled input warning)
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

    const handleActionChange = (idx, field, value) => {
        const updated = actions.map((action, i) =>
            i === idx ? { ...action, [field]: value } : action
        );
        setActions(updated);
    };

    const handleSchedule = async () => {
        setLoading(true);
        setScheduleStatus("");
        try {
            const toSchedule = actions
                .filter(a => a.include && a.owner && a.date && a.time)
                .map(a => {
                    // Combine local date and time, convert to ISO UTC string for start and end
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

    return (
        <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
            <div className="border rounded p-4 mb-4 space-y-2">
                {actions.map((action, idx) => (
                    <div key={idx}>
                        <div className="font-semibold text-sm mb-1">{action.text}</div>
                        <textarea
                            className="w-full p-2 border border-gray-300 rounded"
                            value={action.text}
                            readOnly
                        />
                        <input
                            className="w-full p-2 border border-gray-300 rounded"
                            placeholder="Owner"
                            type="text"
                            value={action.owner || ""}
                            onChange={e => handleActionChange(idx, "owner", e.target.value)}
                        />
                        <div className="flex gap-2 mt-1">
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="date"
                                value={action.date || ""}
                                onChange={e => handleActionChange(idx, "date", e.target.value)}
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="time"
                                value={action.time || ""}
                                onChange={e => handleActionChange(idx, "time", e.target.value)}
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
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
                        <div className="flex items-center space-x-2 mt-2">
                            <input
                                aria-label="Include this action"
                                type="checkbox"
                                checked={action.include !== undefined ? action.include : true}
                                onChange={e => handleActionChange(idx, "include", e.target.checked)}
                            />
                            <span>Include this action</span>
                        </div>
                    </div>
                ))}
            </div>
            <button
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                onClick={handleSchedule}
                disabled={loading}
            >
                {loading ? "Scheduling..." : "Schedule Selected"}
            </button>
            {scheduleStatus === "success" && (
                <p className="mt-2 text-sm text-center text-green-600" role="status">
                    Events scheduled successfully!
                </p>
            )}
            {scheduleStatus === "error" && (
                <p className="mt-2 text-sm text-center text-red-600" role="alert">
                    Error scheduling events
                </p>
            )}
        </div>
    );
};

export default ReviewPanel;
