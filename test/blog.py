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
from pages import PageController


notes_controller = NotesController()
pages_controller = PageController()
bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Returns
    -------
    Response

    """
    return redirect(url_for("blog.home"))


@bp.route("/home")
def home() -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Returns
    -------
    Response

    """
    posts = notes_controller.get_posts_data()

    page = request.args.get("page", 1, type=int)
    items_per_page = 10
    start = (page - 1) * items_per_page
    end = start + items_per_page

    total_pages = (len(posts) + items_per_page - 1) // items_per_page
    items_on_page = list(posts.keys())[start:end]

    if page > total_pages or page < 1:
        return redirect(url_for("blog.home", page=total_pages))

    return render_template(
        "blog/index.html",
        posts=posts,
        items_on_page=items_on_page,
        total_pages=total_pages,
        page=page
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

    notes_controller.set_post(
        "create",
        None,
        title,
        request.form["body"]
    )

    return redirect(url_for("blog.home"))


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
    if not notes_controller.set_post("validate", post_id):
        return redirect(url_for("blog.home"))

    return render_template(
        "blog/update.html",
        post=notes_controller.set_post("validate", post_id),
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
        return redirect(url_for("blog.home", page_id="1"))

    title = request.form["title"]

    if not title:
        return render_template(
            "blog/update.html",
            current_post=notes_controller.set_post("validate", post_id),
            post_id=post_id,
            error="Title is required"
        )

    notes_controller.set_post(
        "update",
        post_id,
        title,
        request.form["body"]
    )

    return redirect(url_for("blog.home"))


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
        return redirect(url_for("blog.home", page_id="1"))

    notes_controller.set_post("delete", post_id)

    return redirect(url_for("index"))
