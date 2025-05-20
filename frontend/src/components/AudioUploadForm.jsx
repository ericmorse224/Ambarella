import React, { useRef } from "react";

export default function AudioUploadForm({ file, onFileChange, onSubmit, isLoading, uploadAttempts }) {
    const fileInputRef = useRef();

    return (
        <form onSubmit={onSubmit} className="mb-4">
            <label className="block font-medium mb-1 dark:text-white" htmlFor="audio-upload">
                Upload Audio
            </label>
            {/* Hidden file input */}
            <input
                ref={fileInputRef}
                data-testid="audio-upload"
                id="audio-upload"
                name="audio"
                type="file"
                accept="audio/*"
                onChange={onFileChange}
                className="hidden"
            />
            {/* Custom Button */}
            <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded mb-2"
            >
                Choose File
            </button>
            {/* Always-styled filename */}
            <p className="text-sm mt-1 dark:text-white text-gray-700">
                Selected file:{" "}
                {file
                    ? <span className="font-semibold">{file.name}</span>
                    : <span className="italic">No file selected</span>
                }
            </p>
            <button
                type="submit"
                disabled={isLoading || !file}
                aria-label="Transcribe Audio"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded mt-3"
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
                <div className="text-sm text-gray-600 dark:text-white mt-2">
                    Attempt {uploadAttempts + 1} of 2...
                </div>
            )}
        </form>
    );
}
