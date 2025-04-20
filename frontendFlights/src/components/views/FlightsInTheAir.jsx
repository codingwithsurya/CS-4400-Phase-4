import React, { useState, useEffect } from 'react';
import { getFlights } from '../../utils/api';
import './ViewStyles.css';

const FlightsInTheAir = () => {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFlightsInAir = async () => {
      try {
        // Fetch all flights using the exported getFlights function
        const allFlights = await getFlights();
        
        // Filter to only include flights that are in the air (airplane_status = 'in_flight')
        const inAirFlights = allFlights.filter(flight => 
          flight.airplane_status === 'in_flight');
        
        setFlights(inAirFlights);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching flights in air:', error);
        setError('Could not fetch flights in air. ' + error.message);
        setLoading(false);
      }
    };

    fetchFlightsInAir();
  }, []);

  if (loading) {
    return <div className="loading">Loading flights in air...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="view-container">
      <h1>Flights Currently In The Air</h1>
      {flights.length === 0 ? (
        <p>No flights are currently in the air.</p>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Flight ID</th>
                <th>Route ID</th>
                <th>Airline</th>
                <th>Tail Number</th>
                <th>Progress</th>
                <th>Status</th>
                <th>Next Time</th>
                <th>Cost</th>
              </tr>
            </thead>
            <tbody>
              {flights.map((flight) => (
                <tr key={flight.flightid}>
                  <td>{flight.flightid}</td>
                  <td>{flight.routeid}</td>
                  <td>{flight.support_airline || 'N/A'}</td>
                  <td>{flight.support_tail || 'N/A'}</td>
                  <td>{flight.progress}</td>
                  <td>{flight.airplane_status}</td>
                  <td>{flight.next_time || 'N/A'}</td>
                  <td>${flight.cost}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default FlightsInTheAir;
