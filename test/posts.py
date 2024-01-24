import json
from datetime import datetime

from flask import session

import config


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
        post_id: str | None,
        title: str | None,
        body: str | None
    ):
        """Interface that opens necessary files for needed function and does
        file manipulations. It's created because we don't want to open
        a lot of copies of the same file inside different functions.

        Parameters
        ----------
        action : str
        post_id : str | None
        title : str | None
        body : str | None

        """
        with open(config.posts_path, "r+") as posts_json:
            posts_data = json.load(posts_json)

            getattr(self, f"{action}_post")(
                posts_data=posts_data,
                posts_json=posts_json,
                post_id=post_id,
                title=title,
                body=body
            )

    @staticmethod
    def delete_post(**kwargs) -> None:

        kwargs['posts_json'].seek(0)
        kwargs['posts_json'].truncate()

        del kwargs['posts_data'][kwargs['post_id']]

        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)

    @staticmethod
    def update_post(**kwargs) -> None:

        kwargs['posts_json'].seek(0)

        kwargs['posts_data'][kwargs['post_id']] = {
            "post_id": kwargs['post_id'],
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)

    @staticmethod
    def create_post(**kwargs) -> None:

        kwargs['posts_json'].seek(0)

        post_id = 1 if not kwargs['posts_data'] else int(max(
            kwargs['posts_data'])) + 1

        kwargs['posts_data'][post_id] = {
            "post_id": post_id,
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        json.dump(kwargs['posts_data'], kwargs['posts_json'], indent=2)
