"""
Analysis 1: Top 10 Restaurants by Average Verified Review Score
Only counts reviews from users who verified their visit
"""

import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()


def top_rated_restaurants():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    
    # Query: Restaurants with average review score, restricted to active status
    query = """
    SELECT 
        r.restaurant_id,
        r.name,
        r.category,
        r.price_level,
        AVG(rv.overall_score) AS avg_score,
        COUNT(rv.review_id) AS review_count
    FROM restaurant r
    JOIN review rv ON r.restaurant_id = rv.restaurant_id
    WHERE r.status = 'active'
    GROUP BY r.restaurant_id, r.name, r.category, r.price_level
    HAVING review_count >= 1
    ORDER BY avg_score DESC, review_count DESC
    LIMIT 10;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def visualize_top_rated(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df_sorted = df.sort_values('avg_score', ascending=True)
    
    bars = ax.barh(df_sorted['name'], df_sorted['avg_score'], color='#4A90E2')
    
    for bar, score in zip(bars, df_sorted['avg_score']):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f'{score:.2f}', va='center', fontsize=10)
    
    ax.set_xlabel('Average Review Score', fontsize=12)
    ax.set_title('Top 10 Restaurants by Average Review Score', 
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, 5.5)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    os.makedirs('docs', exist_ok=True)
    plt.savefig('docs/top_rated_restaurants.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    df = top_rated_restaurants()
    print("=" * 70)
    print("Top 10 Restaurants by Average Review Score")
    print("=" * 70)
    print(df.to_string(index=False))
    print()
    visualize_top_rated(df)