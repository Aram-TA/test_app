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
from dataBase import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET",))
def get_register() -> Response:
    """ Renders register template

    Returns
    -------
    Response

    """
    return render_template("auth/register.html", error=None)


@bp.route("/register", methods=("POST",))
def register() -> Response:
    """ Does some validation for registration
        then if it succeed redirects to login

    Returns
    -------
    Response

    """
    users = Users()

    if error := users.validate_registration(request.form):
        return render_template("auth/register.html", error=error)

    users.reg_new_acc(request.form)

    return redirect(url_for("auth.login"))


@bp.route("/login", methods=("GET",))
def get_login() -> Response:
    """ Renders login template

    Returns
    -------
    Response

    """
    return render_template("auth/login.html", error=None)


@bp.route("/login", methods=("POST",))
def login() -> Response:
    """ Does some validation for login then if it succeed redirects
        to index page. Also handles current session of logged in user

    Returns
    -------
    Response

    """
    error: str | None

    error = Users().validate_login(request.form)

    if error:
        return render_template("auth/login.html", error=error)

    cursor = get_db().cursor()

    cursor.execute(
        'SELECT id, username FROM users WHERE email = ?',
        (request.form['email'],)
    )
    session.clear()
    session["current_user"], session["username"] = cursor.fetchone()

    cursor.close()
    return redirect(url_for("blog.home"))


def login_required(view: Callable) -> Callable:
    """ Decorator that checks is user logged in or not
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


@bp.route("/logout")
@login_required
def logout() -> Response:
    """ Clears all data of current flask session and redirects to index page

    Returns
    -------
    Response

    """
    session.clear()
    return redirect(url_for("blog.home"))
