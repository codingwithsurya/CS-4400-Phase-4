-- CS4400: Introduction to Database Systems: Monday, March 3, 2025
-- Simple Airline Management System Course Project Mechanics [TEMPLATE] (v0)
-- Views, Functions & Stored Procedures

/* This is a standard preamble for most of our scripts.  The intent is to establish
a consistent environment for the database behavior. */
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'flight_tracking';
use flight_tracking;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [_] supporting functions, views and stored procedures
-- -----------------------------------------------------------------------------
/* Helpful library capabilities to simplify the implementation of the required
views and procedures. */
-- -----------------------------------------------------------------------------
drop function if exists leg_time;
delimiter //
create function leg_time (ip_distance integer, ip_speed integer)
	returns time reads sql data
begin
	declare total_time decimal(10,2);
    declare hours, minutes integer default 0;
    set total_time = ip_distance / ip_speed;
    set hours = truncate(total_time, 0);
    set minutes = truncate((total_time - hours) * 60, 0);
    return maketime(hours, minutes, 0);
end //
delimiter ;

-- [1] add_airplane()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airplane.  A new airplane must be sponsored
by an existing airline, and must have a unique tail number for that airline.
username.  An airplane must also have a non-zero seat capacity and speed. An airplane
might also have other factors depending on it's type, like the model and the engine.  
Finally, an airplane must have a new and database-wide unique location
since it will be used to carry passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airplane;
delimiter //
create procedure add_airplane (in ip_airlineID varchar(50), in ip_tail_num varchar(50),
	in ip_seat_capacity integer, in ip_speed integer, in ip_locationID varchar(50),
    in ip_plane_type varchar(100), in ip_maintenanced boolean, in ip_model varchar(50),
    in ip_neo boolean)
sp_main: begin

    -- Plane ID doesn't exist in airport table
    -- Duplicates, does it already exist
		-- Ensure airline exists
    if not exists (select 1 from airline where airlineID = ip_airlineID) then
        leave sp_main;
    end if;

    -- Ensure tail number is unique for the airline
    if exists (select 1 from airplane where airlineID = ip_airlineID and tail_num = ip_tail_num) then
        leave sp_main;
    end if;

    -- Ensure seat capacity and speed are non-null and positive
    if ip_seat_capacity is null or ip_speed is null or ip_seat_capacity <= 0 or ip_speed <= 0 then
        leave sp_main;
    end if;

    -- Ensure the location ID is provided (cannot be null or empty)
    if ip_locationID is null or ip_locationID = '' then
        leave sp_main;
    end if;

    -- 
    if ip_plane_type='Boeing' and ip_neo is not null then
        leave sp_main;
    end if;

    if (ip_plane_type is null or ip_plane_type not in ('Boeing', 'Airbus')) and (ip_neo is not null or ip_maintenanced is not null or ip_model is not null) then
        leave sp_main;
    end if;

    if (ip_plane_type is null or ip_plane_type not in ('Boeing', 'Airbus')) then
        leave sp_main;
    end if;


    -- Insert into location first due to FK constraint
    insert into location (locationID) values (ip_locationID);

    -- Insert into airplane
    insert into airplane (airlineID, tail_num, seat_capacity, speed, locationID, plane_type, maintenanced, model, neo)
    values (ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID, ip_plane_type, ip_maintenanced, ip_model, ip_neo);


end //
delimiter ;

-- [2] add_airport()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airport.  A new airport must have a unique
identifier along with a new and database-wide unique location if it will be used
to support airplane takeoffs and landings.  An airport may have a longer, more
descriptive name.  An airport must also have a city, state, and country designation. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airport;
delimiter //
create procedure add_airport (in ip_airportID char(3), in ip_airport_name varchar(200),
    in ip_city varchar(100), in ip_state varchar(100), in ip_country char(3), in ip_locationID varchar(50))
sp_main: begin

    -- Additional considerations

	-- Ensure that the airport and location values are new and unique
    -- Add airport and location into respective tables
    -- Ensure the airport ID is unique

    -- Ensure the airport ID is unique
    if exists (select * from airport where airportID = ip_airportID) then
        leave sp_main;
    end if;
    
    -- Ensure that location is unique and doesn't exist already in location table
    -- Ensure Databasewide
    if exists (select * from location where locationID = ip_locationID) then
        leave sp_main;
    end if;

    -- Ensure that location is unique and doesn't exist already in airport table
    if exists (select * from airport where locationID = ip_locationID) then
        leave sp_main;
    end if;

    -- Check if airport has a unique identifier
    if ip_airportID is null or ip_airportID = '' or exists (select * from airport where airportID=ip_airportID) then 
        leave sp_main;
    end if ;

    -- Verify that aiportID is not already existing in other tables
    if ip_airportID is null or ip_airportID = '' or exists (select * from leg where departure=ip_airportID or arrival=ip_airportID) then
        leave sp_main;
    end if ;

    -- Ensure that location including city, country and state are not null
    if not exists (select * from airport where (city is not null and country is not null and state is not null )) then
        leave sp_main;
    end if;

    -- Check additional airport location values

    insert into location (locationID) values (ip_locationID);
    insert into airport (airportID, airport_name, city, state, country, locationID)
    values (ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID);

end //
delimiter ;

-- [3] add_person()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new person.  A new person must reference a unique
identifier along with a database-wide unique location used to determine where the
person is currently located: either at an airport, or on an airplane, at any given
time.  A person must have a first name, and might also have a last name.

