import React, { useState } from "react";
import axios from "axios";
import { addOneHour } from "../utils/dateUtils";

/**
 * ReviewPanel component for reviewing and scheduling action items.
 *
 * @param {Object[]} actions - Array of action objects.
 * @param {Function} setActions - Function to update actions.
 */
const ReviewPanel = ({ actions, setActions }) => {
    const [scheduleStatus, setScheduleStatus] = useState(""); // "", "success", "error"
    const [loading, setLoading] = useState(false);

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
            // Only send included actions with owner and datetime
            const toSchedule = actions
                .filter(a => a.include && a.owner && a.datetime)
                .map(a => {
                    const [datePart, timePart] = a.datetime.split("T");
                    return {
                        text: a.text,
                        owner: a.owner,
                        start: a.datetime,
                        end: addOneHour(datePart, timePart),
                    };
                });

            const res = await axios.post("/api/schedule-actions", { actions: toSchedule });
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
                            value={action.owner}
                            onChange={e => handleActionChange(idx, "owner", e.target.value)}
                        />
                        <input
                            className="w-full p-2 border border-gray-300 rounded"
                            type="datetime-local"
                            value={action.datetime}
                            onChange={e => handleActionChange(idx, "datetime", e.target.value)}
                        />
                        <div className="flex items-center space-x-2">
                            <input
                                aria-label="Include this action"
                                type="checkbox"
                                checked={action.include}
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
