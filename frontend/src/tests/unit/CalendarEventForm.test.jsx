/**
 * File: CalendarEventForm.test.jsx
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 *   Unit tests for the CalendarEventForm component. This file tests all
 *   major behaviors, including rendering, form submission, error handling,
 *   and interaction with the backend API (mocked via axios).
 * 
 *   The test suite uses React Testing Library and Vitest.
 * 
 * Key Test Cases:
 *   - Renders all required form fields and the submit button
 *   - Handles successful event creation and form reset
 *   - Handles backend error messages (from API)
 *   - Handles generic network errors and displays a generic alert
 */

import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import CalendarEventForm from '../../components/CalendarEventForm';
import axios from "axios";

// Mock axios for backend API calls
vi.mock("axios");

describe("CalendarEventForm", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    // Test that all fields and the button are present in the form
    it("renders all inputs and button", () => {
        render(<CalendarEventForm />);
        expect(screen.getByPlaceholderText("Title")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Description")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Participant Email")).toBeInTheDocument();
        expect(screen.getByText("Create Event")).toBeInTheDocument();
    });

    // Test that submitting the form triggers a backend request and shows success
    it("submits form and shows success message", async () => {
        axios.post.mockResolvedValueOnce({ data: { status: "success" } });

        render(<CalendarEventForm />);

        fireEvent.change(screen.getByPlaceholderText("Title"), { target: { value: "My Event" } });
        fireEvent.change(screen.getByPlaceholderText("Description"), { target: { value: "A test event" } });
        fireEvent.change(screen.getByPlaceholderText("Participant Email"), { target: { value: "bob@example.com" } });
        fireEvent.change(screen.getByPlaceholderText("Date"), { target: { value: "2025-06-01" } });
        fireEvent.change(screen.getByPlaceholderText("Time"), { target: { value: "12:30" } });

        fireEvent.click(screen.getByText("Create Event"));

        await waitFor(() =>
            expect(screen.getByRole("status")).toHaveTextContent(/event created/i)
        );

        // Form should reset after success
        expect(screen.getByPlaceholderText("Title").value).toBe("");
        expect(screen.getByPlaceholderText("Description").value).toBe("");
        expect(screen.getByPlaceholderText("Participant Email").value).toBe("");
        expect(screen.getByLabelText(/date/i).value).toBe("");
        expect(screen.getByLabelText(/time/i).value).toBe("");
    });

    // Test backend error responses (from the API)
    it("shows backend error", async () => {
        axios.post.mockRejectedValueOnce({ response: { data: { error: "Backend error" } } });

        render(<CalendarEventForm />);
        // Fill in the form fields...
        fireEvent.change(screen.getByLabelText(/title/i), { target: { value: "Event" } });
        fireEvent.change(screen.getByLabelText(/description/i), { target: { value: "Desc" } });
        fireEvent.change(screen.getByLabelText(/date/i), { target: { value: "2025-06-01" } });
        fireEvent.change(screen.getByLabelText(/time/i), { target: { value: "12:30" } });
        fireEvent.change(screen.getByLabelText(/participant email/i), { target: { value: "bob@example.com" } });

        fireEvent.click(screen.getByText(/create event/i));

        await waitFor(() =>
            expect(screen.getByRole("alert")).toHaveTextContent("Backend error")
        );
    });

    // Test error display for thrown axios errors with .response.data.error
    it("shows axios thrown error", async () => {
        axios.post.mockRejectedValueOnce({ response: { data: { error: "Server down" } } });

        render(<CalendarEventForm />);
        fireEvent.change(screen.getByPlaceholderText("Title"), { target: { value: "My Event" } });
        fireEvent.change(screen.getByPlaceholderText("Description"), { target: { value: "A test event" } });
        fireEvent.change(screen.getByPlaceholderText("Participant Email"), { target: { value: "bob@example.com" } });
        fireEvent.change(screen.getByPlaceholderText("Date"), { target: { value: "2025-06-01" } });
        fireEvent.change(screen.getByPlaceholderText("Time"), { target: { value: "12:30" } });

        fireEvent.click(screen.getByText("Create Event"));

        await waitFor(() =>
            expect(screen.getByRole("alert")).toHaveTextContent("Server down")
        );
    });

    it("shows network error (generic error message)", async () => {
        axios.post.mockRejectedValueOnce(new Error("Network Error"));

        render(<CalendarEventForm />);
        fireEvent.change(screen.getByPlaceholderText("Title"), { target: { value: "My Event" } });
        fireEvent.change(screen.getByPlaceholderText("Description"), { target: { value: "A test event" } });
        fireEvent.change(screen.getByPlaceholderText("Participant Email"), { target: { value: "bob@example.com" } });
        fireEvent.change(screen.getByPlaceholderText("Date"), { target: { value: "2025-06-01" } });
        fireEvent.change(screen.getByPlaceholderText("Time"), { target: { value: "12:30" } });

        fireEvent.click(screen.getByText("Create Event"));

        await waitFor(() =>
            expect(screen.getByRole("alert")).toHaveTextContent(/network error/i)
        );
    });
});
