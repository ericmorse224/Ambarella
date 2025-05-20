/**
 * File: dateUtils.js
 * Author: Eric Morse
 * Date: May 11th, 2025
 *
 * Description:
 * This utility provides a function for adding one hour to a date/time,
 * outputting the result as an ISO 8601 string in "YYYY-MM-DDTHH:mm" format.
 * It handles input validation and throws errors for invalid date/time inputs.
 */

/**
 * Adds one hour to the provided date and time strings.
 *
 * @param {string} dateStr - The date in "YYYY-MM-DD" format.
 * @param {string} timeStr - The time in "HH:mm" (24-hour) format.
 * @returns {string} - The incremented date and time as an ISO string ("YYYY-MM-DDTHH:mm").
 * @throws {Error} - Throws if date or time inputs are invalid.
 *
 * Example:
 *   addOneHour("2025-05-11", "13:30") // "2025-05-11T14:30"
 */
export function addOneHour(dateStr, timeStr) {
  // Split date string and convert to numbers: year, month, day
  const [year, month, day] = dateStr.split('-').map(Number);
  // Split time string and convert to numbers: hour, minute
  const [hour, minute] = timeStr.split(':').map(Number);

  // Input validation: ensure no value is NaN
  if (
    [year, month, day, hour, minute].some(n => Number.isNaN(n))
  ) {
    throw new Error("Invalid date or time");
  }

  // Construct Date object in local time zone
  const start = new Date(year, month - 1, day, hour, minute);

  // Check for an invalid Date object
  if (isNaN(start.getTime())) {
    throw new Error("Invalid date or time");
  }

  // Add one hour to the date/time
  start.setHours(start.getHours() + 1);

  // Helper function: pad numbers with leading zero if needed
  const pad = n => n.toString().padStart(2, '0');
  // Return formatted date/time string
  return `${start.getFullYear()}-${pad(start.getMonth() + 1)}-${pad(start.getDate())}T${pad(start.getHours())}:${pad(start.getMinutes())}`;
}