A person can hold a pilot role or a passenger role (exclusively).  As a pilot,
a person must have a tax identifier to receive pay, and an experience level.  As a
passenger, a person will have some amount of frequent flyer miles, along with a
certain amount of funds needed to purchase tickets for flights. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_person;
delimiter //
create procedure add_person (in ip_personID varchar(50), in ip_first_name varchar(100),
    in ip_last_name varchar(100), in ip_locationID varchar(50), in ip_taxID varchar(50),
    in ip_experience integer, in ip_miles integer, in ip_funds integer)
sp_main: begin

      -- Ensure personID is unique
    if exists (select 1 from person where personID = ip_personID) then
        leave sp_main;
    end if;

    -- Null check for personID or locationID
    if (ip_personID is null) or (ip_locationID is null) then
        leave sp_main;
    end if;

    -- Ensure location exists
    if not exists (select 1 from location where locationID = ip_locationID) then
        leave sp_main;
    end if;

    -- Ensure first name is provided
    if ip_first_name is null or ip_first_name = '' then
        leave sp_main;
    end if;

    -- Determine role: Pilot if taxID is not NULL, Passenger otherwise
    -- Ensure exclusivity (cannot have both pilot and passenger attributes according to description, though inputs allow it)
    -- If it's a pilot (taxID provided), passenger attributes (miles, funds) should ideally be NULL according to the description's intent.
    -- If it's a passenger (taxID not provided), pilot attributes (experience) should ideally be NULL.
    -- The structure allows passing all, let's prioritize taxID for pilot role.

    -- Insert into person table first
    insert into person (personID, first_name, last_name, locationID)
    values (ip_personID, ip_first_name, ip_last_name, ip_locationID);

    -- Check if pilot (based on taxID presence)
    if ip_taxID is not null and ip_taxID <> '' then
        -- Ensure taxID is unique among pilots
         if exists (select 1 from pilot where taxID = ip_taxID) then
             -- Rollback the person insert or handle error - let's just leave, assuming transaction handles rollback
             delete from person where personID = ip_personID; -- Manual rollback
             leave sp_main;
         end if;
        -- Insert into pilot table
        insert into pilot (personID, taxID, experience, commanding_flight)
        values (ip_personID, ip_taxID, coalesce(ip_experience, 0), NULL);
    else
        -- Check if passenger (at least one passenger attribute should be non-null, or just default to passenger if not pilot)
        -- Let's assume if not a pilot, they are a passenger.
        -- Insert into passenger table
        insert into passenger (personID, miles, funds)
        values (ip_personID, coalesce(ip_miles, 0), coalesce(ip_funds, 0));
    end if;

end //
delimiter ;

-- [4] grant_or_revoke_pilot_license()
-- -----------------------------------------------------------------------------
/* This stored procedure inverts the status of a pilot license.  If the license
doesn't exist, it must be created; and, if it aready exists, then it must be removed. */
-- -----------------------------------------------------------------------------
drop procedure if exists grant_or_revoke_pilot_license;
delimiter //
create procedure grant_or_revoke_pilot_license (in ip_personID varchar(50), in ip_license varchar(100))
sp_main: begin

   -- Ensure that the person is a valid pilot
    if not exists (select * from pilot where personID = ip_personID and taxID is not null) then
        leave sp_main;
    end if;
    
    -- Check if the license already exists for this pilot
    if exists (select * from pilot_licenses where personID = ip_personID and license = ip_license) then
        -- If it exists, delete it
        delete from pilot_licenses where personID = ip_personID and license = ip_license;
    else
        -- If it doesn't exist, add it
        insert into pilot_licenses (personID, license) values (ip_personID, ip_license);
    end if;



end //
delimiter ;

-- [5] offer_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new flight.  The flight can be defined before
an airplane has been assigned for support, but it must have a valid route.  And
the airplane, if designated, must not be in use by another flight.  The flight
can be started at any valid location along the route except for the final stop,
and it will begin on the ground.  You must also include when the flight will
takeoff along with its cost. */
-- -----------------------------------------------------------------------------
drop procedure if exists offer_flight;
delimiter //
create procedure offer_flight (in ip_flightID varchar(50), in ip_routeID varchar(50),
    in ip_support_airline varchar(50), in ip_support_tail varchar(50), in ip_progress integer,
    in ip_next_time time, in ip_cost integer)
