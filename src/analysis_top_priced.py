"""
Analysis 3: Top 5 Restaurants by Price Level
Also shows their average review score for value-vs-price comparison
"""

import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()


def top_priced_restaurants():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    
    query = """
    SELECT 
        r.restaurant_id,
        r.name,
        r.category,
        r.price_level,
        r.address,
        AVG(rv.overall_score) AS avg_review_score,
        COUNT(rv.review_id) AS review_count
    FROM restaurant r
    LEFT JOIN review rv ON r.restaurant_id = rv.restaurant_id
    WHERE r.status = 'active' AND r.price_level IS NOT NULL
    GROUP BY r.restaurant_id, r.name, r.category, r.price_level, r.address
    ORDER BY r.price_level DESC
    LIMIT 5;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def visualize_top_priced(df):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    df_sorted = df.sort_values('price_level', ascending=True)
    
    # Bars: price level
    bars = ax1.barh(df_sorted['name'], df_sorted['price_level'], 
                    color='#B04A7A', label='Price Level')
    
    for bar, price in zip(bars, df_sorted['price_level']):
        ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{price:.2f}', va='center', fontsize=10)
    
    ax1.set_xlabel('Price Level', fontsize=12, color='#B04A7A')
    ax1.set_title('Top 5 Most Expensive Restaurants (with Review Scores)', 
                  fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', labelcolor='#B04A7A')
    ax1.grid(axis='x', alpha=0.3)
    
    # Second axis: review score as dots
    ax2 = ax1.twiny()
    review_scores = df_sorted['avg_review_score'].fillna(0)
    ax2.scatter(review_scores, range(len(df_sorted)), 
                color='#4A90E2', s=100, zorder=5, label='Avg Review Score')
    ax2.set_xlabel('Average Review Score', fontsize=12, color='#4A90E2')
    ax2.tick_params(axis='x', labelcolor='#4A90E2')
    ax2.set_xlim(0, 5.5)
    
    plt.tight_layout()
    os.makedirs('docs', exist_ok=True)
    plt.savefig('docs/top_priced_restaurants.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    df = top_priced_restaurants()
    print("=" * 70)
    print("Top 5 Most Expensive Restaurants")
    print("=" * 70)
    print(df.to_string(index=False))
    print()
    visualize_top_priced(df)
    
print(os.getcwd())    