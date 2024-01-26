import json
from datetime import datetime

from flask import session

import config


class PostController:
    __slots__ = "posts_path",

    def __init__(self) -> None:
        self.posts_path = config.posts_path

    def get_posts_data(self):
        """
        Opens posts json and returns it's loaded data

        Returns
        -------
        dict

        """
        with open(self.posts_path, "r") as posts_file:
            return json.load(posts_file)

    def set_post(
        self,
        action: str,
        post_id: str | None,
        title: str | None,
        body: str | None
    ):
        """
        Interface that opens necessary files for needed function and does
        file manipulations. It's created because we don't want to open
        a lot of copies of the same file inside different functions.

        Parameters
        ----------
        action : str
        post_id : str | None
        title : str | None
        body : str | None

        """
        with open(self.posts_path, "r+") as posts_json:
            posts_data = json.load(posts_json)

            getattr(self, f"{action}_post")(
                posts_data=posts_data,
                posts_json=posts_json,
                post_id=post_id,
                title=title,
                body=body
            )

    def delete_post(self, **kwargs) -> None:
        """
        Deletes post by id from database
        """
        posts_json = kwargs['posts_json']
        posts_data = kwargs['posts_data']

        posts_json.seek(0)
        posts_json.truncate()

        del posts_data[kwargs['post_id']]

        json.dump(posts_data, posts_json, indent=2)

    def update_post(self, **kwargs) -> None:
        """
        Updates posts_data dict then saves new data
        """
        posts_json = kwargs['posts_json']
        posts_data = kwargs["posts_data"]

        posts_json.seek(0)

        posts_data[kwargs['post_id']].update({
            "title": kwargs['title'],
            "body": kwargs['body'],
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        json.dump(posts_data, posts_json, indent=2)

    def create_post(self, **kwargs) -> None:
        """
        Creates new key value pair where value have all necessary data
        about post then saves it to database
        """
        posts_json = kwargs['posts_json']
        posts_data = kwargs["posts_data"]
        post_id = kwargs['post_id']

        posts_json.seek(0)

        post_id = 1 if not posts_data else int(max(
            posts_data)) + 1

        posts_data[post_id] = {
            "post_id": post_id,  # Can't handle delete without this guy
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        json.dump(posts_data, posts_json, indent=2)
