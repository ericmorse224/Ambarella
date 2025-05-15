import { useState, useCallback ***REMOVED*** from 'react';
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
            formData.append('file', file);

            // Use the endpoint your tests expect
            const response = await axios.post('/api/transcribe', formData);
            const { transcript ***REMOVED*** = response.data;
            setTranscript(transcript);
            return true;
        ***REMOVED*** catch (err) {
            setError(
                err.response?.data?.message || 'Error processing audio'
            );
            console.error('Error processing audio:', err);
            return false;
        ***REMOVED*** finally {
            setIsLoading(false);
        ***REMOVED***
    ***REMOVED***, []);

    const processTranscript = useCallback(async () => {
        setIsLoading(true);
        setError(false);
        try {
            const response = await axios.post('/api/process', { transcript ***REMOVED***);
            const { summary, actions, decisions ***REMOVED*** = response.data;
            setSummary(summary);
            setActions(actions);
            setDecisions(decisions);
        ***REMOVED*** catch (err) {
            setError(
                err.response?.data?.message || 'Error processing transcript'
            );
            console.error('Error processing transcript:', err);
        ***REMOVED*** finally {
            setIsLoading(false);
        ***REMOVED***
    ***REMOVED***, [transcript]);

    const resetTranscript = useCallback(() => {
        setTranscript('');
        setSummary([]);
        setActions([]);
        setDecisions([]);
        setUploadAttempts(0);
        setError(false);
    ***REMOVED***, []);

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
    ***REMOVED***;
***REMOVED***;

export default useMeetingState;
