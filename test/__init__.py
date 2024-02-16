from flask import Flask

import blog
import auth
from dataBase import init_notes_table, init_users_table


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
    app = app_constructor()

    init_users_table(app)
    init_notes_table(app)

    app.run(debug=True)
