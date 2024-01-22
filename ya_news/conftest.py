from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.utils import timezone
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def news_item():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_set():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments(author, news_item):
    now = timezone.now()
    for index in range(2):
        comm = Comment.objects.create(
            news=news_item, author=author, text=f'Tекст {index}',
        )
        comm.created = now + timedelta(days=index)
        comm.save()
    return comm


@pytest.fixture
def comment(author, news_item):
    comm = Comment.objects.create(
        news=news_item, author=author, text='Текст',
    )
    return comm


@pytest.fixture
def id_for_args(news_item):
    return news_item.id,
