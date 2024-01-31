import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(news_home_url, client, news_set):
    assert (len(client.get(news_home_url).context['object_list'])
            == settings.NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(news_home_url, client, news_set):
    all_dates = [news.date for news in
                 client.get(news_home_url).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comment_order(news_detail_url, client, comments):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    all_dates = [comment.created for comment in
                 response.context['news'].comment_set.all()]
    assert all_dates == sorted(all_dates)


def test_anonymous_client_has_no_form(news_detail_url, client, news_item):
    assert 'form' not in client.get(news_detail_url).context


def test_authorized_client_has_form(news_detail_url, author_client, news_item):
    assert isinstance(author_client.get(news_detail_url).context.get('form'),
                      CommentForm)
