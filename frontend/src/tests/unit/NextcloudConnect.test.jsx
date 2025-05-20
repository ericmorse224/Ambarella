/**
 * File: NextcloudConnect.test.jsx
 * Author: Eric Morse
 * Date: May 11th 2025
 * 
 * Description:
 * This file contains unit tests for the NextcloudConnect component. It uses the
 * React Testing Library to verify that the "Connect to Nextcloud" button renders
 * correctly and that clicking the button opens the Nextcloud dashboard in a new browser tab.
 * 
 * The tests mock the global `window.open` function to ensure it is called with the expected
 * arguments and do not actually open a browser window during testing.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import NextcloudConnect from '../../components/NextcloudConnect';

describe('NextcloudConnect', () => {
    beforeEach(() => {
        // Mock window.open before each test
        window.open = vi.fn();
    });

    test('renders button and opens Nextcloud dashboard on click', () => {
        // Render the component
        render(<NextcloudConnect />);
        // Get the button by its accessible name
        const btn = screen.getByRole('button', { name: /Connect to Nextcloud/i });
        // Simulate a click event on the button
        fireEvent.click(btn);
        // Assert that window.open was called with the correct Nextcloud dashboard URL
        expect(window.open).toHaveBeenCalledWith('http://localhost:8080/apps/dashboard/', '_blank');
    });
});
