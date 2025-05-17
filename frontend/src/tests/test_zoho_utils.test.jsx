import { vi } from 'vitest';
import axios from 'axios';
import * as zoho from '../utils/zoho_utils.jsx';

vi.mock('axios');

global.fetch = vi.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ access_token: 'test_token' })
    })
);

const mockActions = [
    {
        datetime: '2025-05-14T14:30',
        include: true,
        owner: 'Alice',
        summary: 'Prepare report'
    },
    {
        datetime: '2025-05-14T15:00',
        include: true,
        owner: 'Bob',
        summary: 'Action B'
    }
];


describe('zoho_utils', () => {
    beforeEach(() => {
        axios.post.mockClear(); // Reset the mock before each test
    });
    describe('createEvent', () => {
        it('does not schedule actions that are not included', async () => {
            const actions = [
                { summary: 'Action A', owner: 'Alice', datetime: '2025-05-14T14:30', include: false },
                { summary: 'Action B', owner: 'Bob', datetime: '2025-05-14T15:00', include: true },
            ];

            axios.post.mockResolvedValue({});
            await zoho.createEvent(actions);
            expect(axios.post).toHaveBeenCalledTimes(1);
        });

        it("creates event with correct parameters", async () => {
            axios.post.mockResolvedValueOnce({});

            await zoho.createEvent(mockActions);

            expect(axios.post).toHaveBeenCalledWith(
                "http://localhost:5000/create-event",
                mockActions
            );
        });

        it('handles missing datetime gracefully', async () => {
            const mockActions = [
                { summary: 'Do something', owner: 'Alice', include: true },
                { summary: 'Another thing', owner: 'Bob', datetime: '2025-05-14T15:00', include: true },
                { summary: 'Third task', owner: 'Carol', include: true }
            ];

            axios.post.mockResolvedValue({ data: { message: 'event created' } });

            await zoho.createEvent(mockActions);

            // Update your expectation to match actual behavior
            expect(axios.post).toHaveBeenCalledTimes(1);
            expect(axios.post).toHaveBeenCalledWith(
                "http://localhost:5000/create-event",
                [
                    { datetime: '2025-05-14T15:00', include: true, owner: 'Bob', summary: 'Another thing' }
                ]
            );
        });


        it("handles API error gracefully", async () => {
            axios.post.mockRejectedValueOnce(new Error("Error scheduling events"));

            await expect(zoho.createEvent(mockActions)).rejects.toThrow("Error creating event via backend");
        });

        it("creates event with correct parameters when only included actions are passed", async () => {
            axios.post.mockResolvedValueOnce({});

            const includedActions = mockActions.filter((action) => action.include);

            await zoho.createEvent(includedActions);

            expect(axios.post).toHaveBeenCalledWith(
                "http://localhost:5000/create-event",
                includedActions
            );
        });

        it('creates an event with valid input', async () => {
            const mockActions = [
                { include: true, datetime: '2025-05-20T15:00', title: 'Test', description: 'desc', owner: 'Alice' }
            ];
            const result = await zoho.createEvent(mockActions);
            expect(result).toEqual({ message: 'event created' });
            expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/create-event', mockActions);
        });

        it('throws error on request failure', async () => {
            axios.post.mockRejectedValue(new Error('Network Error'));
            await expect(zoho.createEvent({})).rejects.toThrow('Error creating event via backend');
        });
    });

    describe('getAccessToken', () => {
        it('returns access token from Zoho', async () => {
            const token = await zoho.getAccessToken();
            expect(token).toBe('test_token');
        });

        it('throws error on failure', async () => {
            fetch.mockImplementationOnce(() => Promise.reject('fail'));
            await expect(zoho.getAccessToken()).rejects.toBe('fail');
        });
    });
    describe('formatEventData', () => {
        it('formats event correctly with owner', () => {
            const action = { text: 'Meeting', datetime: '2025-05-20T15:00', owner: 'bob@example.com' };
            const result = zoho.formatEventData(action);
            expect(result).toEqual({
                summary: 'Meeting',
                start: { dateTime: '2025-05-20T15:00', timeZone: 'America/New_York' },
                end: { dateTime: '2025-05-20T15:00', timeZone: 'America/New_York' },
                attendees: [{ email: 'bob@example.com' }]
            });
        });

        it('formats event correctly without owner', () => {
            const action = { text: 'Call', datetime: '2025-05-20T12:00' };
            const result = zoho.formatEventData(action);
            expect(result.attendees).toEqual([]);
        });
    });

    describe('listEvents', () => {
        it('returns event data on success', async () => {
            const mockData = { events: [{ id: 1, summary: 'Mock Event' }] };
            axios.get.mockResolvedValueOnce({ data: mockData });
            const result = await zoho.listEvents();
            expect(result).toEqual(mockData);
        });

        it('throws error on failure', async () => {
            axios.get.mockRejectedValueOnce(new Error('Fetch failed'));
            await expect(zoho.listEvents()).rejects.toThrow('Failed to list events');
        });
    });
});
