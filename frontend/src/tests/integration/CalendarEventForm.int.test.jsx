import { render, fireEvent } from "@testing-library/react";
import CalendarEventForm from '../../components/CalendarEventForm';

describe("CalendarEventForm (Integration)", () => {
    it("submits form and shows success or error message from backend", async () => {
        const { getByPlaceholderText, getByText, findByText, findByRole } = render(<CalendarEventForm />);
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

        let successMessage = null, alertMessage = null;

        try {
            successMessage = await findByText(
                (content) => /event created!|success/i.test(content),
                {},
                { timeout: 5000 }
            );
        } catch {
            // Not found
        }

        try {
            alertMessage = await findByRole('alert', {}, { timeout: 5000 });
        } catch {
            // Not found
        }

        if (successMessage) {
            expect(successMessage).toBeInTheDocument();
        } else if (alertMessage) {
            expect(alertMessage).toHaveTextContent(/request failed|error|not found|fail/i);
        } else {
            throw new Error('Neither success nor error message rendered');
        }
    }, 20000);
});
