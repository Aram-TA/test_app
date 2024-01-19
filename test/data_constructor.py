from typing import ClassVar
from datetime import datetime
import json
import os


class DataConstructor:
    users_path: ClassVar = "data/users.json"
    posts_path: ClassVar = "data/posts.json"
    current_post_id_path: ClassVar = "data/current_post_id.txt"

    @classmethod
    def init_data(cls) -> None:
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

        if not os.path.exists(cls.users_path):
            cls.write_data(cls.users_path, {})

        if not os.path.exists(cls.posts_path):
            cls.write_data(cls.posts_path, {})

        if not os.path.exists(cls.current_post_id_path):
            with open(cls.current_post_id_path, "w") as current_post_id_file:
                current_post_id_file.write("1")

    @classmethod
    def insert_post(
        cls,
        id: int,
        title: str,
        body: str,
        author_email: str
    ) -> None:
        """
        Inserts or changes new key-value pairs to posts database

        Parameters
        -----------
        id: int
        title: str
        body: str
        author_email: str

        Returns
        -------
        None

        """
        data = cls.load_posts_data()
        data[id] = {
            # Without this id I can't get id from decorator for delete function
            "id": id,
            "title": title,
            "body": body,
            "author": cls.load_user_data()[author_email]["username"],
            "author_email": author_email,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        cls.write_data(cls.posts_path, data)

    @staticmethod
    def write_data(path: str, data: dict) -> None:
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

    @classmethod
    def load_user_data(cls) -> dict:
        """
        Loads data from json file

        Parameters
        -----------
        None

        Returns
        -------
        dict

        """
        with open(cls.users_path, "r") as users_file:
            return json.load(users_file)

    @classmethod
    def get_post_id(cls) -> str:
        """
        Gets next post id from file
        Parameters
        -----------
        None

        Returns
        -------
        str

        """
        with open(cls.current_post_id_path, "r+") as current_post_id_file:
            current_post_id = current_post_id_file.read()
            current_post_id_file.seek(0)
            current_post_id_file.write(str(int(current_post_id) + 1))

        return current_post_id

    @classmethod
    def load_posts_data(cls) -> dict:
        """
        Loads post data from json file

        Parameters
        -----------
        None

        Returns
        -------
        dict

        """
        with open(cls.posts_path, "r") as posts_file:
            return json.load(posts_file)


DataConstructor.init_data()
