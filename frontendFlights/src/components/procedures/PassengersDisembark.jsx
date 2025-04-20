import React, { useState, useEffect } from 'react';
import { passengersDisembark, getFlights } from '../../utils/api';

const PassengersDisembark = () => {
  const [flightID, setFlightID] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });
  const [flights, setFlights] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Filter for flights that are ready for disembarking (on_ground status)
  const disembarkableFlights = flights.filter(f => f.airplane_status === 'on_ground');

  // Fetch available flights
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

    const fetchFlights = async () => {
      setIsLoading(true);
      try {
        try {
          const flightsData = await getFlights();
          
          if (isMounted) {
            setFlights(flightsData || []);
            
            // If no disembarkable flights, show a message
            if (flightsData && flightsData.filter(f => f.airplane_status === 'on_ground').length === 0) {
              setMessage({ 
                text: 'No flights currently on the ground available for disembarking.', 
                type: 'info' 
              });
            }
          }
        } catch (apiError) {
          console.error('API error:', apiError);
          if (isMounted) {
            setMessage({ 
              text: `Could not fetch flights from server. Using default values.`, 
              type: 'error' 
            });
            // Set default data
            setFlights([
              { flightID: 'F1', routeID: 'R1', airplane_status: 'on_ground' },
              { flightID: 'F2', routeID: 'R2', airplane_status: 'in_flight' }
            ]);
          }
        }
      } catch (error) {
        if (isMounted) {
          setMessage({ text: `Error loading flights: ${error.message}`, type: 'error' });
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchFlights();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleChange = (e) => {
    setFlightID(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: '', type: '' });
    setIsLoading(true);

    // Validation
    if (!flightID) {
      setMessage({ text: 'Please select a flight.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Check if flight exists and is on_ground
    const flightExists = flights.some(f => f.flightID === flightID);
    if (!flightExists) {
      setMessage({ text: 'Selected flight does not exist.', type: 'error' });
      setIsLoading(false);
      return;
    }

    const isOnGround = flights.some(f => f.flightID === flightID && f.airplane_status === 'on_ground');
    if (!isOnGround) {
      setMessage({ text: 'Selected flight must be on the ground for passengers to disembark.', type: 'error' });
      setIsLoading(false);
      return;
    }

    try {
      // Call the API
      const response = await passengersDisembark({ ip_flightID: flightID });

      setMessage({
        text: response?.message || 'Passengers disembarked successfully!',
        type: 'success'
      });

      // Reset selection
      setFlightID('');

    } catch (error) {
      console.error("Passengers Disembark Error:", error);
      setMessage({
        text: `Error: ${error.message || 'Failed to disembark passengers.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Passengers Disembark</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">passengers_disembark()</div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Flight</div>
                <select
                  className="form-input"
                  value={flightID}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select a flight for disembarking</option>
                  {disembarkableFlights.map(flight => (
                    <option key={flight.flightID} value={flight.flightID}>
                      {flight.flightID} (Route: {flight.routeID})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              onClick={() => setFlightID('')} 
              className="btn"
            >
              Cancel
            </button>
            <button type="submit" className="btn" disabled={isLoading || disembarkableFlights.length === 0}>
              {isLoading ? 'Processing...' : 'Disembark Passengers'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PassengersDisembark;
