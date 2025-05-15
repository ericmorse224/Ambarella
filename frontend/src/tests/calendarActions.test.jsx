import { scheduleActions ***REMOVED*** from "../utils/calendar_integration";
import { vi ***REMOVED*** from 'vitest';
import axios from "axios";

vi.mock("axios");

const mockActions = [
  { include: true, owner: 'Alice', datetime: '2025-05-14T14:30', summary: 'Prepare report' ***REMOVED***,
  { include: true, owner: 'Bob', datetime: '2025-05-14T15:00', summary: 'Action B' ***REMOVED***,
];

describe('calendarActions', () => {
  it('does not schedule actions that are not included', async () => {
    const mockActions = [
      { summary: 'Action A', owner: 'Alice', datetime: '2025-05-14T14:30', include: false ***REMOVED***,
      { summary: 'Action B', owner: 'Bob', datetime: '2025-05-14T15:00', include: true ***REMOVED***,
    ];

    axios.post.mockResolvedValue({***REMOVED***);

    await scheduleActions(mockActions);

    expect(axios.post).toHaveBeenCalledTimes(1); // Only one action should be scheduled
  ***REMOVED***);

  it("creates event with correct parameters", async () => {
    axios.post.mockResolvedValueOnce({ data: {***REMOVED*** ***REMOVED***);

    await scheduleActions(mockActions);

    expect(axios.post).toHaveBeenCalledWith(
      "https://www.zohoapis.com/calendar/v2/events",
      {
        data: [
          {
            summary: "Prepare report",
            owner: "Alice",
            datetime: "2025-05-14T14:30", // changed from start_time to datetime
            include: true,
          ***REMOVED***,
          {
            summary: "Action B",
            owner: "Bob",
            datetime: "2025-05-14T15:00", // changed from start_time to datetime
            include: true,
          ***REMOVED***,
        ],
      ***REMOVED***
    );
  ***REMOVED***);

  it("handles missing datetime gracefully", async () => {
    const actionsWithMissingDatetime = [
      { include: true, owner: "Alice", summary: "Do something" ***REMOVED***, // Missing datetime
      { include: true, owner: "Bob", summary: "Another thing", datetime: "2025-05-14T15:00" ***REMOVED***,
      { include: true, owner: "Carol", summary: "Third task" ***REMOVED*** // Missing datetime
    ];

    axios.post.mockClear(); // 👈 Clear previous calls if any
    await scheduleActions(actionsWithMissingDatetime);

    // Expect only one call for the single valid datetime
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
          ***REMOVED***
        ]
      ***REMOVED***
    );
  ***REMOVED***);


  it("handles API error gracefully", async () => {
    axios.post.mockRejectedValueOnce(new Error("Error scheduling events"));

    try {
      await scheduleActions(mockActions);
    ***REMOVED*** catch (error) {
      expect(error.message).toBe("Error scheduling events");
    ***REMOVED***
  ***REMOVED***);

  it("creates event with correct parameters when only included actions are passed", async () => {
    axios.post.mockResolvedValueOnce({ data: {***REMOVED*** ***REMOVED***);

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
          ***REMOVED***,
          {
            summary: "Action B",
            owner: "Bob",
            datetime: "2025-05-14T15:00", // changed from start_time to datetime
            include: true,
          ***REMOVED***,
        ],
      ***REMOVED***
    );
  ***REMOVED***);
***REMOVED***);
