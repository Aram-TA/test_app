from flask import (
    url_for,
    request,
    Response,
    redirect,
    Blueprint,
    render_template,
)

from auth import login_required
from notes import PostController

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
        posts=PostController.get_posts_data(),
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create_post() -> Response:
    """
    Does validations for post creating process then writes new data by using
    PostController. Then redirects to index if everything is OK.

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

        PostController().set_post("create", None, title, request.form["body"])

        return redirect(url_for("index"))

    else:
        return render_template("blog/create.html")


@bp.route("/<post_id>/update", methods=("GET", "POST"))
@login_required
def update_post(post_id: str) -> Response:
    """
    Updates post by post_id by using PostController

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    if request.method == "POST":
        PostController().set_post(
            "update",
            post_id,
            request.form["title"],
            request.form["body"]
        )

        return redirect(url_for("index"))

    else:
        return render_template(
            "blog/update.html",
            post=PostController.get_posts_data()[post_id]
        )


@bp.route("/<post_id>/delete", methods=("POST",))
@login_required
def delete_post(post_id: str) -> Response:
    """
    Deletes post by post_id

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    PostController().set_post("delete", post_id, None, None)
    return redirect(url_for("index"))
