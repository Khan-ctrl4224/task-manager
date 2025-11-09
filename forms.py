from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Create account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description')
    priority = SelectField('Priority', choices=[('LOW','LOW'), ('MEDIUM','MEDIUM'), ('HIGH','HIGH')], default='MEDIUM')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[], default=None)
    is_done = BooleanField('Done')
    submit = SubmitField('Save')
