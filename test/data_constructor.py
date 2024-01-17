from typing import Any
import json
import os

users_path = "test/data/users.json"
posts_path = "test/data/posts.json"
current_id_path = "test/data/current_id.txt"


def init_data():
    """
    Creates all necessary dirs if they does't exist

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(users_path):
        write_data(users_path, {})
    if not os.path.exists(posts_path):
        write_data(posts_path, {})
    if not os.path.exists(current_id_path):
        with open(current_id_path, "w") as current_id_file:
            current_id_file.write("1")


init_data()


def write_data(path: str, data: Any):
    """
    Writes received data to target path

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=1)


def load_user_data():
    """
    Loads data from json file

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(users_path, "r") as users_file:
        return json.load(users_file)


def get_post_id():
    """
    Gets next post id from file
    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(current_id_path, "r") as current_id_file:
        current_id = current_id_file.read()

    with open(current_id_path, "w") as current_id_file:
        current_id_file.write(str(int(current_id) + 1))

    return current_id


def load_posts_data():
    """
    Loads post data from json file

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(posts_path, "r") as posts_file:
        return json.load(posts_file)
