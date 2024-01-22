import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from http import HTTPStatus

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import News, Comment

COMMENT_TEXT = 'Текст комментария'
form_data = {'text': COMMENT_TEXT}

@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_item):
    url = reverse('news:detail', args=(news_item.id,))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0

@pytest.mark.django_db
def test_user_can_create_comment(author_client, news_item):
    url = reverse('news:detail', args=(news_item.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news_item


def test_user_cant_use_bad_words(author_client, news_item):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news_item.id,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
        )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, news_item, comments):
    delete_url = reverse('news:delete', args=(comments.id,))  
    response = author_client.delete(delete_url)
    news_url = reverse('news:detail', args=(news_item.id,))
    url_to_comments = news_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 1

def test_author_can_edit_comment(author_client, news_item, comments):
    new_comment_text = 'Обновлённый комментарий'
    edit_url = reverse('news:edit', args=(comments.id,)) 
    response = author_client.post(edit_url, data=form_data)
    news_url = reverse('news:detail', args=(news_item.id,))
    url_to_comments = news_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments.refresh_from_db()
    comments.text == new_comment_text

def test_user_cant_edit_comment_of_another_user(client, comment):
    edit_url = reverse('news:edit', args=(comment.id,)) 
    response = client.post(edit_url, data={'text': 'Новый текст'})
    comment.refresh_from_db()
    comment.text == COMMENT_TEXT 