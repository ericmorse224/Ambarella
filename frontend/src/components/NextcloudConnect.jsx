/**
 * File: NextcloudConnect.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 *   React component for connecting to the local Nextcloud dashboard.
 *   Renders a button that, when clicked, opens the Nextcloud dashboard in a new browser tab.
 */

/**
 * NextcloudConnect Component
 * --------------------------
 * Renders a button that opens the Nextcloud dashboard when clicked.
 */
export default function NextcloudConnect() {
    /**
     * handleNextcloudConnect
     * ----------------------
     * Opens the Nextcloud dashboard in a new browser tab/window.
     */
    const handleNextcloudConnect = () => {
        // The URL is hardcoded for local development; update as needed for deployment.
        window.open('http://localhost:8080/apps/dashboard/', '_blank');
    };
    return (
        <button
            onClick={handleNextcloudConnect}
            className="mb-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
            Connect to Nextcloud
        </button>
    );
}
