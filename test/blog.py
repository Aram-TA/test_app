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
    return redirect(url_for("blog.home", page_id="1"))


@bp.route("/home/<page_id>")
def home(page_id) -> Response:
    """
    Returns rendered index template when client goes to "/" url

    Returns
    -------
    Response

    """
    pages_data = pages_controller.set_page("get", None, None)

    if page_id not in pages_data:
        return redirect(url_for("index", page_id="1"))

    return render_template(
        "blog/index.html",
        posts=notes_controller.get_posts_data(),
        current_page=pages_data[page_id],
        pages_list=pages_data.keys(),
        page_id=page_id
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

    new_post_id = notes_controller.set_post(
        "create",
        None,
        title,
        request.form["body"]
    )

    page_id = pages_controller.set_page("add", new_post_id, None)

    return redirect(url_for("blog.home", page_id=page_id))


@bp.route("/update/<page_id>/<post_id>", methods=("GET",))
@login_required
def get_update_post(Page_id: str, post_id: str) -> Response:
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


@bp.route("/update/<page_id>/<post_id>", methods=("POST",))
@login_required
def update_post(page_id: str, post_id: str) -> Response:
    """
    Updates post by post_id by using NotesController

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    pages_data = pages_controller.set_page("get", None, None)

    if page_id not in pages_data:
        return redirect(url_for("index", page_id="1"))

    if post_id not in pages_data[page_id] \
            or not notes_controller.set_post("validate", post_id):

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


@bp.route("/delete/<page_id>/<post_id>", methods=("POST",))
@login_required
def delete_post(page_id: str, post_id: str) -> Response:
    """
    Deletes post by post_id

    Parameters
    -----------
    post_id: str

    Returns
    -------
    Response

    """
    pages_data = pages_controller.set_page("get", None, None)

    if page_id not in pages_data:
        return redirect(url_for("index", page_id="1"))

    if post_id not in pages_data[page_id] \
            or not notes_controller.set_post("validate", post_id):

        return redirect(url_for("index"))

    notes_controller.set_post("delete", post_id)

    pages_controller.delete_data("delete", post_id, page_id)

    return redirect(url_for("index"))
