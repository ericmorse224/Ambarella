import { render, screen, fireEvent } from '@testing-library/react';
import TranscriptPanel from '../../components/TranscriptPanel';

describe('TranscriptPanel (Integration)', () => {
    it('renders transcript and download button', () => {
        const mockDownload = vi.fn();
        render(<TranscriptPanel transcript="Test transcript" onDownload={mockDownload} />);
        expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
        const btn = screen.getByText(/Download Transcript/i);
        fireEvent.click(btn);
        expect(mockDownload).toHaveBeenCalledWith('Test transcript', 'transcript.txt');
    }, 20000);
});
