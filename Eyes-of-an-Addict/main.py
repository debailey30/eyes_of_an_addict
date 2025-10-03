import os
from importlib import util


def _load_local_app():
    """Dynamically load the local app.py module and return create_app.

    This avoids relative import issues when running main.py as a script
    (the package folder name contains a hyphen and isn't importable).
    """
    base = os.path.dirname(__file__)
    app_path = os.path.join(base, 'app.py')
    if not os.path.exists(app_path):
        raise RuntimeError(f"app.py not found at expected path: {app_path}")

    spec = util.spec_from_file_location('local_app', app_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'create_app'):
        raise RuntimeError('create_app not found in app.py')
    return module.create_app


def main():
    create_app = _load_local_app()
    app = create_app()

    # Use environment PORT if provided
    port = int(os.environ.get('PORT', 5000))
    # Enable debug mode only if FLASK_ENV is not 'production'
    debug = os.environ.get('FLASK_ENV', '').lower() != 'production' and os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
