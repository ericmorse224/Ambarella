import { render, screen, fireEvent } from '@testing-library/react';
import NextcloudConnect from '../../components/NextcloudConnect';

describe('NextcloudConnect', () => {
    beforeEach(() => {
        window.open = vi.fn();
    });

    test('renders button and opens Nextcloud dashboard on click', () => {
        render(<NextcloudConnect />);
        const btn = screen.getByRole('button', { name: /Connect to Nextcloud/i });
        fireEvent.click(btn);
        expect(window.open).toHaveBeenCalledWith('http://localhost:8080/apps/dashboard/', '_blank');
    });
});
