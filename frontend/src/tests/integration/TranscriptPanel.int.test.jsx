/**
 * File: TranscriptPanel.int.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * This file contains integration tests for the TranscriptPanel component.
 * The TranscriptPanel is responsible for displaying the meeting transcript
 * and providing a button to download the transcript as a file.
 * 
 * The tests verify:
 *   - That the transcript is rendered properly.
 *   - That the download button appears and calls the provided download handler
 *     with the correct arguments when clicked.
 * 
 * Tools/Libraries Used:
 *   - @testing-library/react: For rendering and interaction testing.
 *   - vi (Vitest): For mocking and assertions.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import TranscriptPanel from '../../components/TranscriptPanel';

describe('TranscriptPanel (Integration)', () => {
    /**
     * Test: renders transcript and download button
     * 
     * - Renders the TranscriptPanel with a sample transcript and a mocked download handler.
     * - Asserts that the transcript text is displayed.
     * - Asserts that the "Download Transcript" button is present.
     * - Simulates a click on the download button and checks that the handler
     *   is called with the correct transcript text and filename.
     */
    it('renders transcript and download button', () => {
        const mockDownload = vi.fn();
        render(<TranscriptPanel transcript="Test transcript" onDownload={mockDownload} />);
        expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
        const btn = screen.getByText(/Download Transcript/i);
        fireEvent.click(btn);
        expect(mockDownload).toHaveBeenCalledWith('Test transcript', 'transcript.txt');
    }, 20000); // Increased timeout for potential longer integration tests
});
