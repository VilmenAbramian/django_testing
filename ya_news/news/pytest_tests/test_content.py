from django.conf import settings
import pytest

from .consts import Urls
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url', [Urls.NEWS_HOME]
)
def test_news_count(url, client, news_set):
    response = client.get(url)
    news_list = response.context['object_list']
    assert len(news_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize(
    'url', [Urls.NEWS_HOME]
)
def test_news_order(url, client, news_set):
    response = client.get(url)
    news_list = response.context['object_list']
    all_dates = [news.date for news in news_list]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.parametrize(
    'url', [Urls.NEWS_DETAIL]
)
def test_comment_order(url, client, comments):
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_dates = [comment.created for comment in all_comments]
    assert all_dates == sorted(all_dates)


@pytest.mark.parametrize(
    'url', [Urls.NEWS_DETAIL]
)
def test_anonymous_client_has_no_form(url, client, news_item):
    assert 'form' not in client.get(url).context


@pytest.mark.parametrize(
    'url', [Urls.NEWS_DETAIL]
)
def test_authorized_client_has_form(url, author_client, news_item):
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
