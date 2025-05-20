/**
 * File: ReviewPanel.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 * 
 * Description:
 * Unit tests for the ReviewPanel component in the AI Meeting Summarizer project.
 * These tests validate that the ReviewPanel renders action items, allows for their modification,
 * properly handles scheduling (including API/network error states), disables controls during
 * loading, and manages empty/invalid input states. Uses React Testing Library and Vitest (vi) for mocking.
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ReviewPanel from '../../components/ReviewPanel';
import axios from 'axios';
import React, { useState } from "react";

vi.mock('axios');

// Test utility wrapper to provide setActions for controlled input testing
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
    // Default actions for repeated use
    const defaultActions = [
        { text: 'Action A', owner: '', datetime: '', include: true },
        { text: 'Action B', owner: '', datetime: '', include: true }
    ];

    /**
     * Test: Renders actions with default input values.
     * Verifies that both action rows and their associated Owner inputs appear.
     */
    it('renders actions with default input values', () => {
        render(<ReviewPanel actions={defaultActions} setActions={() => { }} />);
        expect(screen.getAllByText("Action A").length).toBeGreaterThan(0);
        expect(screen.getAllByText("Action B").length).toBeGreaterThan(0);
        expect(screen.getAllByPlaceholderText("Owner").length).toBe(2);
        expect(screen.getAllByDisplayValue("").length).toBeGreaterThan(0);
    });

    /**
     * Test: Allows updating action fields (date, time).
     * Simulates user changing action input values and asserts state updates.
     */
    it('allows updating action fields', () => {
        const initialActions = [
            { text: "Action A", owner: "Alice", date: "", time: "" },
            { text: "Action B", owner: "Bob", date: "", time: "" },
        ];
        render(<Wrapper initialActions={initialActions} />);
        const dateInputs = screen.getAllByLabelText(/date/i);
        const timeInputs = screen.getAllByLabelText(/time/i);

        fireEvent.change(dateInputs[1], { target: { value: "2025-07-01" } });
        fireEvent.change(timeInputs[1], { target: { value: "12:00" } });

        expect(dateInputs[1].value).toBe("2025-07-01");
        expect(timeInputs[1].value).toBe("12:00");
    });

    /**
     * Test: Schedules actions and shows a success message.
     * Mocks a successful API response and ensures the success alert is displayed.
     */
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

    /**
     * Test: Shows error if scheduling fails due to API returning unsuccessful result.
     */
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

    /**
     * Test: Shows error if scheduling throws a network error.
     */
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

    /**
     * Test: Does not render any action rows if actions is empty.
     * Ensures the panel does not show controls if there are no actions.
     */
    it('does not render any action rows if actions is empty', () => {
        render(<ReviewPanel actions={[]} setActions={() => { }} />);
        expect(screen.queryByText(/owner/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/schedule selected/i)).not.toBeInTheDocument();
    });

    /**
     * Test: Disables schedule button after click (loading state).
     * Ensures UI disables the button to prevent double submissions.
     */
    it('disables schedule button after click (loading state)', async () => {
        render(<ReviewPanel actions={[{ text: "Test", owner: "Me", date: "2025-07-01", time: "12:00", duration: 60, include: true }]} setActions={() => { }} />);
        const button = screen.getByText(/schedule selected/i);
        fireEvent.click(button);
        await waitFor(() => {
            expect(button).toBeDisabled();
        });
    });

    /**
    * Test: Shows error if schedule is clicked with no included actions.
    * Simulates all checkboxes being unchecked and ensures error feedback.
    */
    it('shows error if schedule is clicked with no included actions', async () => {
        let actions = [{ text: "Action X", owner: "", date: "", time: "", include: false }];
        render(<ReviewPanel actions={actions} setActions={() => { }} />);
        fireEvent.click(screen.getByText(/schedule selected/i));
        await waitFor(() =>
            expect(screen.getByRole('alert')).toHaveTextContent(/error scheduling events/i)
        );
    });
});
