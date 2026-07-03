// ============================================================
// Boston Restaurant Database - MongoDB Queries
// ============================================================

use boston_restaurant_db;

// ------------------------------------------------------------
// Query 1: Retrieve restaurants in zip code 02115
// ------------------------------------------------------------
// Business question: Which restaurants are located in the 02115 area?
// Technique: $regex pattern matching, field projection

print("\n===== Query 1: Restaurants in zip 02115 =====\n");

db.restaurant.find(
  {
    address: { $regex: "02115" }
  },
  {
    restaurant_id: 1,
    name: 1,
    address: 1,
    phone: 1,
    _id: 0
  }
);


// ------------------------------------------------------------
// Query 2: Active restaurants with at least one review scored 4
// ------------------------------------------------------------
// Business question: Which active restaurants have received good reviews?
// Technique: $lookup (join), $match on multiple conditions, $project

print("\n===== Query 2: Active restaurants with review score = 4 =====\n");

db.restaurant.aggregate([
  {
    $lookup: {
      from: "review",
      localField: "restaurant_id",
      foreignField: "restaurant_id",
      as: "reviews"
    }
  },
  {
    $match: {
      status: "active",
      "reviews.overall_score": 4
    }
  },
  {
    $project: {
      restaurant_id: 1,
      name: 1,
      phone: 1,
      address: 1,
      _id: 0
    }
  }
]);


// ------------------------------------------------------------
// Query 3: Top 10 most favorited restaurants
// ------------------------------------------------------------
// Business question: Which restaurants are the most popular by favorites?
// Technique: $group + $sum for counting, $sort + $limit for ranking

print("\n===== Query 3: Top 10 favorited restaurants =====\n");

db.favoriterestaurant.aggregate([
  {
    $group: {
      _id: "$restaurant_id",
      total_favorites: { $sum: 1 }
    }
  },
  {
    $sort: { total_favorites: -1 }
  },
  {
    $limit: 10
  }
]);


// ------------------------------------------------------------
// Query 4: Highest-favorited restaurant with review score >= 4
// ------------------------------------------------------------
// Business question: What is the top restaurant combining review quality and popularity?
// Technique: Multi-stage pipeline with two $lookup joins, $addFields, $sort, $limit

print("\n===== Query 4: Top favorited restaurant with review score >= 4 =====\n");

db.restaurant.aggregate([
  // Step 1: Join review collection
  {
    $lookup: {
      from: "review",
      localField: "restaurant_id",
      foreignField: "restaurant_id",
      as: "reviews"
    }
  },
  // Step 2: Filter restaurants with at least one review score >= 4
  {
    $match: {
      "reviews.overall_score": { $gte: 4 }
    }
  },
  // Step 3: Join favoriterestaurant collection
  {
    $lookup: {
      from: "favoriterestaurant",
      localField: "restaurant_id",
      foreignField: "restaurant_id",
      as: "favorites"
    }
  },
  // Step 4: Compute total favorite count
  {
    $addFields: {
      favorite_count: { $size: "$favorites" }
    }
  },
  // Step 5: Sort by favorite count descending
  {
    $sort: { favorite_count: -1 }
  },
  // Step 6: Take the top result
  {
    $limit: 1
  },
  // Step 7: Project only relevant fields
  {
    $project: {
      _id: 0,
      restaurant_id: 1,
      name: 1,
      phone: 1,
      status: 1,
      address: 1,
      favorite_count: 1
    }
  }
]);