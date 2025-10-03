## Eyes-of-an-Addict — AI assistant guide

This repository is a small Flask-based website for a recovery community. The guidance below is focused and actionable so an AI coding agent can be immediately productive.

High-level architecture (what to know):
- App is a Flask web app split into small modules under `Eyes-of-an-Addict/` (models, forms, services, static assets). Look at `models.py`, `forms.py`, `email_service.py`, and `stripe_service.py` for most business logic.
- Data layer: SQLAlchemy models are defined in `models.py` and expect an `app` module that exposes `db` (imported as `from app import db`). There isn't a `create_app` in this copy; routes and app entry may be in a missing `main.py` / `routes.py` (compiled .pyc present). Prefer to search repo for `app` import when making changes.
- Services:
  - Email: `email_service.py` uses SendGrid (`SENDGRID_API_KEY` env var) and reads attachments from `static/downloads/`.
  - Billing/subscriptions: `stripe_service.py` uses Stripe (`STRIPE_SECRET_KEY` env var) and creates checkout/portal sessions. Domain is chosen from `REPLIT_DEV_DOMAIN` / `REPLIT_DEPLOYMENT` or falls back to `localhost:5000`.

Key environment variables (used in code):
- SENDGRID_API_KEY — required by `email_service.py` to send welcome/newsletter emails.
- STRIPE_SECRET_KEY — required by `stripe_service.py` to interact with Stripe.
- REPLIT_DEPLOYMENT / REPLIT_DEV_DOMAIN — optional; used to construct checkout/redirect URLs. Local fallback is `http://localhost:5000`.

Developer workflows (how to run and debug):
- This repo uses Flask + SQLAlchemy (pyproject.toml / requirements.txt list versions). Typical dev flow:
  - Set required env vars (SENDGRID_API_KEY, STRIPE_SECRET_KEY). For local Stripe testing, set a test key.
  - Run the Flask app (if `main.py` exists locally) or set FLASK_APP to the app entry and run `flask run` on port 5000. If an app entry is missing, search for `if __name__ ==` or `from app import db` usage to locate the entrypoint.
- When editing models, run migrations if you use Alembic (none present). For quick dev, drop/create the DB via the `db` exposed by the app.

Project-specific conventions and patterns:
- `from app import db` is used throughout; changes should preserve the single `db` instance pattern.
- Email personalization uses the `{{greeting}}` token in newsletter HTML — `forms.NewsletterForm` includes a `render_kw` placeholder calling this out.
- Attachments are read from `static/downloads/` in `email_service.py` — prefer using files from that directory when building email templates or tests.
- Stripe domain selection: code checks `REPLIT_DEPLOYMENT` to decide whether to use HTTPS/production domain or `localhost:5000`. When testing locally, set `REPLIT_DEPLOYMENT` to an empty value so `http://localhost:5000` is used.

Examples and quick references (use these in patches):
- Add a new subscriber: `models.EmailSubscriber(email='x@y.com', name='X')` and `db.session.add(...)`, `db.session.commit()`.
- Send a welcome email: call `email_service.send_welcome_email(to_email, subscriber_name)` — this function expects files under `static/downloads/` and `SENDGRID_API_KEY` in env.
- Create a Stripe checkout: call `stripe_service.create_checkout_session(user_email, user_name)`; it returns a redirect URL.

Testing and safety notes:
- The repo currently has no automated tests. When adding tests, prefer small unit tests for service modules (`email_service.py`, `stripe_service.py`, `models.py`). Mock external services (SendGrid, Stripe) with well-known libraries (responses, unittest.mock).
- Avoid committing secrets. The project expects secrets to be provided via environment variables.

Files & directories to inspect when making a change:
- `Eyes-of-an-Addict/models.py` — domain models and helper methods (e.g., `JournalEntry.get_completion_percentage`).
- `Eyes-of-an-Addict/email_service.py` — SendGrid integration and attachment handling.
- `Eyes-of-an-Addict/stripe_service.py` — Stripe session/portal helpers and domain fallback logic.
- `Eyes-of-an-Addict/forms.py` — WTForms usage and validation messages; example: `NewsletterForm` uses `{{greeting}}` token.
- `static/downloads/` — shipping attachments and content used by emails.

If you can't find the Flask entrypoint or routes:
- There are `.pyc` artifacts for `main` and `routes` in `Eyes-of-an-Addict/__pycache__/`. If the `.py` files are missing, ask the maintainer before recreating them. Search for `from app import db` to find usage sites.

When creating patches, be conservative with style and imports:
- Keep `from app import db` pattern. Import services locally inside functions when they may create circular imports (see `email_service.py` importing `models` inside the function).

Questions for maintainers (if unclear when working):
- Where is the Flask app entry (main/routes)? The repo contains `.pyc` files but no `main.py`/`routes.py` sources.
- Are DB migrations (Alembic) used, and if so, where are migration scripts stored?

If this file is out of date or you want additions, tell me which areas you'd like expanded (run/debug commands, tests, CI, or more examples) and I'll update.

How to run locally (quick start)
- Create and activate a virtual environment, install dependencies, set env vars, then run the minimal entrypoint.

Windows PowerShell example (from repo root):

```powershell
# create venv (one-time)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r .\Eyes-of-an-Addict\requirements.txt

# set required env vars (example test keys)
$env:SENDGRID_API_KEY = ''
$env:STRIPE_SECRET_KEY = ''
$env:REPLIT_DEPLOYMENT = ''  # leave empty for local http://localhost:5000 redirects

# run the app
python .\Eyes-of-an-Addict\main.py
```

Notes:
- The repository doesn't include the original `main.py`/`routes.py` sources (compiled `.pyc` exist). I added a minimal, safe entrypoint under `Eyes-of-an-Addict/` so you can run the app locally for development and debugging. If you have the original entrypoint files, prefer them; the created files are intentionally minimal and non-destructive.
- When editing models, use the `db` object imported as `from app import db` (this codebase expects that pattern).
