from typing import Any, NewType

from flask import (
    url_for,
    request,
    session,
    redirect,
    Blueprint,
    render_template
)


from auth import login_required
from data_constructor import DataConstructor

bp = Blueprint("blog", __name__)
Response = NewType("Response", Any)


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
    return render_template(
        "blog/index.html",
        posts=DataConstructor.load_posts_data(),
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

    DataConstructor.insert_post(
        DataConstructor.get_post_id(),
        title,
        body,
        session["current_user"]
    )
    DataConstructor.write_data(
        DataConstructor.posts_path,
        DataConstructor.load_posts_data()
    )
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
    if request.method != "POST":
        return render_template(
            "blog/update.html",
            post=DataConstructor.load_posts_data()[id]
        )

    title = request.form["title"]
    body = request.form["body"]

    if not title:
        return render_template(
            "blog/update.html",
            post=DataConstructor.load_posts_data()[id],
            error="Title is required."
        )

    DataConstructor.insert_post(id, title, body, session["current_user"])
    DataConstructor.write_data(
        DataConstructor.posts_path,
        DataConstructor.load_posts_data()
    )
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
