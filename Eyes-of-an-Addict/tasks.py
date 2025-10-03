"""Simple background task examples using RQ + Redis.

This file demonstrates how to enqueue sending emails so the web process stays responsive.
"""
import os
from redis import Redis
from rq import Queue


def get_redis():
    url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    return Redis.from_url(url)


def enqueue_welcome_email(to_email, subscriber_name=None):
    redis_conn = get_redis()
    q = Queue('default', connection=redis_conn)
    # Import here to avoid importing sendgrid at worker startup if not needed
    from . import email_service
    job = q.enqueue(email_service.send_welcome_email, to_email, subscriber_name)
    return job.get_id()
