from functools import wraps
from typing import Callable

from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    session,
    url_for,
    Response,
)

from users import Users

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET",))
def get_register() -> Response:
    """
    Renders register template

    Returns
    -------
    Response

    """
    return render_template("auth/register.html")


@bp.route("/register", methods=("POST",))
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
    users = Users()

    error = users.set_account(request.form, mode="registration")

    if error:
        return render_template("auth/register.html", error=error)

    users.register_new_account(request.form)

    return redirect(url_for("auth.login"))


@bp.route("/login", methods=("GET",))
def get_login() -> Response:
    """
    Renders login template

    Returns
    -------
    Response

    """
    return render_template("auth/login.html")


@bp.route("/login", methods=("POST",))
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
    email = request.form["email"]

    error, users_data = Users().set_account(request.form, mode="login")
    if error:
        return render_template("auth/login.html", error=error)

    session.clear()

    session["current_user"] = email
    session["username"] = users_data[email]["username"]

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


def login_required(view: Callable) -> Callable:
    """
    Decorator that checks is user logged in or not
    if not redirects to login page

    Parameters
    -----------
    view: Callable

    Returns
    -------
    Callable

    """

    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("current_user"):
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
