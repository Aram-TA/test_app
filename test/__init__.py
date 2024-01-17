from flask import Flask
import blog
import auth


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.secret_key = "dev"

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
        # silent = if exists
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    @app.route("/hello")
    def say_hello():
        return "Hello, World!"

    app.run()


if __name__ == "__main__":
    create_app()
