/**
 * @file ReviewPanel.int.test.jsx
 * @author Eric Morse
 * @date May 11th, 2025
 * @description
 *   Integration tests for the ReviewPanel component.
 *   This test suite verifies that the ReviewPanel component interacts
 *   with the backend to schedule actions and properly displays
 *   real success or error messages based on backend responses.
 *
 *   The tests here run against the actual backend (not mocked),
 *   making sure the full user flow from UI interaction to backend
 *   response and user feedback is working as intended.
 *
 *   Usage:
 *     Run this test with your testing framework (e.g., Vitest or Jest)
 *     after ensuring your backend is running and accessible to the frontend.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import ReviewPanel from '../../components/ReviewPanel';

describe('ReviewPanel Integration', () => {
    /**
     * Test: schedules actions and shows real success or error message from backend
     *
     * This integration test checks that clicking the "Schedule Selected" button
     * in ReviewPanel triggers a backend API call, and that the UI displays
     * either a success message (role="status") or an error alert (role="alert"),
     * depending on the backend's response.
     */
    it('schedules actions and shows real success or error message from backend', async () => {
        // Test action input
        const actions = [
            { text: 'Integration Action', owner: 'test@example.com', datetime: '2025-06-01T10:00', include: true }
        ];
        // Render ReviewPanel with test actions
        render(<ReviewPanel actions={actions} setActions={() => { }} />);
        // Find and click the schedule button
        const button = screen.getByText('Schedule Selected');
        fireEvent.click(button);

        let statusMessage = null, alertMessage = null;

        try {
            statusMessage = await screen.findByRole('status', {}, { timeout: 5000 });
        } catch {
            // Success message not found
        }
        try {
            alertMessage = await screen.findByRole('alert', {}, { timeout: 5000 });
        } catch {
            // Error alert not found
        }
        // Assert that a result message was shown to the user
        if (statusMessage) {
            // Successful scheduling feedback
            expect(statusMessage).toHaveTextContent(/events scheduled successfully/i);
        } else if (alertMessage) {
            // Error feedback
            expect(alertMessage).toHaveTextContent(/error scheduling events/i);
        } else {
            // Neither message found – fail the test
            throw new Error('Neither success nor error message rendered');
        }
    }, 20000); // Increase timeout for backend roundtrip
});
