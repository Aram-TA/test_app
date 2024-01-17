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
from datetime import datetime
import data_constructor

bp = Blueprint("blog", __name__)

user_data = data_constructor.load_user_data()
posts_data = data_constructor.load_posts_data()


def insert_post(id: int, title: str, body: str, author: str):
    posts_data[id] = {
                "id": id,
                "title": title,
                "body": body,
                "author": author,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }


@bp.route("/")
def index():
    return render_template("blog/index.html", posts=posts_data)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        if not title:
            flash("Title is required")
        else:
            insert_post(data_constructor.get_post_id(), title, body, g.user)
            data_constructor.write_data(
                data_constructor.posts_path, posts_data
            )
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update_post(id):
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
                data_constructor.write_data(
                    data_constructor.posts_path, posts_data
                )
                return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=posts_data[id])


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    try:
        del posts_data[id]
        data_constructor.write_data(data_constructor.posts_path, posts_data)
    except KeyError:
        abort(404, f"Post id {id} doesn't exist.")
    return redirect(url_for('blog.index'))
