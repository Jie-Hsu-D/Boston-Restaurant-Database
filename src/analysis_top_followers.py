"""
Analysis 2: Top 5 Users by Follower Count
Uses the follow_user table to identify most-followed community members
"""

import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()


def top_users_by_followers():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    
    query = """
    SELECT 
        u.user_id,
        u.nickname,
        u.bio,
        COUNT(f.follower) AS follower_count,
        CASE 
            WHEN vu.user_id IS NOT NULL THEN 'Verified'
            ELSE 'Normal'
        END AS user_type
    FROM user u
    LEFT JOIN follow_user f ON u.user_id = f.followed
    LEFT JOIN verificated_user vu ON u.user_id = vu.user_id
    GROUP BY u.user_id, u.nickname, u.bio, vu.user_id
    ORDER BY follower_count DESC
    LIMIT 5;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def visualize_top_followers(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df_sorted = df.sort_values('follower_count', ascending=True)
    
    # Different colors for Verified vs Normal
    colors = ['#7F77DD' if t == 'Verified' else '#B4B2A9' 
              for t in df_sorted['user_type']]
    
    bars = ax.barh(df_sorted['nickname'], df_sorted['follower_count'], 
                   color=colors)
    
    for bar, count in zip(bars, df_sorted['follower_count']):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f'{int(count)}', va='center', fontsize=10)
    
    ax.set_xlabel('Follower Count', fontsize=12)
    ax.set_title('Top 5 Users by Follower Count', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#7F77DD', label='Verified User'),
        Patch(facecolor='#B4B2A9', label='Normal User')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    os.makedirs('docs', exist_ok=True)
    plt.savefig('docs/top_follower_count.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    df = top_users_by_followers()
    print("=" * 70)
    print("Top 5 Users by Follower Count")
    print("=" * 70)
    print(df.to_string(index=False))
    print()
    visualize_top_followers(df)