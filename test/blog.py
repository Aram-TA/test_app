from flask import (
    url_for,
    request,
    Response,
    redirect,
    Blueprint,
    render_template,
)

from auth import login_required
from datahandler import PostSetter, get_posts_data

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
    Response

    """
    return render_template(
            "blog/index.html",
            posts=get_posts_data(),
        )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create_post() -> Response:
    """
    Does validations for post creating process then writes new data by using
    PostSetter. Then redirects to index if everything is OK.

    Parameters
    -----------
    None

    Returns
    -------
    Response

    """
    if request.method == "POST":

        title = request.form["title"]

        if not title:
            return render_template(
                "blog/create.html",
                error="Title is required"
            )

        PostSetter().set_post("create", None, title, request.form["body"])

        return redirect(url_for("index"))

    else:
        return render_template("blog/create.html")


@bp.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update_post(id: str) -> Response:
    """
    Does validations for post updating process then updates data by using
    PostSetter. Then redirects to index if everything is OK.

    Parameters
    -----------
    id: str

    Returns
    -------
    Response

    """
    if request.method == "POST":

        PostSetter().set_post(
            "update",
            id,
            request.form["title"],
            request.form["body"]
        )

        return redirect(url_for("index"))

    else:
        return render_template("blog/update.html", post=get_posts_data()[id])


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete_post(id) -> Response:
    """
    Deletes post by id then applies changes to data by using data constructor

    Parameters
    -----------
    id: str

    Returns
    -------
    Response

    """
    PostSetter().set_post("delete", id, None, None)
    return redirect(url_for('index'))
