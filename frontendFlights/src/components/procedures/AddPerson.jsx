import React, { useState, useEffect } from 'react';
// Import the actual API functions
import { addPerson, getLocations } from '../../utils/api';

const AddPerson = () => {
  const [formData, setFormData] = useState({
    personID: '',
    first_name: '',
    last_name: '',
    locationID: '',
    taxID: '', // Pilot field (optional)
    experience: '', // Pilot field (optional)
    miles: '', // Passenger field (optional)
    funds: '' // Passenger field (optional)
  });

  const [personType, setPersonType] = useState('passenger'); // 'pilot' or 'passenger'
  const [message, setMessage] = useState({ text: '', type: '' });
  const [locations, setLocations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch initial data for dropdowns
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

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
  }, []);

  const handlePersonTypeChange = (e) => {
    setPersonType(e.target.value);
    
    // Reset fields not relevant to the selected person type
    if (e.target.value === 'pilot') {
      setFormData(prev => ({
        ...prev,
        miles: '',
        funds: ''
      }));
    } else { // passenger
      setFormData(prev => ({
        ...prev,
        taxID: '',
        experience: ''
      }));
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // For numeric fields, ensure only numbers are entered
    if (['experience', 'miles', 'funds'].includes(name)) {
      const numericValue = value === '' ? '' : value.replace(/\D/g, '');
      setFormData(prev => ({ ...prev, [name]: numericValue }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: '', type: '' });
    setIsLoading(true);

    // Basic validation
    if (!formData.personID) {
      setMessage({ text: 'Person ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.first_name) {
      setMessage({ text: 'First name is required.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.locationID) {
      setMessage({ text: 'Location ID is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Additional validation based on person type
    if (personType === 'pilot' && !formData.taxID) {
      setMessage({ text: 'Tax ID is required for pilots.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Prepare data for API call
    const dataToSubmit = {
      ip_personID: formData.personID,
      ip_first_name: formData.first_name,
      ip_last_name: formData.last_name || null,
      ip_locationID: formData.locationID,
      ip_taxID: personType === 'pilot' ? formData.taxID : null,
      ip_experience: personType === 'pilot' && formData.experience ? parseInt(formData.experience, 10) : null,
      ip_miles: personType === 'passenger' && formData.miles ? parseInt(formData.miles, 10) : null,
      ip_funds: personType === 'passenger' && formData.funds ? parseInt(formData.funds, 10) : null
    };

    try {
      // Call the actual backend API
      const response = await addPerson(dataToSubmit);

      setMessage({
        text: response?.message || 'Person added successfully!',
        type: 'success'
      });

      // Reset form
      setFormData({
        personID: '',
        first_name: '',
        last_name: '',
        locationID: '',
        taxID: '',
        experience: '',
        miles: '',
        funds: ''
      });

    } catch (error) {
      console.error("Add Person Error:", error);
      setMessage({
        text: `Error: ${error.message || 'Failed to add person. Check constraints.'}`,
        type: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      personID: '',
      first_name: '',
      last_name: '',
      locationID: '',
      taxID: '',
      experience: '',
      miles: '',
      funds: ''
    });
    setMessage({ text: '', type: '' });
  };

  return (
    <div className="procedure-container">
      <h2>Procedure: Add Person</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">add_person()</div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Person Type</div>
                <select
                  className="form-input"
                  value={personType}
                  onChange={handlePersonTypeChange}
                >
                  <option value="passenger">Passenger</option>
                  <option value="pilot">Pilot</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Person ID</div>
                <input
                  className="form-input"
                  type="text"
                  name="personID"
                  value={formData.personID}
                  onChange={handleChange}
                  placeholder="Unique identifier"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">First Name</div>
                <input
                  className="form-input"
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  placeholder="First name"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Last Name</div>
                <input
                  className="form-input"
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  placeholder="Last name (optional)"
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
                  placeholder="Location identifier"
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

            {personType === 'pilot' && (
              <>
                <div className="form-group">
                  <div className="form-row">
                    <div className="form-label">Tax ID</div>
                    <input
                      className="form-input"
                      type="text"
                      name="taxID"
                      value={formData.taxID}
                      onChange={handleChange}
                      placeholder="Tax identifier"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <div className="form-row">
                    <div className="form-label">Experience</div>
                    <input
                      className="form-input"
                      type="text"
                      name="experience"
                      value={formData.experience}
                      onChange={handleChange}
                      placeholder="Flight hours"
                    />
                  </div>
                </div>
              </>
            )}

            {personType === 'passenger' && (
              <>
                <div className="form-group">
                  <div className="form-row">
                    <div className="form-label">Miles</div>
                    <input
                      className="form-input"
                      type="text"
                      name="miles"
                      value={formData.miles}
                      onChange={handleChange}
                      placeholder="Frequent flyer miles"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <div className="form-row">
                    <div className="form-label">Funds</div>
                    <input
                      className="form-input"
                      type="text"
                      name="funds"
                      value={formData.funds}
                      onChange={handleChange}
                      placeholder="Available funds"
                    />
                  </div>
                </div>
              </>
            )}
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

export default AddPerson;