sp_main: begin
    
    -- Calculating route length (max sequence)
    select max(sequence) into @route_value_length from route_path where routeID = ip_routeID;

    -- Special considerations:

    -- The flight must have a valid route (exists in the route table) is there more here? 
    -- It's fine if other values are null (tail_num etc.)
    if ip_routeID is null or not exists (select * from route where ip_routeID=routeID) then 
        leave sp_main;
    end if;

    -- The airplane, if designated, must not be in use by another flight
    if exists (select * from airplane a 
                join flight f on a.airlineID=f.support_airline 
                and a.tail_num=f.support_tail 
                where ip_support_tail=f.support_tail 
                and ip_support_airline=f.support_airline) then
        leave sp_main;
    end if;

    select max(sequence) into @MaxSeqCheck from flight f 
        join route_path rp on f.routeID=rp.routeID
        where f.flightID=ip_flightID
        group by f.flightID ;

    -- The flight cannot start at the final stop of the route
    if exists (select * from flight f where ip_flightID=f.flightID and ip_progress=@MaxSeqCheck) then 
        leave sp_main;
    end if;
    
    -- Ensure that the progress is less than the length of the route
    if ip_progress >= @route_value_length then
        leave sp_main;
    end if;
    
    -- A flight can be assigned before a supporting airplane is added
    -- So can handle null values, as long as route exists.But route must exist in route table
    -- If an airplane is specified, ensure it exists and is not already in use another airplane
    if  not exists (select * from airplane 
        where airlineID = ip_support_airline 
        and tail_num = ip_support_tail) then 
        leave sp_main;
    end if;
        
    -- Check if the airplane is already assigned to another flight
    if  exists (select * from flight 
        where support_airline = ip_support_airline 
        and flightID != ip_flightID
        and support_tail = ip_support_tail) then
        leave sp_main;
    end if;

    -- Check if time is provided
    if ip_next_time is null or ip_next_time='' then
        leave sp_main;
    end if;
    
    -- Check if cost is provided
    if ip_cost is null or ip_cost='' then
        leave sp_main;
    end if;


    -- Check if the flight already exists and update if it does (update of all values)
    if exists (select * from flight where flightID = ip_flightID) then
        update flight
        set routeID = ip_routeID,
            support_airline = ip_support_airline,
            support_tail = ip_support_tail,
            progress = ip_progress,
            airplane_status = 'on_ground',
            next_time = ip_next_time,
            cost = ip_cost

        -- apply to flight based on id
        where flightID = ip_flightID;
    else

        -- Create the flight with the airplane starting on the ground
        insert into flight (flightID, routeID, support_airline, support_tail, 
                            progress, airplane_status, next_time, cost)

        values (ip_flightID, ip_routeID, ip_support_airline, ip_support_tail, 
                ip_progress, 'on_ground', ip_next_time, ip_cost);
    end if;


end //
delimiter ;

-- [6] flight_landing()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight landing at the next airport
along it's route.  The time for the flight should be moved one hour into the future
to allow for the flight to be checked, refueled, restocked, etc. for the next leg
of travel.  Also, the pilots of the flight should receive increased experience, and
the passengers should have their frequent flyer miles updated. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_landing;
delimiter //
create procedure flight_landing (in ip_flightID varchar(50))
sp_main: begin
	-- Ensure that the flight exists
    -- Ensure that the flight is in the air
    -- Increment the pilot's experience by 1
    -- Increment the frequent flyer miles of all passengers on the plane
    -- Update the status of the flight and increment the next time to 1 hour later
		-- Hint: use addtime()
-- 	select ip_flightID;
	if ip_flightID not in (select flightID from flight) then
		-- select 'flightID not valid';
--         select ip_flightID;
        leave sp_main;
	end if;
    if (select airplane_status from flight where flightID = ip_flightID) <> 'in_flight' then
		-- select 'plane not in flight';
--         select ip_flightID;
        leave sp_main;
	end if;
    update pilot
	set experience = experience + 1
	where ip_flightID = commanding_flight;
	update passenger pa
-- 		join (select pe.personID, f.flightID, sum(l.distance), pe.locationID, pa.miles from passenger pa 
-- 		join person pe using(personID) 
-- 		join airplane a using(locationID) 
-- 		join flight f on f.support_tail = a.tail_num
-- 		join route_path rp using(routeID)
-- 		join leg l using(legID)
-- 		group by pa.personID) t using(personID)
		join person pe using(personID) 
		join airplane a using(locationID) 
		join flight f on f.support_tail = a.tail_num
		join route_path rp using(routeID)
		join leg l using(legID)
	set pa.miles = pa.miles + 
		(select l.distance from flight f 
        join route_path r using(routeID) join leg l using(legID)
		where flightID = ip_flightID and f.progress = r.sequence)
-- 		(select sum(l.distance) from flight f 
-- 		join route_path rp using(routeID) 
-- 		join leg l using(legID) where flightID = ip_flightID
-- 		group by f.flightID)
	where ip_flightID = flightID;
	update flight
	set airplane_status = 'on_ground',
		next_time = addtime(next_time, '1:00:00')
	where ip_flightID = flightID ;
			
end //
delimiter ;

-- [7] flight_takeoff()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight taking off from its current
airport towards the next airport along it's route.  The time for the next leg of
the flight must be calculated based on the distance and the speed of the airplane.
And we must also ensure that Airbus and general planes have at least one pilot
assigned, while Boeing must have a minimum of two pilots. If the flight cannot take
off because of a pilot shortage, then the flight must be delayed for 30 minutes. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_takeoff;
delimiter //
create procedure flight_takeoff (in ip_flightID varchar(50))
sp_main: begin

	 -- Ensure that the flight exists
    if not exists (select * from flight where flightID = ip_flightID) then
        leave sp_main;
    end if;
    
    -- Ensure that the flight is on the ground
    if not exists (select * from flight where flightID = ip_flightID and airplane_status = 'on_ground') then
        leave sp_main;
    end if;
    
    -- Get flight information ( only distinct flights currently showing in flight table)
    select routeID, progress, support_airline, support_tail, next_time into
    @route_id, @current_progress, @airline_id, @tail_num, @next_time
    from flight where flightID = ip_flightID;
    
    -- Ensure that the flight has another leg to fly
    -- Get the total number of legs in the route
    select count(*) into @total_legs
    from route_path
    where routeID = @route_id;
    
    if @current_progress >= @total_legs then
        leave sp_main;
    end if;
    
    -- Get the airplane type to determine required number of pilots
    select plane_type into @plane_type
    from airplane
    where airlineID = @airline_id and tail_num = @tail_num;
    
    -- Count the number of pilots assigned to this flight
    select count(*) into @pilot_count
    from pilot
    where commanding_flight = ip_flightID;
    
    -- Determine required number of pilots based on plane type
    set @required_pilots = 1; -- Default for Airbus and general planes
    if @plane_type = 'Boeing' then
        set @required_pilots = 2; -- Boeing requires 2 pilots
    end if;
    
    -- If there are not enough pilots, move next time to 30 minutes later
    if @pilot_count < @required_pilots then
        update flight
        set next_time = ADDTIME(next_time, '00:30:00')
        where flightID = ip_flightID;
        leave sp_main;
    end if;
    
    -- Get the current leg's distance based on progress
    select leg.distance, leg.legID into @leg_distance, @leg_id
    from route_path
    join leg on route_path.legID = leg.legID
    where route_path.routeID = @route_id and route_path.sequence = @current_progress + 1;
    
    -- Get the airplane speed
    select speed into @plane_speed
    from airplane
    where airlineID = @airline_id and tail_num = @tail_num;
    
    -- Calculate the flight time using leg_time function
    set @flight_time = leg_time(@leg_distance, @plane_speed);
    
    -- Update the flight status, progress, and next time
    update flight
    set progress = progress + 1,
        airplane_status = 'in_flight',
        next_time = ADDTIME(next_time, @flight_time)
    where flightID = ip_flightID;

