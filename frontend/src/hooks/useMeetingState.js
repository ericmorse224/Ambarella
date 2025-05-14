// src/hooks/useMeetingState.js
import { useState ***REMOVED*** from 'react';
import axios from 'axios';

export default function useMeetingState(api = axios) {
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState([]);
  const [actions, setActions] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadAttempts, setUploadAttempts] = useState(0);

  async function processAudio(file) {
    const formData = new FormData();
    formData.append('file', file);
    setIsLoading(true);
    try {
      const response = await api.post('http://localhost:5000/process-audio', formData);
      setTranscript(response.data.transcript);
      return true;
    ***REMOVED*** catch (err) {
      console.error('Error processing audio:', err);
      return false;
    ***REMOVED*** finally {
      setIsLoading(false);
      setUploadAttempts((prev) => prev + 1);
    ***REMOVED***
  ***REMOVED***

  async function processTranscript() {
    setIsLoading(true);
    try {
      const response = await api.post('http://localhost:5000/process-json', {
        transcript,
      ***REMOVED***);
      setSummary(response.data.summary || []);
      setActions(response.data.actions || []);
      setDecisions(response.data.decisions || []);
    ***REMOVED*** catch (err) {
      console.error('Error processing JSON:', err);
    ***REMOVED*** finally {
      setIsLoading(false);
    ***REMOVED***
  ***REMOVED***

  return {
    transcript,
    summary,
    actions,
    decisions,
    isLoading,
    uploadAttempts,
    processAudio,
    processTranscript,
    setTranscript,
    setActions
  ***REMOVED***;
***REMOVED***