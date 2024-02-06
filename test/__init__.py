import os
import json

from flask import Flask

import blog
import auth
import config


def init_files():
    """
    Creates all necessary files for file system.
    """
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists(config.users_path):
        with open(config.users_path, "w") as users_file:
            users_file.write("{}")

    if not os.path.exists(config.posts_path):
        with open(config.posts_path, "w") as posts_file:
            posts_file.write("{}")

    if not os.path.exists(config.pages_path):
        with open(config.pages_path, "w") as pages_file:
            json.dump({"1": {}}, pages_file, indent=2)


def app_constructor(test_config: dict = {}) -> None:
    """
    configures flasks application object

    Parameters
    -----------
    test_config: dict

    Returns
    -------
    None

    """
    app = Flask(__name__)
    app.secret_key = "dev"

    if not test_config:
        app.config.from_pyfile("app_config.py", silent=True)
        # silent = if exists
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
    return app


if __name__ == "__main__":
    init_files()
    app = app_constructor()
    app.run(debug=True)
