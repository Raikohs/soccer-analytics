# Soccer Analytics

**Soccer Analytics** is a project for analyzing and visualizing player and team statistics based on football data. The project allows you to create charts, metrics, and evaluate player performance.
<img width="806" height="788" alt="image" src="https://github.com/user-attachments/assets/461ab3a8-9755-4936-950e-415bee17d251" />

---

## Features

- Visualization of top players by goals and overall rating
- Comparison of teams and players based on various metrics
- Support for different data sources (SQLite, CSV)
- Interactive dashboards with Superset

---

##  Project Structure
soccer-analytics/
├── soccer/ # Main data
│ ├── players.csv # Player statistics
│ ├── matches.csv # Match statistics
│ └── database.sqlite # SQLite database (not included in repo)
├── superset_config.py # Superset configuration
├── main.py # Main script
├── requirements.txt # Dependencies
└── README.md
```bash
git clone https://github.com/Raikohs/soccer-analytics.git
cd soccer-analytics
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
superset db upgrade
superset init
superset run -p 8088 --with-threads --reload --debugger
Usage

Open Superset in your browser at: http://localhost:8088

Import CSV data or connect to SQLite / PostgreSQL

Create dashboards and charts, for example:

Bar Chart — top players by goals

Line Chart — player rating trends
The project .gitignore is configured to exclude large files and the virtual environment:

*.csv
*.sqlite
*.db
venv/
__pycache__/
*.log

License

MIT License © 2025 Raimbek Serikkali
 Contact

For questions or suggestions, contact
