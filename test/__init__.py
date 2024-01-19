from flask import Flask
import blog
import auth


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
        app.config.from_pyfile("config.py", silent=True)
        # silent = if exists
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")


if __name__ == "__main__":
    app_constructor()
    app.run()
