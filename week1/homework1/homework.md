Question 1
Answer: --iidfile string

Question 2:
docker run -it --entrypoint /bin/bash python:3.9
pip list
Answer: 3
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4

Question 3:
Code: 
with helper as (SELECT lpep_pickup_datetime, lpep_dropoff_datetime, 
		CASE WHEN lpep_pickup_datetime > lpep_dropoff_datetime THEN 'Error'
			 WHEN lpep_pickup_datetime < lpep_dropoff_datetime THEN 'OK'
			 ELSE 'Nothing' END AS is_ok
FROM yellow_taxi WHERE DATE(lpep_pickup_datetime) = '2019-01-15' AND DATE(lpep_dropoff_datetime) = '2019-01-15')
select count(*) from helper;
Answer: 20530

Question 4:
Code:
select DATE(lpep_pickup_datetime) from yellow_taxi where trip_distance = (select max(trip_distance) from yellow_taxi);
Answer: 2019-01-15

Question 5:
Code:
select passenger_count, count(passenger_count)
from yellow_taxi 
where DATE(lpep_pickup_datetime) = '2019-01-01'  and passenger_count in (2,3)
group by passenger_count; 
Answer:
2: 1282
3: 254

Question 6:
Code:
with helper as (SELECT yt.*, tz.locationid, tz.borough, tz.zone as real_zone, tz.service_zone
FROM yellow_taxi yt
INNER JOIN taxi_zone tz
ON yt.pulocationid = tz.locationid
WHERE tz.zone = 'Astoria')
SELECT tz.zone
FROM helper h
INNER JOIN taxi_zone tz
ON h.dolocationid = tz.locationid
WHERE tip_amount = (SELECT MAX(tip_amount) FROM helper);
Answer:
Long Island City/Queens Plaza
