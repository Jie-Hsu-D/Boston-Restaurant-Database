import os
from dotenv import load_dotenv
from flask import Flask, render_template_string, abort, request, url_for
import mysql.connector

load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

THEME = "#cc2025"

BASE_CSS = f"""
:root {{
  --theme: {THEME};
  --black: #000000;
  --white: #ffffff;
  --light-gray: #f2f2f2;
  --dark-gray: #666666;
}}

* {{ box-sizing: border-box; }}

html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; background: var(--light-gray); color: var(--black); font-family: Arial, Helvetica, sans-serif; }}

body {{ overflow: hidden; }}

a {{ color: var(--theme); text-decoration: none; }}

.app {{ width: min(100vw, calc(100vh * 9 / 16)); height: 100vh; margin: 0 auto; background: var(--white); border-left: 1px solid var(--light-gray); border-right: 1px solid var(--light-gray); display: flex; flex-direction: column; }}

.topbar {{ height: 60px; min-height: 60px; background: var(--white); border-bottom: 1px solid var(--light-gray); display: flex; align-items: center; justify-content: center; padding: 0 16px; font-size: 20px; font-weight: 700; text-align: center; font-family: "Segoe Print", "Lucida Handwriting", "Brush Script MT", cursive; }}

.main {{ flex: 1; overflow-y: auto; background: var(--white); padding: 16px; }}

.bottom-nav {{ height: 64px; min-height: 64px; background: var(--white); border-top: 1px solid var(--light-gray); display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 10px 16px; }}

.nav-item {{ display: flex; align-items: center; justify-content: center; border-radius: 16px; background: var(--light-gray); color: var(--dark-gray); font-weight: 700; }}

.nav-item.active {{ background: var(--theme); color: var(--white); }}

.section {{ margin-bottom: 16px; }}

.toolbar {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }}

.toolbar-button {{ min-height: 44px; border: 1px solid var(--theme); border-radius: 16px; background: var(--white); color: var(--theme); display: flex; align-items: center; justify-content: center; font-weight: 700; }}

.toolbar-button.active {{ background: var(--theme); color: var(--white); }}

.card {{ background: var(--white); border: 1px solid var(--light-gray); border-radius: 18px; padding: 14px; margin-bottom: 12px; }}

.card-link {{ cursor: pointer; }}

.title-line {{ font-size: 18px; font-weight: 700; line-height: 1.35; }}

.meta-line {{ margin-top: 6px; color: var(--dark-gray); font-size: 14px; line-height: 1.5; }}

.small-line {{ margin-top: 8px; color: var(--dark-gray); font-size: 13px; line-height: 1.5; }}

.split {{ border-top: 1px solid var(--light-gray); margin: 16px 0; }}

.back-link {{ display: inline-block; margin-bottom: 12px; font-weight: 700; }}

.detail-title {{ font-size: 24px; font-weight: 700; line-height: 1.35; }}

.detail-meta {{ margin-top: 8px; color: var(--dark-gray); font-size: 15px; line-height: 1.6; }}

.block-title {{ font-size: 16px; font-weight: 700; margin-bottom: 12px; }}

.hours-row, .contact-row, .stat-row {{ display: flex; justify-content: space-between; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--light-gray); line-height: 1.5; }}

.hours-row:last-child, .contact-row:last-child, .stat-row:last-child {{ border-bottom: none; }}

.tabs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }}

.tab-pill {{ min-height: 42px; border-radius: 16px; background: var(--light-gray); color: var(--dark-gray); display: flex; align-items: center; justify-content: center; font-weight: 700; }}

.tab-pill.active {{ background: var(--theme); color: var(--white); }}

.photo-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}

.photo-cell {{ min-height: 92px; border-radius: 18px; background: var(--light-gray); display: flex; align-items: center; justify-content: center; font-size: 42px; line-height: 1; }}

.review-top {{ display: flex; align-items: flex-start; gap: 12px; }}

.avatar {{ width: 42px; height: 42px; min-width: 42px; border-radius: 999px; background: var(--dark-gray); }}

.review-body {{ min-width: 0; flex: 1; }}

.review-name {{ font-size: 15px; font-weight: 700; line-height: 1.3; }}

.review-stars {{ margin-top: 4px; color: var(--dark-gray); font-size: 14px; }}

.review-text {{ margin-top: 10px; line-height: 1.55; word-break: break-word; }}

.review-emojis {{ margin-top: 10px; font-size: 30px; line-height: 1.4; }}

.review-footer {{ margin-top: 10px; color: var(--dark-gray); font-size: 13px; line-height: 1.5; }}

.center-box {{ text-align: center; }}

.profile-avatar {{ width: 88px; height: 88px; border-radius: 999px; background: var(--dark-gray); margin: 0 auto 12px; }}

.profile-name {{ font-size: 22px; font-weight: 700; line-height: 1.35; }}

.profile-bio {{ margin-top: 8px; color: var(--dark-gray); font-style: italic; line-height: 1.5; }}

.profile-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 16px; }}

.profile-stat {{ background: var(--light-gray); border-radius: 18px; padding: 12px 10px; text-align: center; }}

.profile-stat-value {{ font-size: 20px; font-weight: 700; }}

.profile-stat-label {{ margin-top: 4px; color: var(--dark-gray); font-size: 13px; }}

.empty-box {{ background: var(--light-gray); border-radius: 18px; padding: 24px 16px; text-align: center; color: var(--dark-gray); line-height: 1.6; }}

.restaurant-link-inline {{ display: inline-block; margin-top: 10px; font-weight: 700; }}

@media (max-width: 520px) {{
  .main {{ padding: 14px; }}
  .detail-title {{ font-size: 22px; }}
  .photo-cell {{ min-height: 82px; font-size: 38px; }}
}}
"""

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# 工具
def normalize_sort_state(value, default="none"):
    value = (value or default).lower()
    if value not in {"asc", "desc", "none"}:
        return default
    return value

