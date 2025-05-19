import { render, screen, fireEvent } from '@testing-library/react';
import NextcloudConnect from '../../components/NextcloudConnect';

describe('NextcloudConnect (Integration)', () => {
    beforeEach(() => {
        window.open = vi.fn();
    });

    it('opens Nextcloud dashboard', () => {
        render(<NextcloudConnect />);
        const btn = screen.getByRole('button', { name: /Connect to Nextcloud/i });
        fireEvent.click(btn);
        expect(window.open).toHaveBeenCalledWith('http://localhost:8080/apps/dashboard/', '_blank');
    }, 20000);
});
