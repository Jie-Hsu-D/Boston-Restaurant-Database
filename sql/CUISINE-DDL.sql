DROP SCHEMA IF EXISTS CUISINE;
CREATE SCHEMA CUISINE;
USE CUISINE;

CREATE TABLE USER
(user_id CHAR(6) NOT NULL PRIMARY KEY,
nickname VARCHAR(50) NOT NULL,
bio VARCHAR(150),
profile_visibility ENUM('show_reviews_and_scores', 'show_visits', 'show_scores', 'hidden') DEFAULT 'show_reviews_and_scores');

CREATE TABLE VERIFICATED_USER
(user_id CHAR(6) NOT NULL,
email VARCHAR(100),
PRIMARY KEY (user_id),
FOREIGN KEY (user_id) REFERENCES USER (user_id) 
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE NORMAL_USER
(user_id CHAR(6) NOT NULL,
email VARCHAR(100),
PRIMARY KEY (user_id),
FOREIGN KEY (user_id) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE FOLLOW_USER
(follower CHAR(6) NOT NULL,
followed CHAR(6) NOT NULL,
PRIMARY KEY (follower, followed),
FOREIGN KEY (follower) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (followed) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE RESTAURANT 
(restaurant_id CHAR(6) NOT NULL PRIMARY KEY,
name VARCHAR(60) NOT NULL,
category VARCHAR(40),
price_level DOUBLE
    COMMENT 'price_level IN USD',
address VARCHAR(50),
website_url VARCHAR(50),
phone VARCHAR(20),
status VARCHAR(20) DEFAULT 'active',
    CONSTRAINT CC1 CHECK (status IN ('active', 'closed', 'moved', 'hidden')));
 
CREATE TABLE BUSINESSHOUR
(business_hours_id CHAR(6) NOT NULL PRIMARY KEY,
restaurant_id CHAR(6) NOT NULL,
weekday VARCHAR(10),
    CONSTRAINT CC2 CHECK (weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
start_time TIME,
end_time TIME,
FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT (restaurant_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE REVIEW
(review_id CHAR(6) NOT NULL PRIMARY KEY,
user_id CHAR(6) NOT NULL,
restaurant_id CHAR(6) NOT NULL,
created_at DATETIME,
updated_at DATETIME,
review_text VARCHAR(180),
overall_score INT,
    CONSTRAINT CC3 CHECK (overall_score BETWEEN 1 AND 5),
FOREIGN KEY (user_id ) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE PHOTO
(photo_id CHAR(6) NOT NULL PRIMARY KEY,
user_id CHAR(6) NOT NULL,
review_id CHAR(6) NOT NULL,
created_at DATETIME,
status VARCHAR(20) DEFAULT 'pending',
    CONSTRAINT CC4 CHECK (status IN ('approved', 'pending', 'rejected')),
emoji_content BLOB,
FOREIGN KEY (user_id) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (review_id) REFERENCES REVIEW (review_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE VISITVERIFICATION
(user_id CHAR(6) NOT NULL,
restaurant_id CHAR(6) NOT NULL,
status VARCHAR(20) DEFAULT 'pending'
    CONSTRAINT CC5 CHECK (status IN ('pending', 'verified', 'unverified')),
submitted_at DATETIME,
updated_at DATETIME,
PRIMARY KEY (user_id, restaurant_id),
FOREIGN KEY (user_id) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT (restaurant_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE FAVORITERESTAURANT
(user_id CHAR(6) NOT NULL,
restaurant_id CHAR(6) NOT NULL,
PRIMARY KEY (user_id, restaurant_id),
FOREIGN KEY (user_id) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT (restaurant_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE FAVORITEREVIEW
(user_id CHAR(6) NOT NULL,
review_id CHAR(6) NOT NULL,
PRIMARY KEY (user_id, review_id),
FOREIGN KEY (user_id) REFERENCES USER (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (review_id) REFERENCES REVIEW (review_id)
    ON DELETE CASCADE ON UPDATE CASCADE);

-- PRESENTATION
-- mysql
-- simple query
-- inner join / outer join
-- aggregate query
-- correlated query
-- all / any query
--

-- NoSQL Demo
-- a simple query
-- a more complex query
-- an aggregate (or MapReduce)

-- application Demo
-- Python or R
-- (show application connect database) 
-- at least 3 queries
-- Scatter plot
-- Histogram
-- Pie chart
-- Boxplot
