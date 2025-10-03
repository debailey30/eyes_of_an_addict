from flask import current_app as app, render_template_string, jsonify, request


@app.route('/')
def index():
    # Minimal index page that references the static assets
    html = """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Eyes of an Addict</title></head>
      <body>
        <h1>Eyes of an Addict</h1>
        <p>Development server is running.</p>
      </body>
    </html>
    """
    return render_template_string(html)


import re

@app.route('/subscription/success')
def subscription_success():
    session_id = request.args.get('session_id')
    # Validate session_id: must be present and alphanumeric (adjust pattern as needed)
    if not session_id or not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
        return jsonify({'status': 'error', 'message': 'Invalid or missing session_id'}), 400
    return jsonify({'status': 'success', 'session_id': session_id})


@app.route('/subscription/cancel')
def subscription_cancel():
    return jsonify({'status': 'canceled'})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})
