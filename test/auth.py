from functools import wraps

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

from werkzeug.security import generate_password_hash

from data_constructor import DataConstructor
import validator

bp = Blueprint("auth", __name__, url_prefix="/auth")
data_handler = DataConstructor()
user_data = data_handler.load_user_data()


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
        print("This works")
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        username = request.form["username"]
        password = request.form["password"]
        repeated_password = request.form["password_repeat"]
        error = None

        error = validator.validate_email(email, user_data)
        if error is not None:
            flash(error)
            return render_template("auth/register.html")
        print("email validated")

        error = validator.validate_phone_number(phone_number)
        if error is not None:
            flash(error)
            return render_template("auth/register.html")
        print("Phone number validated")

        if password != repeated_password:
            flash("Passwords in both fields should be same.")
            return render_template("auth/register.html")
        print("Passwords are same.")

        error = validator.validate_password(email, password, user_data)
        if error is not None:
            flash(error)
            return render_template("auth/register.html")
        print("Password is not empty it passed")

        user_data[email] = {
            "phone_number": phone_number,
            "username": username,
            "password": generate_password_hash(password),
        }
        data_handler.write_data(data_handler.users_path, user_data)
        return redirect(url_for("auth.login"))
    else:
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
        print("We are in login post")
        email = request.form["email"]
        password = request.form["password"]

        error = validator.validate_email(email, user_data, True)
        if error is not None:
            flash(error)
            return render_template("auth/login.html")
        print("Email validated")

        error = validator.validate_password(email, password, user_data, True)
        if error is not None:
            flash(error)
            return render_template("auth/login.html")
        print("Password validated.")

        session.clear()
        session["current_user"] = email
        return redirect(url_for("index"))
    else:
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
        g.username = user_data[current_user]["username"]


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
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
