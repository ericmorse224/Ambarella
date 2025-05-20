/**
 * File: TranscriptPanel.test.jsx
 * Author: Eric Morse
 * Date: May 11th 2025
 *
 * Purpose:
 * This test file provides comprehensive unit tests for the TranscriptPanel React component.
 * It ensures that transcript display and download features behave as expected, and that the component
 * conditionally renders depending on whether the transcript string is empty.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import TranscriptPanel from '../../components/TranscriptPanel';

describe('TranscriptPanel', () => {
    /**
     * Test: Renders transcript and download button
     *
     * - Checks that the transcript text appears in the DOM.
     * - Simulates a click on the download button and verifies that the
     *   mock download handler is called with the correct arguments.
     */
    test('renders transcript and download button', () => {
        // Mock download function to track calls
        const mockDownload = vi.fn();
        // Render the component with a sample transcript
        render(<TranscriptPanel transcript="Test transcript" onDownload={mockDownload} />);
        expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
        // Find the download button and simulate a click
        const btn = screen.getByText(/Download Transcript/i);
        fireEvent.click(btn);
        expect(mockDownload).toHaveBeenCalledWith('Test transcript', 'transcript.txt');
    });

    /**
     * Test: Does not render if transcript is empty
     *
     * - Verifies that if an empty transcript string is provided,
     *   the component does not render the download button.
     */
    test('does not render if transcript is empty', () => {
        render(<TranscriptPanel transcript="" onDownload={() => {}} />);
        expect(screen.queryByText(/Download Transcript/i)).not.toBeInTheDocument();
    });
});
