from flask import (
    url_for,
    request,
    Response,
    redirect,
    Blueprint,
    render_template,
)

from auth import login_required
from notes import NotesController

notes_controller = NotesController()
bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Returns
    -------
    Response

    """
    return render_template(
        "blog/index.html",
        posts=notes_controller.get_posts_data(),
    )


@bp.route("/create", methods=("GET",))
@login_required
def get_create_post() -> Response:
    """
    Renders post creating html for our server.

    Returns
    -------
    Response

    """
    return render_template("blog/create.html")


@bp.route("/create", methods=("POST",))
@login_required
def create_post() -> Response:
    """
    Does validations for post creating process then writes new data by using
    NotesController. Then redirects to index if everything is OK.

    Returns
    -------
    Response

    """
    title = request.form["title"]

    if not title:
        return render_template(
            "blog/create.html",
            error="Title is required"
        )

    notes_controller.set_post("create", None, title, request.form["body"])

    return redirect(url_for("index"))


@bp.route("/update/<post_id>", methods=("GET",))
@login_required
def get_update_post(post_id: str) -> Response:
    """
    Renders page for post updating for user, if validation is ok. If not
    redirects to index page

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    current_post = notes_controller.set_post("validate", post_id)

    if not current_post:
        return redirect(url_for("index"))

    return render_template(
        "blog/update.html",
        post=current_post,
        post_id=post_id
    )


@bp.route("/update/<post_id>", methods=("POST",))
@login_required
def update_post(post_id: str) -> Response:
    """
    Updates post by post_id by using NotesController

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    if not notes_controller.set_post("validate", post_id):
        return redirect(url_for("index"))

    title = request.form["title"]

    if not title:
        return render_template(
            "blog/update.html",
            error="Title is required"
        )

    notes_controller.set_post(
        "update",
        post_id,
        title,
        request.form["body"]
    )

    return redirect(url_for("index"))


@bp.route("/delete/<post_id>", methods=("POST",))
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
    if not notes_controller.set_post("validate", post_id):
        return redirect(url_for("index"))

    notes_controller.set_post("delete", post_id)

    return redirect(url_for("index"))
