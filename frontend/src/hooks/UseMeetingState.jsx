/**
 * UseMeetingState.jsx
 * 
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Custom React hook for managing meeting transcription state,
 * summary generation, action/decision extraction, and related UI flags.
 * Encapsulates all backend API interactions for audio and transcript processing.
 */

import { useState, useCallback } from 'react';
import axios from 'axios';

/**
 * Custom hook providing state and logic for AI Meeting Summarizer UI.
 * - Handles file upload and transcription (audio -> transcript)
 * - Handles transcript analysis (summary, actions, decisions)
 * - Tracks loading, error, and retry state
 */
const useMeetingState = () => {
    // --- State variables ---
    // The transcript text generated from uploaded audio
    const [transcript, setTranscript] = useState('');
    // The meeting summary (array of sentences)
    const [summary, setSummary] = useState([]);
    // List of extracted action items from the transcript
    const [actions, setActions] = useState([]);
    // List of extracted decisions from the transcript
    const [decisions, setDecisions] = useState([]);
    // Loading flag for any backend operation
    const [isLoading, setIsLoading] = useState(false);
    // Error message or boolean (if present, signals error in processing)
    const [error, setError] = useState(false);
    // Number of upload attempts (for retry logic/UI feedback)
    const [uploadAttempts, setUploadAttempts] = useState(0);

    /**
     * Uploads an audio file and gets the transcript from backend.
     * @param {File} file - Audio file to transcribe.
     * @returns {Promise<boolean>} - Success flag.
     */
    const processAudio = useCallback(async (file) => {
        setIsLoading(true);
        setError(false);
        setUploadAttempts(prev => prev + 1);
        try {
            // Prepare file upload
            const formData = new FormData();
            formData.append('audio', file);

            // POST to backend audio endpoint
            const response = await axios.post('http://localhost:5000/process-audio', formData);
            const { transcript } = response.data;
            setTranscript(transcript);
            return true;
        } catch (err) {
            // Set error message from backend if available
            setError(
                err.response?.data?.message || 'Error processing audio'
            );
            console.error('Error processing audio:', err);
            return false;
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Sends current transcript to backend for NLP analysis,
     * receiving summary, actions, and decisions.
     */
    const processTranscript = useCallback(async () => {
        // Defensive: Ensure transcript is present and valid
        console.log("DEBUG transcript value:", transcript, "|", typeof transcript, "|", transcript.length);
        if (!transcript || typeof transcript !== 'string' || transcript.length === 0) {
            setError('Transcript is missing or invalid.');
            return;
        }
        setIsLoading(true);
        setError(false);
        try {
            // POST transcript to backend NLP endpoint
            const response = await axios.post(
                'http://localhost:5000/process-json',
                { transcript, entities: [] },  // Always send entities
                { headers: { 'Content-Type': 'application/json' } }
            );
            // Extract results
            const { summary, actions, decisions } = response.data;
            setSummary(summary);
            setActions(actions);
            setDecisions(decisions);
        } catch (err) {
            // Show backend or generic error
            setError(
                err.response?.data?.error ||
                err.response?.data?.message ||
                'Error processing transcript'
            );
            console.error('Error processing transcript:', err);
        } finally {
            setIsLoading(false);
        }
    }, [transcript]);

    /**
     * Resets all transcript and NLP-related state.
     * Typically used after a successful workflow or on user reset.
     */
    const resetTranscript = useCallback(() => {
        setTranscript('');
        setSummary([]);
        setActions([]);
        setDecisions([]);
        setUploadAttempts(0);
        setError(false);
    }, []);

    // Return all state and handlers for use in UI components
    return {
        transcript,
        setTranscript,
        summary,
        actions,
        setActions,
        decisions,
        isLoading,
        error,
        uploadAttempts,
        setUploadAttempts,
        processAudio,
        processTranscript,
        resetTranscript,
    };
};

export default useMeetingState;
