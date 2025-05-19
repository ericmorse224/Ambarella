// src/components/NextcloudConnect.jsx
export default function NextcloudConnect() {
    const handleNextcloudConnect = () => {
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
