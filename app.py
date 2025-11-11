from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Task
from forms import RegisterForm, LoginForm, TaskForm
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('tasks_list'))
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('tasks_list'))
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data.lower()).first():
                flash('Email already registered', 'warning')
                return redirect(url_for('register'))
            user = User(email=form.email.data.lower())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created. Please sign in.', 'success')
            return redirect(url_for('login'))
        return render_template('auth_register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('tasks_list'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Welcome back!', 'success')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('tasks_list'))
            flash('Invalid credentials', 'danger')
        return render_template('auth_login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Signed out successfully', 'info')
        return redirect(url_for('index'))

    
    @app.route('/tasks')
    @login_required
    def tasks_list():
        from datetime import date
    q = request.args.get('q')
    show = request.args.get('show', 'all')  # all | open | done | today
    page = request.args.get('page', 1, type=int)
    per_page = 5  # you can tweak

    tasks_query = Task.query.filter_by(user_id=current_user.id)
    if q:
        tasks_query = tasks_query.filter(Task.title.ilike(f"%{q}%"))
    if show == 'open':
        tasks_query = tasks_query.filter_by(is_done=False)
    elif show == 'done':
        tasks_query = tasks_query.filter_by(is_done=True)
    elif show == 'today':
        tasks_query = tasks_query.filter(Task.due_date == date.today())

    tasks_query = tasks_query.order_by(
        Task.is_done.asc(),
        Task.due_date.asc().nulls_last(),
        Task.created_at.desc()
    )

    # NEW: paginate
    tasks = tasks_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('tasks_list.html', tasks=tasks)

    @app.route('/tasks/new', methods=['GET', 'POST'])
    @login_required
    def tasks_new():
        form = TaskForm()
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                due_date=form.due_date.data,
                is_done=form.is_done.data,
                user_id=current_user.id,
            )
            db.session.add(task)
            db.session.commit()
            flash('Task created', 'success')
            return redirect(url_for('tasks_list'))
        return render_template('tasks_form.html', form=form, heading='New Task')

    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    @login_required
    def tasks_edit(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            form.populate_obj(task)
            db.session.commit()
            flash('Task updated', 'success')
            return redirect(url_for('tasks_list'))
        return render_template('tasks_form.html', form=form, heading='Edit Task')

    @app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
    @login_required
    def tasks_toggle(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        task.is_done = not task.is_done
        db.session.commit()
        return redirect(url_for('tasks_list'))

    @app.route('/tasks/<int:task_id>/delete', methods=['GET', 'POST'])
    @login_required
    def tasks_delete(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        if request.method == 'POST':
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted', 'info')
            return redirect(url_for('tasks_list'))
        return render_template('tasks_confirm_delete.html', task=task)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

import csv
from io import StringIO
from flask import Response

@app.route('/tasks/export.csv')
@login_required
def tasks_export_csv():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["id", "title", "description", "priority", "due_date", "is_done", "created_at"])
    for t in tasks:
        writer.writerow([t.id, t.title, t.description or "", t.priority, t.due_date or "", "YES" if t.is_done else "NO", t.created_at])

    output = si.getvalue()
    headers = {
        "Content-Disposition": "attachment; filename=tasks.csv",
        "Content-Type": "text/csv",
    }
    return Response(output, headers=headers)
