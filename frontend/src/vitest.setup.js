import axios from 'axios';
import { vi } from 'vitest';

// Mocking OpenAI API
vi.spyOn(axios, 'post').mockImplementation((url, data) => {
  if (url.includes('openai')) {
    return Promise.resolve({
      data: {
        choices: [{ text: 'Mocked OpenAI response' }],
      },
    });
  }
  return Promise.reject(new Error('API not mocked'));
});

// Mocking Zoho token retrieval
vi.spyOn(axios, 'get').mockImplementation((url) => {
  if (url.includes('zoho')) {
    return Promise.resolve({
      data: { access_token: 'mock_zoho_token' },
    });
  }
  return Promise.reject(new Error('API not mocked'));
});

// Mocking AssemblyAI API
vi.spyOn(axios, 'post').mockImplementation((url, data) => {
  if (url.includes('assemblyai')) {
    return Promise.resolve({
      data: {
        text: 'Mocked AssemblyAI transcription result.',
      },
    });
  }
  return Promise.reject(new Error('API not mocked'));
});

// Example: Mocking other API calls (e.g., token retrieval or custom APIs)
vi.spyOn(axios, 'get').mockImplementation((url) => {
  if (url.includes('someTokenEndpoint')) {
    return Promise.resolve({
      data: { access_token: 'mock_token' },
    });
  }
  return Promise.reject(new Error('API not mocked'));
});


