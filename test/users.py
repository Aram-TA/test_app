import re
import json
from string import ascii_lowercase, ascii_uppercase, digits

from werkzeug.security import check_password_hash, generate_password_hash

import config


class Users:
    __slots__ = "users_path",
    """
    Class for our inputs from html forms, it takes then validates
    inputs from routing functions
    """
    def __init__(self) -> None:
        self.users_path = config.users_path

    def set_account(self, request_form: dict, mode: str) -> tuple | str | None:
        """
        Interface that opens necessary files for needed function and does
        selected validation. It's created because we don't want to open
        a lot of copies of the same file inside different functions

        Parameters
        ----------
        request_form : dict
        mode : str

        Returns
        -------
        str | None

        """
        with open(self.users_path, "r+") as users_json:
            user_data = json.load(users_json)

            return getattr(self, f"validate_{mode}")(
                request_form=request_form,
                user_data=user_data,
                users_json=users_json
            )

    def validate_reg_new_acc(self, **kwargs) -> None:
        """
        Inserts new account values to database
        """
        users_json = kwargs["users_json"]
        user_data = kwargs["user_data"]
        request_form = kwargs["request_form"]

        users_json.seek(0)

        user_data[request_form["email"]] = {
            "phone_number": request_form["phone_number"],
            "username": request_form["username"],
            "password": generate_password_hash(request_form["password"]),
        }

        json.dump(user_data, users_json, indent=2)

    def validate_login(self, **kwargs) -> tuple:
        """
        Validates user login by using existing password and email.
        Also gives back user data for use to routing function

        Returns
        -------
        tuple

        """
        error = None
        text = "User with that email not found or Incorrect password"

        request_form = kwargs["request_form"]
        user_data = kwargs["user_data"]
        email = request_form["email"]

        if email not in user_data:
            error = text

        elif not check_password_hash(
            user_data[email]["password"],
            request_form["password"]
        ) or email not in user_data:

            error = text

        return error, user_data

    def validate_registration(self, **kwargs) -> None | str:
        """
        Validates registration by using some functions above
        If we have some errors in validation we will receive error as string

        Returns
        -------
        str | None

        """
        request_form = kwargs['request_form']

        if request_form["email"] in kwargs["user_data"]:
            return "That user already exists."

        if request_form['password'] != request_form['password_repeat']:
            return "Passwords in both fields should be same."

        for input_type in ("email", "phone_number", "username", "password"):

            if error := getattr(self, f"validate_{input_type}")(
                request_form[input_type]
            ):
                return error

    def validate_phone_number(self, phone_number: str) -> None | str:
        """
        Validates phone number

        Parameters
        -----------
        phone_number : str

        Returns
        -------
        str | None

        """
        if not phone_number:
            return "Phone number can't be empty."

        cleaned_phone = phone_number.replace(
            "-", "").replace(" ", "").replace("+", "")

        if not cleaned_phone.isdigit():
            return """You used a character that is not allowed for phone number
                Please use arabic digit. From special
                characters only underscore, space, period
                and plus are allowed from special characters.""".strip()

        number_length = len(cleaned_phone)

        if not (6 <= number_length <= number_length <= 36):
            return """Phone number should be longer that 6 characters
                    and less than 37.""".strip()

    def validate_username(self, username: str) -> None | str:
        """
        Validates username

        Parameters
        -----------
        username : str

        Returns
        -------
        str | None

        """
        allowed_characters = set(
            f"_-.{ascii_lowercase}{ascii_uppercase}{digits}"
        )
        usr_length = len(username)

        if usr_length < 2 or usr_length > 36:
            return """Username should have length that is greater than 0 and
            less than 36 characters.""".strip()

        for char in username:
            if char not in allowed_characters:
                return """You used a character that is not allowed for username
                Please use latin letters and only underscore, hyphen,
                period are allowed from special characters.""".strip()

    def validate_password(self, password: str) -> None | str:
        """
        Validates password. Function makes sure that password format is right

        Parameters
        -----------
        password : str

        Returns
        -------
        str | None

        """
        pwd_set = set(password)

        if not password:
            return "Password is required."

        if not pwd_set | set(ascii_lowercase):
            return "Password should contain at least 1 lowercase letters."

        if not pwd_set | set(ascii_uppercase):
            return "Password should contain at least 1 uppercase letters."

        if not pwd_set | set(digits):
            return "Password should contain at least 1 digit."

        if len(password) < 8:
            return "Password min length should be 8 characters."

    def validate_email(self, email: str) -> None | str:
        """
        Validates email by using regex.

        Parameters
        ----------
        email : str

        Returns
        -------
        None | str

        """
        if not re.match(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{1,30}$",
                email
        ):
            return "Invalid email format. Please use correct email format."