end //
delimiter ;

-- [8] passengers_board()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting on a flight at
its current airport.  The passengers must be at the same airport as the flight,
and the flight must be heading towards that passenger's desired destination.
Also, each passenger must have enough funds to cover the flight.  Finally, there
must be enough seats to accommodate all boarding passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists passengers_board;
delimiter //
create procedure passengers_board (in ip_flightID varchar(50))
sp_main: begin


-- Ensure the flight exists
    if not exists (select * from flight where flightID = ip_flightID) then
        leave sp_main;
    end if;

    -- Ensure that the flight is on the ground
    if not exists (select * from flight where flightID = ip_flightID and airplane_status = 'on_ground') then
        leave sp_main;
    end if;

    -- Identify max possible sequence
    select max(rp.sequence) as maxVal into @MaxSeq
    from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID
    where flightID=ip_flightID
    group by flightID;
    
    -- Save flight info for current flight given ip_flightID
    select routeID, progress, support_airline, support_tail, next_time into
    @route_id, @current_progress, @airline_id, @tail_num, @next_time
    from flight where flightID = ip_flightID; 

    -- If progress value not < Max Sequence, then has no more legs to travel, leave sp_main
    if not exists ( select @current_progress < @MaxSeq) then
        leave sp_main;
    end if;

    -- The airport the airplane is currently located at as well as plane location
    select ai.locationID, a.locationID, a.tail_num, l.departure, l.arrival, f.cost, ai.airportID 
    into @airportLoc, @planeLocation, @tail_num, @departure, @arrival, @ticketCost, @airportID
    from flight f
    join airplane a on a.tail_num = f.support_tail
    join route_path rp on f.routeID = rp.routeID
    join leg l on rp.legID = l.legID 
    join airport ai on l.departure=ai.airportID
    -- what about progress=0 ? What if there are 0's and 1's., THere should only be 0 or 1 in current database state per flight
    where f.progress in (0,1) and rp.sequence=1
    and f.flightID= ip_flightID
    group by ai.locationID, a.locationID, a.tail_num, l.departure, l.arrival, f.cost;

    if @departure is null or @arrival is null then
        leave sp_main;
    end if;

    -- Get available seats (minus current passengers)
    select (airpl.seat_capacity - count(p.personID)), count(p.personID) into @availableSeats, @currentBoardedPassengers
    from airplane airpl
    left join person p on p.locationID = @planeLocation
    where airpl.tail_num = @tail_num
    group by airpl.tail_num, airpl.seat_capacity; 

-- Count Elgible passengers (have to be at sequence 1)
-- Filter out any sequences must be sequence 1 Must be flight arriving at that position
-- Plane new york,chicago,LA . Need to check, they would still board the flight
-- If going to chicago.
-- Route (sequence) --> check all legs if sequence
-- To Find passenger destination: Airport ID in passenger_vacations

    -- Handle duplicate passengers listed 
    select count(pe.personID) into @ElgiblePassengerCount from person pe
    join passenger pa on pa.personID=pe.personID
    join passenger_vacations pv on pv.personID=pe.personID
    where
    -- Can you have 0's here? 
    -- pv.sequence=1 and
    pe.locationID = @airportLoc and
    pa.funds >= @ticketCost and
    (pv.sequence = 1 and pv.airportID = @arrival)
    or 
    (pv.sequence = 0 and pv.airportID = @departure)
    and pv.airportID in ( select distinct(airportID) from passenger_vacations where pe.personId=pv.personID );

    -- and pv.airportID = @airportID;
    -- and pe.sequence in (0,1)
    --        and
    --        ((pe.sequence > 0 and pv_dest.airportID = @arrival)
     --       or 
     --       (pe.sequence <= 0 AND pv_dest.airportID = @departure))
   /* select * from passenger_vacations
   join passenger_vacations pv_dest on pv.personID=pv_dest.personID 
   and pv.sequence=pv_dest.sequence - 1 */
    -- Consider all possible stops for a sequence (how to do this)
    -- and @departure in (select distinct(airportID) from passenger_vacations pv2 where pv2.personID=pe.personID )
    -- Handle all airports the passenger is travelling to


     -- select @ElgiblePassengerCount, @availableSeats;
    -- Need to update both person and passenger tables

-- Dont board any passengers if the available seats are < elgible passengers

