import { scheduleActions } from "../utils/calendar_integration";
import { vi } from 'vitest';
import axios from "axios";

vi.mock("axios");

const mockActions = [
    { include: true, owner: 'Alice', datetime: '2025-05-14T14:30', summary: 'Prepare report' },
    { include: true, owner: 'Bob', datetime: '2025-05-14T15:00', summary: 'Action B' },
];

describe('calendarActions', () => {
    it('does not schedule actions that are not included', async () => {
        const mockActions = [
            { summary: 'Action A', owner: 'Alice', datetime: '2025-05-14T14:30', include: false },
            { summary: 'Action B', owner: 'Bob', datetime: '2025-05-14T15:00', include: true },
        ];

        axios.post.mockResolvedValue({});
        await scheduleActions(mockActions);
        expect(axios.post).toHaveBeenCalledTimes(1);
    });

    it("creates event with correct parameters", async () => {
        axios.post.mockResolvedValueOnce({ data: {} });

        await scheduleActions(mockActions);

        expect(axios.post).toHaveBeenCalledWith(
            "https://www.zohoapis.com/calendar/v2/events",
            {
                data: [
                    {
                        summary: "Prepare report",
                        owner: "Alice",
                        datetime: "2025-05-14T14:30",
                        include: true,
                    },
                    {
                        summary: "Action B",
                        owner: "Bob",
                        datetime: "2025-05-14T15:00",
                        include: true,
                    },
                ],
            }
        );
    });

    it("handles missing datetime gracefully", async () => {
        const actionsWithMissingDatetime = [
            { include: true, owner: "Alice", summary: "Do something" },
            { include: true, owner: "Bob", summary: "Another thing", datetime: "2025-05-14T15:00" },
            { include: true, owner: "Carol", summary: "Third task" }
        ];

        axios.post.mockClear();
        await scheduleActions(actionsWithMissingDatetime);

        expect(axios.post).toHaveBeenCalledTimes(1);
        expect(axios.post).toHaveBeenCalledWith(
            "https://www.zohoapis.com/calendar/v2/events",
            {
                data: [
                    {
                        include: true,
                        owner: "Bob",
                        summary: "Another thing",
                        datetime: "2025-05-14T15:00"
                    }
                ]
            }
        );
    });

    it("handles API error gracefully", async () => {
        axios.post.mockRejectedValueOnce(new Error("Error scheduling events"));

        try {
            await scheduleActions(mockActions);
        } catch (error) {
            expect(error.message).toBe("Error scheduling events");
        }
    });
});


it("creates event with correct parameters when only included actions are passed", async () => {
    axios.post.mockResolvedValueOnce({ data: {} });

    const includedActions = mockActions.filter((action) => action.include);

    await scheduleActions(includedActions);

    expect(axios.post).toHaveBeenCalledWith(
        "https://www.zohoapis.com/calendar/v2/events",
        {
            data: [
                {
                    summary: "Prepare report",
                    owner: "Alice",
                    datetime: "2025-05-14T14:30", // changed from start_time to datetime
                    include: true,
                },
                {
                    summary: "Action B",
                    owner: "Bob",
                    datetime: "2025-05-14T15:00", // changed from start_time to datetime
                    include: true,
                },
            ],
        }
    );
});

