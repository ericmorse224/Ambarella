import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import CalendarEventForm from '../../components/CalendarEventForm';
import axios from "axios";

// Mock axios
vi.mock("axios");

describe("CalendarEventForm", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("renders all inputs and button", () => {
        render(<CalendarEventForm />);
        expect(screen.getByPlaceholderText("Title")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Description")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Participant Email")).toBeInTheDocument();
        expect(screen.getByText("Create Event")).toBeInTheDocument();
    });

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

        // After success, form resets
        expect(screen.getByPlaceholderText("Title").value).toBe("");
        expect(screen.getByPlaceholderText("Description").value).toBe("");
        expect(screen.getByPlaceholderText("Participant Email").value).toBe("");
        expect(screen.getByLabelText(/date/i).value).toBe("");
        expect(screen.getByLabelText(/time/i).value).toBe("");
    });

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
