from functools import wraps

from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    session,
    url_for,
)

from werkzeug.security import generate_password_hash

from data_constructor import DataConstructor

from validator import (
    validate_registration,
    validate_login
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


def save_registered_account(email, phone_number, username, password):
    data = DataConstructor.load_user_data()
    data[email] = {
        "phone_number": phone_number,
        "username": username,
        "password": generate_password_hash(password),
    }
    DataConstructor.write_data(
        DataConstructor.users_path,
        data
    )


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
    if request.method != "POST":
        return render_template("auth/register.html")
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    username = request.form["username"]
    password = request.form["password"]
    repeated_password = request.form["password_repeat"]

    error = validate_registration(
        email,
        phone_number,
        password,
        repeated_password
    )
    if error:
        return render_template("auth/register.html", error=error)

    save_registered_account(email, phone_number, username, password)
    return redirect(url_for("auth.login"))


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
    if request.method != "POST":
        return render_template("auth/login.html")

    email = request.form["email"]
    password = request.form["password"]

    error = validate_login(email, password)
    if error:
        return render_template("auth/login.html", error=error)

    session.clear()
    session["current_user"] = email
    session["username"] = DataConstructor.load_user_data()[email]["username"]
    return redirect(url_for("index"))


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
    """
    Decorator that checks is user logged in or not,
    if not redirects to login page

    Parameters
    -----------
    function

    Returns
    -------
    function

    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get("current_user") is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
