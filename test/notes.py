import json
from datetime import datetime

import uuid
from flask import session

import config


class NotesController:
    """
    Class that validates, creates, deletes, and updates notes/posts
    """
    __slots__ = "posts_path",

    def __init__(self) -> None:
        self.posts_path: str = config.posts_path

    def __write_data(self, posts_data: dict) -> None:
        """ Writes data to notes.json file

        Parameters
        ----------
        posts_data : dict

        """
        with open(self.posts_path, "w") as posts_json:
            json.dump(posts_data, posts_json, indent=2)

    def get_posts_data(self) -> dict:
        """ Opens posts json and returns it's loaded data

        Returns
        -------
        dict

        """
        with open(self.posts_path, "r") as posts_file:
            return json.load(posts_file)

    def init_pages(self, page: int) -> tuple[list, int, dict]:
        """ Defines pages count, content, current page for application

        Parameters
        ----------
        page : int

        Returns
        -------
        tuple[list, int, dict]

        """
        posts: dict = self.get_posts_data()

        items_per_page = 10

        start: int = (page - 1) * items_per_page
        end: int = start + items_per_page

        total_pages: int = (len(posts) + items_per_page - 1) // items_per_page\
            if len(posts) > 0 else 1

        items_on_page: list = list(posts.keys())[start:end]

        return items_on_page, total_pages, posts

    def validate_post(
        self,
        post_id: str,
        read_mode: bool = False
    ) -> dict | None:
        """ Validates post id for usage. Returns current post if id is valid

        Parameters
        ----------
        post_id : str
        read_mode : bool

        Returns
        -------
        dict | None

        """
        posts_data: dict = self.get_posts_data()

        if post_id not in posts_data:
            return

        current_post: dict = posts_data[post_id]

        if (
            current_post["author_email"] != session.get("current_user")
            and not read_mode
        ):
            return

        return current_post

    def delete_post(self, post_id: str) -> None:
        """ Deletes post by id form database

        Parameters
        ----------
        post_id : str

        """
        posts_data: dict = self.get_posts_data()

        del posts_data[post_id]

        self.__write_data(posts_data)

    def update_post(
        self,
        post_id: str,
        title: str,
        body: str
    ) -> None:
        """ Updates post by id

        Parameters
        ----------
        post_id : str
        title : str
        body : str

        """
        posts_data: dict = self.get_posts_data()

        posts_data[post_id].update({
            "title": title,
            "body": body,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.__write_data(posts_data)

    def create_post(
        self,
        title: str,
        body: str
    ) -> None:
        """ Creates new post, assigns id to it by using uuid4

        Parameters
        ----------
        title : str
        body : str

        """
        posts_data: dict = self.get_posts_data()
        post_id: str = str(uuid.uuid4())

        posts_data[post_id] = {
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.__write_data(posts_data)
