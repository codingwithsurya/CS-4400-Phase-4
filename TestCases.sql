

-- Check if airplane tail num is unique
call flight_tracking.add_airplane('Air_France', 'n118f', 4, 400, NULL, 'Boeing', 0, '777', null);

-- Check if try to assign person as pilot
call assign_pilot('p21','aa12' );

-- Check if add person without license, tax ID or funds and miles
call add_person('p1', 'Jeanne', 'Nelson', 'port_1', NULL, NULL, NULL, NULL);

-- Check if add person without license, tax ID or funds and miles
call add_person('p1', 'Jeanne', 'Nelson', 'port_1', NULL, NULL, NULL, NULL);
-- Check if add duplicate person
call add_person('p2', 'Jeanne', 'Nelson', 'port_1', NULL, NULL, 100, 100);

-- Check if add boeing license pilot on airbus flight
call assign_pilot('af_19','p12');

-- Failing
-- Check if add airbus license pilot on boeing flight what happens; 
call assign_pilot('ry_34','p1');

-- Check if can assign pilot to flight with already assigned; 

-- Create tmp table ( )


-- A flight does not require pilots to be assigned if it’s not in the air.

-- A flight requires pilots to be assigned if it’s in the air.

-- Boeing / airbus limits for pilots before takeoff
-- Boeing needs to two pilots
call flight_takeoff();
select * from airplane;

select * from flight f join airplane a on f.support_tail=a.tail_num;

select * from pilot pi join 
pilot_licenses pl on pi.personID=pl.personID
order by commanding_flight;

select * from passenger_vacations order by personID;
select * from flight;
select * from person;

select max(sequence) from flight f 
join route_path rp on f.routeID=rp.routeID
group by f.flightID;


select * from airport;
select * from location;

-- Make sure that revenue is added to airline
select * from airline a join flight f on f.support_airline=a.airlineID;

--
select count(distinct(support_tail)) from flight group by support_tail;

select *
    from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID 
    join airport ai on l.departure=ai.airportID
    -- what about progress=0 ? What if there are 0's and 1's., THere should only be 0 or 1 in current database state per flight
    where -- f.progress in (0,1) and rp.sequence=1
	f.flightID= 'af_19'
    group by ai.locationID, a.locationID, a.tail_num, l.departure, l.arrival, f.cost;

select * from flight where flightID='af_19';

select * from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID 
    join airport ai on l.departure=ai.airportID
    -- what about progress=0 ? What if there are 0's and 1's., THere should only be 0 or 1 in current database state per flight
    -- where f.progress in (0,1) and rp.sequence=1
    where f.flightID= 'dl_10'
    -- and f.airplane_status='on_ground'
    group by ai.locationID, a.locationID, a.tail_num, l.departure, l.arrival, f.cost;


select * from flight where airplane_status='in_flight';

drop table if exists disembark_passengers_test;
create temporary table  disembark_passengers_test as
           select personID from person where personID in
           (select personID from leg l
           join route_path rp using(legID)
           join flight f using(routeID)
           join airplane a on f.support_tail = a.tail_num
           join person p using(locationID)
           join passenger_vacations pv using(personID)
           join airport ap using(airportID)
           where f.progress = rp.sequence
           and l.arrival = pv.airportID
           and f.flightID='dl_10');
select * from person where personID in (select * from disembark_passengers_test);
call passengers_disembark('dl_10');

select * from person where personID in (select * from disembark_passengers_test);


select p.personID, p.locationID
			from leg l 
			join route_path rp using(legID)
			join flight f using(routeID)
			join airplane a on f.support_tail = a.tail_num 
			join person p using(locationID) 
			join (select * from passenger_vacations) as pvv using(personID)
			join airport ap using(airportID)
			where f.progress = rp.sequence 
            and l.arrival = pvv.airportID; 
 --           and f.flightID = 'ke_64';

select p.personID, p.locationID, route_path
			from leg l 
			join route_path rp using(legID)
			join flight f using(routeID)
			join airplane a on f.support_tail = a.tail_num 
			join person p using(locationID) 
			join (select * from passenger_vacations) as pvv using(personID)
			join airport ap using(airportID)
			where f.progress = rp.sequence 
            and l.arrival = pvv.airportID; 


select * from flight f join
airplane a where f.tail_num=a.support_tail;

		select p.personID, f.flightID, p.locationID, l.departure, l.arrival, ap.airportiD, f.progress
			from leg l 
			join route_path rp using(legID)
			join flight f using(routeID)
			join airplane a on f.support_tail = a.tail_num 
			join person p using(locationID) 
			join (select * from passenger_vacations) as pvv using(personID)
			join airport ap using(airportID)
			where f.progress = rp.sequence 
            and l.arrival = pvv.airportID ;


-- Passengers board

-- Passengers disembark
select * from passenger pa
join person pe on pa.personID=pe.personID;

select * from flight;

call board_passengers();
call flight_tracking.passengers_board('aa_12');

START TRANSACTION;
call flight_tracking.passengers_disembark('aa_12');
COMMIT;


call recycle_crew('dl_10');
select * from person;

select * from flight f join airplane a on f.support_tail=a.tail_num;



select * from flight;

-- Flight simulation

call simulation_cycle();




    from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID 
    join airport ai on l.departure=ai.airportID
    -- what about progress=0 ? What if there are 0's and 1's., THere should only be 0 or 1 in current database state per flight
    -- where f.progress in (0,1) and rp.sequence=1
    where f.flightID= ip_flightID
    and f.progress = l.sequence
    group by ai.locationID, a.locationID, a.tail_num, l.departure, l.arrival, f.cost;

select * from flight;

select *
    from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID 
    join airport ai on l.departure=ai.airportID
    -- what about progress=0 ? What if there are 0's and 1's., THere should only be 0 or 1 in current database state per flight
    -- where f.progress in (0,1) and rp.sequence=1
    where f.flightID= 'dl_10';


