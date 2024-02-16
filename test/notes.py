from datetime import datetime

from flask import session

from dataBase import get_db


class NotesController:
    """
    Class that validates, creates, deletes, and updates notes/posts
    """
    __slots__ = ()

    def init_pages(self, page: int) -> tuple[list, int]:
        """ Defines pages count, content, current page for application

        Parameters
        ----------
        page : int

        Returns
        -------
        tuple[list, int]

        """
        cursor = get_db().cursor()
        all_posts: list = cursor.execute('SELECT * FROM notes').fetchall()

        posts_count: int = len(all_posts)
        items_per_page: int = 10

        start: int = (page - 1) * items_per_page
        end: int = start + items_per_page

        total_pages: int = (posts_count + items_per_page - 1) // \
            items_per_page if posts_count > 0 else 1

        items_on_page: list = all_posts[start:end]

        cursor.close()
        return items_on_page, total_pages

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
        cursor = get_db().cursor()

        current_post: dict = cursor.execute(
            'SELECT * FROM notes WHERE id = ?',
            (post_id,)
        ).fetchone()

        cursor.close()

        if not current_post:
            return

        if (
            not read_mode and
            current_post["author_id"] != session.get("current_user")
        ):
            return

        return current_post

    def delete_post(self, post_id: str) -> None:
        """ Deletes post by id form database

        Parameters
        ----------
        post_id : str

        """
        db = get_db()
        cursor = db.cursor()

        cursor.execute('DELETE FROM notes WHERE id = ?', (post_id))

        cursor.close()
        db.commit()

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
        if not title:
            return "Title is required."

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            'UPDATE notes SET title = ?, body= ? WHERE id = ?',
            (title, body, post_id)
        )

        cursor.close()
        db.commit()

    def create_post(
        self,
        title: str,
        body: str
    ) -> None:
        """ Creates new post, assigns id to it by using

        Parameters
        ----------
        title : str
        body : str

        """
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            '''INSERT INTO notes (
                title,
                body,
                created,
                author_username,
                author_id
            )
            VALUES (?, ?, ?, ?, ?)''',
            (
                title,
                body,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                session['username'],
                session['current_user']
            )
        )

        cursor.close()
        db.commit()
