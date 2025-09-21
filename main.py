import psycopg2
import pandas as pd
import os


conn = psycopg2.connect(
    dbname="soccer",
    user="postgres",
    password="raim",   
    host="localhost",
    port="5432"
)

queries = {
    "q1": "SELECT * FROM country LIMIT 10;",
    "q2": "SELECT * FROM league WHERE name LIKE '%Premier%' ORDER BY name;",
    "q3": "SELECT season, COUNT(*) AS matches FROM match GROUP BY season ORDER BY season;",
    "q4": "SELECT AVG(home_team_goal + away_team_goal) AS avg_goals FROM match;",
    "q5": "SELECT league_id, AVG(home_team_goal) AS avg_home_goals, AVG(away_team_goal) AS avg_away_goals FROM match GROUP BY league_id;",
    
    "q7": """SELECT m.season, t.team_long_name, AVG(m.home_team_goal + m.away_team_goal) AS avg_goals
             FROM match m
             JOIN team t ON m.home_team_api_id = t.team_api_id
             GROUP BY m.season, t.team_long_name
             ORDER BY avg_goals DESC LIMIT 10;""",
    "q8": "SELECT stage, COUNT(*) AS matches_per_stage FROM match GROUP BY stage ORDER BY stage;",
    "q9": "SELECT COUNT(DISTINCT player_api_id) AS total_players FROM player;",
    "q10": """SELECT pa.overall_rating, COUNT(*) AS cnt
              FROM player_attributes pa
              GROUP BY pa.overall_rating
              ORDER BY pa.overall_rating DESC LIMIT 10;"""
}

# папка для сохранения
os.makedirs("results", exist_ok=True)

for name, query in queries.items():
    df = pd.read_sql(query, conn)
    print(f"\n=== {name} ===")
    print(df.head())
    df.to_csv(f"results/{name}.csv", index=False)

conn.close()
print("\n✅ Все запросы выполнены, результаты сохранены в папку results/")
