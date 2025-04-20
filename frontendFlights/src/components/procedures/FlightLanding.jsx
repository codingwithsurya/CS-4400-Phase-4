import React, { useState, useEffect } from 'react';
import { flightLanding, getFlights } from '../../utils/api';

const FlightLanding = () => {
  const [flightID, setFlightID] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });
  const [flights, setFlights] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Filter for flights that can be landed (in_flight status)
  const landableFlights = flights.filter(f => f.airplane_status === 'in_flight');

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
            
            // If no landable flights, show a message
            if (flightsData && flightsData.filter(f => f.airplane_status === 'in_flight').length === 0) {
              setMessage({ 
                text: 'No flights currently in the air available for landing.', 
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

    // Check if flight exists and is in_flight
    const flightExists = flights.some(f => f.flightID === flightID);
    if (!flightExists) {
      setMessage({ text: 'Selected flight does not exist.', type: 'error' });
      setIsLoading(false);
      return;
    }

    const isInFlight = flights.some(f => f.flightID === flightID && f.airplane_status === 'in_flight');
    if (!isInFlight) {
      setMessage({ text: 'Selected flight is not currently in the air.', type: 'error' });
      setIsLoading(false);
      return;
    }

    try {
      // Call the API
      const response = await flightLanding({ ip_flightID: flightID });

      setMessage({
        text: response?.message || 'Flight landed successfully!',
        type: 'success'
      });

      // Update the local flight data
      setFlights(prev => 
        prev.map(f => 
          f.flightID === flightID 
            ? { ...f, airplane_status: 'on_ground' } 
            : f
        )
      );

      // Reset selection
      setFlightID('');

    } catch (error) {
      console.error("Flight Landing Error:", error);
      setMessage({
        text: `Error: ${error.message || 'Failed to land flight.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Flight Landing</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">flight_landing()</div>

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
                  <option value="">Select a flight to land</option>
                  {landableFlights.map(flight => (
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
            <button type="submit" className="btn" disabled={isLoading || landableFlights.length === 0}>
              {isLoading ? 'Processing...' : 'Land Flight'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FlightLanding;
