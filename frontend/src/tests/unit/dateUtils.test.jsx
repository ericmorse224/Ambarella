// src/utils/dateUtils.test.js

import { addOneHour } from '../../utils/dateUtils';

describe('addOneHour', () => {
  it('adds one hour to a given date and time', () => {
    expect(addOneHour('2025-05-21', '15:30')).toBe('2025-05-21T16:30');
    expect(addOneHour('2025-12-31', '23:00')).toBe('2026-01-01T00:00');
  });

  it('pads single digit hours and minutes', () => {
    expect(addOneHour('2025-05-21', '09:05')).toBe('2025-05-21T10:05');
  });

  it('handles invalid date/time gracefully', () => {
    expect(() => addOneHour('bad-date', '10:00')).toThrow();
    expect(() => addOneHour('2025-05-21', 'bad-time')).toThrow();
  });
});
