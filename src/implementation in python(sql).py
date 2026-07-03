#Demo via MySQL workbench:
#Demo must be live demo, all queries must have been tested and in a single tab ready to run. 
#There must be 8-10 queries at different levels

#1st Simple query
#Retrieve the restaurant ID, name, address, and phone number from the restaurant table where the zip code in the address is 'MA 02115'.

import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

DB_CONFIG ={
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),   
    "database": os.getenv("MYSQL_DATABASE")
}

conn = mysql.connector.connect(**DB_CONFIG)

query1 = """
SELECT restaurant_id, name, address, phone
FROM restaurant
WHERE address LIKE '%MA 02115';
"""

df = pd.read_sql_query(query1, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

#2nd is the query with Aggregate function
#Retrieve the user ID and the total number of restaurants visited by each user.

query2 = """
SELECT user_id, count(*) AS total_visits
FROM visitverification
GROUP BY user_id
ORDER BY total_visits DESC; 
"""                                 
# Sort the results in descending order by total_visit

df = pd.read_sql_query(query2, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

#3rd query: Inner join
#Retrieve the ID, name, phone, and address of restaurants 
#that have at least one review with a score of 5 and the status are active.

query3 = """
SELECT DISTINCT r.restaurant_id, r.name, r.phone, r.address
FROM restaurant r, review re
WHERE r.restaurant_id = re.restaurant_id 
AND re.overall_score = 5
AND r.status = 'active';
"""

df = pd.read_sql_query(query3, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

#4th  Nested query
#Retrieve the restaurant ID, name, phone, status, and address for restaurants 
#that have at least one review with a score of 5 and have the highest number of user favorites.

query4 = """
SELECT DISTINCT r.restaurant_id, r.name, r.phone, r.status, r.address
FROM restaurant r, review re
WHERE r.restaurant_id = re.restaurant_id                
AND re.overall_score = 5
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
"""

df = pd.read_sql_query(query4, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)
    
#5th Correlated query
#Retrieve the user IDs and their follower counts for users ranked in the top 5 by number of followers.

query5 = """
SELECT f1.user_id, f1.number_of_followers
FROM (SELECT followed AS user_id, COUNT(*) AS number_of_followers
      FROM follow_user
      GROUP BY followed) AS f1
WHERE 5 > (
    SELECT COUNT(*)                                    
    FROM (SELECT COUNT(*) AS number_of_followers       
          FROM follow_user
          GROUP BY followed) AS f2
	WHERE f1.number_of_followers < f2.number_of_followers)
ORDER BY f1.number_of_followers DESC;
"""
df = pd.read_sql_query(query5, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)
    
# >=ALL/>ANY/Exists/Not Exists
# 6th Query >=ALL
# Retrieve the user IDs and their follower counts for users who have the largest number of followers.

query6 = """
SELECT followed AS user_id
FROM follow_user
GROUP BY followed
HAVING COUNT(*) >= ALL (
    SELECT COUNT(*) 
    FROM follow_user
    GROUP BY followed);
"""
df = pd.read_sql_query(query6, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

# 7th Query Exists
# Retrieve the user ID and total number of followers for each verified user.
query7 = """
SELECT followed AS user_id, COUNT(*) AS total_followed_number
FROM follow_user f
WHERE EXISTS (
    SELECT *
    FROM verificated_user v
    WHERE f.followed = v.user_id
    )
GROUP BY followed;
"""
df = pd.read_sql_query(query7, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

# 8th Query with set operation (retrieve by Union): 
# Retrieve the user ID of the user with the most followers,
# as well as the user IDs of users who have given a score of 5 to at least 2 different restaurants.

query8 = """
SELECT followed AS user_id
FROM follow_user
GROUP BY followed 
HAVING COUNT(*) = (
    SELECT MAX(total_followed_number)
    FROM (SELECT COUNT(*) AS total_followed_number
	    FROM follow_user
	    GROUP BY followed) AS f
        )
UNION
SELECT DISTINCT r1.user_id
FROM review r1
WHERE 1 < (
    SELECT COUNT(DISTINCT restaurant_id)
    FROM review r2
    WHERE Overall_score = 5
    AND r1.user_id = r2.user_id
    GROUP BY user_id
    );
"""

df = pd.read_sql_query(query8, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

# 9th Query Subqueries in From 
# Retrieve the restaurant ID, name, phone, status, and address for restaurants 
# that have at least one review with a score of 5 and have the highest number of user favorites.

query9 = """
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
"""
df = pd.read_sql_query(query9, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)
  
# 10th Query Subqueries in Select
# Retrieve the restaurant ID and the average review score of each restaurant visited by user 100002.

query10 = """
SELECT v.restaurant_id, (
    SELECT AVG(overall_score) AS average_score
    FROM review re
    WHERE re.restaurant_id = v.restaurant_id
    GROUP BY restaurant_id) AS average_score
FROM visitverification v
WHERE v.user_id = '100002'
"""
df = pd.read_sql_query(query10, conn)
pd.set_option('display.max_columns', None)
print("\n")
print(df)

conn.close()