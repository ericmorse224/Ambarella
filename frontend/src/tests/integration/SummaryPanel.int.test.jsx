/**
 * @file SummaryPanel.int.test.jsx
 * @author Eric Morse
 * @date May 11th 2025
 * @description
 * Integration test for the SummaryPanel component in the AI Meeting Summarizer frontend.
 * This test ensures that the summary panel renders the provided summary content
 * and handles the download functionality correctly.
 * 
 * The test uses React Testing Library to render the component,
 * verifies the summary content is displayed,
 * and checks that clicking the "Download Summary" button triggers the download callback
 * with the expected summary text and file name.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import SummaryPanel from '../../components/SummaryPanel';

describe('SummaryPanel (Integration)', () => {
    /**
     * Test: renders summary and download button
     * - Renders the SummaryPanel with example summary points.
     * - Verifies summary content appears in the DOM.
     * - Simulates clicking the download button.
     * - Expects the download callback to be called with joined summary and filename.
     */
    it('renders summary and download button', () => {
        const mockDownload = vi.fn();
        render(<SummaryPanel summary={['Point 1', 'Point 2']} onDownload={mockDownload} />);
        expect(screen.getByText('Point 1')).toBeInTheDocument();
        fireEvent.click(screen.getByText(/Download Summary/i));
        expect(mockDownload).toHaveBeenCalledWith('Point 1\nPoint 2', 'summary.txt');
    }, 20000);
});
