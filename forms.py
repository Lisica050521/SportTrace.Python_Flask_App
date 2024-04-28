from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AchievementForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()])
    run_distance = IntegerField('Дистанция пробежки')
    pull_ups = IntegerField('Подтягивания')
    push_ups = IntegerField('Отжимания')
    upper_abs = IntegerField('Упражнения на верхний пресс')
    lower_abs = IntegerField('Упражнения на нижний пресс')
    glute_bridges = IntegerField('Подкачка ягодиц')
    submit = SubmitField('Добавить')
