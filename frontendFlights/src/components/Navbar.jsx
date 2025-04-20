import React from 'react';

const Navbar = ({ setCurrentView }) => {
  return (
    <nav className="navbar">
      <div className="nav-section">
        <h3>Create</h3>
        <div className="nav-links">
          <span className="nav-link" onClick={() => setCurrentView('add-airplane')}>Add Airplane</span>
          <span className="nav-link" onClick={() => setCurrentView('add-airport')}>Add Airport</span>
          <span className="nav-link" onClick={() => setCurrentView('add-person')}>Add Person</span>
          <span className="nav-link" onClick={() => setCurrentView('grant-revoke-license')}>Pilot License</span>
          <span className="nav-link" onClick={() => setCurrentView('offer-flight')}>Offer Flight</span>
        </div>
      </div>

      <div className="nav-section">
        <h3>Operations</h3>
        <div className="nav-links">
          <span className="nav-link" onClick={() => setCurrentView('flight-landing')}>Flight Landing</span>
          <span className="nav-link" onClick={() => setCurrentView('flight-takeoff')}>Flight Takeoff</span>
          <span className="nav-link" onClick={() => setCurrentView('passengers-board')}>Passengers Board</span>
          <span className="nav-link" onClick={() => setCurrentView('passengers-disembark')}>Passengers Disembark</span>
          <span className="nav-link" onClick={() => setCurrentView('assign-pilot')}>Assign Pilot</span>
          <span className="nav-link" onClick={() => setCurrentView('recycle-crew')}>Recycle Crew</span>
          <span className="nav-link" onClick={() => setCurrentView('retire-flight')}>Retire Flight</span>
          <span className="nav-link" onClick={() => setCurrentView('simulation-cycle')}>Simulation Cycle</span>
        </div>
      </div>

      <div className="nav-section">
        <h3>Views</h3>
        <div className="nav-links">
          <span className="nav-link" onClick={() => setCurrentView('flights-in-air')}>Flights In Air</span>
          <span className="nav-link" onClick={() => setCurrentView('flights-on-ground')}>Flights On Ground</span>
          <span className="nav-link" onClick={() => setCurrentView('people-in-air')}>People In Air</span>
          <span className="nav-link" onClick={() => setCurrentView('people-on-ground')}>People On Ground</span>
          <span className="nav-link" onClick={() => setCurrentView('route-summary')}>Route Summary</span>
          <span className="nav-link" onClick={() => setCurrentView('alternative-airports')}>Alternative Airports</span>
        </div>
      </div>
      
      <div className="nav-section">
        <h3>Home</h3>
        <div className="nav-links">
          <span className="nav-link" onClick={() => setCurrentView('home')}>Dashboard</span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
