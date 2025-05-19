import { render, screen, fireEvent } from '@testing-library/react';
import ReviewPanel from '../../components/ReviewPanel';

describe('ReviewPanel Integration', () => {
    it('schedules actions and shows real success or error message from backend', async () => {
        const actions = [
            { text: 'Integration Action', owner: 'test@example.com', datetime: '2025-06-01T10:00', include: true }
        ];
        render(<ReviewPanel actions={actions} setActions={() => { }} />);
        const button = screen.getByText('Schedule Selected');
        fireEvent.click(button);

        let statusMessage = null, alertMessage = null;

        try {
            statusMessage = await screen.findByRole('status', {}, { timeout: 5000 });
        } catch {
            // Not found
        }
        try {
            alertMessage = await screen.findByRole('alert', {}, { timeout: 5000 });
        } catch {
            // Not found
        }

        if (statusMessage) {
            expect(statusMessage).toHaveTextContent(/events scheduled successfully/i);
        } else if (alertMessage) {
            expect(alertMessage).toHaveTextContent(/error scheduling events/i);
        } else {
            throw new Error('Neither success nor error message rendered');
        }
    }, 20000);
});
