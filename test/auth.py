from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import data_constructor
from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    session,
    url_for,
    flash,
    g
)

bp = Blueprint("auth", __name__, url_prefix="/auth")
user_data = data_constructor.load_user_data()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Does some validation for registration then if it succeed redirects to login

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
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
    """
    Does some validation for login then if it succeed redirects to index page

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
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
    """
    Defines if current user is logged in or not by using flask's g object

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    current_user = session.get("current_user")

    if current_user is None:
        g.user = None
    else:
        g.user = current_user


@bp.route("/logout")
def logout():
    """
    Clears all data of current flask session and redirects to index page

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