def next_sort_state(value):
    return {"none": "asc", "asc": "desc", "desc": "none"}.get(value, "asc")

def sort_symbol(value):
    return {"asc": "▲", "desc": "▼", "none": "-"}.get(value, "-")

def stars(score):
    if score is None:
        return "No score"
    try:
        score = int(score)
    except (TypeError, ValueError):
        return "No score"
    return "⭐" * max(score, 0)

def format_avg(value):
    if value is None:
        return "No ratings"
    try:
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return "No ratings"

def safe_text(value, fallback="N/A"):
    if value is None:
        return fallback
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            value = value.decode("utf-8", errors="ignore")
    value = str(value).strip()
    return value if value else fallback

def wrap_page(page_title, header_title, active_tab, content_template, **context):
    shell = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page_title }}</title>
  <style>""" + BASE_CSS + """</style>
</head>
<body>
  <div class="app">
    <header class="topbar">{{ header_title }}</header>

    <main class="main">
""" + content_template + """
    </main>

    <nav class="bottom-nav">
      <a class="nav-item{% if active_tab == 'restaurants' %} active{% endif %}" href="{{ url_for('home') }}">Restaurants</a>
      <a class="nav-item{% if active_tab == 'trends' %} active{% endif %}" href="{{ url_for('trends') }}">Trends</a>
    </nav>
  </div>
