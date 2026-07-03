# Boston Restaurant Database — End-to-End Data Pipeline

A multi-database project designed to support community-based restaurant 
sharing and dining insights across the Boston area. This project demonstrates 
end-to-end data management: from conceptual modeling through schema design, 
multi-database implementation (MySQL, MongoDB), and Python-based 
application integration.

**Course:** IE 6700 Data Management for Analytics | Northeastern University | Spring 2026

---

## 🎯 Project Overview

**Business Problem:** Boston-area diners lack a unified platform to browse 
restaurants, share reviews, and discover dining options through structured 
and flexible queries.

**Solution:** A three-tier restaurant discovery application featuring:
- **Data Layer**: Multi-database backend (MySQL for structured entities, 
  MongoDB for flexible review/favorite content)
- **Application Layer**: Flask-based Python web service handling routing, 
  business logic, and database integration
- **Presentation Layer**: HTML views rendered via Flask templates for 
  browser-based interaction

**Key Deliverables:**
- Conceptual data model (EER, UML)
- Normalized MySQL schema with DDL and DML implementation
- MongoDB collections demonstrating document-oriented storage and 
  aggregation pipelines (`$lookup`, `$group`, multi-stage queries)
- Flask web application integrating MySQL for real-time restaurant queries

---

## 🏗️ System Architecture

```
                    ┌──────────────────┐
                    │   User Browser   │
                    │   HTTP requests  │
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │      Flask Application       │
              │        Python web layer      │
              │  Routes, templates, logic    │
              └───────┬──────────────┬───────┘
                      │              │
                     SQL          Aggregation
                      │              │
                      ▼              ▼
              ┌───────────┐   ┌───────────┐
              │   MySQL   │   │  MongoDB  │
              │Relational │   │ Document  │
              │Restaurants│   │  Reviews  │
              │  Users    │   │ Favorites │
              └───────────┘   └───────────┘
```

---

## 📁 Repository Structure
```
Boston-Restaurant-Database/
│
├── README.md                   
├── LICENSE                   
├── .gitignore                 
│
├── docs/                       
│   ├── EER_diagram.png
│   ├── UML_diagram.png
│   ├── schema_design.png
│   ├── top_follower_count.png 
│   ├── top_priced_restaurants.png
│   └── top_rated_restaurants.png
│
├── sql/                        
│   ├── 01_CUISINE_DDL.sql   
│   ├── 02_CUISINE_DML.sql      
│   ├── 03_insert_data.sql   
│   └── 04_SQL_queries.sql
│
├── mongodb/                    
│   ├── 01_insert_data.js           
│   ├── 02_queries.js   
│   ├── #_Sample_Query_Results.md
│   └── README.md
│
├── src/                        
│   ├── project_applicatiopn_web.py
│   ├── implementation in python(sql).py
│   ├── analysis_top_followers.py
│   ├── analysis_top_priced.py
│   ├── analysis_top_rated.py 
│   └── Table_description.py           
│
└── notebooks/                   
    └── analysis.ipynb
```

---

## 🛠️ Tech Stack

- **Databases:** MySQL 8.0, MongoDB 6.0, Neo4j 5.x
- **Language:** Python 3.10+
- **Libraries:** mysql-connector-python, pymongo, neo4j (Python driver), pandas
- **Modeling Tools:** MySQL Workbench (EER), Draw.io (UML)

---

## 📊 Data Model

### Conceptual Design (EER)

<img width="1094" height="849" alt="EER diagram" src="https://github.com/user-attachments/assets/0e748f78-90eb-4466-bfc9-16a4b2272356" />

### Conceptual Design (UML)

<img width="1606" height="1169" alt="UML diagram" src="https://github.com/user-attachments/assets/96a81980-d677-4a13-aaf8-9b244f455820" />

### Schema Design

<img width="595" height="834" alt="schema_design" src="https://github.com/user-attachments/assets/656cd070-a9fb-4fae-ab1c-8b60b77d39f6" />

### Key Entities

- **Restaurant**: name, cuisine, location, price_range, rating
- **User**: username, preferences, dietary_restrictions
- **Review**: rating, text, timestamp, tags
- **Reservation**: date, party_size, status

### Relationships

- User → writes → Review → about → Restaurant
- User → follows → User
- User → recommends → Restaurant

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- MongoDB 6.0+

### Installation

```bash
# Clone the repo
git clone https://github.com/Jie-Hsu-D/Boston-Restaurant-Database.git
cd Boston-Restaurant-Database

# Install Python dependencies
pip install -r requirements.txt

# Set up MySQL
mysql -u root -p < sql/01_create_schema.sql
mysql -u root -p < sql/02_insert_data.sql

# Set up MongoDB
mongo < mongodb/setup.js

```

### Configuration

Create a `.env` file (see `.env.example`) with your database credentials:

```
MYSQL_HOST=localhost
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MONGO_URI=mongodb://localhost:27017
```

### Running the Application

```bash
python src/main.py
```

---

## 💡 Sample Queries

### MySQL: Top-rated restaurants by cuisine
```sql
SELECT cuisine, name, AVG(rating) as avg_rating
FROM Restaurant r JOIN Review rv ON r.id = rv.restaurant_id
GROUP BY cuisine, name
ORDER BY avg_rating DESC
LIMIT 10;
```

### MongoDB: Reviews with specific tags
```javascript
db.reviews.find({ tags: { $in: ["vegetarian", "family-friendly"] } })
```

---

## 📈 Key Learnings & Design Decisions

- **Why multi-database?** Relational storage handles structured entities 
  and transactions well, but restaurant reviews (variable-length text with 
  arbitrary tags) fit MongoDB's flexibility, and social recommendations 
  naturally form graph traversal problems where Neo4j excels.

- **Normalization tradeoffs:** MySQL schema uses 3NF for consistency; 
  denormalized views were added for read-heavy analytics queries.

- **Schema-on-read vs schema-on-write:** Reviews are stored schema-on-read 
  in MongoDB to support evolving tag taxonomies without migration overhead.

---

## 🔮 Future Improvements

- [ ] Add REST API layer (FastAPI)
- [ ] Implement full-text search on reviews (Elasticsearch)
- [ ] Build recommendation engine leveraging Neo4j graph
- [ ] Add data pipeline for real-time review ingestion (Kafka)
- [ ] Deploy on AWS (RDS + DocumentDB + Neptune)

---

## 👤 Author

**Jie Xu**
- MS Data Analytics Engineering, Northeastern University
- GitHub: [@Jie-Hsu-D](https://github.com/Jie-Hsu-D)
- LinkedIn: [https://www.linkedin.com/in/jie-xu-dae/]

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details
