import { render, screen, fireEvent } from '@testing-library/react';
import ReviewPanel from '../components/ReviewPanel';
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios'); // Only mock the external dependency

const sampleActions = [
    { text: 'Action A', owner: 'Alice', dueDate: '2025-05-14T14:30', include: true },
    { text: 'Action B', owner: 'Bob', dueDate: '2025-05-14T15:00', include: true },
];

describe('ReviewPanel Component', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    test('renders action inputs', () => {
        render(<ReviewPanel actions={sampleActions} />);
        expect(screen.getByDisplayValue('Alice')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Bob')).toBeInTheDocument();
    });

    test('shows error message when Zoho token fetch fails', async () => {
        axios.get.mockRejectedValueOnce(new Error('Network Error'));

        render(<ReviewPanel actions={sampleActions} />);
        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i }));

        const errorMessage = await screen.findByText(/Error fetching Zoho token/i);
        expect(errorMessage).toBeInTheDocument();
    });

    test('shows success message when actions are scheduled', async () => {
        axios.get.mockResolvedValueOnce({ data: { access_token: 'mock_token' } });
        axios.post.mockResolvedValueOnce({ status: 200 });

        render(<ReviewPanel actions={sampleActions} />);
        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i }));

        const successMessage = await screen.findByText(/Scheduled successfully!/i);
        expect(successMessage).toBeInTheDocument();
    });

    test('shows error message when scheduling fails', async () => {
        axios.get.mockResolvedValueOnce({ data: { access_token: 'mock_token' } });
        axios.post.mockRejectedValueOnce(new Error('Error scheduling events'));

        render(<ReviewPanel actions={sampleActions} />);
        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i }));

        const errorMessage = await screen.findByText(/Error scheduling events/i);
        expect(errorMessage).toBeInTheDocument();
    });
});

