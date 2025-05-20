/**
 * CalendarEventForm.int.test.jsx
 * Integration test for the CalendarEventForm component.
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * This test suite verifies the integration between the CalendarEventForm UI and
 * the (mocked) backend response. It checks whether the form correctly submits event data
 * and properly displays either a success message or an error/alert message depending on
 * the response from the backend.
 *
 * The test simulates user interaction:
 *   - Fills in the Title, Description, Participant Email, Date, and Time fields
 *   - Submits the form by clicking "Create Event"
 *   - Waits for a success or error message to appear
 *   - Asserts that one or the other is rendered appropriately
 *
 * The test passes if:
 *   - A success message with "event created" or "success" is rendered, OR
 *   - An error/alert message matching "request failed", "error", "not found", or "fail" is rendered
 *   - Otherwise, the test fails if neither message appears
 */
import { render, fireEvent } from "@testing-library/react";
import CalendarEventForm from '../../components/CalendarEventForm';

describe("CalendarEventForm (Integration)", () => {
    it("submits form and shows success or error message from backend", async () => {
        const { getByPlaceholderText, getByText, findByText, findByRole } = render(<CalendarEventForm />);
        // Fill out form fields
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
        // Submit the form
        fireEvent.click(getByText("Create Event"));

        let successMessage = null, alertMessage = null;

        // Try to find a success message
        try {
            successMessage = await findByText(
                (content) => /event created!|success/i.test(content),
                {},
                { timeout: 5000 }
            );
        } catch {
            // Not found
        }
        // Try to find an error alert
        try {
            alertMessage = await findByRole('alert', {}, { timeout: 5000 });
        } catch {
            // Not found
        }
        // Assert that either a success or an error message is shown
        if (successMessage) {
            expect(successMessage).toBeInTheDocument();
        } else if (alertMessage) {
            expect(alertMessage).toHaveTextContent(/request failed|error|not found|fail/i);
        } else {
            throw new Error('Neither success nor error message rendered');
        }
    }, 20000);
});
