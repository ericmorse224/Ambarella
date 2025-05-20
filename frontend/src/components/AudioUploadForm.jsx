/**
 * AudioUploadForm.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * This component provides a user interface for uploading audio files.
 * It supports file selection, visual feedback on file selection,
 * a custom button for file picking, and a submit button for triggering audio transcription.
 * Additional upload state is handled with isLoading and uploadAttempts props.
 */

import React, { useRef } from "react";

/**
 * AudioUploadForm component
 *
 * @param {Object} props
 * @param {File|null} props.file - The currently selected file (if any).
 * @param {function} props.onFileChange - Callback for file input change.
 * @param {function} props.onSubmit - Callback for form submit.
 * @param {boolean} props.isLoading - Whether upload/transcription is in progress.
 * @param {number} props.uploadAttempts - Number of upload attempts so far.
 */
export default function AudioUploadForm({ file, onFileChange, onSubmit, isLoading, uploadAttempts }) {
    // Reference to the hidden file input for programmatic click
    const fileInputRef = useRef();

    return (
        <form onSubmit={onSubmit} className="mb-4">
            <label className="block font-medium mb-1 dark:text-white" htmlFor="audio-upload">
                Upload Audio
            </label>
            {/* Hidden file input (shown via button) */}
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
            {/* Custom button for triggering file input */}
            <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded mb-2"
            >
                Choose File
            </button>
            {/* Selected file name, or fallback message */}
            <p className="text-sm mt-1 dark:text-white text-gray-700">
                Selected file:{" "}
                {file
                    ? <span className="font-semibold">{file.name}</span>
                    : <span className="italic">No file selected</span>
                }
            </p>
            {/* Submit button (transcription trigger) */}
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
            {/* Display current upload attempt when loading */}
            {isLoading && (
                <div className="text-sm text-gray-600 dark:text-white mt-2">
                    Attempt {uploadAttempts + 1} of 2...
                </div>
            )}
        </form>
    );
}
