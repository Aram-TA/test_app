import json
from datetime import datetime
from typing import NewType, Any

from flask import (
    url_for,
    request,
    session,
    Response,
    redirect,
    Blueprint,
    render_template,
)

from auth import login_required
from data_constructor import DataConstructor

bp = Blueprint("blog", __name__)
File = NewType("File", Any)


def posts_deleter(id: str) -> None:
    """
    Deletes post by id from data
    Parameters
    -----------
    id: str

    Returns
    -------
    None

    """
    with open(DataConstructor.posts_path, "r+") as posts_json:
        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        del data[id]

        json.dump(data, posts_json, indent=2)


def post_updater(
    posts_data: dict,
    posts_json: File,
    id: str,
    title: str,
    body: str = ""
) -> None:
    """
    Updates post and saves new updated data

    Parameters
    -----------
    posts_data: dict
    posts_json: File
    id: str
    title: str
    body: str

    Returns
    -------
    None

    """
    posts_json.seek(0)
    posts_json.truncate()

    posts_data[id] = {
        "id": id,
        "title": title,
        "body": body,
        "author": session["username"],
        "author_email": session["current_user"],
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    json.dump(posts_data, posts_json, indent=2)


def post_creator(title: str, body: str = "") -> None:
    """
    Creates post and saves it's data

    Parameters
    -----------
    title: str
    body: str

    Returns
    -------
    None

    """
    with open(
        DataConstructor.current_post_id_path, "r+"
    ) as current_post_id_file:

        id = current_post_id_file.read()

        current_post_id_file.seek(0)
        current_post_id_file.truncate()

        current_post_id_file.write(str(int(id) + 1))

    with open(DataConstructor.posts_path, "r+") as posts_json:
        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["current_user"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(data, posts_json, indent=2)


@bp.route("/")
def index() -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    with open(DataConstructor.posts_path, "r") as posts_file:
        data = json.load(posts_file)
        return render_template(
            "blog/index.html",
            posts=data,
        )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> Response:
    """
    Does validations for post creating process then writes new data by using
    data constructor. Then redirects to index if everything is OK.

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    if request.method == "POST":

        title = request.form["title"]
        body = request.form["body"]

        if not title:
            return render_template(
                "blog/create.html",
                error="Title is required"
            )

        post_creator(title, body)

        return redirect(url_for("index"))

    else:
        return render_template("blog/create.html")


@bp.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update_post(id: str) -> Response:
    """
    Does validations for post updating process then updates data by using
    data constructor. Then redirects to index if everything is OK.

    Parameters
    -----------
    id: str

    Returns
    -------
    Response

    """
    with open(DataConstructor.posts_path, "r+") as posts_json:
        posts_data = json.load(posts_json)

        if request.method == "POST":

            title = request.form["title"]
            body = request.form["body"]

            if not title:
                return render_template(
                    "blog/update.html",
                    post=posts_data[id],
                    error="Title is required"
                )

            post_updater(posts_data, posts_json, id, title, body)

            return redirect(url_for("index"))

        else:
            return render_template("blog/update.html", post=posts_data[id])


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id) -> Response:
    """
    Deletes post by id then applies changes to data by using data constructor

    Parameters
    -----------
    id: str

    Returns
    -------
    Response

    """
    posts_deleter(id)
    return redirect(url_for('index'))