</body>
</html>
"""
    return render_template_string(
        shell,
        page_title=page_title,
        header_title=header_title,
        active_tab=active_tab,
        **context
    )

# 筛选
def build_restaurant_order(price_sort, rating_sort):
    clauses = []
    if price_sort == "asc":
        clauses.append("r.price_level ASC")
    elif price_sort == "desc":
        clauses.append("r.price_level DESC")

    if rating_sort == "asc":
        clauses.append("COALESCE(AVG(rv.overall_score), -1) ASC")
    elif rating_sort == "desc":
        clauses.append("COALESCE(AVG(rv.overall_score), -1) DESC")

    clauses.append("r.restaurant_id ASC")
    return ", ".join(clauses)

# 数据
def fetch_restaurant_list(cursor, price_sort, rating_sort):
    order_sql = build_restaurant_order(price_sort, rating_sort)
    sql = f"""
        SELECT
            r.restaurant_id,
            r.name,
            r.category,
            r.price_level,
            r.status,
            ROUND(AVG(rv.overall_score), 1) AS avg_score,
            COUNT(DISTINCT rv.review_id) AS review_count,
            COUNT(DISTINCT CASE WHEN vv.status = 'verified' THEN vv.user_id END) AS visit_count
        FROM `RESTAURANT` r
        LEFT JOIN `REVIEW` rv ON r.restaurant_id = rv.restaurant_id
        LEFT JOIN `VISITVERIFICATION` vv ON r.restaurant_id = vv.restaurant_id
        GROUP BY
            r.restaurant_id,
            r.name,
            r.category,
            r.price_level,
            r.status
        ORDER BY {order_sql}
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        row["avg_score_text"] = format_avg(row.get("avg_score"))
        row["category_text"] = safe_text(row.get("category"))
        row["price_text"] = safe_text(row.get("price_level"))
    return rows

def fetch_restaurant_detail(cursor, restaurant_id):
    cursor.execute("""
        SELECT
            r.restaurant_id,
            r.name,
            r.category,
            r.price_level,
            r.address,
            r.website_url,
            r.phone,
            r.status,
            ROUND(AVG(rv.overall_score), 1) AS avg_score,
            COUNT(DISTINCT rv.review_id) AS review_count,
            COUNT(DISTINCT CASE WHEN vv.status = 'verified' THEN vv.user_id END) AS visit_count
        FROM `RESTAURANT` r
        LEFT JOIN `REVIEW` rv ON r.restaurant_id = rv.restaurant_id
        LEFT JOIN `VISITVERIFICATION` vv ON r.restaurant_id = vv.restaurant_id
        WHERE r.restaurant_id = %s
        GROUP BY
            r.restaurant_id,
            r.name,
            r.category,
            r.price_level,
            r.address,
            r.website_url,
            r.phone,
            r.status
    """, (restaurant_id,))
    row = cursor.fetchone()
    if row:
        row["avg_score_text"] = format_avg(row.get("avg_score"))
        row["category_text"] = safe_text(row.get("category"))
        row["price_text"] = safe_text(row.get("price_level"))
        row["address_text"] = safe_text(row.get("address"))
        row["website_text"] = safe_text(row.get("website_url"))
        row["phone_text"] = safe_text(row.get("phone"))
        row["status_text"] = safe_text(row.get("status"))
    return row

def fetch_business_hours(cursor, restaurant_id):
    restaurant_id_str = str(restaurant_id).strip()
    restaurant_id_int = int(restaurant_id_str) if restaurant_id_str.isdigit() else -1

    cursor.execute("""
        SELECT
            business_hours_id,
            `weekday` AS weekday,
            start_time,
            end_time
        FROM `BUSINESSHOUR`
        WHERE TRIM(CAST(restaurant_id AS CHAR)) = %s
           OR CAST(restaurant_id AS UNSIGNED) = %s
        ORDER BY
            FIELD(`weekday`, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            business_hours_id
    """, (restaurant_id_str, restaurant_id_int))
    return cursor.fetchall()

def fetch_restaurant_photos(cursor, restaurant_id):
    cursor.execute("""
        SELECT
            p.photo_id,
            CAST(p.emoji_content AS CHAR) AS emoji_content
        FROM `PHOTO` p
        INNER JOIN `REVIEW` rv ON p.review_id = rv.review_id
        WHERE rv.restaurant_id = %s
          AND (p.status = 'approved' OR p.status IS NULL)
        ORDER BY p.created_at DESC, p.photo_id DESC
    """, (restaurant_id,))
    rows = cursor.fetchall()
    for row in rows:
        row["emoji_content"] = safe_text(row.get("emoji_content"), fallback="📷")
    return rows

