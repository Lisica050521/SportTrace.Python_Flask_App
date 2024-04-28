from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
import os
import base64
from datetime import datetime

# Функция валидатора, проверяющая, что поле не отрицательное
def non_negative(form, field):
    if field.data is not None and field.data < 0:
        raise ValidationError('Это поле не может быть отрицательным.')

# Функция для установки значения по умолчанию, если поле пустое
def default_if_empty(default_value):
    def _default_if_empty(form, field):
        if not field.data:
            field.data = default_value
    return _default_if_empty

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'null'
app.config['SECRET_KEY'] = 'your_secret_key'  # Ключ для поддержания сессий пользователя
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/noch2/PycharmProjects/SportTrace. Python Flask App/instance/database123.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Страница входа

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Форма входа
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Функция для проверки логина и пароля
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('profile'))
        else:
            flash('Вход не выполнен. Пожалуйста, проверьте имя пользователя и пароль', 'danger')
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Модель достижений
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    run_distance = db.Column(db.Integer, nullable=True)
    pull_ups = db.Column(db.Integer, nullable=True)
    push_ups = db.Column(db.Integer, nullable=True)
    upper_abs = db.Column(db.Integer, nullable=True)
    lower_abs = db.Column(db.Integer, nullable=True)
    glute_bridges = db.Column(db.Integer, nullable=True)

# Форма регистрации
class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

# Форма достижений
class AchievementForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()])
    run_distance = IntegerField('Дистанция бега', validators=[default_if_empty(None), non_negative])
    pull_ups = IntegerField('Подтягивания', validators=[default_if_empty(None), non_negative])
    push_ups = IntegerField('Отжимания', validators=[default_if_empty(None), non_negative])
    upper_abs = IntegerField('Верхние пресс', validators=[default_if_empty(None), non_negative])
    lower_abs = IntegerField('Нижние пресс', validators=[default_if_empty(None), non_negative])
    glute_bridges = IntegerField('Мостик', validators=[default_if_empty(None), non_negative])
    submit = SubmitField('Добавить достижение')

    # Переопределяем метод __init__, чтобы убрать стрелки из полей ввода
    def __init__(self, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.run_distance.render_kw = {'type': 'number', 'min': '0'}
        self.pull_ups.render_kw = {'type': 'number', 'min': '0'}
        self.push_ups.render_kw = {'type': 'number', 'min': '0'}
        self.upper_abs.render_kw = {'type': 'number', 'min': '0'}
        self.lower_abs.render_kw = {'type': 'number', 'min': '0'}
        self.glute_bridges.render_kw = {'type': 'number', 'min': '0'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Ваш аккаунт создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = AchievementForm()
    achievements = Achievement.query.filter_by(user_id=current_user.id).order_by(desc(Achievement.date)).all()

    if form.validate_on_submit():
        # Получаем данные из формы
        run_distance = form.run_distance.data if form.run_distance.data is not None else 0
        pull_ups = form.pull_ups.data if form.pull_ups.data is not None else 0
        push_ups = form.push_ups.data if form.push_ups.data is not None else 0
        upper_abs = form.upper_abs.data if form.upper_abs.data is not None else 0
        lower_abs = form.lower_abs.data if form.lower_abs.data is not None else 0
        glute_bridges = form.glute_bridges.data if form.glute_bridges.data is not None else 0

        # Создаем новую запись в базе данных
        new_achievement = Achievement(
            user_id=current_user.id,
            date=form.date.data,
            run_distance=run_distance,
            pull_ups=pull_ups,
            push_ups=push_ups,
            upper_abs=upper_abs,
            lower_abs=lower_abs,
            glute_bridges=glute_bridges
        )
        db.session.add(new_achievement)
        db.session.commit()
        flash('Ваше достижение добавлено!', 'success')
        return redirect(url_for('profile'))

    # Получаем все достижения текущего пользователя, сортируем их по дате
    achievements = Achievement.query.filter_by(user_id=current_user.id).order_by(desc(Achievement.date)).all()

    # Получаем flash-сообщения
    flash_messages = get_flashed_messages(with_categories=True)

    # Формируем данные для графика
    dates = [achievement.date.strftime('%d.%m.%Y') for achievement in achievements]
    run_distances = [achievement.run_distance for achievement in achievements]
    pull_ups = [achievement.pull_ups for achievement in achievements]
    push_ups = [achievement.push_ups for achievement in achievements]
    upper_abs = [achievement.upper_abs for achievement in achievements]
    lower_abs = [achievement.lower_abs for achievement in achievements]
    glute_bridges = [achievement.glute_bridges for achievement in achievements]

    return render_template('profile.html', achievements=achievements, form=form, flash_messages=flash_messages,
                           dates=dates, run_distances=run_distances, pull_ups=pull_ups, push_ups=push_ups,
                           upper_abs=upper_abs, lower_abs=lower_abs, glute_bridges=glute_bridges)


@app.route('/delete_achievement/<int:achievement_id>', methods=['POST'])
def delete_achievement(achievement_id):
    achievement = Achievement.query.get_or_404(achievement_id)
    db.session.delete(achievement)
    db.session.commit()
    flash('Достижение успешно удалено!', 'success')
    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_database', methods=['POST'])
def reset_database():
    db.drop_all()  # Drop all tables
    db.create_all()  # Recreate all tables
    return 'Database reset successfully.'

if __name__ == '__main__':
    with app.app_context():
        if not os.path.isfile('instance/database123.db'):
            print("Файл базы данных не существует")
        db.create_all()  # Создание всех таблиц базы данных
    app.run(debug=True)  # Запуск приложения с включенным режимом отладки