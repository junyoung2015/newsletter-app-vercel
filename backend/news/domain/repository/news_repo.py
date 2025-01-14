from abc import ABCMeta, abstractmethod
from user.domain.user import User
from news.domain.news import Newsletter
from news.domain.news import NewsletterSent


class INewsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_news(self, user: User):
        """
        유저가 생성한 뉴스레터 정보를 가져온다.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_news(self, user_id: str, news: Newsletter):
        """
        뉴스레터 정보를 저장한다.
        """
        raise NotImplementedError

    @abstractmethod
    async def create_news(self, newsletter_sent_info: NewsletterSent):
        """
        뉴스레터 생성
        """
        raise NotImplementedError
