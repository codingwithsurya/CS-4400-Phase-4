import React, { useState } from 'react';
import { simulationCycle } from '../../utils/api';
import './SimulationCycle.css';

const SimulationCycle = () => {
  const [message, setMessage] = useState({ text: '', type: '' });
  const [isLoading, setIsLoading] = useState(false);

  const handleRunSimulation = async () => {
    setMessage({ text: '', type: '' });
    setIsLoading(true);

    try {
      await simulationCycle();
      setMessage({ 
        text: 'Simulation cycle completed successfully!', 
        type: 'success' 
      });
    } catch (error) {
      console.error('Error running simulation cycle:', error);
      setMessage({ 
        text: `Error running simulation cycle: ${error.message}`, 
        type: 'error' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="procedure-container">
      <h2>Simulation Cycle</h2>
      <div className="procedure-description">
        Execute the next step in the simulation cycle. This will advance time for the flight with the 
        smallest next time, updating its status based on whether it's taking off, landing, or continuing its route.
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="procedure-form-container">
        <div className="procedure-form">
          <p>
            Clicking the button below will process the next flight in chronological order. The selected flight will 
            progress according to its current status and position along its route.
          </p>
        </div>

        <div className="form-actions">
          <button 
            type="button" 
            className="btn" 
            onClick={handleRunSimulation}
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : 'Advance Simulation'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimulationCycle;
