import axios from 'axios';

//Function to create a new event in Zoho Calendar
// Instead of talking to Zoho directly, this talks to your Flask backend.
export async function createEvent(actions) {
    const includedActions = Array.isArray(actions) ? actions.filter(a => a.include && a.datetime) : [];
    try {
        const response = await axios.post('http://localhost:5000/create-event', includedActions);
        return response.data;
    } catch (error) {
        console.error("Error creating event via backend:", error);
        throw new Error("Error creating event via backend");
    }
}

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

// Function to fetch Zoho access token using refresh token
export const getAccessToken = async () => {
    try {
        const response = await fetch('https://accounts.zoho.com/oauth/v2/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                refresh_token: process.env.ZOHO_REFRESH_TOKEN,
                client_id: process.env.ZOHO_CLIENT_ID,
                client_secret: process.env.ZOHO_CLIENT_SECRET,
                grant_type: 'refresh_token',
            }),
        });

        const data = await response.json();
        return data.access_token;
    } catch (error) {
        console.error('Error fetching Zoho access token:', error);
        throw error;
    }
};

/* Create event in Zoho using the provided token
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
};*/
