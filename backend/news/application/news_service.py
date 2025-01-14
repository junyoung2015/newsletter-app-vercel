from news.domain.repository.news_repo import INewsRepository
from dependency_injector.wiring import inject
from news.domain.news import Newsletter
from datetime import datetime
from news.domain.news import Topic
from news.domain.news import Source
from ulid import ULID
from newsletter.newsletter_generator import create_newsletter
from news.domain.news import NewsletterSent
from common.celery import create_newsletter_task
from celery.result import AsyncResult


class NewsService:
    @inject
    def __init__(
        self,
        news_repo: INewsRepository,
    ):
        self.news_repo = news_repo
        self.ulid = ULID()

    async def get_news(
        self,
        user_id: str,
    ):
        return await self.news_repo.get_news(user_id)

    async def save_news(
        self,
        user_id: str,
        name: str,
        description: str,
        custom_prompt: str,
        send_frequency: str,
        is_active: bool,
        topic: list[str] = [],
        source: list[str] = [],
    ):
        now = datetime.now()

        topics = [
            Topic(
                name=topic_name,
                created_at=now,
                updated_at=now,
            )
            for topic_name in topic
        ]

        sources = [
            Source(
                source_url=source_url,
                created_at=now,
                updated_at=now,
            )
            for source_url in source
        ]

        newsletter = Newsletter(
            user_id=user_id,
            name=name,
            description=description,
            custom_prompt=custom_prompt,
            send_frequency=send_frequency,
            is_active=is_active,
            topics=topics,
            sources=sources,
            created_at=now,
            updated_at=now,
        )
        # 뉴스레터 생성
        newsletter_id = await self.news_repo.save_news(user_id, newsletter)
        return newsletter_id

    def create_newsletter_task(
        self,
        topics: list[str],
        sources: list[str],
    ) -> AsyncResult:
        task: AsyncResult = create_newsletter_task.delay(topics, sources)
        return task

    # 보낸 뉴스레터 DB에 저장하는 함수
    async def save_sent_newsletter(
        self,
        newsletter_id: str,
        newsletter_sent_result: dict,
    ):
        now = datetime.now()
        newsletter_sent = NewsletterSent(
            newsletter_id=newsletter_id,
            name=newsletter_sent_result["title"],
            generated_content=newsletter_sent_result["content"],
            sent_at=now,
            created_at=now,
            updated_at=now,
        )
        await self.news_repo.create_news(newsletter_sent)
        return newsletter_sent
