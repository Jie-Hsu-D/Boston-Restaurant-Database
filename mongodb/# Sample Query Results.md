# Sample Query Results

Reference output from running `02_queries.js` on the sample dataset.

## Query 1: Restaurants in zip 02115

```json
[
  {
    "restaurant_id": 200001,
    "name": "McDonald's",
    "address": "114 Fenway Terrace, Boston, MA 02115",
    "phone": "1-800-244-6227"
  },
  {
    "restaurant_id": 200002,
    "name": "KFC",
    "address": "282 Huntington Crossing, Boston, MA 02115",
    "phone": "1-800-225-5532"
  },
  {
    "restaurant_id": 200004,
    "name": "Wendy's",
    "address": "77 Symphony Gate, Boston, MA 02115",
    "phone": "1-888-624-8140"
  },
  {
    "restaurant_id": 200005,
    "name": "Subway",
    "address": "501 Gainsborough Walk, Boston, MA 02115",
    "phone": "1-800-888-4848"
  }
]
```

## Query 2: Active restaurants with review score = 4

```json
[
  {
    "restaurant_id": 200001,
    "name": "McDonald's",
    "phone": "1-800-244-6227",
    "address": "114 Fenway Terrace, Boston, MA 02115"
  }
]
```

## Query 3: Top 10 favorited restaurants

```json
[
  { "_id": 200001, "total_favorites": 2 },
  { "_id": 200003, "total_favorites": 2 },
  { "_id": 200009, "total_favorites": 2 },
  { "_id": 200019, "total_favorites": 2 },
  { "_id": 200011, "total_favorites": 2 },
  { "_id": 200006, "total_favorites": 2 },
  { "_id": 200028, "total_favorites": 1 },
  { "_id": 200021, "total_favorites": 1 },
  { "_id": 200014, "total_favorites": 1 },
  { "_id": 200005, "total_favorites": 1 }
]
```

## Query 4: Top favorited restaurant with review score >= 4

```json
[
  {
    "restaurant_id": 200001,
    "name": "McDonald's",
    "phone": "1-800-244-6227",
    "status": "active",
    "address": "114 Fenway Terrace, Boston, MA 02115",
    "favorite_count": 2
  }
]
```