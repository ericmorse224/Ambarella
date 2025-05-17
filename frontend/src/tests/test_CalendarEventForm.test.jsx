import { render, fireEvent, waitFor } from "@testing-library/react";
import CalendarEventForm from "../components/CalendarEventForm";
import axios from "axios";
import { vi } from "vitest";

// Mock axios
vi.mock("axios");

describe("CalendarEventForm", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("submits form and shows success message", async () => {
        axios.post.mockResolvedValueOnce({ status: 200 });

        const { getByPlaceholderText, getByText, findByText } = render(<CalendarEventForm />);

        fireEvent.change(getByPlaceholderText("Title"), { target: { value: "Meeting" } });
        fireEvent.change(getByPlaceholderText("Description"), { target: { value: "Discuss stuff" } });
        fireEvent.change(getByPlaceholderText("Participant Email"), {
            target: { value: "test@example.com" },
        });

        fireEvent.change(getByPlaceholderText("Title").closest("form").querySelector('input[type="date"]'), {
            target: { value: "2025-05-20" },
        });

        fireEvent.change(getByPlaceholderText("Title").closest("form").querySelector('input[type="time"]'), {
            target: { value: "15:00" },
        });

        fireEvent.click(getByText("Create Event"));

        await findByText("Event created!");
    });

    it("shows error on failed request", async () => {
        axios.post.mockRejectedValueOnce(new Error("Network Error"));

        const { getByPlaceholderText, getByText, findByText } = render(<CalendarEventForm />);

        fireEvent.change(getByPlaceholderText("Title"), { target: { value: "Meeting" } });
        fireEvent.change(getByPlaceholderText("Description"), { target: { value: "Discuss stuff" } });
        fireEvent.change(getByPlaceholderText("Participant Email"), {
            target: { value: "test@example.com" },
        });

        fireEvent.change(getByPlaceholderText("Title").closest("form").querySelector('input[type="date"]'), {
            target: { value: "2025-05-20" },
        });

        fireEvent.change(getByPlaceholderText("Title").closest("form").querySelector('input[type="time"]'), {
            target: { value: "15:00" },
        });

        fireEvent.click(getByText("Create Event"));

        await findByText("Failed to create event.");
    });
});
