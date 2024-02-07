import json
from datetime import datetime

from flask import session, request

import config


class NotesController:
    """
    Class that validates, creates, deletes, and updates notes/posts
    """
    __slots__ = "posts_path",

    def __init__(self) -> None:
        self.posts_path = config.posts_path

    def get_posts_data(self) -> dict:
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
        title: str | None = None,
        body: str | None = None
    ) -> None | bool | dict | str:
        """
        Interface that opens necessary files for needed function and does
        file manipulations. It's created because we don't want to open
        a lot of copies of the same file inside different functions.

        Parameters
        ----------
        action : str | "create" | "update" | "validate" | "delete" |
                     | "define_pages"
        post_id : str | None
        title : str | None
        body : str | None

        Returns
        -------
        None | bool | dict | str

        """
        with open(self.posts_path, "r+") as posts_json:
            posts_data = json.load(posts_json)

            return getattr(self, f"{action}_post")(
                posts_data=posts_data,
                posts_json=posts_json,
                post_id=post_id,
                title=title,
                body=body
            )

    def __write_data(self, posts_data: dict, posts_json):
        posts_json.seek(0)
        posts_json.truncate()
        json.dump(posts_data, posts_json, indent=2)

    def define_pages_post(self, **kwargs):
        posts = kwargs["posts_data"]

        page = request.args.get("page", 1, type=int)
        items_per_page = 10

        start = (page - 1) * items_per_page
        end = start + items_per_page

        if len(posts) > 0:
            total_pages = (len(posts) + items_per_page - 1) // items_per_page
        else:
            total_pages = 1
        items_on_page = list(posts.keys())[start:end]

        return page, items_on_page, total_pages, posts

    def validate_post(self, **kwargs) -> None | dict:
        """
        Validates post id when user want to get, delete or update post

        Returns
        -------
        dict | None
        """
        if kwargs["post_id"] not in kwargs["posts_data"]:
            return

        current_post = kwargs["posts_data"][kwargs["post_id"]]

        if session.get("current_user"):
            if current_post["author_email"] != session["current_user"]:
                return

        return current_post

    def delete_post(self, posts_data: dict, posts_json, **kwargs) -> None:
        """
        Deletes post by id from database
        """

        del posts_data[kwargs['post_id']]

        self.__write_data(posts_data, posts_json)

    def update_post(self, posts_data: dict, posts_json, **kwargs) -> None:
        """
        Updates posts_data dict then saves new data
        """
        posts_data[kwargs['post_id']].update({
            "title": kwargs['title'],
            "body": kwargs['body'],
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.__write_data(posts_data, posts_json)

    def create_post(self, posts_data: dict, posts_json, **kwargs) -> None:
        """
        Creates new key value pair where value have all necessary data
        about post then saves it to database
        """
        if not posts_data:
            post_id = "1"
        else:
            key, post = posts_data.popitem()
            posts_data[key] = post  # I took last key by pop then restored dict
            post_id = str(int(key) + 1)

        posts_data[post_id] = {
            "title": kwargs['title'],
            "body": kwargs['body'],
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.__write_data(posts_data, posts_json)
