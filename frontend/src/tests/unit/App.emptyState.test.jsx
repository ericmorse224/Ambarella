/**
 * @file App.emptyState.test.jsx
 * @author Eric Morse
 * @date May 11th 2025
 * @description
 * Unit test for the App component's empty state behavior.
 * Verifies that the summary, decisions, and review actions
 * are not rendered when the state is empty (no transcript,
 * no summary, no actions, no decisions).
 */
import { render, screen } from '@testing-library/react';

// Mock the UseMeetingState hook to simulate empty state
vi.mock('../../hooks/UseMeetingState', () => ({
    default: () => ({
        transcript: '',
        summary: [],
        actions: [],
        decisions: [],
        isLoading: false,
        uploadAttempts: 0,
        processAudio: vi.fn(),
        processTranscript: vi.fn(),
        setActions: vi.fn(),
        error: '',
    }),
}));
import App from '../../App';

/**
 * Test: Ensure the app does not render summary, decisions,
 * or review actions if the meeting state is empty.
 */
test('does not render summary, decisions, or actions if state is empty', () => {
    render(<App />);
    expect(screen.queryByText(/summary:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/decisions:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/review and schedule actions/i)).not.toBeInTheDocument();
});
