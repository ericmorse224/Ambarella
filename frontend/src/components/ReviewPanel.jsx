import React from "react";
import axios from "axios";

const ReviewPanel = ({ actions, setActions }) => {
    const [statusMessage, setStatusMessage] = React.useState("");
    const [statusType, setStatusType] = React.useState(""); // "success" or "error"
    const [isLoading, setIsLoading] = React.useState(false);

    const handleSchedule = async () => {
        setIsLoading(true);
        setStatusMessage("");
        setStatusType("");

        let accessToken;
        try {
            // For test: simulate token fetch error
            const tokenResponse = await axios.get("/api/zoho/access-token");
            accessToken = tokenResponse.data.access_token;
        } catch (error) {
            setStatusMessage("Error fetching Zoho token");
            setStatusType("error");
            setIsLoading(false);
            return;
        }

        try {
            const includedActions = actions.filter(
                (action) => action.include !== false // treat undefined as true
            );
            // For test: simulate scheduling error
            await Promise.all(
                includedActions.map((action) =>
                    axios.post(
                        "https://www.zohoapis.com/calendar/v2/events",
                        {
                            data: {
                                event: {
                                    title: action.text || action, // support both string and object
                                    start_time: action.datetime,
                                    end_time: action.datetime,
                                    attendees: [{ email: action.owner }],
                                },
                            },
                        },
                        {
                            headers: {
                                Authorization: `Zoho-oauthtoken ${accessToken}`,
                            },
                        }
                    )
                )
            );
            setStatusMessage("Events scheduled successfully");
            setStatusType("success");
        } catch (error) {
            setStatusMessage("Error scheduling events");
            setStatusType("error");
        } finally {
            setIsLoading(false);
        }
    };

    const updateAction = (index, field, value) => {
        const newActions = [...actions];
        if (typeof newActions[index] === "string") {
            // Convert to object if needed
            newActions[index] = { text: newActions[index] };
        }
        newActions[index][field] = value;
        setActions(newActions);
    };

    return (
        <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
            <div className="border rounded p-4 mb-4 space-y-2">
                {actions.map((action, index) => {
                    // Support both string and object action
                    const actionText = typeof action === "string" ? action : action.text || "";
                    const owner = typeof action === "object" ? action.owner || "" : "";
                    const datetime = typeof action === "object" ? action.datetime || "" : "";
                    const include = typeof action === "object" ? !!action.include : true;

                    return (
                        <div key={index}>
                            {/* Make action text visible for tests */}
                            <div className="font-semibold text-sm mb-1">{actionText}</div>
                            <textarea
                                className="w-full p-2 border border-gray-300 rounded"
                                readOnly
                                value={actionText}
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="text"
                                placeholder="Owner"
                                value={owner}
                                onChange={(e) => updateAction(index, "owner", e.target.value)}
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="datetime-local"
                                value={datetime}
                                onChange={(e) => updateAction(index, "datetime", e.target.value)}
                            />
                            <div className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={include}
                                    onChange={(e) => updateAction(index, "include", e.target.checked)}
                                    aria-label="Include this action"
                                />
                                <span>Include this action</span>
                            </div>
                        </div>
                    );
                })}
            </div>
            <button
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                onClick={handleSchedule}
                disabled={isLoading}
            >
                {isLoading ? "Scheduling..." : "Schedule Selected"}
            </button>
            {statusMessage && (
                <p
                    className={`mt-2 text-sm text-center ${statusType === "success" ? "text-green-600" : "text-red-600"}`}
                    role={statusType === "success" ? "status" : "alert"}
                >
                    {statusMessage}
                </p>
            )}
        </div>
    );
};

export default ReviewPanel;

