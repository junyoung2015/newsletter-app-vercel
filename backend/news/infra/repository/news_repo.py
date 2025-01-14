from news.domain.repository.news_repo import INewsRepository
from database import SessionLocal
from news.infra.db_models.newsletter import Newsletters
from sqlalchemy.future import select
from news.domain.news import Newsletter as NewsletterVO
from news.domain.news import Topic as TopicVO
from news.domain.news import Source as SourceVO
from news.domain.news import NewsletterSent as NewsletterSentVO
from utils.db_utils import row_to_dict
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import HTTPException
from fastapi import status
from news.infra.db_models.newsletter import Topics
from news.infra.db_models.newsletter import Sources
from news.infra.db_models.newsletter import NewslettersSent


class NewsRepository(INewsRepository):
    async def get_news(self, user_id: str) -> List[NewsletterVO]:
        try:
            async with SessionLocal() as db:
                result = await db.execute(
                    select(Newsletters).where(Newsletters.user_id == user_id)
                )
                news = result.scalars().all()
                newsletter_vos = []
                for newsletter in news:
                    topics = [
                        TopicVO(
                            name=topic.name,
                            created_at=topic.created_at,
                            updated_at=topic.updated_at,
                        )
                        for topic in newsletter.topics
                    ]
                    sources = [
                        SourceVO(
                            source_url=source.source_url,
                            created_at=source.created_at,
                            updated_at=source.updated_at,
                        )
                        for source in newsletter.sources
                    ]
                    newsletter_vo = NewsletterVO(
                        user_id=newsletter.user_id,
                        name=newsletter.name,
                        description=newsletter.description,
                        custom_prompt=newsletter.custom_prompt,
                        send_frequency=newsletter.send_frequency,
                        is_active=newsletter.is_active,
                        topics=topics,
                        sources=sources,
                        created_at=newsletter.created_at,
                        updated_at=newsletter.updated_at,
                    )
                    newsletter_vos.append(newsletter_vo)
                return newsletter_vos
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def save_news(self, user_id: str, news: NewsletterVO):
        try:
            async with SessionLocal() as db:
                topics: list[Topics] = []
                for topic in news.topics:
                    existing_topic_result = await db.execute(
                        select(Topics).where(Topics.name == topic.name)
                    )
                    existing_topic = existing_topic_result.scalar_one_or_none()
                    if not existing_topic:
                        topic = Topics(
                            name=topic.name,
                            created_at=topic.created_at,
                            updated_at=topic.updated_at,
                        )
                        db.add(topic)
                        topics.append(topic)
                    else:
                        topics.append(existing_topic)

                sources: list[Sources] = []
                for source in news.sources:
                    existing_source_result = await db.execute(
                        select(Sources).where(Sources.source_url == source.source_url)
                    )
                    existing_source = existing_source_result.scalar_one_or_none()
                    if not existing_source:
                        source = Sources(
                            source_url=source.source_url,
                            created_at=source.created_at,
                            updated_at=source.updated_at,
                        )
                        db.add(source)
                        sources.append(source)
                    else:
                        sources.append(existing_source)

                newsletter = Newsletters(
                    user_id=user_id,
                    name=news.name,
                    description=news.description,
                    custom_prompt=news.custom_prompt,
                    send_frequency=news.send_frequency,
                    is_active=news.is_active,
                    topics=topics,
                    sources=sources,
                    created_at=news.created_at,
                    updated_at=news.updated_at,
                )
                db.add(newsletter)
                await db.commit()
                await db.refresh(newsletter)
                return newsletter.id
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def create_news(self, newsletter_sent_info: NewsletterSentVO):
        try:
            newsletter_sent = NewslettersSent(
                newsletter_id=newsletter_sent_info.newsletter_id,
                name=newsletter_sent_info.name,
                generated_content=newsletter_sent_info.generated_content,
                sent_at=newsletter_sent_info.sent_at,
                created_at=newsletter_sent_info.created_at,
                updated_at=newsletter_sent_info.updated_at,
            )
            async with SessionLocal() as db:
                db.add(newsletter_sent)
                await db.commit()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
