/**
 * @file dateUtils.test.jsx
 * @author Eric Morse
 * @date May 11th, 2025
 * @description
 * Unit tests for the addOneHour utility function in dateUtils.js.
 * This file ensures correct date and time handling for calendar event scheduling logic.
 */
import { addOneHour } from '../../utils/dateUtils';

describe('addOneHour', () => {
  /**
   * Test that addOneHour correctly adds one hour to a date and time string.
   */
  it('adds one hour to a given date and time', () => {
    expect(addOneHour('2025-05-21', '15:30')).toBe('2025-05-21T16:30');
    expect(addOneHour('2025-12-31', '23:00')).toBe('2026-01-01T00:00');
  });

  /**
   * Test that single digit hours and minutes are padded properly.
   */
  it('pads single digit hours and minutes', () => {
    expect(addOneHour('2025-05-21', '09:05')).toBe('2025-05-21T10:05');
  });

 /**
  * Test that invalid date or time inputs throw errors.
  */
  it('handles invalid date/time gracefully', () => {
    expect(() => addOneHour('bad-date', '10:00')).toThrow();
    expect(() => addOneHour('2025-05-21', 'bad-time')).toThrow();
  });
});
