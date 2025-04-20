import React, { useState, useEffect } from 'react';
import { offerFlight, getRoutes, getAirlines, getAirplanes } from '../../utils/api';

const OfferFlight = () => {
  const [formData, setFormData] = useState({
    flightID: '',
    routeID: '',
    support_airline: '',
    support_tail: '',
    progress: '0',
    airplane_status: 'on_ground',
    next_time: '0'
  });

  const [message, setMessage] = useState({ text: '', type: '' });
  const [routes, setRoutes] = useState([]);
  const [airlines, setAirlines] = useState([]);
  const [airplanes, setAirplanes] = useState([]);
  const [filteredAirplanes, setFilteredAirplanes] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch initial data for dropdowns
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

    const fetchData = async () => {
      setIsLoading(true);
      try {
        try {
          const [routesData, airlinesData, airplanesData] = await Promise.all([
            getRoutes(),
            getAirlines(),
            getAirplanes()
          ]);

          if (isMounted) {
            setRoutes(routesData || []);
            const airlines = airlinesData.map ? airlinesData.map(a => a.airlineid).sort() : [];
            setAirlines(airlines);
            setAirplanes(airplanesData || []);
          }
        } catch (apiError) {
          console.error('API error:', apiError);
          if (isMounted) {
            setMessage({ 
              text: `Could not fetch data from server. Using default values.`, 
              type: 'error' 
            });
            // Set default data
            setRoutes([{ routeID: 'route_1', distance: 500 }, { routeID: 'route_2', distance: 1000 }]);
            setAirlines(['Delta', 'United', 'American']);
            setAirplanes([
              { airline: 'Delta', tail_num: 'DL123', seat_capacity: 150 },
              { airline: 'United', tail_num: 'UA456', seat_capacity: 200 }
            ]);
          }
        }
      } catch (error) {
        if (isMounted) {
          setMessage({ text: `Error initializing component: ${error.message}`, type: 'error' });
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

  // Filter airplanes based on selected airline
  useEffect(() => {
    if (formData.support_airline) {
      const filtered = airplanes.filter(
        airplane => airplane.airline === formData.support_airline
      );
      setFilteredAirplanes(filtered);
    } else {
      setFilteredAirplanes([]);
    }
  }, [formData.support_airline, airplanes]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear tail_num when airline changes
    if (name === 'support_airline') {
      setFormData(prev => ({ ...prev, support_tail: '' }));
    }
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
    if (!formData.routeID) {
      setMessage({ text: 'Route ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.support_airline) {
      setMessage({ text: 'Airline is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.support_tail) {
      setMessage({ text: 'Airplane tail number is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Prepare data for API
    const dataToSubmit = {
      ip_flightID: formData.flightID,
      ip_routeID: formData.routeID,
      ip_support_airline: formData.support_airline,
      ip_support_tail: formData.support_tail,
      ip_progress: parseInt(formData.progress, 10),
      ip_airplane_status: formData.airplane_status,
      ip_next_time: parseInt(formData.next_time, 10)
    };

    try {
      // Call the API
      const response = await offerFlight(dataToSubmit);

      setMessage({
        text: response?.message || 'Flight offered successfully!',
        type: 'success'
      });

      // Reset form
      setFormData({
        flightID: '',
        routeID: '',
        support_airline: '',
        support_tail: '',
        progress: '0',
        airplane_status: 'on_ground',
        next_time: '0'
      });

    } catch (error) {
      console.error("Offer Flight Error:", error);
      setMessage({
        text: `Error: ${error.message || 'Failed to offer flight.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Offer Flight</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">offer_flight()</div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Flight ID</div>
                <input
                  className="form-input"
                  type="text"
                  name="flightID"
                  value={formData.flightID}
                  onChange={handleChange}
                  placeholder="Unique flight identifier"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Route ID</div>
                <select
                  className="form-input"
                  name="routeID"
                  value={formData.routeID}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select a route</option>
                  {routes.map(route => (
                    <option key={route.routeID} value={route.routeID}>
                      {route.routeID} (Distance: {route.distance})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Airline</div>
                <select
                  className="form-input"
                  name="support_airline"
                  value={formData.support_airline}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select an airline</option>
                  {airlines.map(airline => (
                    <option key={airline} value={airline}>
                      {airline}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Airplane</div>
                <select
                  className="form-input"
                  name="support_tail"
                  value={formData.support_tail}
                  onChange={handleChange}
                  required
                  disabled={!formData.support_airline}
                >
                  <option value="">Select an airplane</option>
                  {filteredAirplanes.map(airplane => (
                    <option key={airplane.tail_num} value={airplane.tail_num}>
                      {airplane.tail_num} (Seats: {airplane.seat_capacity})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Progress</div>
                <input
                  className="form-input"
                  type="number"
                  name="progress"
                  value={formData.progress}
                  onChange={handleChange}
                  min="0"
                  max="100"
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Status</div>
                <select
                  className="form-input"
                  name="airplane_status"
                  value={formData.airplane_status}
                  onChange={handleChange}
                >
                  <option value="on_ground">On Ground</option>
                  <option value="in_flight">In Flight</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Next Time</div>
                <input
                  className="form-input"
                  type="number"
                  name="next_time"
                  value={formData.next_time}
                  onChange={handleChange}
                  min="0"
                />
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              onClick={() => setFormData({
                flightID: '',
                routeID: '',
                support_airline: '',
                support_tail: '',
                progress: '0',
                airplane_status: 'on_ground',
                next_time: '0'
              })} 
              className="btn"
            >
              Cancel
            </button>
            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Offer Flight'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default OfferFlight;
