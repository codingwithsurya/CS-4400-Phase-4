import React, { useState, useEffect } from 'react';
// Import the actual API functions
import { addAirport, getLocations } from '../../utils/api';

const AddAirport = () => {
  const [formData, setFormData] = useState({
    airportID: '',
    airport_name: '',
    city: '',
    state: '',
    country: '',
    locationID: ''
  });

  const [message, setMessage] = useState({ text: '', type: '' });
  const [locations, setLocations] = useState([]);
  const [isLoading, setIsLoading] = useState(false); // For loading states

  // Fetch initial data for dropdowns
  useEffect(() => {
    let isMounted = true; // Prevent state update on unmounted component
    setMessage({ text: '', type: '' }); // Clear message on mount

    const fetchData = async () => {
      setIsLoading(true);
      try {
        // In production, try to get data from API
        try {
          const locationsData = await getLocations();

          if (isMounted) {
            const locations = locationsData.map ? locationsData.map(l => l.locationid).sort() : [];
            setLocations(locations);
          }
        } catch (apiError) {
          console.error('API error:', apiError);
          // Fallback to default data if API fails
          if (isMounted) {
            setMessage({ 
              text: `Could not fetch data from server. Using default values.`, 
              type: 'error' 
            });
            // Set default locations as fallback
            setLocations(['port_1', 'port_2', 'port_3', 'plane_1', 'plane_2', 'plane_3']);
          }
        }
      } catch (error) {
        if (isMounted) {
          setMessage({ text: `Error initializing component: ${error.message}`, type: 'error' });
          // Set default locations as fallback
          setLocations(['port_1', 'port_2', 'plane_1', 'plane_2']);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    // Cleanup function to prevent setting state on unmounted component
    return () => {
      isMounted = false;
    };
  }, []); // Empty dependency array means run once on mount

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: '', type: '' }); // Clear previous messages
    setIsLoading(true);

    // --- Data Validation ---
    if (!formData.airportID || formData.airportID.length !== 3) {
      setMessage({ text: 'Airport ID must be exactly 3 characters.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.airport_name) {
      setMessage({ text: 'Airport Name is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.city) {
      setMessage({ text: 'City is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.state) {
      setMessage({ text: 'State is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.country || formData.country.length !== 3) {
      setMessage({ text: 'Country code must be exactly 3 characters.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.locationID) {
      setMessage({ text: 'Location ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Convert form values to the format expected by the backend SP
    const dataToSubmit = {
      ip_airportID: formData.airportID,
      ip_airport_name: formData.airport_name,
      ip_city: formData.city,
      ip_state: formData.state,
      ip_country: formData.country,
      ip_locationID: formData.locationID
    };

    // --- API Call ---
    try {
      // Call the actual backend API
      const response = await addAirport(dataToSubmit);

      setMessage({
        text: response?.message || 'Airport added successfully!', // Use backend message if available
        type: 'success'
      });

      // Reset form
      setFormData({
        airportID: '',
        airport_name: '',
        city: '',
        state: '',
        country: '',
        locationID: ''
      });

      // Optionally refetch locations if a new one was added
      try {
        const locationsData = await getLocations();
        setLocations(locationsData.map(l => l.locationid).sort() || []);
      } catch (fetchError) {
        console.error("Failed to refresh locations:", fetchError);
        // Don't overwrite main message
      }

    } catch (error) {
      console.error("Add Airport Error:", error);
      setMessage({
        // Use the error message thrown by apiRequest
        text: `Error: ${error.message || 'Failed to add airport. Check constraints.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      airportID: '',
      airport_name: '',
      city: '',
      state: '',
      country: '',
      locationID: ''
    });
    setMessage({ text: '', type: '' }); // Clear message
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Add Airport</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">add_airport()</div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Airport ID</div>
                <input
                  className="form-input"
                  type="text"
                  name="airportID"
                  value={formData.airportID}
                  onChange={handleChange}
                  placeholder="3-letter code"
                  maxLength="3"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Airport Name</div>
                <input
                  className="form-input"
                  type="text"
                  name="airport_name"
                  value={formData.airport_name}
                  onChange={handleChange}
                  placeholder="Full airport name"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">City</div>
                <input
                  className="form-input"
                  type="text"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="City"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">State</div>
                <input
                  className="form-input"
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  placeholder="State"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Country</div>
                <input
                  className="form-input"
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  placeholder="3-letter country code"
                  maxLength="3"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Location ID</div>
                <input
                  className="form-input"
                  type="text"
                  name="locationID"
                  value={formData.locationID}
                  onChange={handleChange}
                  placeholder="Unique location identifier"
                  list="locations"
                  required
                />
              </div>
              <datalist id="locations">
                {locations.map(loc => (
                  <option value={loc} key={loc} />
                ))}
              </datalist>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" onClick={handleCancel} className="btn">
              Cancel
            </button>
            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Add'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddAirport;
