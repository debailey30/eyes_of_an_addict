from flask import Flask
from flask_sqlalchemy import SQLAlchemy
try:
    from flask_migrate import Migrate
except ImportError:
    class Migrate:
        """Fallback shim when Flask-Migrate is not installed.
        Install the real package with: pip install Flask-Migrate
        """
        def __init__(self, *args, **kwargs):
            # allow module-level instantiation (migrate = Migrate())
            self._present = False

        def init_app(self, app, db):
            raise RuntimeError(
                "flask_migrate is not installed. Install it with: pip install Flask-Migrate"
            )
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, static_folder='static', template_folder='static')

    # Minimal config — adapt as needed
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is not set. Please set it before running the app.")
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register routes lazily to avoid circular imports.
    # This import is required to ensure route registration; do not remove.
    with app.app_context():
        from . import routes  # noqa: F401
    # Register routes lazily to avoid circular imports
    with app.app_context():
        from . import routes  # noqa: F401

    return app
