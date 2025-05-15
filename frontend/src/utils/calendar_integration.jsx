import axios from 'axios';

const ZOHO_API_URL = 'https://www.zohoapis.com/calendar/v2/events';

// Function to get the Zoho access token (e.g., from storage or your API)
export const getZohoToken = async () => {
  try {
    const token = localStorage.getItem('zoho_access_token');
    if (!token) throw new Error('Zoho token not found.');
    return token;
  } catch (error) {
    console.error('Error fetching Zoho token:', error);
    throw new Error('Error fetching Zoho token');
  }
};

// Function to create a calendar event
export const createEvent = async (eventData) => {
  try {
    const token = await getZohoToken();

    const response = await axios.post(
      ZOHO_API_URL,
      { data: [eventData] },
      {
        headers: {
          Authorization: `Zoho-oauthtoken ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return response.data;  // Return the response data from Zoho
  } catch (error) {
    console.error('Error scheduling events:', error);
    throw new Error('Error scheduling events');
  }
};

export async function scheduleActions(actions) {
  const validActions = actions.filter(
    action => action.include && action.datetime
  );

  if (validActions.length > 0) {
    try {
      await axios.post('https://www.zohoapis.com/calendar/v2/events', {
        data: validActions,
      });
    } catch (error) {
      console.error("Error scheduling events", error);
    }
  }
}



