from celery.app import Celery
from newsletter.newsletter_generator import create_newsletter
from config import get_settings

settings = get_settings()
REDIS_URL = settings.redis_url

app = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)


@app.task
def create_newsletter_task(topics: list[str], sources: list[str]):
    return create_newsletter(topics, sources)
