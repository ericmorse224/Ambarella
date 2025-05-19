export function addOneHour(dateStr, timeStr) {
  // Split and parse components
  const [year, month, day] = dateStr.split('-').map(Number);
  const [hour, minute] = timeStr.split(':').map(Number);

  // Check for NaN values (invalid input)
  if (
    [year, month, day, hour, minute].some(n => Number.isNaN(n))
  ) {
    throw new Error("Invalid date or time");
  }

  // Construct date in local time
  const start = new Date(year, month - 1, day, hour, minute);

  // Check for Invalid Date
  if (isNaN(start.getTime())) {
    throw new Error("Invalid date or time");
  }

  start.setHours(start.getHours() + 1);

  // Pad helper
  const pad = n => n.toString().padStart(2, '0');
  return `${start.getFullYear()}-${pad(start.getMonth() + 1)}-${pad(start.getDate())}T${pad(start.getHours())}:${pad(start.getMinutes())}`;
}
