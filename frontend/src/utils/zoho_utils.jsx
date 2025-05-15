import axios from 'axios';

// Format event data for Zoho
export function formatEventData(action) {
  return {
    subject: action.text,
    start_time: action.datetime,
    owner: action.owner,
    // other fields...
  };
}

// Function to create a new event in Zoho Calendar
export const createEvent = async (eventData) => {
  try {
    const response = await axios.post('https://www.zohoapis.com/calendar/v2/events', eventData, {
      headers: {
        'Authorization': `Bearer ${process.env.ZOHO_ACCESS_TOKEN}`,
        'Content-Type': 'application/json',
      },
    });
    
    return response.data;  // Assuming Zoho returns the created event data.
  } catch (error) {
    console.error('Error creating event in Zoho:', error);
    throw new Error('Failed to create event');
  }
};

// Example helper function to format event data for Zoho
export const formatEventData = (action) => {
  return {
    summary: action.text,
    start: {
      dateTime: action.datetime,
      timeZone: 'America/New_York',
    },
    end: {
      dateTime: action.datetime,
      timeZone: 'America/New_York',
    },
    attendees: action.owner ? [{ email: action.owner }] : [],
  };
};

// Example function to list events from Zoho
export const listEvents = async () => {
  try {
    const response = await axios.get('https://www.zohoapis.com/calendar/v2/events', {
      headers: {
        'Authorization': `Bearer ${process.env.ZOHO_ACCESS_TOKEN}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching events from Zoho:', error);
    throw new Error('Failed to list events');
  }
};

// Create event in Zoho using the provided token
export async function createEvent(eventData, token) {
  const url = 'https://www.zohoapis.com/calendar/v2/events';
  
  try {
    const response = await axios.post(
      url,
      eventData,
      {
        headers: {
          Authorization: `Zoho-oauthtoken ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error creating Zoho event:', error);
    throw new Error('Failed to create event in Zoho');
  }
}

