import React, { useState, useEffect } from 'react';
import { retireFlight, getFlights } from '../../utils/api';

const RetireFlight = () => {
  const [formData, setFormData] = useState({
    flightID: ''
  });

  const [flights, setFlights] = useState([]);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [isLoading, setIsLoading] = useState(false);

  // Fetch flights on component mount
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const flightsData = await getFlights();
        if (isMounted) {
          setFlights(flightsData || []);
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error fetching flights:', error);
          setMessage({ 
            text: `Could not fetch flight data: ${error.message}`, 
            type: 'error' 
          });
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: '', type: '' });
    setIsLoading(true);

    // Validation
    if (!formData.flightID) {
      setMessage({ text: 'Flight ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    try {
      await retireFlight({
        ip_flightID: formData.flightID
      });

      setMessage({ 
        text: 'Flight retired successfully!', 
        type: 'success' 
      });
      
      // Update the flights list to remove the retired flight
      setFlights(flights.filter(flight => flight.flightID !== formData.flightID));
      
      // Reset form after successful submission
      setFormData({
        flightID: ''
      });
    } catch (error) {
      console.error('Error retiring flight:', error);
      setMessage({ 
        text: `Error retiring flight: ${error.message}`, 
        type: 'error' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="procedure-container">
      <h2>Retire Flight</h2>
      <div className="procedure-description">
        Remove a flight that has ended from the system. The flight must be on the ground, 
        and either be at the start or end of its route. The flight must also be empty - 
        no pilots or passengers.
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form-container">
        <form onSubmit={handleSubmit}>
          <div className="procedure-form">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Flight ID</div>
                <select
                  className="form-input"
                  name="flightID"
                  value={formData.flightID}
                  onChange={handleChange}
                  required
                  disabled={isLoading}
                >
                  <option value="">Select a flight</option>
                  {flights.map(flight => (
                    <option key={flight.flightID} value={flight.flightID}>
                      {flight.flightID}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => {
                setFormData({
                  flightID: ''
                });
                setMessage({ text: '', type: '' });
              }}
              className="btn"
              disabled={isLoading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn" 
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Retire Flight'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RetireFlight;
