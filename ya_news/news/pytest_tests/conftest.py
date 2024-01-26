from datetime import datetime, timedelta
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    author_client = Client()
    author_client.force_login(author)  # Логиним автора в клиенте.
    return author_client


@pytest.fixture
def reader_client(reader):
    reader_client = Client()
    reader_client.force_login(reader)  # Логиним автора в клиенте.
    return reader_client


@pytest.fixture
def news_item():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def news_set():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, news_item):
    return Comment.objects.create(
        news=news_item, author=author, text='Текст',
    )


@pytest.fixture
def comments(author, news_item):
    now = timezone.now()
    for index in range(222):
        comments_set = Comment.objects.create(
            news=news_item, author=author, text=f'Tекст {index}',
        )
        comments_set.created = now + timedelta(days=index)
        comments_set.save()
    return comments_set


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news_item):
    return reverse('news:detail', args=(news_item.pk,))


@pytest.fixture
def news_delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def news_edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login',)


@pytest.fixture
def logout_url():
    return reverse('users:logout',)


@pytest.fixture
def signup_url():
    return reverse('users:signup',)


@pytest.fixture
def to_news_edit_url_after_login(login_url, news_edit_url):
    return f'{login_url}?next={news_edit_url}'


@pytest.fixture
def to_news_delete_url_after_login(login_url, news_delete_url):
    return f'{login_url}?next={news_delete_url}'


@pytest.fixture
def to_news_detail_url_after_login(login_url, news_detail_url):
    return f'{login_url}?next={news_detail_url}'


@pytest.fixture
def form_data():
    return None
