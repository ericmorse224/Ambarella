/**
 * @file SummaryPanel.test.jsx
 * @author Eric Morse
 * @date May 11th 2025
 * @description
 *   Unit tests for the SummaryPanel component in the AI Meeting Summarizer frontend.
 *   These tests verify correct rendering of summary content, download functionality,
 *   and behavior when the summary is empty.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import SummaryPanel from '../../components/SummaryPanel';

describe('SummaryPanel', () => {
    /**
     * Test: Renders the summary list and download button, and ensures the download callback works.
     */
    test('renders summary and download button', () => {
        const mockDownload = vi.fn();
        render(<SummaryPanel summary={['Point 1', 'Point 2']} onDownload={mockDownload} />);
        // Verify that the summary text is rendered
        expect(screen.getByText('Point 1')).toBeInTheDocument();
        // Simulate clicking the download button and verify the callback
        fireEvent.click(screen.getByText(/Download Summary/i));
        expect(mockDownload).toHaveBeenCalledWith('Point 1\nPoint 2', 'summary.txt');
    });

    /**
     * Test: If the summary is empty, the download button is not rendered.
     */
    test('does not render if summary is empty', () => {
        render(<SummaryPanel summary={[]} onDownload={() => { }} />);
        // The download button should not be present
        expect(screen.queryByText(/Download Summary/i)).not.toBeInTheDocument();
    });
});
