from datetime import datetime

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from werkzeug.exceptions import abort

from auth import login_required
from data_constructor import DataConstructor

data_handler = DataConstructor()
bp = Blueprint("blog", __name__)

user_data = data_handler.load_user_data()
posts_data = data_handler.load_posts_data()


def insert_post(id: int, title: str, body: str, author_email: str):
    """
    Inserts or changes new key-value pair to posts_data global variable

    Parameters
    -----------
    id: int
    title: str
    body: str
    author_email: str

    Returns
    -------
    None

    """
    posts_data[id] = {
        # Without this id I can't get id from decorator for delete function
        "id": id,
        "title": title,
        "body": body,
        "author": user_data[author_email]["username"],
        "author_email": author_email,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@bp.route("/")
def index():
    """
    Returns rendered index template when client goes to "/" url

    Parameters
    -----------
    None

    Returns
    -------
    None

    """
    print("You are in index.")
    return render_template("blog/index.html", posts=posts_data)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
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
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        if not title:
            flash("Title is required")
        else:
            insert_post(data_handler.get_post_id(), title, body, g.user)
            data_handler.write_data(
                data_handler.posts_path, posts_data
            )
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update_post(id):
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
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        if not title:
            flash("Title is required.")
        else:
            if not posts_data.get(id, None):
                abort(404, f"Post id {id} doesn't exist.")
            else:
                insert_post(id, title, body, g.user)
                data_handler.write_data(
                    data_handler.posts_path, posts_data
                )
                return redirect(url_for("index"))

    return render_template("blog/update.html", post=posts_data[id])


@bp.route('/<id>/delete', methods=('POST', "GET"))
@login_required
def delete(id):
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
        del posts_data[id]
        data_handler.write_data(data_handler.posts_path, posts_data)
    except KeyError:
        abort(404, f"Post id {id} doesn't exist.")
    return redirect(url_for('blog.index'))
