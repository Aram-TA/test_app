from typing import Any
import json
import os


class DataConstructor:
    def __init__(self) -> None:
        self.users_path = "data/users.json"
        self.posts_path = "data/posts.json"
        self.current_post_id_path = "data/current_post_id.txt"
        self.current_user_id_path = "data/current_user_id.txt"
        self.init_data()

    def init_data(self):
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

        if not os.path.exists(self.users_path):
            self.write_data(self.users_path, {})

        if not os.path.exists(self.posts_path):
            self.write_data(self.posts_path, {})

        if not os.path.exists(self.current_post_id_path):
            with open(self.current_post_id_path, "w") as current_post_id_file:
                current_post_id_file.write("1")

    def write_data(self, path: str, data: Any):
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

    def load_user_data(self):
        """
        Loads data from json file

        Parameters
        -----------
        None

        Returns
        -------
        None

        """
        with open(self.users_path, "r") as users_file:
            return json.load(users_file)

    def get_post_id(self):
        """
        Gets next post id from file
        Parameters
        -----------
        None

        Returns
        -------
        None

        """
        with open(self.current_post_id_path, "r") as current_post_id_file:
            current_post_id = current_post_id_file.read()

        with open(self.current_post_id_path, "w") as current_post_id_file:
            current_post_id_file.write(str(int(current_post_id) + 1))

        return current_post_id

    def load_posts_data(self):
        """
        Loads post data from json file

        Parameters
        -----------
        None

        Returns
        -------
        None

        """
        with open(self.posts_path, "r") as posts_file:
            return json.load(posts_file)
