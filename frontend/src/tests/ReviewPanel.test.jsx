import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ReviewPanel from '../components/ReviewPanel';
import axios from 'axios';

vi.mock('axios');

beforeEach(() => {
    vi.clearAllMocks(); // or axios.post.mockClear();
});

const defaultProps = {
    actions: [
        {
            text: 'Action A',
            owner: 'john@example.com',
            dateTime: '2025-05-15T15:30',
            include: true,
        },
    ],
    setActions: vi.fn(),
    onSchedule: vi.fn(),
};


describe('ReviewPanel Component', () => {
    const mockActions = [
        { text: 'Action A', owner: '', datetime: '', include: true },
        { text: 'Action B', owner: '', datetime: '', include: true }
    ];

    beforeEach(() => {
        axios.get.mockResolvedValue({ data: { access_token: 'mock_token' } });
        axios.post.mockResolvedValue({}); // success
    });
    it('renders actions with default input values', () => {
        const mockActions = [
            { text: "Follow up with client", owner: "", datetime: "", include: true }
        ];
        render(<ReviewPanel actions={mockActions} setActions={vi.fn()} />);

        expect(screen.getAllByText("Follow up with client").length).toBeGreaterThan(0);
        expect(screen.getByPlaceholderText("Owner")).toHaveValue("");

        const inputsWithEmptyValue = screen.getAllByDisplayValue("");
        // datetime input should be one of them
        const datetimeInput = inputsWithEmptyValue.find(input => input.type === "datetime-local");
        expect(datetimeInput).toBeInTheDocument();
    });


    it('updates owner and datetime fields when user types', () => {
        const mockSetActions = vi.fn();
        const mockActions = [{ text: "Prepare report", owner: "", datetime: "" }];

        render(<ReviewPanel actions={mockActions} setActions={mockSetActions} />);

        const ownerInputs = screen.getAllByPlaceholderText("Owner");
        fireEvent.change(ownerInputs[0], {
            target: { value: "alice@example.com" },
        });

        const datetimeInputs = screen.getAllByDisplayValue("");
        const datetimeInput = datetimeInputs.find(input => input.type === "datetime-local");
        fireEvent.change(datetimeInput, {
            target: { value: "2025-05-15T09:00" },
        });

        expect(mockSetActions).toHaveBeenCalledTimes(2);
    });


    it('disables button and shows "Scheduling..." while scheduling', async () => {
        const mockActions = [{ text: "Call Bob", owner: "bob@example.com", datetime: "2025-05-15T10:00" }];
        axios.get.mockResolvedValue({ data: { access_token: "mock_token" } });
        axios.post.mockResolvedValue({ status: 200 });

        render(<ReviewPanel actions={mockActions} setActions={vi.fn()} />);

        const button = screen.getByText("Schedule Selected");
        fireEvent.click(button);
        expect(button).toHaveTextContent("Scheduling...");

        await waitFor(() => {
            expect(screen.getByRole("status")).toHaveTextContent(/events scheduled successfully/i);
        });
    });

    it('shows error when token fetch fails', async () => {
        axios.get.mockRejectedValue(new Error("Token fetch failed"));
        render(<ReviewPanel actions={[{ text: "Email team" }]} setActions={vi.fn()} />);

        fireEvent.click(screen.getByText("Schedule Selected"));

        await waitFor(() =>
            expect(screen.getByRole("alert")).toHaveTextContent(/error fetching zoho token/i)
        );
    });

    it('shows error when scheduling fails', async () => {
        axios.get.mockResolvedValue({ data: { access_token: "mock_token" } });
        axios.post.mockRejectedValue(new Error("API failure"));

        render(<ReviewPanel actions={[{ text: "Sync calendar", owner: "x@y.com", datetime: "2025-05-15T09:00" }]} setActions={vi.fn()} />);

        fireEvent.click(screen.getByText("Schedule Selected"));

        await waitFor(() =>
            expect(screen.getByRole("alert")).toHaveTextContent(/error scheduling events/i)
        );
    });

    it('calls Zoho API with selected actions and shows success message', async () => {
        axios.get.mockResolvedValue({ data: { access_token: 'mock_token' } });
        axios.post.mockResolvedValue({ status: 200 });

        const { container } = render(<ReviewPanel {...defaultProps} />);
        // Fill in owner and datetime
        const ownerInput = screen.getByPlaceholderText('Owner');
        fireEvent.change(ownerInput, { target: { value: 'john@example.com' } });

        const datetimeInput = container.querySelector('input[type="datetime-local"]');
        fireEvent.change(datetimeInput, { target: { value: '2025-05-15T15:30' } });


        // Click the schedule button
        const button = screen.getByText('Schedule Selected');
        fireEvent.click(button);

        await waitFor(() => {
            expect(axios.get).toHaveBeenCalledWith('/api/zoho/access-token');
            const callsToZoho = axios.post.mock.calls.filter(
                ([url]) => url === 'https://www.zohoapis.com/calendar/v2/events'
            );
            expect(callsToZoho).toHaveLength(1);
            expect(axios.post).toHaveBeenCalledWith(
                'https://www.zohoapis.com/calendar/v2/events',
                {
                    event: {
                        title: 'Action A',
                        start_time: '2025-05-15T15:30',
                        end_time: '2025-05-15T15:30',
                        attendees: [{ email: 'john@example.com' }],
                    },
                },
                {
                    headers: {
                        Authorization: 'Zoho-oauthtoken mock_token',
                    },
                }
            );



        });

        expect(await screen.findByText(/Events scheduled successfully/i)).toBeInTheDocument();
    });
});
