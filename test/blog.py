from flask import (
    url_for,
    request,
    Response,
    redirect,
    Blueprint,
    render_template,
)

from searcher import Searcher
from auth import login_required
from notes import NotesController

bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> Response:
    """ Redirects to home when client goes to "/" url

    Returns
    -------
    Response

    """
    return redirect(url_for("blog.home"))


@bp.route("/home", methods=("GET",))
def home() -> Response:
    """ Returns rendered home template when client goes to "/" url

    Returns
    -------
    Response

    """
    page: int = request.args.get("page", 1, type=int)

    items_on_page: list
    total_pages: int

    items_on_page, total_pages = NotesController().init_pages(page)

    if page > total_pages or page < 1:
        return redirect(url_for("blog.home", page=1))

    return render_template(
        "blog/home.html",
        items_on_page=items_on_page,
        total_pages=total_pages,
        page=page
    )


@bp.route("/search", methods=("GET",))
def get_search() -> Response:
    """ Renders search page.

    Returns
    -------
    Response

    """
    return render_template("blog/search.html", search_result=None)


@bp.route("/search", methods=("POST",))
def search() -> Response:
    """ Searches necessary data in posts database, renders what it found

    Returns
    -------
    Response

    """
    keyword: str = request.form["search_keyword"]
    search_result = Searcher().search_by_title_or_body(keyword)

    return render_template(
        "blog/search.html",
        search_result=search_result
    )


@bp.route("/read-post/<post_id>", methods=("GET",))
def read_post(post_id: str) -> Response:
    """ Renders special page for current post reading.

    Parameters
    ----------
    post_id : str

    Returns
    -------
    Response

    """
    current_post: dict | None

    if not (current_post := NotesController().validate_post(post_id, True)):
        return redirect(url_for("blog.home"))

    return render_template(
        "blog/read-post.html",
        post=current_post,
    )


@bp.route("/create", methods=("GET",))
@login_required
def get_create_post() -> Response:
    """ Renders post creating html for our server.

    Returns
    -------
    Response

    """
    return render_template("blog/create.html", error=None)


@bp.route("/create", methods=("POST",))
@login_required
def create_post() -> Response:
    """ Does validations for post creating process then writes new data
        by using NotesController. Then redirects to index if everything is OK.

    Returns
    -------
    Response

    """
    title: str | None

    if not (title := request.form["title"]):
        return render_template("blog/create.html", error="Title is required")

    NotesController().create_post(title, request.form["body"])

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
    if not (current_post := NotesController().validate_post(post_id)):
        return redirect(url_for("blog.home"))

    return render_template(
        "blog/update.html",
        post=current_post,
        post_id=post_id,
        error=None
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
    notes_controller = NotesController()

    title: str | None = request.form["title"]
    current_post: dict | None

    if current_post := notes_controller.validate_post(post_id):
        if (
            error := notes_controller.update_post(
                post_id,
                title,
                request.form["body"]
            )
        ):
            return render_template(
                "blog/update.html",
                current_post=current_post,
                post_id=post_id,
                error=error
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
    notes_controller = NotesController()

    if notes_controller.validate_post(post_id):
        notes_controller.delete_post(post_id)

    return redirect(url_for("blog.home"))
