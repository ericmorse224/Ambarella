import { render, screen, fireEvent ***REMOVED*** from '@testing-library/react';
import ReviewPanel from '../components/ReviewPanel';
import axios from 'axios';
import { vi ***REMOVED*** from 'vitest';

// Mock axios
vi.mock('axios');

// Sample actions for testing
const sampleActions = [
    {
        text: 'Action A',
        owner: 'Alice',
        dueDate: '2025-05-14T14:30',
        include: true,
    ***REMOVED***,
    {
        text: 'Action B',
        owner: 'Bob',
        dueDate: '2025-05-14T15:00',
        include: true,
    ***REMOVED***,
];

describe('ReviewPanel Component', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    ***REMOVED***);

    test('updates owner field correctly', () => {
        render(<ReviewPanel actions={sampleActions***REMOVED*** />);
        expect(screen.getByDisplayValue('Alice')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Bob')).toBeInTheDocument();
    ***REMOVED***);

    test('shows error message when Zoho token fetch fails', async () => {
        axios.get.mockRejectedValueOnce(new Error('Network Error'));

        render(<ReviewPanel actions={sampleActions***REMOVED*** />);

        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i ***REMOVED***));

        const errorMessage = await screen.findByText(/Error fetching Zoho token/i);
        expect(errorMessage).toBeInTheDocument();
    ***REMOVED***);

    test('shows success message when actions are scheduled', async () => {
        axios.get.mockResolvedValueOnce({ data: { access_token: 'mock_token' ***REMOVED*** ***REMOVED***);
        axios.post.mockResolvedValueOnce({ status: 200 ***REMOVED***);

        render(<ReviewPanel actions={sampleActions***REMOVED*** />);

        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i ***REMOVED***));

        const successMessage = await screen.findByText(/Scheduled successfully!/i);
        expect(successMessage).toBeInTheDocument();
    ***REMOVED***);

    test('shows error message when scheduling fails', async () => {
        axios.get.mockResolvedValueOnce({ data: { access_token: 'mock_token' ***REMOVED*** ***REMOVED***);
        axios.post.mockRejectedValueOnce(new Error('Error scheduling events'));

        render(<ReviewPanel actions={sampleActions***REMOVED*** />);

        fireEvent.click(screen.getByRole('button', { name: /schedule selected/i ***REMOVED***));

        const errorMessage = await screen.findByText(/Error scheduling events/i);
        expect(errorMessage).toBeInTheDocument();
    ***REMOVED***);
***REMOVED***);
