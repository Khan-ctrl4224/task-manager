# TaskManager (Flask + SQLite)

A simple, resume-friendly task manager built with **Flask, SQLAlchemy, Flask-Login, and WTForms**.  
Features: user auth (register/login), create/edit/delete tasks, mark done, search & filters (All/Open/Done/Today), priorities, and due dates.

## Tech Stack
- Python 3.11+
- Flask, Flask-Login, Flask-WTF, SQLAlchemy
- SQLite (local dev)
- Bootstrap (minimal UI)

## Quick Start (Local)
```bash
# clone or open folder, then:
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows (macOS/Linux: cp .env.example .env)
python app.py
# open http://127.0.0.1:5000
