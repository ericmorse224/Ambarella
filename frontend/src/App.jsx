/**
 * App.jsx
 * 
 * Author: Eric Morse
 * Date: May 11th 2025
 * 
 * Main application component for the AI Meeting Summarizer dashboard.
 * Handles app state, file upload, dark mode, transcript processing, 
 * error handling, and renders all major UI panels.
 */

import React, { useState } from 'react';
import useMeetingState from './hooks/UseMeetingState';
import NextcloudConnect from './components/NextcloudConnect';
import AudioUploadForm from './components/AudioUploadForm';
import TranscriptPanel from './components/TranscriptPanel';
import SummaryPanel from './components/SummaryPanel';
import DecisionsPanel from './components/DecisionsPanel';
import ReviewPanel from './components/ReviewPanel';
import ErrorBoundary from './components/ErrorBoundary';

export default function App() {
    /**
     * @state file                The uploaded audio file selected by the user
     * @state scheduleError       Error message for scheduling actions
     * @state scheduleSuccess     Success message for scheduled actions
     * @state dark                Whether dark mode is enabled
     */
    const [file, setFile] = useState(null);
    const [scheduleError, setScheduleError] = useState('');
    const [scheduleSuccess, setScheduleSuccess] = useState('');
    const [dark, setDark] = useState(
        () =>
            typeof window !== "undefined"
                ? window.matchMedia("(prefers-color-scheme: dark)").matches
                : false
    );

    /**
     * useMeetingState - Custom hook for meeting summarizer state and handlers
     */
    const {
        transcript, summary, actions, decisions,
        isLoading, uploadAttempts, processAudio,
        processTranscript, setActions, error
    } = useMeetingState();

    /**
     * Effect: Manage <html> dark mode class for Tailwind
     */
    React.useEffect(() => {
        if (dark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [dark]);

    /**
     * Handle audio file selection
     * - Validates file type and size
     * - Updates file state
     */
    const handleFileChange = (e) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;
        if (selectedFile.size > 25 * 1024 * 1024) {
            window.alert('File size exceeds 25MB limit');
            return;
        }
        if (!selectedFile.type.startsWith('audio/')) {
            window.alert('Unsupported file type! Please upload a valid audio file.');
            return;
        }
        setFile(selectedFile);
    };

    /**
     * Handle file upload form submit
     * - Invokes audio processing via the backend
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        setScheduleError('');
        setScheduleSuccess('');
        if (file) {
            await processAudio(file);
        }
    };

    /**
     * Analyze transcript using the backend/LLM
     * - Extracts summary, actions, decisions
     */
    const handleAnalyze = async () => {
        setScheduleError('');
        setScheduleSuccess('');
        await processTranscript();
    };

    /**
     * Download transcript or summary as a text file
     * @param {string} content  The file content
     * @param {string} filename The filename to save as
     */
    const handleDownload = (content, filename) => {
        const blob = new Blob([content], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    };

    /**
     * Main render: error boundary wraps all app content.
     * Renders header, audio upload, transcript, summary, decisions,
     * and review panels.
     */
    return (
        <ErrorBoundary>
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-950 font-sans transition-colors duration-300">
                {/* Fancy Sticky Header with Logo & Accent */}
                <header className="py-6 bg-gradient-to-r from-[#2A60C9] to-blue-500 dark:from-gray-800 dark:to-gray-900 shadow-lg sticky top-0 z-30 transition-colors duration-300">
                    <div className="max-w-2xl mx-auto flex items-center justify-between px-4">
                        <div className="flex items-center gap-3">
                            {/* Emoji or SVG logo */}
                            <span className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white dark:bg-gray-900 shadow-lg border-2 border-[#2A60C9]">
                                <span className="text-2xl" role="img" aria-label="Calendar">🗓️</span>
                            </span>
                            <h1 className="text-3xl font-extrabold text-white dark:text-blue-100 tracking-tight drop-shadow">
                                AI Meeting Summarizer
                            </h1>
                        </div>
                        <div className="flex items-center gap-2">
                            <NextcloudConnect />
                            {/* Dark mode toggle */}
                            <button
                                className="ml-3 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 w-10 h-10 flex items-center justify-center transition-colors duration-200 border border-gray-300 dark:border-gray-700"
                                onClick={() => setDark((d) => !d)}
                                title={dark ? "Switch to light mode" : "Switch to dark mode"}
                                aria-label="Toggle dark mode"
                            >
                                {dark ? (
                                    // Moon icon
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 0111.21 3a7 7 0 000 14A9 9 0 0121 12.79z" /></svg>
                                ) : (
                                    // Sun icon
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><circle cx={12} cy={12} r={5} /><path d="M12 1v2m0 18v2m11-11h-2M3 12H1m16.95-6.36l-1.41 1.41M4.05 19.95l-1.41-1.41m0-13.18l1.41 1.41M19.95 19.95l1.41-1.41" /></svg>
                                )}
                            </button>
                        </div>
                    </div>
                </header>
                <main className="max-w-2xl mx-auto px-4 py-8">
                    {/* Main Card */}
                    <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-lg hover:shadow-2xl transition-shadow duration-300 p-6 mb-8 border border-[#2A60C9]/10 dark:border-gray-800 animate-fadeIn">
                        <AudioUploadForm
                            file={file}
                            onFileChange={handleFileChange}
                            onSubmit={handleSubmit}
                            isLoading={isLoading}
                            uploadAttempts={uploadAttempts}
                        />
                        {error && (
                            <div className="bg-red-50 dark:bg-red-950 border-l-4 border-red-500 text-red-700 dark:text-red-400 px-4 py-2 rounded-xl shadow my-2 text-center font-semibold" role="alert">
                                {error}
                            </div>
                        )}
                        {scheduleError && (
                            <div className="bg-red-50 dark:bg-red-950 border-l-4 border-red-500 text-red-700 dark:text-red-400 px-4 py-2 rounded-xl shadow my-2 text-center font-semibold" role="alert">
                                {scheduleError}
                            </div>
                        )}
                        {scheduleSuccess && (
                            <div className="bg-green-50 dark:bg-green-950 border-l-4 border-green-500 text-green-700 dark:text-green-300 px-4 py-2 rounded-xl shadow my-2 text-center font-semibold" role="status">
                                {scheduleSuccess}
                            </div>
                        )}
                    </div>
                    <div className="space-y-6">
                        <div className="animate-fadeIn">
                            <TranscriptPanel transcript={transcript} onDownload={handleDownload} />
                        </div>
                        {transcript && transcript.length > 0 && (
                            <button
                                className="mt-4 bg-[#2A60C9] hover:bg-blue-700 dark:bg-blue-800 dark:hover:bg-blue-900 text-white px-6 py-2 rounded-xl font-semibold shadow-md transition-all duration-200 active:scale-95 block mx-auto animate-fadeIn"
                                onClick={handleAnalyze}
                                disabled={isLoading}
                            >
                                Analyze Transcript
                            </button>
                        )}
                        <div className="animate-fadeIn">
                            <SummaryPanel summary={summary} onDownload={handleDownload} />
                        </div>
                        <div className="animate-fadeIn">
                            <DecisionsPanel decisions={decisions} />
                        </div>
                        {actions.length > 0 && (
                            <div className="animate-fadeIn">
                                <ReviewPanel actions={actions} setActions={setActions} />
                            </div>
                        )}
                    </div>
                </main>
                <footer className="py-4 text-center text-gray-400 dark:text-gray-600 text-xs">
                    &copy; {new Date().getFullYear()} AI Meeting Summarizer &mdash; All rights reserved
                </footer>
            </div>
            </ErrorBoundary>
        );
    }
