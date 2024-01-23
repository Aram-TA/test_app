import json
from datetime import datetime

from flask import session
from werkzeug.security import generate_password_hash

import config


def register_new_account(request_form: dict) -> None:
    """
    Loads data from database and after inserts new values there

    Parameters
    -----------
    email: str
    phone_number: str
    username: str
    password: str
    password_repeat: str

    Returns
    -------
    None

    """
    with open(config.users_path, "r+") as users_json:
        data = json.load(users_json)

        users_json.seek(0)

        data[request_form["email"]] = {
            "phone_number": request_form["phone_number"],
            "username": request_form["username"],
            "password": generate_password_hash(request_form["password"]),
        }

        json.dump(data, users_json, indent=2)


class PostController:
    @staticmethod
    def get_posts_data():
        """Opens json posts database then returns it for use

        Returns
        -------
        dict
            dict from loaded json database
        """
        with open(config.posts_path, "r") as posts_file:
            return json.load(posts_file)

    def set_post(
        self,
        action: str,
        id: str | None, title: str | None, body: str | None
    ):
        """Interface that opens necessary files for needed function and does
        file manipulations. It's created because we don't want to open
        a lot of copies of the same file inside different functions.

        Parameters
        ----------
        action : str
            Action of interface, we need it to differ what function to call
        id : str | None
            id of selected post from posts data
        title : str | None
            title of post that user inputted in html form
        body : str | None
            body of post that user inputted in html form
        """
        with open(config.posts_path, "r+") as posts_json:
            posts_data = json.load(posts_json)

            getattr(self, f"{action}_post")(
                posts_data=posts_data,
                posts_json=posts_json,
                id=id,
                title=title,
                body=body
            )

    @staticmethod
    def delete_post(**kwargs) -> None:
        """
        Deletes post by id, from database
        Parameters
        -----------
        id: str
        title: None
        body: None

        Returns
        -------
        None

        """
        kwargs['posts_json'].seek(0)

        del kwargs['posts_data'][id]

        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)

    @staticmethod
    def update_post(**kwargs) -> None:
        """
        Updates post and saves new updated data

        Parameters
        -----------
        id: str
        title: str
        body: str

        Returns
        -------
        None

        """
        kwargs['posts_json'].seek(0)

        kwargs['posts_data'][id] = {
            "id": id,
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)

    @staticmethod
    def create_post(**kwargs) -> None:
        """
        Creates post and saves it's data

        Parameters
        -----------
        id: None
        title: str
        body: str

        Returns
        -------
        None

        """

        kwargs['posts_json'].seek(0)

        id = 1 if not kwargs['posts_data'] else int(max(
            kwargs['posts_data'])) + 1

        kwargs['posts_data'][id] = {
            "id": id,
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)
