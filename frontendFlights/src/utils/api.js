// frontendFlights/src/utils/api.js

// API utility functions for making calls to the backend
const API_BASE_URL = 'http://localhost:8000'; // Using port 8080 for Django server

// Generic function for making API requests
async function apiRequest(endpoint, method = 'GET', data = null) {
  // Log the request for debugging
  console.log(`Making ${method} request to: ${endpoint}`, data);
  
  // Construct the full URL. We need to be careful not to double the slashes.
  const fullUrl = `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      // Add CSRF token header if needed for Django POST requests
      // 'X-CSRFToken': getCookie('csrftoken'), // You'd need a function to get the CSRF cookie
    },
    // credentials: 'include', // Consider if you need cookies for auth
  };

  if (data && (method === 'POST' || method === 'PUT')) {
    options.body = JSON.stringify(data);
  }

  try {
    console.log('Fetch options:', options);
    const response = await fetch(fullUrl, options);
    console.log('Response status:', response.status);

    // For non-2xx responses, try to parse error message
    if (!response.ok) {
      let errorMessage = `Request failed with status ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData?.detail || errorData?.message || JSON.stringify(errorData) || errorMessage;
      } catch (e) {
        // If parsing JSON fails, use the status text
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    // For 204 No Content
    if (response.status === 204) {
      return null;
    }

    // Parse JSON for other successful responses
    return await response.json();
  } catch (error) {
    console.error('API request error:', fullUrl, error); // Log the URL too
    // Provide more specific error message to the component
    const enhancedError = new Error(
      `API request failed: ${error.message}. This could be a network issue or the server might be down.`
    );
    throw enhancedError; // Throw enhanced error for better user feedback
  }
}

// Helper function to get CSRF token (example, may need adjustment)
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//     const cookies = document.cookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//       if (cookie.substring(0, name.length + 1) === (name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }


// --- Procedure endpoints ---
// Note: Adjust endpoints if they are under an /api/ prefix in Django
export const addAirplane = (data) => apiRequest('/api/add-airplane/', 'POST', data); // Example endpoint
export const addAirport = (data) => apiRequest('/api/add-airport/', 'POST', data); // Example endpoint
export const addPerson = (data) => apiRequest('/api/add-person/', 'POST', data); // Example endpoint
export const grantOrRevokePilotLicense = (data) => apiRequest('/api/pilot-licenses/', 'POST', data); // get pilot licenses
export const offerFlight = (data) => apiRequest('/api/offer-flight/', 'POST', data); // Example endpoint
export const flightLanding = (data) => apiRequest('/api/flight-landing/', 'POST', data); // Example endpoint
export const flightTakeoff = (data) => apiRequest('/api/flight-takeoff/', 'POST', data); // Example endpoint
export const passengersBoard = (data) => apiRequest('/api/passengers-board/', 'POST', data); // Example endpoint
export const passengersDisembark = (data) => apiRequest('/api/passengers-disembark/', 'POST', data); // Example endpoint
export const assignPilot = (data) => apiRequest('/api/assign-pilot/', 'POST', data); // Example endpoint
export const recycleCrew = (data) => apiRequest('/api/recycle-crew/', 'POST', data); // Example endpoint
export const retireFlight = (data) => apiRequest('/api/retire-flight/', 'POST', data); // Example endpoint
export const simulationCycle = () => apiRequest('/api/simulation-cycle/', 'POST'); // Example endpoint

// --- View endpoints ---
// Note: These usually point to Django template views or DRF list views
export const getFlightsInTheAir = () => apiRequest('/flights-in-the-air/'); // Assumes DRF or custom JSON view
export const getFlightsOnTheGround = () => apiRequest('/flights-on-the-ground/'); // Assumes DRF or custom JSON view
export const getPeopleInTheAir = () => apiRequest('/people-in-the-air/'); // Assumes DRF or custom JSON view
export const getPeopleOnTheGround = () => apiRequest('/people-on-the-ground/'); // Assumes DRF or custom JSON view
export const getRouteSummary = () => apiRequest('/route-summary/'); // Assumes DRF or custom JSON view
export const getAlternativeAirports = () => apiRequest('/alternative-airport/'); // Assumes DRF or custom JSON view


// --- Utility endpoints ---
// Note: Need corresponding backend views for these
export const getAirlines = () => apiRequest('/api/airlines/'); // Example endpoint
export const getAirports = () => apiRequest('/api/airports/'); // Example endpoint
export const getRoutes = () => apiRequest('/api/routes/'); // Example endpoint
export const getAirplanes = () => apiRequest('/api/airplanes/'); // Example endpoint
export const getPilots = () => apiRequest('/api/pilots/'); // Example endpoint
export const getFlights = () => apiRequest('/api/flights/'); // Example endpoint
export const getLocations = () => apiRequest('/api/locations/'); // Example endpoint
export const getPilotLicenses = () => apiRequest('/api/pilot-licenses/'); // Added for GrantRevokePilotLicense component

// Mock API call for components not yet connected
export const mockApiCall = (data) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Mock API call with data:', data);
      resolve({ success: true, message: 'Mock operation completed successfully' });
    }, 300);
  });
};

export const mockFetchData = (mockData = []) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Mock fetch data');
      resolve(mockData);
    }, 300);
  });
};