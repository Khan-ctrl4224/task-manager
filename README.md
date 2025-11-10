# Task Manager (Flask + SQLite)

A simple, resume-ready task tracker with user authentication, priorities, due dates, and filters.

## Stack
- Flask, Flask-Login, Flask-WTF, SQLAlchemy
- SQLite (local), Bootstrap
- Python 3.x

## Features
- Register / Login / Logout
- Create, edit, delete tasks
- Mark done / filter by Open, Done, Due Today
- Search by title

## Quick Start
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python app.py  # http://127.0.0.1:5000
Fix deployment