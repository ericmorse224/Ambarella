import { renderHook, act ***REMOVED*** from '@testing-library/react'
import useMeetingState from '../hooks/UseMeetingState'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

const mock = new MockAdapter(axios)

describe('UseMeetingState', () => {
    beforeEach(() => {
        mock.reset()
    ***REMOVED***)

    it('initial state is correct', () => {
        const { result ***REMOVED*** = renderHook(() => useMeetingState())
        expect(result.current.transcript).toBe('')
        expect(result.current.summary).toEqual([])
        expect(result.current.actions).toEqual([])
        expect(result.current.decisions).toEqual([])
        expect(result.current.loading).toBe(false)
        expect(result.current.error).toBe('')
        expect(result.current.uploadAttempts).toBe(0)
    ***REMOVED***)

    it('processAudio sets transcript and updates loading/attempts', async () => {
        const dummyFile = new File(['test'], 'audio.mp3', { type: 'audio/mp3' ***REMOVED***)
        mock.onPost('/api/transcribe').reply(200, { transcript: 'Test transcript' ***REMOVED***)

        const { result ***REMOVED*** = renderHook(() => useMeetingState())

        await act(async () => {
            const success = await result.current.processAudio(dummyFile)
            expect(success).toBe(true)
        ***REMOVED***)

        expect(result.current.transcript).toBe('Test transcript')
        expect(result.current.uploadAttempts).toBe(1)
        expect(result.current.error).toBe('')
    ***REMOVED***)

    it('processTranscript sets summary/actions/decisions', async () => {
        const { result ***REMOVED*** = renderHook(() => useMeetingState())

        act(() => {
            result.current.setTranscript('Test transcript')
        ***REMOVED***)

        mock.onPost('/api/process').reply(200, {
            summary: ['Point 1'],
            actions: ['Action A'],
            decisions: ['Decision X'],
        ***REMOVED***)

        await act(async () => {
            await result.current.processTranscript()
        ***REMOVED***)

        expect(result.current.summary).toEqual(['Point 1'])
        expect(result.current.actions).toEqual(['Action A'])
        expect(result.current.decisions).toEqual(['Decision X'])
    ***REMOVED***)

    it('handles API error gracefully in processAudio', async () => {
        const dummyFile = new File(['test'], 'audio.mp3', { type: 'audio/mp3' ***REMOVED***)
        mock.onPost('/api/transcribe').networkError()

        const { result ***REMOVED*** = renderHook(() => useMeetingState())

        await act(async () => {
            const success = await result.current.processAudio(dummyFile)
            expect(success).toBe(false)
        ***REMOVED***)

        expect(result.current.error).toMatch(/Error processing audio/i)
    ***REMOVED***)
***REMOVED***)
