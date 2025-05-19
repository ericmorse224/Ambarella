import { render, screen, fireEvent } from '@testing-library/react';
import SummaryPanel from '../../components/SummaryPanel';

describe('SummaryPanel (Integration)', () => {
    it('renders summary and download button', () => {
        const mockDownload = vi.fn();
        render(<SummaryPanel summary={['Point 1', 'Point 2']} onDownload={mockDownload} />);
        expect(screen.getByText('Point 1')).toBeInTheDocument();
        fireEvent.click(screen.getByText(/Download Summary/i));
        expect(mockDownload).toHaveBeenCalledWith('Point 1\nPoint 2', 'summary.txt');
    }, 20000);
});