if @ElgiblePassengerCount <= @availableSeats then
    -- Update location and deduct funds for eligible passengers
    update person pe
    join passenger pa on pa.personID = pe.personID
    join passenger_vacations pv ON pv.personID = pe.personID
    set 
        pe.locationID = @planeLocation
        -- p.funds = p.funds - @ticketCost
    where  
        -- pv.sequence = 1 
        pe.locationID = @airportLoc
        and pa.funds >= @ticketCost
        and ((pv.sequence = 1 and pv.airportID = @arrival)
            or 
            (pv.sequence = 0 and pv.airportID = @departure))
            and pv.airportID in ( select distinct(airportID) from passenger_vacations where pe.personId=pv.personID );       
        -- Check full sequence for passenger
    update passenger pa
    join person pe on pe.personID = pa.personID
    join passenger_vacations pv on pv.personID = pa.personID
    set 
        pa.funds = pa.funds - @ticketCost
    where  
        -- pv.sequence = 1 
        pe.locationID = @planeLocation
        and pa.funds >= @ticketCost
        and ((pv.sequence = 1 and pv.airportID = @arrival)
            or 
            (pv.sequence = 0 and pv.airportID = @departure))
        and pv.airportID in ( select distinct(airportID) from passenger_vacations where pe.personId=pv.personID );
        -- check full sequence
    /* update airline airli 
    join flight fligh on fligh.support_airline=airli.airlineID
    set
        airli.Revenue = airli.Revenue + @ticketCost
    where 
        fligh.flightID=ip_flightID; */
else
    -- Don't board passengers
    leave sp_main;
end if;




end //
delimiter ;

-- [9] passengers_disembark()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting off of a flight
at its current airport.  The passengers must be on that flight, and the flight must
be located at the destination airport as referenced by the ticket. */
-- -----------------------------------------------------------------------------
drop procedure if exists passengers_disembark;
delimiter //
create procedure passengers_disembark (in ip_flightID varchar(50))
sp_main: begin

	-- Ensure the flight exists
    -- Ensure that the flight is on the ground
    -- Determine the list of passengers who are disembarking
	-- Use the following to check:
		-- Passengers must be on the plane supporting the flight
        -- Passenger has reached their immediate next destionation airport
	-- Move the appropriate passengers to the airport
    -- Update the vacation plans of the passengers
	DECLARE n INT DEFAULT 0;
	DECLARE i INT DEFAULT 0;
    if ip_flightID not in (select flightID from flight) then
		-- select 'flight does not exist';
        leave sp_main;
	end if;
	if (select airplane_status from flight where flightID = ip_flightID) <> 'on_ground' then
		-- select 'plane not on ground';
		leave sp_main;
	end if;
	select count(*) 
		from leg l 
		join route_path rp using(legID)
		join flight f using(routeID)
		join airplane a on f.support_tail = a.tail_num 
		join person p using(locationID) 
		join passenger_vacations pv using(personID)
		where f.progress = rp.sequence and l.arrival = pv.airportID and f.flightID = ip_flightID
		INTO n;
	SET i=0;
	WHILE i<n DO 
-- 		select ap.locationID
-- 			from leg l 
-- 			join route_path rp using(legID)
-- 			join flight f using(routeID)
-- 			join airplane a on f.support_tail = a.tail_num 
-- 			left join person p using(locationID) 
-- 			join passenger_vacations pv using(personID)
-- 			join airport ap using(airportID)
-- 			where flightID = ip_flightID
-- 			limit 1 offset i;
		update leg l2 
			join route_path rp using(legID)
			join flight f using(routeID)
			join airplane a on f.support_tail = a.tail_num 
			join person p using(locationID) 
			join passenger_vacations pv using(personID)
			join airport ap using(airportID)
        set p.locationID = (select ap.locationID
-- 			from leg l 
-- 			join route_path rp using(legID)
-- 			join flight f using(routeID)
-- 			join airplane a on f.support_tail = a.tail_num 
-- 			join person p using(locationID) 
-- 			join passenger_vacations pv using(personID)
-- 			join airport ap using(airportID)
			where flightID = ip_flightID
			limit 1 offset i)
        where f.progress = rp.sequence and l2.arrival = pv.airportID and f.flightID = ip_flightID ; -- l2.arrival = pv.airportID and
        delete from passenger_vacations pv
        where pv.personID = (select p.personID
			from leg l 
			join route_path rp using(legID)
			join flight f using(routeID)
			join airplane a on f.support_tail = a.tail_num 
			join person p using(locationID) 
			join (select * from passenger_vacations) as pvv using(personID)
			join airport ap using(airportID)
			where f.progress = rp.sequence 
            and l.arrival = pvv.airportID 
            and f.flightID = ip_flightID
			limit 1 offset i);
		SET i = i + 1;
	END WHILE;

end //
delimiter ;

