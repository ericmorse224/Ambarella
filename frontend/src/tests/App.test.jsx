import { render, screen, fireEvent, waitFor ***REMOVED*** from "@testing-library/react";
import App from "./App";
import { vi ***REMOVED*** from "vitest";

// Mock global fetch
beforeEach(() => {
    vi.restoreAllMocks();
***REMOVED***);

global.fetch = vi.fn();

vi.mock("./hooks/useMeetingState", () => ({
    default: () => ({
        transcript: "Test transcript",
        setTranscript: vi.fn(),
        summary: ["Summary A"],
        setSummary: vi.fn(),
        actions: [
            { text: "Action A", owner: "", datetime: "", include: true ***REMOVED***
        ],
        setActions: vi.fn(),
        decisions: ["Decision A"],
        setDecisions: vi.fn()
    ***REMOVED***)
***REMOVED***));

describe("App Component", () => {
    it("alerts on large file upload", async () => {
        const alertMock = vi.spyOn(window, "alert").mockImplementation(() => { ***REMOVED***);
        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const largeFile = new File(["a".repeat(11 * 1024 * 1024)], "large.mp3", {
            type: "audio/mp3"
        ***REMOVED***);

        await waitFor(() =>
            fireEvent.change(fileInput, { target: { files: [largeFile] ***REMOVED*** ***REMOVED***)
        );

        expect(alertMock).toHaveBeenCalledWith("File size exceeds 10MB limit.");
        alertMock.mockRestore();
    ***REMOVED***);

    it("fetches and processes audio correctly", async () => {
        fetch
            .mockResolvedValueOnce({
                ok: true,
                json: async () => ({ transcript: "Test transcript", entities: [] ***REMOVED***)
            ***REMOVED***)
            .mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    summary: ["Summary A"],
                    actions: ["Action A"],
                    decisions: ["Decision A"]
                ***REMOVED***)
            ***REMOVED***);

        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const validFile = new File(["audio"], "audio.mp3", { type: "audio/mp3" ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [validFile] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole("button", { name: /Upload & Analyze/i ***REMOVED***));

        await waitFor(() => {
            expect(screen.getByText(/Test transcript/i)).toBeInTheDocument();
            expect(screen.getByText(/Summary A/i)).toBeInTheDocument();
            expect(screen.getByText(/Action A/i)).toBeInTheDocument();
            expect(screen.getByText(/Decision A/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);

    it("shows error when Zoho token fetch fails", async () => {
        fetch.mockRejectedValueOnce(new Error("Network Error"));

        render(<App />);

        fireEvent.click(screen.getByText(/Connect to Zoho/i));

        await waitFor(() => {
            expect(screen.getByText(/Error connecting to Zoho/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);

    it("handles audio API failure gracefully", async () => {
        fetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ error: "API Error" ***REMOVED***)
        ***REMOVED***);

        render(<App />);

        const fileInput = screen.getByLabelText(/upload audio/i);
        const validFile = new File(["audio"], "audio.mp3", { type: "audio/mp3" ***REMOVED***);

        fireEvent.change(fileInput, { target: { files: [validFile] ***REMOVED*** ***REMOVED***);
        fireEvent.click(screen.getByRole("button", { name: /Upload & Analyze/i ***REMOVED***));

        await waitFor(() => {
            expect(screen.getByText(/API Error/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);

    it("schedules selected actions and shows success message", async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: "Events scheduled" ***REMOVED***)
        ***REMOVED***);

        render(<App />);

        fireEvent.click(screen.getByRole("button", { name: /Schedule Selected/i ***REMOVED***));

        await waitFor(() => {
            expect(screen.getByText(/Events scheduled successfully/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);

    it("shows error message when scheduling fails", async () => {
        fetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ error: "Scheduling failed" ***REMOVED***)
        ***REMOVED***);

        render(<App />);

        fireEvent.click(screen.getByRole("button", { name: /Schedule Selected/i ***REMOVED***));

        await waitFor(() => {
            expect(screen.getByText(/Error scheduling events/i)).toBeInTheDocument();
        ***REMOVED***);
    ***REMOVED***);
***REMOVED***);
