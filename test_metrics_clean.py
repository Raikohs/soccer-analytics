import psycopg2
import time
import random


conn = psycopg2.connect(
    dbname="soccer",       
    user="postgres",      
    password="0000",       
    host="localhost",     
    port=5432              
)

cur = conn.cursor()

try:
    while True:
        player_name = f"Player_{random.randint(1,1000)}"
        cur.execute(
            "INSERT INTO test_metrics (name) VALUES (%s)",
            (player_name,)
        )
        conn.commit()
        print(f"Inserted: {player_name}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    cur.close()
    conn.close()
