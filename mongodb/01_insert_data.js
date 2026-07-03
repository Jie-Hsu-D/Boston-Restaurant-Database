// ============================================================
// Boston Restaurant Database - MongoDB Setup & Data Insertion
// ============================================================

use boston_restaurant_db;

// ------------------------------------------------------------
// Restaurant Collection
// ------------------------------------------------------------
db.restaurant.insertMany([
  {
    "restaurant_id": 200001,
    "name": "McDonald's",
    "category": "Burgers",
    "rating": 10,
    "address": "114 Fenway Terrace, Boston, MA 02115",
    "website": "https://www.mcdonalds.com/",
    "phone": "1-800-244-6227",
    "status": "active"
  },
  {
    "restaurant_id": 200002,
    "name": "KFC",
    "category": "Fried Chicken",
    "rating": 12,
    "address": "282 Huntington Crossing, Boston, MA 02115",
    "website": "https://www.kfc.com/",
    "phone": "1-800-225-5532",
    "status": "active"
  },
  {
    "restaurant_id": 200003,
    "name": "Burger King",
    "category": "Burgers",
    "rating": 11,
    "address": "39 Opera House Lane, Boston, MA 02116",
    "website": "https://www.bk.com/",
    "phone": "1-866-394-2493",
    "status": "active"
  },
  {
    "restaurant_id": 200004,
    "name": "Wendy's",
    "category": "Burgers",
    "rating": 11,
    "address": "77 Symphony Gate, Boston, MA 02115",
    "website": "https://www.wendys.com/",
    "phone": "1-888-624-8140",
    "status": "active"
  },
  {
    "restaurant_id": 200005,
    "name": "Subway",
    "category": "Sandwiches",
    "rating": 9,
    "address": "501 Gainsborough Walk, Boston, MA 02115",
    "website": "https://www.subway.com/en-US",
    "phone": "1-800-888-4848",
    "status": "active"
  }
]);

// ------------------------------------------------------------
// Review Collection
// ------------------------------------------------------------
db.review.insertMany([
  {
    "review_id": 400001,
    "user_id": 100001,
    "restaurant_id": 200001,
    "created_at": "2026-01-08 18:20:00",
    "updated_at": "2026-01-08 18:20:00",
    "review_text": "Cheap, fast, and somehow always hits the spot.",
    "overall_score": 4
  },
  {
    "review_id": 400002,
    "user_id": 100001,
    "restaurant_id": 200009,
    "created_at": "2026-01-19 12:45:00",
    "updated_at": "2026-01-19 12:45:00",
    "review_text": null,
    "overall_score": 5
  },
  {
    "review_id": 400003,
    "user_id": 100001,
    "restaurant_id": 200016,
    "created_at": "2026-02-03 19:10:00",
    "updated_at": "2026-02-03 19:10:00",
    "review_text": "The wings were solid, but the table was fighting for its life.",
    "overall_score": 4
  },
  {
    "review_id": 400004,
    "user_id": 100001,
    "restaurant_id": 200023,
    "created_at": "2026-02-18 20:05:00",
    "updated_at": "2026-02-18 20:05:00",
    "review_text": null,
    "overall_score": 3
  },
  {
    "review_id": 400005,
    "user_id": 100001,
    "restaurant_id": 200030,
    "created_at": "2026-03-07 21:30:00",
    "updated_at": "2026-03-07 21:30:00",
    "review_text": "I ate here once and immediately made three bad decisions.",
    "overall_score": 4
  },
  {
    "review_id": 400006,
    "user_id": 100002,
    "restaurant_id": 200012,
    "created_at": "2026-01-11 13:10:00",
    "updated_at": "2026-01-11 13:10:00",
    "review_text": null,
    "overall_score": 5
  },
  {
    "review_id": 400007,
    "user_id": 100002,
    "restaurant_id": 200006,
    "created_at": "2026-01-27 17:40:00",
    "updated_at": "2026-01-27 17:40:00",
    "review_text": "Nothing fancy, but the pizza disappeared in five minutes.",
    "overall_score": 4
  },
  {
    "review_id": 400008,
    "user_id": 100002,
    "restaurant_id": 200018,
    "created_at": "2026-02-09 08:15:00",
    "updated_at": "2026-02-09 08:15:00",
    "review_text": null,
    "overall_score": 3
  },
  {
    "review_id": 400009,
    "user_id": 100002,
    "restaurant_id": 200025,
    "created_at": "2026-02-22 19:25:00",
    "updated_at": "2026-02-22 19:25:00",
    "review_text": "My fries tasted like they had seen things.",
    "overall_score": 2
  },
  {
    "review_id": 400010,
    "user_id": 100002,
    "restaurant_id": 200011,
    "created_at": "2026-03-03 18:50:00",
    "updated_at": "2026-03-03 18:50:00",
    "review_text": null,
    "overall_score": 5
  }
]);

// ------------------------------------------------------------
// FavoriteRestaurant Collection
// ------------------------------------------------------------
db.favoriterestaurant.insertMany([
  { "user_id": 100001, "restaurant_id": 200001 },
  { "user_id": 100001, "restaurant_id": 200009 },
  { "user_id": 100001, "restaurant_id": 200016 },
  { "user_id": 100001, "restaurant_id": 200019 },
  { "user_id": 100002, "restaurant_id": 200006 },
  { "user_id": 100002, "restaurant_id": 200011 },
  { "user_id": 100003, "restaurant_id": 200003 },
  { "user_id": 100003, "restaurant_id": 200017 },
  { "user_id": 100003, "restaurant_id": 200021 },
  { "user_id": 100003, "restaurant_id": 200028 },
  { "user_id": 100004, "restaurant_id": 200002 },
  { "user_id": 100004, "restaurant_id": 200014 },
  { "user_id": 100004, "restaurant_id": 200019 },
  { "user_id": 100005, "restaurant_id": 200005 },
  { "user_id": 100005, "restaurant_id": 200010 },
  { "user_id": 100005, "restaurant_id": 200022 },
  { "user_id": 100005, "restaurant_id": 200029 },
  { "user_id": 100006, "restaurant_id": 200001 },
  { "user_id": 100006, "restaurant_id": 200015 },
  { "user_id": 100007, "restaurant_id": 200006 },
  { "user_id": 100007, "restaurant_id": 200009 },
  { "user_id": 100007, "restaurant_id": 200018 },
  { "user_id": 100007, "restaurant_id": 200023 },
  { "user_id": 100008, "restaurant_id": 200003 },
  { "user_id": 100008, "restaurant_id": 200008 },
  { "user_id": 100008, "restaurant_id": 200011 },
  { "user_id": 100008, "restaurant_id": 200014 },
  { "user_id": 100008, "restaurant_id": 200030 },
  { "user_id": 100009, "restaurant_id": 200002 },
  { "user_id": 100009, "restaurant_id": 200017 },
  { "user_id": 100009, "restaurant_id": 200021 }
]);

// ------------------------------------------------------------
// Create indexes for query performance
// ------------------------------------------------------------
db.restaurant.createIndex({ restaurant_id: 1 });
db.restaurant.createIndex({ status: 1 });
db.review.createIndex({ restaurant_id: 1 });
db.review.createIndex({ overall_score: 1 });
db.favoriterestaurant.createIndex({ restaurant_id: 1 });
db.favoriterestaurant.createIndex({ user_id: 1 });

print("MongoDB setup complete. Collections created and indexed.");