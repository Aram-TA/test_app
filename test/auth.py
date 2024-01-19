import json
from functools import wraps
from typing import Callable,  function

from werkzeug.security import generate_password_hash
from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    session,
    url_for,
    Response
)

from data_constructor import DataConstructor
from validator import (
    validate_registration,
    validate_login
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


def save_registered_account(
    email: str,
    phone_number: str,
    username: str,
    password: str,
    repeated_password: str
) -> None:
    """
    Loads data from database and after inserts new values there

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(DataConstructor.users_path, "r+") as users_json:
        data = json.load(users_json)
        data[email] = {
            "phone_number": phone_number,
            "username": username,
            "password": generate_password_hash(password),
        }

        users_json.seek(0)
        users_json.truncate()

        json.dump(DataConstructor.users_path, data)


@bp.route("/register", methods=("GET", "POST"))
def register() -> Response:
    """
    Does some validation for registration then if it succeed redirects to login

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    if request.method != "POST":
        return render_template("auth/register.html")

    error = validate_registration(
        request.form
    )
    if error:
        return render_template("auth/register.html", error=error)

    save_registered_account(request.form)

    return redirect(url_for("auth.login"))


@bp.route("/login", methods=("GET", "POST"))
def login() -> Response:
    """
    Does some validation for login then if it succeed redirects to index page
    Also handles current session of logged in user

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    if request.method != "POST":
        return render_template("auth/login.html")

    email = request.form["email"]
    password = request.form["password"]

    error = validate_login(email, password)
    if error:
        return render_template("auth/login.html", error=error)

    with open(DataConstructor.users_path, "r") as users:
        session.clear()
        session["current_user"] = email
        session["username"] = users[email]["username"]

    return redirect(url_for("index"))


@bp.route("/logout")
def logout() -> Response:
    """
    Clears all data of current flask session and redirects to index page

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    session.clear()
    return redirect(url_for("index"))


def login_required(view: function) -> Callable:
    """
    Decorator that checks is user logged in or not,
    if not redirects to login page

    Parameters
    -----------
    view: function

    Returns
    -------
    Callable

    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get("current_user") is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
