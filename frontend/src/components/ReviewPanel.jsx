import React from "react";
import axios from "axios";

const ReviewPanel = ({ actions, setActions ***REMOVED***) => {
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
        ***REMOVED*** catch (error) {
            setStatusMessage("Error fetching Zoho token");
            setStatusType("error");
            setIsLoading(false);
            return;
        ***REMOVED***

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
                                    attendees: [{ email: action.owner ***REMOVED***],
                                ***REMOVED***,
                            ***REMOVED***,
                        ***REMOVED***,
                        {
                            headers: {
                                Authorization: `Zoho-oauthtoken ${accessToken***REMOVED***`,
                            ***REMOVED***,
                        ***REMOVED***
                    )
                )
            );
            setStatusMessage("Events scheduled successfully");
            setStatusType("success");
        ***REMOVED*** catch (error) {
            setStatusMessage("Error scheduling events");
            setStatusType("error");
        ***REMOVED*** finally {
            setIsLoading(false);
        ***REMOVED***
    ***REMOVED***;

    const updateAction = (index, field, value) => {
        const newActions = [...actions];
        if (typeof newActions[index] === "string") {
            // Convert to object if needed
            newActions[index] = { text: newActions[index] ***REMOVED***;
        ***REMOVED***
        newActions[index][field] = value;
        setActions(newActions);
    ***REMOVED***;

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
                        <div key={index***REMOVED***>
                            {/* Make action text visible for tests */***REMOVED***
                            <div className="font-semibold text-sm mb-1">{actionText***REMOVED***</div>
                            <textarea
                                className="w-full p-2 border border-gray-300 rounded"
                                readOnly
                                value={actionText***REMOVED***
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="text"
                                placeholder="Owner"
                                value={owner***REMOVED***
                                onChange={(e) => updateAction(index, "owner", e.target.value)***REMOVED***
                            />
                            <input
                                className="w-full p-2 border border-gray-300 rounded"
                                type="datetime-local"
                                value={datetime***REMOVED***
                                onChange={(e) => updateAction(index, "datetime", e.target.value)***REMOVED***
                            />
                            <div className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={include***REMOVED***
                                    onChange={(e) => updateAction(index, "include", e.target.checked)***REMOVED***
                                    aria-label="Include this action"
                                />
                                <span>Include this action</span>
                            </div>
                        </div>
                    );
                ***REMOVED***)***REMOVED***
            </div>
            <button
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                onClick={handleSchedule***REMOVED***
                disabled={isLoading***REMOVED***
            >
                {isLoading ? "Scheduling..." : "Schedule Selected"***REMOVED***
            </button>
            {statusMessage && (
                <p
                    className={`mt-2 text-sm text-center ${statusType === "success" ? "text-green-600" : "text-red-600"***REMOVED***`***REMOVED***
                    role={statusType === "success" ? "status" : "alert"***REMOVED***
                >
                    {statusMessage***REMOVED***
                </p>
            )***REMOVED***
        </div>
    );
***REMOVED***;

export default ReviewPanel;
