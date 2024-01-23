import json
from datetime import datetime

from flask import session
from werkzeug.security import generate_password_hash

import config


def get_posts_data():
    """Opens json posts database then returns it for use

    Returns
    -------
    dict
        dict from loaded json database
    """
    with open(config.posts_path, "r") as posts_file:
        return json.load(posts_file)


def save_registered_account(request_form: dict) -> None:
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

        data[request_form["email"]] = {
            "phone_number": request_form["phone_number"],
            "username": request_form["username"],
            "password": generate_password_hash(request_form["password"]),
        }

        users_json.seek(0)
        users_json.truncate()

        json.dump(data, users_json, indent=2)


class PostSetter:
    def __init__(self):
        self.posts_json = None
        self.posts_data: dict = None

    def set_post(
        self,
        action: str,
        id: str | None,
        title: str | None,
        body: str | None
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
        self.posts_json = open(config.posts_path, "r+")
        self.posts_data = json.load(self.posts_json)

        if action == "create":
            self.create_post(id, title, body)
        elif action == "update":
            self.update_post(id, title, body)
        elif action == "delete":
            self.delete_post(id, title, body)

    def delete_post(self, id: str, title: None, body: None) -> None:
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
        self.posts_json.seek(0)
        self.posts_json.truncate()

        del self.posts_data[id]

        json.dump(self.posts_data, self.posts_json, indent=2)
        self.posts_json.close()

    def update_post(
        self,
        id: str,
        title: str,
        body: str = ""
    ) -> None:
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
        self.posts_json.seek(0)
        self.posts_json.truncate()

        self.posts_data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(self.posts_data, self.posts_json, indent=2)
        self.posts_json.close()

    def create_post(self, id: None, title: str, body: str = "") -> None:
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

        self.posts_json.seek(0)
        self.posts_json.truncate()

        id = 1 if not self.posts_data else max(self.posts_data) + 1

        self.posts_data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(self.posts_data, self.posts_json, indent=2)
        self.posts_json.close()
