from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "Romchik luchi"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Notes.db"
db = SQLAlchemy(app)
manager = LoginManager(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    login = request.form.get("login")
    password = request.form.get("password")

    if request.method == "POST":
        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                return redirect("/feed")
            else:
                flash("Логин или пароль введены некорректно")
        else:
            flash("Вы не ввели логин или пароль")

    return render_template("index.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    login = request.form.get("login")
    password = request.form.get("password")
    re_password = request.form.get("re_password")

    if request.method == "POST":
        if not (login or password or re_password):
            flash("Пожалуйста, заполните все поля")
        elif password != re_password:
            flash("Пароли не совпадают")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("index"))

    return render_template("registration.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/feed")
@login_required
def feed():
    feed = Note.query.all()
    return render_template("feed.html", feed=feed)


@app.route("/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]

        note = Note(title=title, text=text)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect("/feed")
        except:
            return "При добавлении заметки произошла ошибка"
    else:
        return render_template("create.html")


@app.route("/feed/<int:id>/delete")
@login_required
def delete(id):
    post = Note.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('feed'))
    except:
        return "При удалении заметки произошла ошибка"


@app.route("/feed/<int:id>/edit", methods=["POST", "GET"])
@login_required
def edit(id):
    note = Note.query.get(id)

    if request.method == "POST":
        note.title = request.form["title"]
        note.text = request.form["text"]

        try:
            db.session.commit()
            return redirect("/feed")
        except:
            return "При редактировании заметки произошла ошибка"
    else:
        return render_template("edit.html", note=note)


@app.route("/options")
@login_required
def options():
    return render_template("options.html")


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('index'))

    return response


if __name__ == "__main__":
    app.run(debug=True)