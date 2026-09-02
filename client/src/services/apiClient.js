const API_BASE = 'http://localhost:5000/api/v1';

export async function apiRequest(endpoint, method = 'GET', body = null, token = null) {
  const headers = {
    'Content-Type': 'application/json'
  };

  const storedToken = token || localStorage.getItem('accessToken');
  if (storedToken) {
    headers['Authorization'] = `Bearer ${storedToken}`;
  }

  const options = {
    method,
    headers,
    credentials: 'include'
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  const data = await response.json();

  if (!response.ok || !data.success) {
    throw new Error(data.error?.message || 'API request failed.');
  }

  return data;
}
