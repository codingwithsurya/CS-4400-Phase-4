import React, { useState, useEffect } from 'react';
// Import the actual API functions
import { addAirplane, getAirlines, getLocations } from '../../utils/api';

const AddAirplane = () => {
  const [formData, setFormData] = useState({
    airlineID: '',
    tail_num: '',
    seat_capacity: '',
    speed: '',
    locationID: '',
    plane_type: '',
    maintenanced: 'NULL', // Keep string 'NULL' for select default
    model: '', // Default to empty string or NULL if backend handles it
    neo: 'NULL' // Keep string 'NULL' for select default
  });

  const [message, setMessage] = useState({ text: '', type: '' });
  const [airlines, setAirlines] = useState([]);
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
          const [airlinesData, locationsData] = await Promise.all([
            getAirlines(), 
            getLocations()  
          ]);

          if (isMounted) {
            const airlines = airlinesData.map ? airlinesData.map(a => a.airlineid).sort() : [];
            const locations = locationsData.map ? locationsData.map(l => l.locationid).sort() : [];
            
            setAirlines(airlines);
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
            // Set default airlines and locations as fallback
            setAirlines(['Delta', 'United', 'American', 'Spirit', 'British Airways', 'Lufthansa', 'Air_France']);
            setLocations(['port_1', 'port_2', 'port_3', 'plane_1', 'plane_2', 'plane_3']);
          }
        }
      } catch (error) {
        if (isMounted) {
          setMessage({ text: `Error initializing component: ${error.message}`, type: 'error' });
          // Set default airlines and locations as fallback
          setAirlines(['Delta', 'United', 'American', 'Spirit']);
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

    // --- Data Validation & Formatting ---
    const seatCap = parseInt(formData.seat_capacity, 10);
    const speedVal = parseInt(formData.speed, 10);

    if (isNaN(seatCap) || seatCap <= 0) {
      setMessage({ text: 'Seat Capacity must be a positive number.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (isNaN(speedVal) || speedVal <= 0) {
      setMessage({ text: 'Speed must be a positive number.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.locationID) {
        setMessage({ text: 'Location ID is required.', type: 'error' });
        setIsLoading(false);
        return;
    }
     if (!formData.plane_type) {
        setMessage({ text: 'Plane Type is required.', type: 'error' });
        setIsLoading(false);
        return;
    }

    // Convert form values to the format expected by the backend SP
    // Backend SP expects boolean or null for maintenanced/neo
    const dataToSubmit = {
      ip_airlineID: formData.airlineID,
      ip_tail_num: formData.tail_num,
      ip_seat_capacity: seatCap,
      ip_speed: speedVal,
      ip_locationID: formData.locationID,
      ip_plane_type: formData.plane_type,
      // Convert 'NULL', 'TRUE', 'FALSE' strings to null, true, false
      ip_maintenanced: formData.maintenanced === 'NULL' ? null : (formData.maintenanced === 'TRUE'),
      ip_model: formData.model === '' ? null : formData.model, // Send null if empty
      ip_neo: formData.neo === 'NULL' ? null : (formData.neo === 'TRUE')
    };

    // --- API Call ---
    try {
      // Call the actual backend API
      const response = await addAirplane(dataToSubmit);

      setMessage({
        text: response?.message || 'Airplane added successfully!', // Use backend message if available
        type: 'success'
      });

      // Reset form
      setFormData({
        airlineID: '',
        tail_num: '',
        seat_capacity: '',
        speed: '',
        locationID: '',
        plane_type: '',
        maintenanced: 'NULL',
        model: '',
        neo: 'NULL'
      });

      // Optionally refetch locations if a new one was added
      // (or rely on user manually typing new location)
      try {
          const locationsData = await getLocations();
          setLocations(locationsData.map(l => l.locationid).sort() || []);
      } catch (fetchError) {
          console.error("Failed to refresh locations:", fetchError);
          // Don't overwrite main message
      }


    } catch (error) {
      console.error("Add Airplane Error:", error);
      setMessage({
        // Use the error message thrown by apiRequest
        text: `Error: ${error.message || 'Failed to add airplane. Check constraints.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
      setFormData({
        airlineID: '',
        tail_num: '',
        seat_capacity: '',
        speed: '',
        locationID: '',
        plane_type: '',
        maintenanced: 'NULL',
        model: '',
        neo: 'NULL'
      });
      setMessage({ text: '', type: '' }); // Clear message
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Add Airplane</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        {/* Function name display */}
        <div className="procedure-name">add_airplane()</div>
        
        {/* Form grid layout to match mockup */}
        <div className="form-grid">
          {/* Row 1: Airline ID, Tail Num, Seat Cap */}
          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Airline ID</label>
              <select
                className="form-input"
                name="airlineID"
                value={formData.airlineID}
                onChange={handleChange}
                required
                disabled={isLoading}
              >
                <option value="">Select Airline</option>
                {airlines.map(airline => (
                  <option key={airline} value={airline}>{airline}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Tail Num</label>
              <input
                type="text"
                className="form-input"
                name="tail_num"
                value={formData.tail_num}
                onChange={handleChange}
                required
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Seat Cap</label>
              <input
                type="number"
                className="form-input"
                name="seat_capacity"
                value={formData.seat_capacity}
                onChange={handleChange}
                required
                min="1"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Row 2: Speed, Location ID, Plane Type */}
          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Speed</label>
              <input
                type="number"
                className="form-input"
                name="speed"
                value={formData.speed}
                onChange={handleChange}
                required
                min="1"
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Location ID</label>
              <input
                type="text"
                className="form-input"
                name="locationID"
                value={formData.locationID}
                onChange={handleChange}
                required
                list="locations-list"
                disabled={isLoading}
              />
              <datalist id="locations-list">
                {locations.map(location => (
                  <option key={location} value={location} />
                ))}
              </datalist>
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Plane Type</label>
              <select
                className="form-input"
                name="plane_type"
                value={formData.plane_type}
                onChange={handleChange}
                required
                disabled={isLoading}
              >
                <option value="">Select Type</option>
                <option value="Airbus">Airbus</option>
                <option value="Boeing">Boeing</option>
              </select>
            </div>
          </div>

          {/* Row 3: Maintained, Model, Neo */}
          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Maintained</label>
              <select
                className="form-input"
                name="maintenanced"
                value={formData.maintenanced}
                onChange={handleChange}
                disabled={isLoading}
              >
                <option value="NULL">NULL</option>
                <option value="TRUE">TRUE</option>
                <option value="FALSE">FALSE</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Model</label>
              <input
                type="text"
                className="form-input"
                name="model"
                value={formData.model}
                onChange={handleChange}
                placeholder="NULL if blank"
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="form-group">
            <div className="form-row">
              <label className="form-label">Neo</label>
              <select
                className="form-input"
                name="neo"
                value={formData.neo}
                onChange={handleChange}
                disabled={isLoading}
              >
                <option value="NULL">NULL</option>
                <option value="TRUE">TRUE</option>
                <option value="FALSE">FALSE</option>
              </select>
            </div>
          </div>
        </div>

        {/* Action Buttons at the bottom */}
        <div className="form-actions">
          <button 
            type="button" 
            className="btn" 
            onClick={handleCancel} 
            disabled={isLoading}
          >
            Cancel
          </button>
          <button 
            type="button" 
            className="btn" 
            onClick={handleSubmit} 
            disabled={isLoading}
          >
            {isLoading ? 'Adding...' : 'Add'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddAirplane;