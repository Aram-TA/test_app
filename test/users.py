import re
import json

from werkzeug.security import check_password_hash

import config


class Users:
    """
    Validation class for out inputs from html forms, it takes then validates
    inputs from routing functions
    """
    __slots__ = (
        'request_form',
        'user_data',
        'email',
        'phone_number',
        'username',
        'password_repeat',
        'password',
        'login_mode'
    )

    def __init__(self) -> None:
        self.request_form: dict = None
        self.user_data: dict = None
        self.email: str = None
        self.phone_number: str = None
        self.username: str = None
        self.password_repeat: str = None
        self.password: str = None
        self.login_mode: bool = False

    def set_account(self, request_form: dict, login_mode: bool):
        """
        Interface that opens necessary files for needed function and does
        selected validation. It's created because we don't want to open
        a lot of copies of the same file inside different functions

        Parameters
        ----------
        request_form : dict
            dict from html form
        login_mode : bool
            differs registration and login

        Returns
        -------
        str | None

        """
        with open(config.users_path, "r") as users_data:
            self.user_data = json.load(users_data)

        self.request_form = request_form

        if login_mode:
            return self.validate_login()
        else:
            return self.validate_registration()

    def validate_phone_number(self) -> None | str:
        """
        Validates phone number by using regex

        Parameters
        -----------
        user_data: dict

        Returns
        -------
        str | None

        """
        if re.match(r"^[\d+\- ]{6,20}$", self.phone_number) is None:
            return """\t\t\tInvalid phone number.
                    Please use right format for phone number."""

    def validate_password(self) -> None | str:
        """
        Validates password by using hash function

        Parameters
        -----------
        None

        Returns
        -------
        str | None

        """
        if not self.password:
            return "Password is required."

        if self.login_mode:
            if not check_password_hash(
                self.user_data[self.email]["password"], self.password
            ):
                return "Incorrect password"

    def validate_email(self) -> None | str:
        """
        Validates email by using regex

        Parameters
        -----------
        None

        Returns
        -------
        str | None

        """
        if not self.email:
            return "Email is required"

        if (
            not self.login_mode
            and re.match(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email
            )
            is None
        ):
            return "Invalid email format. Please use correct email format."

        if self.login_mode:
            if self.email not in self.user_data:
                return "User with that email not found."

    def validate_login(self) -> tuple:
        """Does user login validation by using another validation functions,
        then if we have error return it inside of tuple with user_data dict

        Returns
        -------
        tuple[str | None, dict]
            tuple that contains error and user data, we need user data
            for session handling
        """
        self.email: str = self.request_form["email"]
        self.password: str = self.request_form["password"]
        self.login_mode: bool = True

        funclist = ("email", "password")

        for func in funclist:
            error = getattr(self, f"validate_{func}")()

            if error:
                return error, self.user_data

        return None, self.user_data

    def validate_password_repeat(self):
        if self.password != self.password_repeat:
            return "Passwords in both fields should be same."

    def validate_registration(self) -> None | str:
        """
        Validates registration by using some functions above
        If we have some errors in validation we will receive error as string

        Parameters
        -----------
        None

        Returns
        -------
        str | None

        """
        self.email: str = self.request_form["email"]
        self.phone_number: str = self.request_form["phone_number"]
        self.username: str = self.request_form["username"]
        self.password_repeat: str = self.request_form["password_repeat"]
        self.password: str = self.request_form["password"]

        funclist = ("email", "phone_number", "password_repeat", "password")
        for func in funclist:
            error = getattr(self, f"validate_{func}")()

            if error:
                return error
