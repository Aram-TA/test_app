import re
from werkzeug.security import check_password_hash


def validate_phone_number(phone_number: str):
    if re.match(r'^[\d+\- ]{6,20}$', phone_number) is None:
        return "Invalid phone number. Please use right format for phone number."


def validate_password(
    email: str, password: str, user_data: str, login_mode: bool = False
):
    if not password:
        return "Password is required."
    if login_mode:
        if not check_password_hash(user_data[email]["password"], password):
            return "Incorrect password"


def validate_email(email: str, user_data: dict, login_mode: bool = False):
    if not email:
        return "Email is required"

    elif re.match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email
    ) is None:

        return "Invalid email format. Please use correct email format."

    if login_mode:
        if email not in user_data:
            return "User with that email not found."