def fetch_review_cards(cursor, where_sql="", params=()):
    sql = f"""
        SELECT
            rv.review_id,
            rv.user_id,
            u.nickname,
            rv.restaurant_id,
            r.name AS restaurant_name,
            rv.updated_at,
            rv.review_text,
            rv.overall_score,
            COALESCE(GROUP_CONCAT(DISTINCT CAST(p.emoji_content AS CHAR) ORDER BY p.photo_id SEPARATOR ' '), '') AS emoji_text,
            COUNT(DISTINCT fr.user_id) AS like_count
        FROM `REVIEW` rv
        INNER JOIN `USER` u ON rv.user_id = u.user_id
        INNER JOIN `RESTAURANT` r ON rv.restaurant_id = r.restaurant_id
        LEFT JOIN `PHOTO` p ON rv.review_id = p.review_id AND (p.status = 'approved' OR p.status IS NULL)
        LEFT JOIN `FAVORITEREVIEW` fr ON rv.review_id = fr.review_id
        {where_sql}
        GROUP BY
            rv.review_id,
            rv.user_id,
            u.nickname,
            rv.restaurant_id,
            r.name,
            rv.updated_at,
            rv.review_text,
            rv.overall_score
        ORDER BY rv.updated_at DESC, rv.review_id DESC
    """
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    for row in rows:
        row["nickname"] = safe_text(row.get("nickname"))
        row["restaurant_name"] = safe_text(row.get("restaurant_name"))
        row["review_text"] = safe_text(row.get("review_text"), fallback="")
        row["emoji_text"] = safe_text(row.get("emoji_text"), fallback="")
        row["stars"] = stars(row.get("overall_score"))
    return rows

def fetch_user_profile(cursor, user_id):
    cursor.execute("""
        SELECT
            u.user_id,
            u.nickname,
            u.bio,
            u.profile_visibility,
            COALESCE(v.email, n.email) AS email,
            CASE
                WHEN v.user_id IS NOT NULL THEN 'Verified User'
                WHEN n.user_id IS NOT NULL THEN 'Normal User'
                ELSE 'Unknown User'
            END AS user_type,
            (
                SELECT COUNT(*)
                FROM `FOLLOW_USER` f1
                WHERE f1.follower = u.user_id
            ) AS following_count,
            (
                SELECT COUNT(*)
                FROM `FOLLOW_USER` f2
                WHERE f2.followed = u.user_id
            ) AS follower_count,
            (
                SELECT COUNT(*)
                FROM `REVIEW` rv
                WHERE rv.user_id = u.user_id
            ) AS post_count
        FROM `USER` u
        LEFT JOIN `VERIFICATED_USER` v ON u.user_id = v.user_id
        LEFT JOIN `NORMAL_USER` n ON u.user_id = n.user_id
        WHERE u.user_id = %s
    """, (user_id,))
    row = cursor.fetchone()
    if row:
        row["nickname"] = safe_text(row.get("nickname"))
        row["bio_text"] = safe_text(row.get("bio"), fallback="No bio yet.")
        row["visibility_text"] = safe_text(row.get("profile_visibility"))
    return row

