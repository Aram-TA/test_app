import re

from werkzeug.security import check_password_hash

from data_constructor import DataConstructor


def validate_phone_number(phone_number: str) -> None | str:
    """
    Validates phone number by using regex

    Parameters
    -----------
    phone_number: str

    Returns
    -------
    str | None

    """
    if re.match(r'^[\d+\- ]{6,20}$', phone_number) is None:
        return """\t\t\tInvalid phone number.
                  Please use right format for phone number."""


def validate_password(
    email: str,
    password: str,
    user_data: dict,
    login_mode: bool = False
) -> None | str:
    """
    Validates password by using hash function

    Parameters
    -----------
    email: str
    password: str
    user_data: dict
    login_mode: bool

    Returns
    -------
    str | None

    """
    if not password:
        return "Password is required."
    if login_mode:
        if not check_password_hash(user_data[email]["password"], password):
            return "Incorrect password"


def validate_email(
    email: str,
    user_data: dict,
    login_mode: bool = False
) -> None | str:
    """
    Validates email by using regex

    Parameters
    -----------
    email: str
    user_data: dict
    login_mode: bool

    Returns
    -------
    str | None

    """
    if not email:
        return "Email is required"

    elif re.match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email
    ) is None:

        return "Invalid email format. Please use correct email format."

    if login_mode:
        if email not in user_data:
            return "User with that email not found."


def validate_login(email: str, password: str) -> None | str:
    """
    Validates login by using some functions above

    Parameters
    -----------
    email: str
    password: str

    Returns
    -------
    str | None

    """
    with open(DataConstructor.users_path, "r") as users_data:
        error = validate_email(
            email,
            users_data,
            True
        )
        if error:
            return error

        error = validate_password(
            email,
            password,
            users_data,
            True
        )
        if error:
            return error


def validate_registration(
    email: str,
    phone_number: str,
    password: str,
    repeated_password: str
) -> None | str:
    """
    Validates registration by using some functions above

    Parameters
    -----------
    email: str
    password: str

    Returns
    -------
    str | None

    """
    with open(DataConstructor.users_path, "r") as users_data:
        error = validate_email(
            email,
            users_data
        )
        if error:
            return error

        error = validate_phone_number(phone_number)
        if error:
            return error

        if password != repeated_password:
            return "Passwords in both fields should be same."

        error = validate_password(
            email,
            password,
            users_data
        )
        if error:
            return error
