import { render, fireEvent, waitFor } from "@testing-library/react";
import CalendarEventForm from '../../components/CalendarEventForm';

describe("CalendarEventForm (Integration)", () => {
    it("submits form and shows success message from backend", async () => {
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
        const successMessage = await findByText(/Event created!|success/i, {}, { timeout: 5000 });
        expect(successMessage).toBeInTheDocument();
    }, 20000);
});
