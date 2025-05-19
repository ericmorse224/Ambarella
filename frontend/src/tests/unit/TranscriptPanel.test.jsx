import { render, screen, fireEvent } from '@testing-library/react';
import TranscriptPanel from '../../components/TranscriptPanel';

describe('TranscriptPanel', () => {
    test('renders transcript and download button', () => {
        const mockDownload = vi.fn();
        render(<TranscriptPanel transcript="Test transcript" onDownload={mockDownload} />);
        expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
        const btn = screen.getByText(/Download Transcript/i);
        fireEvent.click(btn);
        expect(mockDownload).toHaveBeenCalledWith('Test transcript', 'transcript.txt');
    });
    test('does not render if transcript is empty', () => {
        render(<TranscriptPanel transcript="" onDownload={() => {}} />);
        expect(screen.queryByText(/Download Transcript/i)).not.toBeInTheDocument();
    });
});