-- [10] assign_pilot()
-- -----------------------------------------------------------------------------
/* This stored procedure assigns a pilot as part of the flight crew for a given
flight.  The pilot being assigned must have a license for that type of airplane,
and must be at the same location as the flight.  Also, a pilot can only support
one flight (i.e. one airplane) at a time.  The pilot must be assigned to the flight
and have their location updated for the appropriate airplane. */
-- -----------------------------------------------------------------------------
drop procedure if exists assign_pilot;
delimiter //
create procedure assign_pilot (in ip_flightID varchar(50), ip_personID varchar(50))
sp_main: begin

	-- Ensure the flight exists
    if not exists (select * from flight where flightID = ip_flightID) then
        leave sp_main;
    end if;
    
    -- Ensure that the flight is on the ground
    if not exists (select * from flight where flightID = ip_flightID and airplane_status = 'on_ground') then
        leave sp_main;
    end if;
    
    -- Get flight information
    select routeID, progress, support_airline, support_tail into
    @route_id, @current_progress, @airline_id, @tail_num
    from flight where flightID = ip_flightID;
    
    -- Ensure that the flight has further legs to be flown
    select count(*) into @total_legs
    from route_path
    where routeID = @route_id;
    
    if @current_progress >= @total_legs then
        leave sp_main;
    end if;
    
    -- Ensure that the pilot exists
    if not exists (select * from pilot where personID = ip_personID) then
        leave sp_main;
    end if;
    
    -- Ensure the pilot is not already assigned to a flight
    if exists (select * from pilot where personID = ip_personID and commanding_flight is not null) then
        leave sp_main;
    end if;
    
    -- Get the airplane type to check for appropriate license
    select plane_type into @plane_type
    from airplane
    where airlineID = @airline_id and tail_num = @tail_num;
    
    -- Ensure that the pilot has the appropriate license for the airplane type
    if @plane_type is null or not exists (
        select license from pilot_licenses 
        where personID = ip_personID 
        and license = @plane_type
    ) then
        leave sp_main;
    end if;
    
    -- Get the locations of the pilot and airplane
    select locationID into @pilot_location
    from person
    where personID = ip_personID;
    
    select locationID into @airplane_location
    from airplane
    where airlineID = @airline_id and tail_num = @tail_num;
    
    -- Get the departure airport for the current progress of the flight
    select leg.departure into @current_airport
    from route_path
    join leg on route_path.legID = leg.legID
    where route_path.routeID = @route_id and route_path.sequence = @current_progress + 1;
    
    -- Ensure the pilot is at the same airport as the airplane
    select locationID into @airport_location
    from airport
    where airportID = @current_airport;
    
    if @pilot_location != @airport_location then
        leave sp_main;
    end if;
    
    -- Assign the pilot to the flight
    update pilot
    set commanding_flight = ip_flightID
    where personID = ip_personID;
    
    -- Update the pilot's location to be on the plane
    update person
    set locationID = @airplane_location
    where personID = ip_personID;

end //
delimiter ;

-- [11] recycle_crew()
-- -----------------------------------------------------------------------------
/* This stored procedure releases the assignments for a given flight crew.  The
flight must have ended, and all passengers must have disembarked. */
-- -----------------------------------------------------------------------------
drop procedure if exists recycle_crew;
delimiter //
create procedure recycle_crew (in ip_flightID varchar(50))
sp_main: begin

	-- Ensure that the flight is on the ground
    if not exists (select * from flight where flightID = ip_flightID and airplane_status = 'on_ground') then
        leave sp_main;
    end if;
    
    -- Get flight information
    select routeID, progress, support_airline, support_tail into
    @route_id, @current_progress, @airline_id, @tail_num
    from flight where flightID = ip_flightID;
    
    -- Ensure that the flight does not have any more legs
    select max(sequence) into @max_sequence
    from route_path
    where routeID = @route_id;
    
    if @current_progress < @max_sequence then
        leave sp_main;
    end if;
    
    -- Get the airplane's location
    select locationID into @airplane_location
    from airplane
    where airlineID = @airline_id and tail_num = @tail_num;
    
    -- Ensure that the flight is empty of passengers
    select count(*) into @passenger_count
    from person p
    join passenger pa on p.personID = pa.personID
    where p.locationID = @airplane_location;
    
    if @passenger_count > 0 then
        leave sp_main;
    end if;
    
    -- Get the current airport location
    select leg.arrival into @current_airport
    from route_path
    join leg on route_path.legID = leg.legID
    where route_path.routeID = @route_id and route_path.sequence = @current_progress;
    
    select locationID into @airport_location
    from airport
    where airportID = @current_airport;
    
    -- Move all pilots to the airport where the plane is located
    update person p
    join pilot pi on p.personID = pi.personID
    set p.locationID = @airport_location
    where pi.commanding_flight = ip_flightID;
    
    -- Update assignments of all pilots
    update pilot
    set commanding_flight = null
    where commanding_flight = ip_flightID;

end //
delimiter ;

-- [12] retire_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a flight that has ended from the system.  The
flight must be on the ground, and either be at the start its route, or at the
end of its route.  And the flight must be empty - no pilots or passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists retire_flight;
delimiter //
create procedure retire_flight (in ip_flightID varchar(50))
sp_main: begin

	-- Ensure that the flight is on the ground
    -- If not exists (select * from flight where status=) 
    -- Ensure that the flight does not have any more legs
    -- Ensure that there are no more people on the plane supporting the flight
    -- Remove the flight from the system
	if (select airplane_status from flight where flightID = ip_flightID) <> 'on_ground' then
		-- select 'plane not on ground';
		leave sp_main;
	end if;
	if (select progress from flight f where flightID = ip_flightID) <>
		(select max(sequence) from flight f join route_path rp using(routeID) where flightID = ip_flightID)
		then
		-- select 'flight not at start or end';
        leave sp_main;
	end if;
    if (select count(*) from person p where locationID = 
		(select locationID from flight f join airplane a on support_tail = tail_num where f.flightID = ip_flightID)) 
		<> 0
		then
		-- select 'flight is not empty';
        leave sp_main;
	end if;
    delete from flight 
    where flightID = ip_flightID;
    update pilot
    set commanding_flight = null
    where commanding_flight = ip_flightID;

end //
delimiter ;

