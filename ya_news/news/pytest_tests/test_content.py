import pytest

from django.conf import settings
from django.urls import reverse


HOME_URL = reverse('news:home')

@pytest.mark.django_db
def test_news_count(client, news_set):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_news_order(client, news_set):
        response = client.get(HOME_URL)
        object_list = response.context['object_list']
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        # Проверяем, что исходный список был отсортирован правильно.
        assert all_dates == sorted_dates

@pytest.mark.django_db
def test_comment_order(client, comments):
        news_item_url = reverse('news:detail', args=(comments.news.id,))
        response = client.get(news_item_url)
        assert 'news' in response.context
        news = response.context['news']
        all_comments = news.comment_set.all()
        all_comments[0].created < all_comments[1].created

@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_item):
        detail_url = reverse('news:detail', args=(news_item.id,))
        response = client.get(detail_url)
        assert 'form' not in response.context

def test_authorized_client_has_form(author_client, news_item):
    detail_url = reverse('news:detail', args=(news_item.id,))
    response = author_client.get(detail_url)
    assert 'form' in response.context 