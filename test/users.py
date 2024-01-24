import re
import json

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

    def register_new_account(self, request_form: dict) -> None:
        """
        Loads data from database and after inserts new values there

        Parameters
        -----------
        request_form : dict

        """
        with open(self.users_path, "r+") as users_json:
            users_data = json.load(users_json)

            users_json.seek(0)

            users_data[request_form["email"]] = {
                "phone_number": request_form["phone_number"],
                "username": request_form["username"],
                "password": generate_password_hash(request_form["password"]),
            }

            json.dump(users_data, users_json, indent=2)

    def set_account(self, request_form: dict, mode: str):
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
        with open(self.users_path, "r") as users_json:
            user_data = json.load(users_json)

        return getattr(self, f"validate_{mode}")(
            request_form=request_form,
            user_data=user_data
        )

    def validate_phone_number(self, phone_number: str) -> None | str:
        """
        Validates phone number by using regex

        Parameters
        -----------
        phone_number : str

        Returns
        -------
        str | None

        """
        if not re.match(r"^[\d+\- ]{6,20}$", phone_number):
            return """\t\t\tInvalid phone number.
                    Please use right format for phone number."""

    def validate_password(self, password: str) -> None | str:
        """
        Validates password. Function makes sure that password is not empty

        Parameters
        -----------
        password : str

        Returns
        -------
        str | None

        """
        if not password:
            return "Password is required."

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
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                email
        ):
            return "Invalid email format. Please use correct email format."

    def validate_login(self, request_form: dict, user_data: dict) -> tuple:
        """
        Validates user login by using existing password and email.
        Also gives back user data for use to routing function

        Parameters
        ----------
        request_form : dict
        user_data : dict

        Returns
        -------
        tuple

        """
        error = None
        email = request_form["email"]

        if email not in user_data:
            return "User with that email not found.", user_data

        if not check_password_hash(
            user_data[email]["password"],
            request_form["password"]
        ):
            error = "Incorrect password"

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

        if request_form['password'] !=\
                request_form['password_repeat']:
            return "Passwords in both fields should be same."

        for input_type in ("email", "phone_number", "password"):

            if error := getattr(self, f"validate_{input_type}")(
                request_form[input_type]
            ):
                return error