def fetch_user_visits(cursor, user_id):
    cursor.execute("""
        SELECT
            vv.restaurant_id,
            r.name AS restaurant_name,
            vv.updated_at,
            vv.submitted_at
        FROM `VISITVERIFICATION` vv
        INNER JOIN `RESTAURANT` r ON vv.restaurant_id = r.restaurant_id
        WHERE vv.user_id = %s
          AND vv.status = 'verified'
        ORDER BY COALESCE(vv.updated_at, vv.submitted_at) DESC, vv.restaurant_id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    for row in rows:
        row["restaurant_name"] = safe_text(row.get("restaurant_name"))
    return rows

@app.template_filter("datetime_text")
def datetime_text(value):
    if value is None:
        return "N/A"
    try:
        return value.strftime("%Y-%m-%d %H:%M")
    except AttributeError:
        return str(value)

@app.template_filter("time_text")
def time_text(value):
    if value is None:
        return "N/A"
    try:
        return value.strftime("%H:%M")
    except AttributeError:
        return str(value)

@app.route("/")
def home():
    raw_price = request.args.get("price")
    raw_rating = request.args.get("rating")

    if raw_price is None and raw_rating is None:
        price_sort = "none"
        rating_sort = "desc"
    else:
        price_sort = normalize_sort_state(raw_price, default="none")
        rating_sort = normalize_sort_state(raw_rating, default="none")

    price_next = next_sort_state(price_sort)
    rating_next = next_sort_state(rating_sort)

    price_url = url_for("home", price=price_next, rating="none")
    rating_url = url_for("home", price="none", rating=rating_next)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    restaurants = fetch_restaurant_list(cursor, price_sort, rating_sort)

    cursor.close()
    conn.close()

    content = """
<div class="section">
  <div class="toolbar">
    <a class="toolbar-button{% if price_sort != 'none' %} active{% endif %}" href="{{ price_url }}">
      Price {{ price_symbol }}
    </a>
    <a class="toolbar-button{% if rating_sort != 'none' %} active{% endif %}" href="{{ rating_url }}">
      Rating {{ rating_symbol }}
    </a>
  </div>
</div>

<div class="section">
  {% for r in restaurants %}
    <div class="card card-link" onclick="window.location='{{ url_for('restaurant_detail', restaurant_id=r.restaurant_id) }}'">
      <div class="title-line">{{ r.name }}</div>
      <div class="meta-line">
        {{ r.avg_score_text }} ({{ r.review_count }}) &bull; {{ r.visit_count }} visits
      </div>
      <div class="meta-line">
        {{ r.category_text }} &bull; ${{ r.price_text }}
      </div>
    </div>
  {% else %}
    <div class="empty-box">No restaurants found.</div>
  {% endfor %}
</div>
"""
    return wrap_page(
        page_title="Boston Dining Database - Restaurants",
        header_title="BOS Restaurants",
        active_tab="restaurants",
        content_template=content,
        restaurants=restaurants,
        price_sort=price_sort,
        rating_sort=rating_sort,
        price_symbol=sort_symbol(price_sort),
        rating_symbol=sort_symbol(rating_sort),
        price_url=price_url,
        rating_url=rating_url
    )

@app.route("/restaurant/<restaurant_id>")
def restaurant_detail(restaurant_id):
    tab = request.args.get("tab", "photos")
    if tab not in {"photos", "reviews"}:
        tab = "photos"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    restaurant = fetch_restaurant_detail(cursor, restaurant_id)
    if not restaurant:
        cursor.close()
        conn.close()
        abort(404)

    hours = fetch_business_hours(cursor, restaurant_id)
    photos = fetch_restaurant_photos(cursor, restaurant_id)
    reviews = fetch_review_cards(cursor, "WHERE rv.restaurant_id = %s", (restaurant_id,))

    cursor.close()
    conn.close()

    content = """
<a class="back-link" href="{{ url_for('home') }}">&#8592; Back</a>

<div class="section card">
  <div class="detail-title">{{ restaurant.name }}</div>
  <div class="detail-meta">
    {{ restaurant.avg_score_text }} ({{ restaurant.review_count }}) &bull; {{ restaurant.visit_count }} visits
  </div>
  <div class="detail-meta">
    {{ restaurant.category_text }} &bull; ${{ restaurant.price_text }}
  </div>

  <div class="split"></div>

  <div class="block-title">Business Hours</div>
  {% if hours %}
    {% for h in hours %}
      <div class="hours-row">
        <div>{{ h.weekday }}</div>
        <div>{{ h.start_time|time_text }} - {{ h.end_time|time_text }}</div>
      </div>
    {% endfor %}
  {% else %}
    <div class="empty-box">No business hours available.</div>
  {% endif %}

  <div class="split"></div>

  <div class="block-title">Contact Information</div>
  <div class="contact-row">
    <div>Address</div>
    <div>{{ restaurant.address_text }}</div>
  </div>
  <div class="contact-row">
    <div>Website</div>
    <div>
      {% if restaurant.website_url %}
        <a href="{{ restaurant.website_url }}" target="_blank" rel="noreferrer">{{ restaurant.website_text }}</a>
      {% else %}
        N/A
      {% endif %}
    </div>
  </div>
  <div class="contact-row">
    <div>Phone</div>
    <div>{{ restaurant.phone_text }}</div>
  </div>
</div>

<div class="section">
  <div class="tabs">
    <a class="tab-pill{% if tab == 'photos' %} active{% endif %}" href="{{ url_for('restaurant_detail', restaurant_id=restaurant.restaurant_id, tab='photos') }}">Photos</a>
    <a class="tab-pill{% if tab == 'reviews' %} active{% endif %}" href="{{ url_for('restaurant_detail', restaurant_id=restaurant.restaurant_id, tab='reviews') }}">Reviews</a>
  </div>

  {% if tab == 'photos' %}
    {% if photos %}
      <div class="photo-grid">
        {% for photo in photos %}
          <div class="photo-cell">{{ photo.emoji_content }}</div>
        {% endfor %}
      </div>
    {% else %}
      <div class="empty-box">No photos yet.</div>
    {% endif %}
  {% else %}
    {% if reviews %}
      {% for review in reviews %}
        <div class="card">
          <div class="review-top">
            <a href="{{ url_for('user_detail', user_id=review.user_id) }}" onclick="event.stopPropagation();">
              <div class="avatar"></div>
            </a>
            <div class="review-body">
              <div class="review-name">
                <a href="{{ url_for('user_detail', user_id=review.user_id) }}">{{ review.nickname }}</a>
              </div>
              <div class="review-stars">{{ review.stars }}</div>

              {% if review.review_text %}
                <div class="review-text">{{ review.review_text }}</div>
              {% endif %}

              {% if review.emoji_text %}
                <div class="review-emojis">{{ review.emoji_text }}</div>
              {% endif %}

              <div class="review-footer">
                {{ review.updated_at|datetime_text }} &bull; &#10084; {{ review.like_count }}
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty-box">No reviews yet.</div>
    {% endif %}
  {% endif %}
</div>
"""
    return wrap_page(
        page_title=f"{restaurant['name']} - Boston Dining Database",
        header_title="Restaurant Details",
        active_tab="restaurants",
        content_template=content,
        restaurant=restaurant,
        hours=hours,
        photos=photos,
        reviews=reviews,
        tab=tab
    )

@app.route("/user/<user_id>")
def user_detail(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    user = fetch_user_profile(cursor, user_id)
    if not user:
        cursor.close()
        conn.close()
        abort(404)

    review_cards = []
    visits = []

    if user["profile_visibility"] == "show_reviews_and_scores":
        review_cards = fetch_review_cards(cursor, "WHERE rv.user_id = %s", (user_id,))
    elif user["profile_visibility"] == "show_scores":
        review_cards = fetch_review_cards(cursor, "WHERE rv.user_id = %s", (user_id,))
    elif user["profile_visibility"] == "show_visits":
        visits = fetch_user_visits(cursor, user_id)

    cursor.close()
    conn.close()

    content = """
<a class="back-link" href="{{ request.referrer or url_for('home') }}">&#8592; Back</a>

<div class="section card center-box">
  <div class="profile-avatar"></div>
  <div class="profile-name">{{ user.nickname }}</div>
  <div class="profile-bio">{{ user.bio_text }}</div>

  <div class="profile-stats">
    <div class="profile-stat">
      <div class="profile-stat-value">{{ user.following_count }}</div>
      <div class="profile-stat-label">Following</div>
    </div>
    <div class="profile-stat">
      <div class="profile-stat-value">{{ user.follower_count }}</div>
      <div class="profile-stat-label">Followers</div>
    </div>
    <div class="profile-stat">
      <div class="profile-stat-value">{{ user.post_count }}</div>
      <div class="profile-stat-label">Posts</div>
    </div>
  </div>
</div>

<div class="section">
  {% if user.profile_visibility == 'hidden' %}
    <div class="empty-box">Private user, details are hidden.</div>
  {% elif user.profile_visibility == 'show_visits' %}
    {% if visits %}
      {% for visit in visits %}
        <div class="card card-link" onclick="window.location='{{ url_for('restaurant_detail', restaurant_id=visit.restaurant_id) }}'">
          <div class="title-line">{{ visit.restaurant_name }}</div>
          <div class="meta-line">{{ (visit.updated_at or visit.submitted_at)|datetime_text }}</div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty-box">No verified visits yet.</div>
    {% endif %}
  {% else %}
    {% if review_cards %}
      {% for review in review_cards %}
        <div class="card card-link" onclick="window.location='{{ url_for('restaurant_detail', restaurant_id=review.restaurant_id) }}'">
          <div class="title-line">{{ review.restaurant_name }}</div>
          <div class="meta-line">{{ review.stars }}</div>

          {% if user.profile_visibility == 'show_reviews_and_scores' and review.review_text %}
            <div class="review-text">{{ review.review_text }}</div>
          {% endif %}

          {% if user.profile_visibility == 'show_reviews_and_scores' and review.emoji_text %}
            <div class="review-emojis">{{ review.emoji_text }}</div>
          {% endif %}

          <div class="review-footer">
            {{ review.updated_at|datetime_text }}
            {% if user.profile_visibility == 'show_reviews_and_scores' %}
              &bull; &#10084; {{ review.like_count }}
            {% endif %}
          </div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty-box">No public posts yet.</div>
    {% endif %}
  {% endif %}
</div>
"""
    return wrap_page(
        page_title=f"{user['nickname']} - Boston Dining Database",
        header_title="User Profile",
        active_tab="",
        content_template=content,
        user=user,
        review_cards=review_cards,
        visits=visits,
        request=request
    )

@app.route("/trends")
def trends():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    trend_reviews = fetch_review_cards(cursor)

    cursor.close()
    conn.close()

    content = """
<div class="section">
  {% if trend_reviews %}
    {% for review in trend_reviews %}
      <div class="card card-link" onclick="window.location='{{ url_for('restaurant_detail', restaurant_id=review.restaurant_id) }}'">
        <div class="review-top">
          <a href="{{ url_for('user_detail', user_id=review.user_id) }}" onclick="event.stopPropagation();">
            <div class="avatar"></div>
          </a>
          <div class="review-body">
            <div class="review-name">
              <a href="{{ url_for('user_detail', user_id=review.user_id) }}" onclick="event.stopPropagation();">{{ review.nickname }}</a>
            </div>
            <div class="review-stars">{{ review.stars }}</div>

            {% if review.review_text %}
              <div class="review-text">{{ review.review_text }}</div>
            {% endif %}

            {% if review.emoji_text %}
              <div class="review-emojis">{{ review.emoji_text }}</div>
            {% endif %}

            <div class="review-footer">
              {{ review.updated_at|datetime_text }} &bull; &#10084; {{ review.like_count }}
            </div>
          </div>
        </div>

        <a class="restaurant-link-inline" href="{{ url_for('restaurant_detail', restaurant_id=review.restaurant_id) }}" onclick="event.stopPropagation();">
          {{ review.restaurant_name }}
        </a>
      </div>
    {% endfor %}
  {% else %}
    <div class="empty-box">No posts yet.</div>
  {% endif %}
</div>
"""
    return wrap_page(
        page_title="Boston Dining Database - Trends",
        header_title="BOS Trends",
        active_tab="trends",
        content_template=content,
        trend_reviews=trend_reviews
    )

@app.errorhandler(404)
def page_not_found(_error):
    content = """
<div class="empty-box">
  The page you requested was not found.
</div>
"""
    return wrap_page(
        page_title="Not Found - Boston Dining Database",
        header_title="Not Found",
        active_tab="",
        content_template=content
    ), 404

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)