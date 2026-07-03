\# MongoDB Implementation



This directory contains the NoSQL implementation of the Boston Restaurant 

Database using MongoDB, demonstrating document-oriented data modeling and 

aggregation pipeline queries.



\## Collections



The MongoDB implementation includes three collections:



\- \*\*`restaurant`\*\* — Restaurant entities (id, name, category, rating, address, contact, status)

\- \*\*`review`\*\* — User reviews on restaurants (review\_id, user\_id, restaurant\_id, timestamps, review\_text, overall\_score)

\- \*\*`favoriterestaurant`\*\* — Many-to-many relationship between users and their favorite restaurants



\## Files



| File | Description |

|------|-------------|

| `01\_insert\_data.js` | Creates collections and inserts sample data |

| `02\_queries.js` | Four analytical queries demonstrating MongoDB aggregation |

| `sample\_results.md` | Expected results for each query |



\## How to Run



Using \*\*mongosh\*\* (MongoDB Shell):



```bash

\# Load data

mongosh < 01\_insert\_data.js



\# Run queries interactively

mongosh

> load("02\_queries.js")

```



\## Queries Demonstrated



1\. \*\*Simple filter\*\* — Retrieve restaurants by zip code (using `$regex`)

2\. \*\*Join + Filter\*\* — Restaurants with reviews scored 4+ and active status (using `$lookup`, `$match`)

3\. \*\*Aggregation\*\* — Top 10 most favorited restaurants (using `$group`, `$sort`, `$limit`)

4\. \*\*Multi-stage pipeline\*\* — Restaurant with highest favorite count that also has a review score of 4+ (using `$lookup`, `$match`, `$addFields`, `$sort`, `$limit`, `$project`)



\## Key MongoDB Concepts Applied



\- Document-oriented data modeling

\- Aggregation pipeline (`$lookup`, `$match`, `$group`, `$project`, `$sort`, `$limit`, `$addFields`)

\- Cross-collection joins using `$lookup`

\- Regex-based filtering

\- Field projection for query optimization

