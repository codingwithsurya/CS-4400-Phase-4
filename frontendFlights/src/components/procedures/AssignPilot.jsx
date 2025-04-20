import React, { useState, useEffect } from 'react';
import { assignPilot, getFlights, getPilots, getPilotLicenses } from '../../utils/api';

const AssignPilot = () => {
  const [formData, setFormData] = useState({
    flightID: '',
    personID: ''
  });

  const [flights, setFlights] = useState([]);
  const [pilots, setPilots] = useState([]);
  const [pilotLicenses, setPilotLicenses] = useState([]);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [isLoading, setIsLoading] = useState(false);

  // Fetch initial data
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [flightsData, pilotsData, licensesData] = await Promise.all([
          getFlights(),
          getPilots(),
          getPilotLicenses()
        ]);

        if (isMounted) {
          setFlights(flightsData || []);
          setPilots(pilotsData || []);
          setPilotLicenses(licensesData || []);
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error fetching data:', error);
          setMessage({ 
            text: `Could not fetch data: ${error.message}`, 
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
    if (!formData.personID) {
      setMessage({ text: 'Pilot ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    try {
      const response = await assignPilot({
        ip_flightID: formData.flightID,
        ip_personID: formData.personID
      });

      setMessage({ 
        text: 'Pilot assigned successfully!', 
        type: 'success' 
      });
      
      // Reset form after successful submission
      setFormData({
        flightID: '',
        personID: ''
      });
    } catch (error) {
      console.error('Error assigning pilot:', error);
      setMessage({ 
        text: `Error assigning pilot: ${error.message}`, 
        type: 'error' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Filter pilots that have appropriate licenses
  const getPilotLicenseInfo = (pilotID) => {
    const licenses = pilotLicenses
      .filter(l => l.personID === pilotID)
      .map(l => l.license);
    return licenses.length > 0 ? `(Licenses: ${licenses.join(', ')})` : '(No licenses)';
  };

  return (
    <div className="procedure-container">
      <h2>Assign Pilot</h2>
      <div className="procedure-description">
        Assign a pilot to a flight. The pilot must have an appropriate license for the flight's aircraft.
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

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Pilot</div>
                <select
                  className="form-input"
                  name="personID"
                  value={formData.personID}
                  onChange={handleChange}
                  required
                  disabled={isLoading}
                >
                  <option value="">Select a pilot</option>
                  {pilots.map(pilot => (
                    <option key={pilot.personID} value={pilot.personID}>
                      {pilot.name || `${pilot.personID}`} {getPilotLicenseInfo(pilot.personID)}
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
                  flightID: '',
                  personID: ''
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
              {isLoading ? 'Processing...' : 'Assign Pilot'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AssignPilot;
