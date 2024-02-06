import json

import config
from notes import NotesController


class PageController:
    __slots__ = "notes_controller",

    def __init__(self) -> None:
        self.notes_controller = NotesController()
        pass

    def __write_data(self, pages_data: dict, pages_file):
        pages_file.seek(0)
        pages_file.truncate()
        json.dump(pages_data, pages_file, indent=2)

    def set_page(
        self,
        command: str,
        new_post_id: str | None,
        page_id: str | None
    ) -> list | None:

        with open(config.pages_path, "r+") as pages_file:
            pages_data = json.load(pages_file)

            return getattr(self, f"{command}_data")(
                pages_file=pages_file,
                pages_data=pages_data,
                new_post_id=new_post_id,
                page_id=page_id
            )

    def get_data(self, **kwargs):
        return kwargs["pages_data"]

    def add_data(self, **kwargs):

        pages_data = kwargs["pages_data"]
        current_free_page = str(
            len(self.notes_controller.get_posts_data()) // 10 + 1)

        if current_free_page not in pages_data:
            pages_data[current_free_page] = {}

        new_post_id = kwargs["new_post_id"]
        pages_data[current_free_page][new_post_id] = new_post_id

        self.__write_data(pages_data, kwargs["pages_file"])

        return current_free_page

    def delete_data(self, **kwargs):
        pages_data = kwargs["pages_data"]
        del pages_data[kwargs["page_id"]][kwargs["post_id"]]
        self.__write_data(pages_data, kwargs["pages_file"])