-- [13] simulation_cycle()
-- -----------------------------------------------------------------------------
/* This stored procedure executes the next step in the simulation cycle.  The flight
with the smallest next time in chronological order must be identified and selected.
If multiple flights have the same time, then flights that are landing should be
preferred over flights that are taking off.  Similarly, flights with the lowest
identifier in alphabetical order should also be preferred.

If an airplane is in flight and waiting to land, then the flight should be allowed
to land, passengers allowed to disembark, and the time advanced by one hour until
the next takeoff to allow for preparations.

If an airplane is on the ground and waiting to takeoff, then the passengers should
be allowed to board, and the time should be advanced to represent when the airplane
will land at its next location based on the leg distance and airplane speed.

If an airplane is on the ground and has reached the end of its route, then the
flight crew should be recycled to allow rest, and the flight itself should be
retired from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists simulation_cycle;
delimiter //
create procedure simulation_cycle ()
sp_main: begin

	-- Identify the next flight to be processed
    -- Select the flight with the smallest next_time, prioritizing landing flights over takeoff flights,
    -- and then the lowest flight ID alphabetically
    select flightID
    from flight
    order by next_time, 
        case when airplane_status = 'in_flight' then 0 else 1 end, 
        flightID asc
    limit 1
    into @selected_flightID;
    
    -- If no flight found, exit
    if @selected_flightID is null then
        leave sp_main;
    end if;
    
    -- Get current flight status
    select airplane_status, routeID, progress into @flight_status, @route_id, @current_progress
    from flight
    where flightID = @selected_flightID;
    
    -- Get max sequence for the route to determine if flight has reached the end
    
    /* -- Run this after in_flight check step
    select max(sequence) into @max_sequence
    from route_path
    where routeID = @route_id; */
    
    -- If the flight is in the air:
    if @flight_status = 'in_flight' then
        select max(sequence) into @max_sequence
        from route_path
        where routeID = @route_id;
        -- Land the flight
        call flight_landing(@selected_flightID);
        
        -- Disembark passengers
        call passengers_disembark(@selected_flightID);
        
        -- If it has reached the end of its route
        if @current_progress = @max_sequence then
            -- Recycle the crew
            call recycle_crew(@selected_flightID);
            
            -- Retire the flight
            -- In air and about to approach final airport. Before retire, disembark
            call retire_flight(@selected_flightID);
        /* else
            -- Update the time for the next takeoff (1 hour from now)
            update flight
            set next_time = addtime(next_time, '01:00:00')
            where flightID = @selected_flightID; */
        end if;
    
    -- If the flight is on the ground:
    else
        -- Board passengers
        call passengers_board(@selected_flightID);
        
        -- Save flight info before takeoff to calculate new time
        select support_airline, support_tail, progress, routeID, next_time into 
        @airline_id, @tail_num, @current_progress, @route_id, @current_time
        from flight
        where flightID = @selected_flightID;
        
        -- Get the next leg's distance
        select l.distance into @leg_distance
        from route_path rp
        join leg l on rp.legID = l.legID
        where rp.routeID = @route_id and rp.sequence = @current_progress + 1;
        
        -- Get the airplane's speed
        select speed into @airplane_speed
        from airplane
        where airlineID = @airline_id and tail_num = @tail_num;
        
        -- Have the plane takeoff
        call flight_takeoff(@selected_flightID);
        
        -- Calculate flight time in hours (distance/speed) and convert to time format
        set @flight_hours = @leg_distance / @airplane_speed;
        set @flight_minutes = floor((@flight_hours - floor(@flight_hours)) * 60);
        set @flight_seconds = floor(((@flight_hours - floor(@flight_hours)) * 60 - @flight_minutes) * 60);
        set @flight_time = concat(floor(@flight_hours), ':', @flight_minutes, ':', @flight_seconds);
        
        -- Update the flight's next_time to when it will land
        /* update flight
        set next_time = addtime(@current_time, @flight_time)
        where flightID = @selected_flightID; */
    end if;

end //
delimiter ;

