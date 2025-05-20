/**
 * File: NextcloudConnect.int.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 *   Integration test for the NextcloudConnect component.
 *   This test suite verifies that the "Connect to Nextcloud" button
 *   in the NextcloudConnect component correctly opens the Nextcloud
 *   dashboard URL in a new browser tab/window when clicked.
 *
 *   The test mocks `window.open` to intercept calls and checks the
 *   correct URL and target are used.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import NextcloudConnect from '../../components/NextcloudConnect';

describe('NextcloudConnect (Integration)', () => {
    // Before each test, mock window.open
    beforeEach(() => {
        window.open = vi.fn();
    });

    // Test: Should open Nextcloud dashboard when button is clicked
    it('opens Nextcloud dashboard', () => {
        render(<NextcloudConnect />);
        const btn = screen.getByRole('button', { name: /Connect to Nextcloud/i });
        fireEvent.click(btn);
        expect(window.open).toHaveBeenCalledWith('http://localhost:8080/apps/dashboard/', '_blank');
    }, 20000);
});
