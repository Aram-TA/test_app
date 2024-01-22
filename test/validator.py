import re
import json

from werkzeug.security import check_password_hash

from data_constructor import DataConstructor


class Validator:
    def __init__(self) -> None:
        self.email: str | None = None
        self.phone_number: str | None = None
        self.username: str | None = None
        self.password_repeat: str | None = None
        self.password: str | None = None
        self.login_mode: bool = False
        self.user_data: dict | None = None

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
        if re.match(r'^[\d+\- ]{6,20}$', self.phone_number) is None:
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
                self.user_data[self.email]["password"],
                self.password
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

        if not self.login_mode and re.match(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                self.email
        ) is None:

            return "Invalid email format. Please use correct email format."

        if self.login_mode:
            if self.email not in self.user_data:
                return "User with that email not found."

    def validate_login(self, request_form: dict) -> None | str:
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
        self.email: str = request_form["email"]
        self.password: str = request_form["password"]
        self.login_mode: bool = True

        with open(DataConstructor.users_path, "r") as users_data:
            self.user_data = json.load(users_data)

        funclist = ("email", "password")

        for func in funclist:
            error = getattr(self, f"validate_{func}")()

            if error:
                return error

    def validate_password_repeat(self):
        if self.password != self.password_repeat:
            return "Passwords in both fields should be same."

    def validate_registration(self, request_form: dict) -> None | str:
        """
        Validates registration by using some functions above

        Parameters
        -----------
        email: str
        phone_number: str
        username: str
        password: str
        password_repeat: str

        Returns
        -------
        str | None

        """
        self.email: str = request_form["email"]
        self.phone_number: str = request_form["phone_number"]
        self.username: str = request_form["username"]
        self.password_repeat: str = request_form["password_repeat"]

        with open(DataConstructor.users_path, "r") as users_data:
            self.user_data = json.load(users_data)

        funclist = (
            "email",
            "phone_number",
            "password_repeat",
            "password"
        )
        for func in funclist:
            error = getattr(self, f"validate_{func}")()

            if error:
                return error
