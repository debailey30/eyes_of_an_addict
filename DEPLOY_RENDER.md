# Deploying to Render (quick start)

This repo includes a Dockerfile, `Procfile`, and `docker-compose.yml` to help you deploy to Render.

Basic steps:

1. Push this repository to GitHub (if not already).
2. On Render, create a new "Web Service" and point it at this repo.
   - Choose Docker or the default build (our Dockerfile is included).
   - Start command: `gunicorn "Eyes-of-an-Addict.app:create_app()" --workers 3 --bind 0.0.0.0:$PORT`
3. Add the following environment variables in the Render dashboard:
   - `SENDGRID_API_KEY`, `STRIPE_SECRET_KEY`, `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL` (if using worker)
4. Create a managed Postgres service and set `DATABASE_URL` to the connection string.
5. (Recommended) Create a Background Worker on Render and set the start command to `rq worker default`.
6. Deploy and verify `/health` and the index page.

Notes:
- For newsletters, use the example RQ flow in `Eyes-of-an-Addict/tasks.py` to enqueue email sends.
- Configure Stripe webhooks and store the webhook signing secret as an env var.
