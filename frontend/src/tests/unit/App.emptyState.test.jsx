// src/tests/unit/App.emptyState.test.jsx
import { render, screen } from '@testing-library/react';
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

test('does not render summary, decisions, or actions if state is empty', () => {
    render(<App />);
    expect(screen.queryByText(/summary:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/decisions:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/review and schedule actions/i)).not.toBeInTheDocument();
});
