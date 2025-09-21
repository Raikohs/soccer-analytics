import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("postgresql+psycopg2://postgres:raim@localhost:5432/soccer")

csv_path = "C:/Users/Raimbek/Desktop/soccer/"


tables = {
     "match": "Match.csv",
}


for table, filename in tables.items():
    file_path = csv_path + filename
    print(f"Загружаю {filename} в таблицу {table}...")
    df = pd.read_csv(file_path, sep=",")  # CSV с разделителем ","
    df.to_sql(table, engine, if_exists="replace", index=False)  # replace = пересоздать таблицу

print("✅ Все таблицы успешно импортированы в PostgreSQL!")
