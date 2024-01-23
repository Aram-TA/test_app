import os
import json
from flask import Flask

import blog
import auth
import config

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists(config.users_path):
    with open(config.users_path, "w") as users_file:
        json.dump({}, users_file, indent=2)

if not os.path.exists(config.posts_path):
    with open(config.posts_path, "w") as posts_file:
        json.dump({}, posts_file, indent=2)

app = Flask(__name__)


def app_constructor(test_config: dict = None):
    """
    Creates flasks application object, configures it then runs it

    Parameters
    -----------
    test_config: dict

    Returns
    -------
    None

    """

    app.secret_key = "dev"

    if test_config is None:
        app.config.from_pyfile("app_config.py", silent=True)
        # silent = if exists
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")


if __name__ == "__main__":
    app_constructor()
    app.run()
