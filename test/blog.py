import json
from datetime import datetime

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


@bp.route("/")
def index() -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(DataConstructor.posts_path, "r") as posts:
        return render_template(
            "blog/index.html",
            posts=posts,
            session=session
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
    None

    """
    if request.method != "POST":
        return render_template("blog/create.html")

    title = request.form["title"]
    body = request.form["body"]

    if not title:
        return render_template("blog/create.html", error="Title is required")

    with open(
        DataConstructor.current_post_id_path, "r+"
    ) as current_post_id_file:

        current_post_id = current_post_id_file.read()
        current_post_id_file.seek(0)
        current_post_id_file.truncate()
        current_post_id_file.write(str(int(current_post_id) + 1))

    with open(DataConstructor.posts_path, "r+") as posts_json:
        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["email"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(data)
    return redirect(url_for("index"))


@bp.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update_post(id: str) -> Response:
    """
    Does validations for post updating process then updates data by using
    data constructor. Then redirects to index if everything is OK.

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    with open(DataConstructor.posts_path, "r+") as posts_json:
        if request.method != "POST":
            return render_template(
                "blog/update.html",
                post=posts_json[id]
            )

        title = request.form["title"]
        body = request.form["body"]

        if not title:
            return render_template(
                "blog/update.html",
                post=posts_json,
                error="Title is required."
            )

        data = json.load(posts_json)

        posts_json.seek(0)
        posts_json.truncate()

        data[id] = {
            "id": id,
            "title": title,
            "body": body,
            "author": session["username"],
            "author_email": session["email"],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(data)

        return redirect(url_for("index"))


@bp.route('/<id>/delete', methods=('POST', "GET"))
@login_required
def delete(id) -> Response:
    """
    Deletes post by id then applies changes to data by using data constructor
    Aborts operation with 404 http error if post id does't found.

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    try:
        data = DataConstructor.load_posts_data()
        del data[id]
        DataConstructor.write_data(
            DataConstructor.posts_path,
            data
            )
    except KeyError:
        return render_template(
            "blog/update.html",
            post=DataConstructor.load_posts_data()[id],
            error=f"Post id {id} doesn't exist."
        )
    return redirect(url_for('index'))
