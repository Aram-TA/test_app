import json
from datetime import datetime
from typing import NewType, Any

from flask import session
from werkzeug.security import generate_password_hash

from config import get_config


config = get_config()
file = NewType("file", Any)


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
    with open(config["users_path"], "r+") as users_json:
        data = json.load(users_json)
        data[request_form["email"]] = {
            "phone_number": request_form["phone_number"],
            "username": request_form["username"],
            "password": generate_password_hash(request_form["password"]),
        }

        users_json.seek(0)
        users_json.truncate()

        json.dump(data, users_json, indent=2)


def do_post_delete(id: str) -> None:
    """
    Deletes post by id from data
    Parameters
    -----------
    id: str

    Returns
    -------
    None

    """
    with open(config["posts_path"], "r+") as posts_json:
        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        del data[id]

        json.dump(data, posts_json, indent=2)


def do_post_update(
    posts_data: dict,
    posts_json: file,
    id: str,
    title: str,
    body: str = ""
) -> None:
    """
    Updates post and saves new updated data

    Parameters
    -----------
    posts_data: dict
    posts_json: File
    id: str
    title: str
    body: str

    Returns
    -------
    None

    """
    posts_json.seek(0)
    posts_json.truncate()

    posts_data[id] = {
        "id": id,
        "title": title,
        "body": body,
        "author": session["username"],
        "author_email": session["current_user"],
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    json.dump(posts_data, posts_json, indent=2)


def create_new_post(title: str, body: str = "") -> None:
    """
    Creates post and saves it's data

    Parameters
    -----------
    title: str
    body: str

    Returns
    -------
    None

    """
    with open(
        config["current_post_id_path"], "r+"
    ) as current_post_id_file:

        id = current_post_id_file.read()

        current_post_id_file.seek(0)
        current_post_id_file.truncate()

        current_post_id_file.write(str(int(id) + 1))

    with open(config["posts_path"], "r+") as posts_json:
        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(data, posts_json, indent=2)
