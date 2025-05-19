import { useState, useCallback } from 'react';
import axios from 'axios';

const useMeetingState = () => {
    const [transcript, setTranscript] = useState('');
    const [summary, setSummary] = useState([]);
    const [actions, setActions] = useState([]);
    const [decisions, setDecisions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(false);
    const [uploadAttempts, setUploadAttempts] = useState(0);

    const processAudio = useCallback(async (file) => {
        setIsLoading(true);
        setError(false);
        setUploadAttempts(prev => prev + 1);
        try {
            const formData = new FormData();
            formData.append('audio', file);

            // Use the endpoint your tests expect
            const response = await axios.post('http://localhost:5000/process-audio', formData);
            const { transcript } = response.data;
            setTranscript(transcript);
            return true;
        } catch (err) {
            setError(
                err.response?.data?.message || 'Error processing audio'
            );
            console.error('Error processing audio:', err);
            return false;
        } finally {
            setIsLoading(false);
        }
    }, []);

    const processTranscript = useCallback(async () => {
        setIsLoading(true);
        setError(false);
        try {
            const response = await axios.post('http://localhost:5000/process-json', { transcript });
            const { summary, actions, decisions } = response.data;
            setSummary(summary);
            setActions(actions);
            setDecisions(decisions);
        } catch (err) {
            setError(
                err.response?.data?.message || 'Error processing transcript'
            );
            console.error('Error processing transcript:', err);
        } finally {
            setIsLoading(false);
        }
    }, [transcript]);

    const resetTranscript = useCallback(() => {
        setTranscript('');
        setSummary([]);
        setActions([]);
        setDecisions([]);
        setUploadAttempts(0);
        setError(false);
    }, []);

    return {
        transcript,
        setTranscript,
        summary,
        actions,
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

