import { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import AddAirplane from './components/procedures/AddAirplane';
import AddAirport from './components/procedures/AddAirport';
import AddPerson from './components/procedures/AddPerson';
import GrantRevokePilotLicense from './components/procedures/GrantRevokePilotLicense';
import OfferFlight from './components/procedures/OfferFlight';
import FlightLanding from './components/procedures/FlightLanding';
import FlightTakeoff from './components/procedures/FlightTakeoff';
import PassengersBoard from './components/procedures/PassengersBoard';
import PassengersDisembark from './components/procedures/PassengersDisembark';
import AssignPilot from './components/procedures/AssignPilot';
import RecycleCrew from './components/procedures/RecycleCrew';
import RetireFlight from './components/procedures/RetireFlight';
import SimulationCycle from './components/procedures/SimulationCycle';
import FlightsInTheAir from './components/views/FlightsInTheAir';
// import FlightsOnTheGround from './components/views/FlightsOnTheGround';
// import PeopleInTheAir from './components/views/PeopleInTheAir';
// import PeopleOnTheGround from './components/views/PeopleOnTheGround';
// import RouteSummary from './components/views/RouteSummary';
// import AlternativeAirports from './components/views/AlternativeAirports';

function App() {
  const [currentView, setCurrentView] = useState('home');

  const renderView = () => {
    switch (currentView) {
      case 'add-airplane':
        return <AddAirplane />;
      case 'add-airport':
        return <AddAirport />;
      case 'add-person':
        return <AddPerson />;
      case 'grant-revoke-license':
        return <GrantRevokePilotLicense />;
      case 'offer-flight':
        return <OfferFlight />;
      case 'flight-landing':
        return <FlightLanding />;
      case 'flight-takeoff':
        return <FlightTakeoff />;
      case 'passengers-board':
        return <PassengersBoard />;
      case 'passengers-disembark':
        return <PassengersDisembark />;
      case 'assign-pilot':
        return <AssignPilot />;
      case 'recycle-crew':
        return <RecycleCrew />;
      case 'retire-flight':
        return <RetireFlight />;
      case 'simulation-cycle':
        return <SimulationCycle />;
      case 'flights-in-air':
        return <FlightsInTheAir />;
      // case 'flights-on-ground':
      //   return <FlightsOnTheGround />;
      // case 'people-in-air':
      //   return <PeopleInTheAir />;
      // case 'people-on-ground':
      //   return <PeopleOnTheGround />;
      // case 'route-summary':
      //   return <RouteSummary />;
      // case 'alternative-airports':
      //   return <AlternativeAirports />;
      default:
        return (
          <div className="home-container">
            <h1>Welcome to Airport Management System</h1>
            <p>Select an option from the menu to continue</p>
          </div>
        );
    }
  };

  return (
    <div className="app">
      <Navbar setCurrentView={setCurrentView} />
      <main className="main-content">
        {renderView()}
      </main>
    </div>
  );
}

export default App;