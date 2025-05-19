import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ReviewPanel from '../../components/ReviewPanel';
import axios from 'axios';
import React, { useState } from "react";

vi.mock('axios');

function Wrapper({ initialActions }) {
    const [actions, setActions] = useState(initialActions);
    return (
        <ReviewPanel
            actions={actions}
            setActions={setActions}
            loading={false}
            error={null}
            onSchedule={() => { }}
        />
    );
}

describe('ReviewPanel Component', () => {
    const defaultActions = [
        { text: 'Action A', owner: '', datetime: '', include: true },
        { text: 'Action B', owner: '', datetime: '', include: true }
    ];

    it('renders actions with default input values', () => {
        render(<ReviewPanel actions={defaultActions} setActions={() => { }} />);
        expect(screen.getAllByText("Action A").length).toBeGreaterThan(0);
        expect(screen.getAllByText("Action B").length).toBeGreaterThan(0);
        expect(screen.getAllByPlaceholderText("Owner").length).toBe(2);
        expect(screen.getAllByDisplayValue("").length).toBeGreaterThan(0);
    });

    it('allows updating action fields', () => {
        const initialActions = [
            { text: "Action A", owner: "Alice", datetime: "" },
            { text: "Action B", owner: "Bob", datetime: "" },
        ];
        render(<Wrapper initialActions={initialActions} />);
        const datetimeInputs = screen.getAllByDisplayValue("");
        fireEvent.change(datetimeInputs[1], { target: { value: "2025-07-01T12:00" } });
        expect(datetimeInputs[1].value).toBe("2025-07-01T12:00");
    });

    it('schedules actions and shows success message', async () => {
        let actions = [
            { text: 'Action C', owner: 'Alice', datetime: '2025-07-01T15:00', include: true }
        ];
        const setActions = () => { };
        axios.post.mockResolvedValue({ data: { success: true } });
        render(<ReviewPanel actions={actions} setActions={setActions} />);
        fireEvent.click(screen.getByText('Schedule Selected'));
        await waitFor(() =>
            expect(screen.getByRole('status')).toHaveTextContent(/events scheduled successfully/i)
        );
    });

    it('shows error if scheduling fails (API error)', async () => {
        let actions = [
            { text: 'Action D', owner: 'Bob', datetime: '2025-07-02T14:00', include: true }
        ];
        const setActions = () => { };
        axios.post.mockResolvedValue({ data: { success: false } });
        render(<ReviewPanel actions={actions} setActions={setActions} />);
        fireEvent.click(screen.getByText('Schedule Selected'));
        await waitFor(() =>
            expect(screen.getByRole('alert')).toHaveTextContent(/error scheduling events/i)
        );
    });

    it('shows error if scheduling throws (network)', async () => {
        let actions = [
            { text: 'Action E', owner: 'Frank', datetime: '2025-07-03T14:00', include: true }
        ];
        const setActions = () => { };
        axios.post.mockRejectedValue(new Error("Network error"));
        render(<ReviewPanel actions={actions} setActions={setActions} />);
        fireEvent.click(screen.getByText('Schedule Selected'));
        await waitFor(() =>
            expect(screen.getByRole('alert')).toHaveTextContent(/error scheduling events/i)
        );
    });
});
