from flask import Flask, request, url_for, render_template, redirect

from data import db_session
from data.user import User
from forms.loginform import LoginForm
from forms.login import LoginForm1
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user
from forms.job_form import JobForm
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login_alert', methods=['GET', 'POST'])
def login_alert():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm1()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('auth.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auth.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return 'успех'


@app.route('/')
def start():
    return render_template('base.html', title='РжакаСмеяка.ру')


@app.route('/jokes')
def jokes():
    return render_template('jokes.html', title='Анекдоты')

@app.route('/memes')
def memes():
    return render_template('memes.html', title='Смешные картинки')

@app.route('/video')
def video():
    return render_template('video.html', title='Смешные видео')

@app.route('/other/<arg>')
def other(arg):
    return render_template('other.html', arg=arg)

@app.route('/load_joke', methods=['POST', 'GET'])
def load_joke():
    if request.method == 'GET':
        return render_template('load_joke.html')
    elif request.method == 'POST':
        photo = request.files['file']
        with open('static/img/img.jpg', mode='wb') as f:
            f.write(photo.read())
        return render_template('show_photo.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_1.data:
            return render_template('register.html', form=form, message='Пароли не совпали')
        sess = db_session.create_session()

        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form, message='Такой пользователь есть!')

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        sess.add(user)
        sess.commit()
        return render_template('register.html',
                               form=form, message='Пользователь зарегестрирован!')
    return render_template('register.html', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()