use flight_tracking;
select * from airplane;


-- View representing add_airplane
select * from airplane ap 
join airline al 
on ap.airlineID=al.airlineID;

-- Test Cases Add airplane Sucess (Works Currently)
call add_airplane('Delta', 'n281fc', 6, 500, 'plane_41', 'Airbus', null, null, TRUE);

select * from airplane ap 
join airline al 
on ap.airlineID=al.airlineID;

-- Test Cases Add airplane Failure

-- Test Cases Add airport Success (Works Currently)
call add_airport('JFK', 'John F_Kennedy International', 'New York', 'New York', 'USA', 'port_33');

select * from airport;

-- Test Cases Add airport Failure

-- Test Cases Add Person Success (error currently? )
# Error: (1318, 'Incorrect number of arguments for PROCEDURE flight_tracking.add_airplane; expected 9, got 8')
call add_person('p61', 'Sabrina', 'Duncan', 'port_1', '366-50-3732', 27, null, null);

-- Test Cases Add Person Failure

-- Test Cases grant or revoke pilot Success
call grant_or_revoke_pilot_license('p1','jets');

-- Test Cases grant or revoke pilot Failure

-- Test Cases offer flight Success
call offer_flight('un_41', 'americas_three', 'United', 'n330ss', 0, '11:30:00', 400);

-- Test Cases offer flight Failure

-- Test Cases (flight landing) Sucess Case
call flight_landing('dl_10');

-- Test Cases (flight landing) Failure Case
call flight_landing('oh_99');

-- Test Cases (flight takeoff) Success Case
call flight_takeoff('ba_61');

-- Test Cases (flight takeoff) Failure Case
call flight_takeoff('oh_99');

-- Test Cases (Passenger board) Success Case
call passengers_board('dl_42');

-- Test Cases (Passenger board) Failure Case
call passengers_board('');

-- Test Cases passengers_disembark Success Case
call passengers_disembark('lf_67');

-- Test Cases passengers_disembark Failure Case
call passengers_disembark('lf_20');

-- Test Cases assign_pilot Success Case
call assign_pilot('ry_34', 'p19');

-- Test Cases recycle_crew Success Case
call recycle_crew('ke_64');

-- Test Cases retire_flight Success Case
call retire_flight('ke_88');

-- TO DO: Simulation Cycle and Sequences


