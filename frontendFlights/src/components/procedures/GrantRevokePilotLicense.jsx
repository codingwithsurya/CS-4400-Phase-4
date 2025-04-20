import React, { useState, useEffect } from 'react';
import { grantOrRevokePilotLicense, getPilots, getPilotLicenses } from '../../utils/api';

const GrantRevokePilotLicense = () => {
  const [formData, setFormData] = useState({
    personID: '',
    license: ''
  });

  const [message, setMessage] = useState({ text: '', type: '' });
  const [pilots, setPilots] = useState([]);
  const [existingLicenses, setExistingLicenses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch initial data (pilots and existing licenses)
  useEffect(() => {
    let isMounted = true;
    setMessage({ text: '', type: '' });

    const fetchData = async () => {
      setIsLoading(true);
      try {
        try {
          const [pilotsData, licensesData] = await Promise.all([
            getPilots(),
            getPilotLicenses()
          ]);

          if (isMounted) {
            // Process pilots data
            setPilots(pilotsData || []);
            
            // Process license data
            setExistingLicenses(licensesData || []);
          }
        } catch (apiError) {
          console.error('API error:', apiError);
          if (isMounted) {
            setMessage({ 
              text: `Could not fetch data from server. Using default values.`, 
              type: 'error' 
            });
            // Set some default data
            setPilots([
              { personID: 'p1', first_name: 'John', last_name: 'Doe' },
              { personID: 'p2', first_name: 'Jane', last_name: 'Smith' }
            ]);
            setExistingLicenses([
              { personID: 'p1', license: 'Boeing 737' },
              { personID: 'p1', license: 'Airbus A320' }
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData);
    setMessage({ text: '', type: '' });
    setIsLoading(true);

    // Validation
    if (!formData.personID) {
      setMessage({ text: 'Please select a pilot.', type: 'error' });
      setIsLoading(false);
      return;
    }
    if (!formData.license || formData.license.trim() === '') {
      setMessage({ text: 'License type is required.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Check if the selected pilot exists
    const pilotExists = pilots.some(pilot => pilot.personID === formData.personID);
    if (!pilotExists) {
      setMessage({ text: 'Selected pilot does not exist.', type: 'error' });
      setIsLoading(false);
      return;
    }

    // Prepare data for API
    const dataToSubmit = {
      ip_personID: formData.personID,
      ip_license: formData.license
    };

    try {
      console.log('Sending data to API:', dataToSubmit);
      // Call the API
      const response = await grantOrRevokePilotLicense(dataToSubmit);
      console.log('API response:', response);

      // Check if the license exists for this pilot
      const licenseExists = existingLicenses.some(
        lic => lic.personID === formData.personID && lic.license === formData.license
      );

      // Determine if we granted or revoked based on existence
      const action = licenseExists ? 'revoked' : 'granted';
      
      setMessage({
        text: response?.message || `Pilot license ${action} successfully!`,
        type: 'success'
      });

      // Update our local state of licenses
      if (licenseExists) {
        // License was revoked
        setExistingLicenses(prev => 
          prev.filter(lic => !(lic.personID === formData.personID && lic.license === formData.license))
        );
      } else {
        // License was granted
        const pilot = pilots.find(p => p.personID === formData.personID);
        const newLicense = {
          personID: formData.personID,
          license: formData.license,
          first_name: pilot?.first_name,
          last_name: pilot?.last_name
        };
        setExistingLicenses(prev => [...prev, newLicense]);
      }

      // Reset the form
      setFormData({
        personID: '',
        license: ''
      });

    } catch (error) {
      console.error("Grant/Revoke License Error:", error);
      setMessage({
        text: `Error: ${error.message || 'Failed to update pilot license. Please check the console for details.'}`,
        type: 'error'
      });
      // Additional error logging
      console.log('Error details:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Get current licenses for selected pilot
  const currentLicenses = formData.personID 
    ? existingLicenses.filter(lic => lic.personID === formData.personID).map(lic => lic.license) 
    : [];

  return (
    <div className="procedure-container">
      <h2>Procedure: Grant or Revoke Pilot License</h2>

      {message.text && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form">
        <div className="procedure-name">grant_or_revoke_pilot_license()</div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <div className="form-row">
                <div className="form-label">Pilot</div>
                <select
                  className="form-input"
                  name="personID"
                  value={formData.personID}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select a pilot</option>
                  {pilots.map(pilot => (
                    <option key={pilot.personID} value={pilot.personID}>
                      {pilot.first_name} {pilot.last_name} ({pilot.personID})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="form-row">
                <div className="form-label">License</div>
                <input
                  className="form-input"
                  type="text"
                  name="license"
                  value={formData.license}
                  onChange={handleChange}
                  placeholder="License type"
                  required
                />
              </div>
            </div>
          </div>

          {formData.personID && (
            <div className="info-box">
              <h4>Current Licenses for Selected Pilot:</h4>
              {currentLicenses.length > 0 ? (
                <ul>
                  {currentLicenses.map(license => (
                    <li key={license}>{license}</li>
                  ))}
                </ul>
              ) : (
                <p>No licenses currently held.</p>
              )}
            </div>
          )}

          <div className="form-actions">
            <button 
              type="button" 
              onClick={() => setFormData({ personID: '', license: '' })} 
              className="btn"
            >
              Cancel
            </button>
            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Submit'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default GrantRevokePilotLicense;
