# Task Manager (Flask + SQLite)

A simple task tracker with user auth (register/login), CRUD tasks, search & filters (all/open/done/today), priorities and due dates.

## Tech
- Python, Flask, Flask-Login, Flask-WTF
- SQLAlchemy + SQLite
- Bootstrap 5 (Jinja templates)

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
# visit http://127.0.0.1:5000
