from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g
)
from werkzeug.security import check_password_hash, generate_password_hash
import data_constructor

bp = Blueprint("auth", __name__, url_prefix="/auth")
user_data = data_constructor.load_user_data()


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif username in user_data:
            error = "Username already exists"

        if error is None:
            user_data[username] = generate_password_hash(password)
            data_constructor.write_data(data_constructor.users_path, user_data)
            return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif username not in user_data:
            error = "Username doesn't exist"
        elif not check_password_hash(user_data[username], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["current_user"] = username
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    current_user = session.get("current_user")

    if current_user is None:
        g.user = None
    else:
        g.user = current_user


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
