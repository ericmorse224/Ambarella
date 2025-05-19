// src/components/AudioUploadForm.jsx
export default function AudioUploadForm({ file, onFileChange, onSubmit, isLoading, uploadAttempts }) {
    return (
        <form onSubmit={onSubmit} className="mb-4">
            <label className="block font-medium mb-1" htmlFor="audio-upload">Upload Audio</label>
            <input
                data-testid="audio-upload"
                id="audio-upload"
                name="audio"
                type="file"
                accept="audio/*"
                onChange={onFileChange}
                className="w-full p-2 border border-gray-300 rounded mb-2"
            />
            <p className="text-sm text-gray-600 mt-1">
                Selected file: {file ? file.name : 'None'}
            </p>
            <button
                type="submit"
                disabled={isLoading || !file}
                aria-label="Transcribe Audio"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            >
                {isLoading ? (
                    <span>
                        <span className="sr-only">Transcribe Audio</span>
                        Processing...
                    </span>
                ) : (
                    'Transcribe Audio'
                )}
            </button>
            {isLoading && (
                <div className="text-sm text-gray-600 mt-2">Attempt {uploadAttempts + 1} of 2...</div>
            )}
        </form>
    );
}
