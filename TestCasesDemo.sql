use flight_tracking;
select * from airplane;


-- View representing add_airplane
select * from airplane ap 
join airline al 
on ap.airlineID=al.airlineID;

-- Test Cases Add airplane Sucess (Works Currently)
call add_airplane('Delta', 'n281fc', 6, 500, 'plane_41', 'Airbus', null, null, TRUE);
-- Note neo is integer column, so shows True=1

select * from airplane where tail_num='n281fc';


select * from airplane ap 
join airline al 
on ap.airlineID=al.airlineID;

-- Test Cases Add airplane Failure
select * from person;

-- Test Cases Add airport Success (Works Currently)
call add_airport('JFK', 'John F_Kennedy International', 'New York', 'New York', 'USA', 'port_33');

select * from airport where airportID='JFK';

-- Test Cases Add airport Failure

-- Test Cases Add Person Success
call add_person('p61', 'Sabrina', 'Duncan', 'port_1', '366-50-3732', 27, null, null);

select * from pilot;

select * from person pe
left join passenger pa on pa.personID=pe.personID
left join pilot pil on pil.personID=pe.personID;

-- Test Cases Add Person Failure

-- Test Cases grant or revoke pilot Success
call grant_or_revoke_pilot_license('p1','jets');

select * from pilot pil
join pilot_licenses pl on pil.personID=pl.personID
where pil.personID='p1';

-- Test Cases grant or revoke pilot Failure

-- Test Cases offer flight Success
call offer_flight('un_41', 'americas_three', 'United', 'n330ss', 0, '11:30:00', 400);

select * from flight 
where flightID='un_41';

-- Test Cases offer flight Failure

-- Test Cases (flight landing) Sucess Case
call flight_landing('dl_10');
select * from flight where flightID='dl_10';

-- Test Cases (flight landing) Failure Case
call flight_landing('oh_99');
select * from flight where flightID='oh_99';

-- Test Cases (flight takeoff) Success Case
call flight_takeoff('ba_61');
select * from flight where flightID='ba_61';

-- Test Cases (flight takeoff) Failure Case
call flight_takeoff('oh_99');
select * from flight where flightID='oh_99';

-- Test Cases (Passenger board) Success Case
call passengers_board('dl_42');

select * from passenger pa
join person pe on 
pa.personID=pe.personID where locationID in 
(select locationID from flight fl
join airplane a on fl.support_tail=a.tail_num
where flightID='dl_42');

-- Test Cases (Passenger board) Failure Case
call passengers_board('');

select * from passenger pa
join person pe on 
pa.personID=pe.personID where locationID in 
(select locationID from flight fl
join airplane a on fl.support_tail=a.tail_num
where flightID='');


-- Test Cases passengers_disembark Success Case
call passengers_disembark('lf_67');

select * from passenger pa
join person pe on 
pa.personID=pe.personID where locationID in 
(select locationID from flight fl
join airplane a on fl.support_tail=a.tail_num
where flightID='lf_67');

-- Test Cases passengers_disembark Failure Case
call passengers_disembark('lf_20');

select * from passenger pa
join person pe on 
pa.personID=pe.personID where locationID in 
(select locationID from flight fl
join airplane a on fl.support_tail=a.tail_num
where flightID='lf_20');

-- Test Cases assign_pilot Success Case
call assign_pilot('ry_34', 'p19');

-- Before being assigned, commanding flight is null;
select * from pilot pil
join person pe on pil.personID=pe.personID
where pe.personID='p19';

-- Test Cases recycle_crew Success Case
-- Consider the location of the pilots at the airport the flight landed at. 
select * from flight fl 
join airplane ai on fl.support_tail=ai.tail_num
where flightID='ke_64';

select *
from route_path
join leg on route_path.legID = leg.legID
where route_path.routeID = 'korea_direct' ## Fill in from query above 
and route_path.sequence = 1; ## Fill in from query above

-- Recycle pilots. shouldn't be commanding flight
select * from pilot where commanding_flight='ke_64';
call recycle_crew('ke_64');

-- Test Cases retire_flight Success Case
-- Just removes the flight. Flight must be empty. 
call retire_flight('ke_88');
select * from flight fl 
left join pilot pil
on fl.flightID=pil.commanding_flight
where flightID='ke_88';


-- TO DO: Simulation Cycle and Sequences


-- Sample Sequence
call passengers_board('dl_42');
call flight_takeoff('dl_42');

-- Check Views (Matching)
select * from alternative_airports;
select * from flights_in_the_air;
select * from flights_on_the_ground;
select * from people_in_the_air;
select * from people_on_the_ground;
select * from route_summary;







