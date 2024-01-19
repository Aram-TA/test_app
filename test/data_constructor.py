import os
import json
from typing import ClassVar


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
            with open(cls.users_path, "w") as users_file:
                json.dump({}, users_file, indent=2)

        if not os.path.exists(cls.posts_path):
            with open(cls.posts_path, "w") as posts_file:
                json.dump({}, posts_file, indent=2)

        if not os.path.exists(cls.current_post_id_path):
            with open(cls.current_post_id_path, "w") as current_post_id_file:
                current_post_id_file.write("1")
