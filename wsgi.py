from importlib import util
import os


def _load_create_app():
    # Import app.py dynamically because package name contains a hyphen
    base = os.path.dirname(__file__)
    app_path = os.path.join(base, 'Eyes-of-an-Addict', 'app.py')
    spec = util.spec_from_file_location('local_app', app_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.create_app


create_app = _load_create_app()
app = create_app()