-- [14] flights_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where flights that are currently airborne are located. 
We need to display what airports these flights are departing from, what airports 
they are arriving at, the number of flights that are flying between the 
departure and arrival airport, the list of those flights (ordered by their 
flight IDs), the earliest and latest arrival times for the destinations and the 
list of planes (by their respective flight IDs) flying these flights. */
-- -----------------------------------------------------------------------------
create or replace view flights_in_the_air (departing_from, arriving_at, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as
select 
    l.departure as departing_from,
    l.arrival as arriving_at,
    count(f.flightID) as num_flights,
    group_concat(f.flightID order by f.flightID separator ',') as flight_list,
    min(f.next_time) as earliest_arrival,
    max(f.next_time) as latest_arrival,
    group_concat(a.locationID order by f.flightID separator ',') as airplane_list
from flight f
join route_path rp on f.routeID = rp.routeID and f.progress = rp.sequence
join leg l on rp.legID = l.legID
join airplane a on f.support_airline = a.airlineID and f.support_tail = a.tail_num
where f.airplane_status = 'in_flight'
group by l.departure, l.arrival;

-- [15] flights_on_the_ground()
-- ------------------------------------------------------------------------------
/* This view describes where flights that are currently on the ground are 
located. We need to display what airports these flights are departing from, how 
many flights are departing from each airport, the list of flights departing from 
each airport (ordered by their flight IDs), the earliest and latest arrival time 
amongst all of these flights at each airport, and the list of planes (by their 
respective flight IDs) that are departing from each airport.*/
-- ------------------------------------------------------------------------------
create or replace view flights_on_the_ground (departing_from, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as 
    -- select * from airports join
select
    case 
        when f.progress > 0 then l.arrival
        else l.departure
    end as departing_from,
    count(f.flightID) as num_flights,
    group_concat(f.flightID order by f.flightID separator ',') as flight_list,
    min(f.next_time) as earliest_arrival,
    max(f.next_time) as latest_arrival,
    group_concat(a.locationID order by f.flightID separator ',') as airplane_list
from flight f
join airplane a on a.tail_num = f.support_tail 
join route_path rp on f.routeID = rp.routeID
join leg l on rp.legID = l.legID
where f.airplane_status = 'on_ground' 
and sequence = f.progress + case when f.progress = 0 then 1 else 0 end
group by departing_from;

-- [16] people_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently airborne are located. We 
need to display what airports these people are departing from, what airports 
they are arriving at, the list of planes (by the location id) flying these 
people, the list of flights these people are on (by flight ID), the earliest 
and latest arrival times of these people, the number of these people that are 
pilots, the number of these people that are passengers, the total number of 
people on the airplane, and the list of these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_in_the_air (departing_from, arriving_at, num_airplanes,
	airplane_list, flight_list, earliest_arrival, latest_arrival, num_pilots,
	num_passengers, joint_pilots_passengers, person_list) as
-- select '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_';
select departure, arrival, count(distinct tail_num), group_concat(distinct a.locationID), group_concat(distinct flightID),
min(next_time), max(next_time),
count(distinct a.locationID), count(distinct t1.personID),
count(distinct a.locationID) + count(distinct t1.personID), group_concat(distinct p.personID)
from leg 
	join route_path rp using(legID)
	join flight f using(routeID)
	join airplane a on tail_num = support_tail
    join pilot pi on flightID = commanding_flight
    left join (select * from person p where p.personID in (select pa.personID from passenger pa)) t1 using(locationID)
    join person p using(locationID)
where airplane_status = 'in_flight' and progress = sequence group by departure, arrival order by departure;

-- [17] people_on_the_ground()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently on the ground and in an 
airport are located. We need to display what airports these people are departing 
from by airport id, location id, and airport name, the city and state of these 
airports, the number of these people that are pilots, the number of these people 
that are passengers, the total number people at the airport, and the list of 
these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_on_the_ground (departing_from, airport, airport_name,
	city, state, country, num_pilots, num_passengers, joint_pilots_passengers, person_list) as
select 
    ap.airportID as departing_from, -- The airport they are currently at
    ap.locationID as airport_location,
    ap.airport_name,
    ap.city,
    ap.state,
    ap.country,
    count(distinct pi.personID) as num_pilots,
    count(distinct pa.personID) as num_passengers,
    count(distinct p.personID) as joint_pilots_passengers,
    group_concat(distinct p.personID order by p.personID separator ',') as person_list
from person p
join airport ap on p.locationID = ap.locationID -- Join person directly to airport location
left join pilot pi on p.personID = pi.personID
left join passenger pa on p.personID = pa.personID
group by ap.airportID, ap.locationID, ap.airport_name, ap.city, ap.state, ap.country;

-- [18] route_summary()
-- -----------------------------------------------------------------------------
/* This view will give a summary of every route. This will include the routeID, 
the number of legs per route, the legs of the route in sequence, the total 
distance of the route, the number of flights on this route, the flightIDs of 
those flights by flight ID, and the sequence of airports visited by the route. */
-- -----------------------------------------------------------------------------
create or replace view route_summary (route, num_legs, leg_sequence, route_length,
	num_flights, flight_list, airport_sequence) as

select r1.routeID as routeIDCheck, 
    count(distinct r2.legID) as num_legs,
    group_concat(distinct r2.legID order by r2.sequence ASC separator ',') AS leg_sequence,
    -- Make sure this is INT
    -- If flight count is 0, then return current distance
    case when count(distinct f.flightID) = 0 then 
            cast(sum(l.distance) as signed)
    -- If flight has flight num > 1
        else cast(sum(l.distance) / count(distinct f.flightID) AS signed)
    end as route_length,
    count(distinct f.flightID) as num_flights,
    group_concat(distinct f.flightID separator ',') AS flight_list,
    
    
    group_concat(distinct
        concat(
            case when r2.sequence = 1 then l.departure  
                else (
                    select l_initial.arrival 
                    from route_path rp_initial 
                    join leg l_initial on rp_initial.legID = l_initial.legID 
                    where rp_initial.routeID = r1.routeID
                    -- match sequences 
                    and rp_initial.sequence = r2.sequence - 1
                    )
            end,'->',l.arrival)
        order by r2.sequence asc separator ',') as airport_sequence

    from
    route r1
    -- Join route info and leg
    join route_path r2 on r1.routeID = r2.routeID
    join leg l on r2.legID = l.legID
    left join flight f on r1.routeID = f.routeID    
    group by
    r1.routeID;


-- [19] alternative_airports()
-- -----------------------------------------------------------------------------
/* This view displays airports that share the same city and state. It should 
specify the city, state, the number of airports shared, and the lists of the 
airport codes and airport names that are shared both by airport ID. */
-- -----------------------------------------------------------------------------
create or replace view alternative_airports (city, state, country, num_airports,
	airport_code_list, airport_name_list) as
select city, state, group_concat(distinct country) as country, count(airportID) as num_airports, group_concat(airportID order by airportID asc) as airport_code_list, group_concat(airport_name order by airportID asc) as airport_name_list
from airport a
group by city, state having count(airportID) > 1;
