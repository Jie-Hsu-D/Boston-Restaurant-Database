USE CUISINE;

-- Demo via MySQL workbench:
-- Demo must be live demo, all queries must have been tested and in a single tab ready to run. There must be 8-10 queries at different levels

-- 1st Simple query
-- Retrieve the restaurant ID, name, address, and phone number from the restaurant table where the zip code in the address is 'MA 02115'.

SELECT restaurant_id, name, address, phone
FROM restaurant
WHERE address LIKE '%MA 02115';

-- 2nd is the query with Aggregate function
-- Retrieve the user ID and the total number of restaurants visited by each user.

SELECT user_id, count(*) AS total_visits
FROM visitverification
GROUP BY user_id
ORDER BY total_visits DESC;  -- Sort the results in descending order by total_visit

-- 3rd query: Inner join
-- Retrieve the ID, name, phone, and address of restaurants 
-- that have at least one review with a score of 5 and the status are active.

 SELECT DISTINCT r.restaurant_id, r.name, r.phone, r.address
 FROM restaurant r, review re
 WHERE r.restaurant_id = re.restaurant_id 
 AND re.overall_score = 5
 AND r.status = 'active';
 
-- 4th  Nested query
-- Retrieve the restaurant ID, name, phone, status, and address for restaurants 
-- that have at least one review with a score of 5 and have the highest number of user favorites.

 SELECT DISTINCT r.restaurant_id, r.name, r.phone, r.status, r.address
 FROM restaurant r, review re
 WHERE r.restaurant_id = re.restaurant_id                -- 4 Use inner join to retrieve the restuatants that have review score of 5 and have the highest number of favorites
 AND re.overall_score = 5
 AND r.restaurant_id IN (
    SELECT f1.restaurant_id                              -- 3 Retrieve the restaurants that have the max total favorirte number
	FROM favoriterestaurant f1
    GROUP BY f1.restaurant_id 
    HAVING COUNT(*) = (
	    SELECT MAX(total_favorite_number)                -- 2 Select the Max total favoriate number
	    FROM (
	        SELECT COUNT(*) AS total_favorite_number     -- 1 Count the total favorite number of each restaurant
	        FROM favoriterestaurant
	        GROUP BY restaurant_id) AS f2
		)
    );
    
-- 5th Correlated query
-- Retrieve the user IDs and their follower counts for users ranked in the top 5 by number of followers.

SELECT f1.user_id, f1.number_of_followers
FROM (SELECT followed AS user_id, COUNT(*) AS number_of_followers
      FROM follow_user
      GROUP BY followed) AS f1
WHERE 5 > (
    SELECT COUNT(*)                                    -- count the users who are rank in the top 5
    FROM (SELECT COUNT(*) AS number_of_followers       -- Use correlated query to find the number of followers of each user
          FROM follow_user
          GROUP BY followed) AS f2
	WHERE f1.number_of_followers < f2.number_of_followers)
ORDER BY f1.number_of_followers DESC;
    
-- >=ALL/>ANY/Exists/Not Exists
-- 6th Query >=ALL
-- Retrieve the user IDs and their follower counts for users who have the largest number of followers.
SELECT followed AS user_id
FROM follow_user
GROUP BY followed
HAVING COUNT(*) >= ALL (
    SELECT COUNT(*) 
    FROM follow_user
    GROUP BY followed);
    
-- 7th Query Exists
-- Retrieve the user ID and total number of followers for each verified user.

SELECT followed AS user_id, COUNT(*) AS total_followed_number
FROM follow_user f
WHERE EXISTS (
    SELECT *
    FROM verificated_user v
    WHERE f.followed = v.user_id
    )
GROUP BY followed;

-- 8th Query with set operation (retrieve by Union): 
-- Retrieve the user ID of the user with the most followers,
-- as well as the user IDs of users who have given a score of 5 to at least 2 different restaurants.
 
SELECT followed AS user_id                     -- find out the user who has the most followers 
FROM follow_user
GROUP BY followed 
HAVING COUNT(*) = (
    SELECT MAX(total_followed_number)
    FROM (SELECT COUNT(*) AS total_followed_number
	    FROM follow_user
	    GROUP BY followed) AS f
        )
UNION                                         -- applied union to combine the tables
SELECT DISTINCT r1.user_id                    -- find out the user who has given a score of 5 to at least 2 different restaurants
FROM review r1
WHERE 1 < (
    SELECT COUNT(DISTINCT restaurant_id)
    FROM review r2
    WHERE Overall_score = 5
    AND r1.user_id = r2.user_id
    GROUP BY user_id
    );
    
-- 9th Query Subqueries in From 
-- Retrieve the restaurant ID, name, phone, status, and address for restaurants 
-- that have at least one review with a score of 5 and have the highest number of user favorites.

 SELECT r.restaurant_id, r.name, r.phone, r.status, r.address
 FROM restaurant r
 WHERE EXISTS (
     SELECT *
     FROM review re
     WHERE re.restaurant_id = r.restaurant_id
     AND overall_score = 5
     ) 
 AND r.restaurant_id IN (
    SELECT f1.restaurant_id
	FROM favoriterestaurant f1
    GROUP BY f1.restaurant_id 
    HAVING COUNT(*) = (
	    SELECT MAX(total_favorite_number)
	    FROM (
	        SELECT COUNT(*) AS total_favorite_number
	        FROM favoriterestaurant
	        GROUP BY restaurant_id) AS f2
		)
    );
    
-- 10th Query Subqueries in Select
-- Retrieve the restaurant ID and the average review score of each restaurant visited by user 100002.

SELECT v.restaurant_id, (                            -- caculated the average number of review score in the select clase
    SELECT AVG(overall_score) AS average_score
    FROM review re
    WHERE re.restaurant_id = v.restaurant_id
    GROUP BY restaurant_id) AS average_score
FROM visitverification v
WHERE v.user_id = '100002'                          -- find out the specified user in where clauser
