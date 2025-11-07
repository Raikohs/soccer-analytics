import psycopg2, time, random
conn = psycopg2.connect(
    dbname="soccer",
    user="postgres",
    password="0000",
    host="host.docker.internal"
)
cur = conn.cursor()
while True:
    cur.execute("INSERT INTO test_metrics (name) VALUES (%s)", (f"Player_{random.randint(1,1000)}",))
    conn.commit()
    time.sleep(2)
