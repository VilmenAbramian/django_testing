import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
comment_data = {'text': 'Текст комментария'}


def test_anonymous_user_cant_create_comment(news_detail_url, client):
    client.post(news_detail_url, data=comment_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        news_detail_url,
        reader_client,
        reader,
        news_item
):
    comments_before = set(Comment.objects.all())
    assertRedirects(
        reader_client.post(news_detail_url, data=comment_data),
        f'{news_detail_url}#comments'
    )
    new_comments_set = set(Comment.objects.all()) - comments_before
    assert len(new_comments_set) == 1
    comment = new_comments_set.pop()
    assert comment.text == comment_data['text']
    assert comment.news == news_item
    assert comment.author == reader


def test_user_cant_use_bad_words(news_detail_url, author_client, news_item):
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, news_delete_url, comment):
    comments_before = len(Comment.objects.all())
    author_client.post(news_delete_url)
    assert len(Comment.objects.all()) == comments_before - 1
    assert Comment.objects.filter(pk=comment.pk).exists() is False


refresh_comment_data = {
    'text': 'Обновлённый комментарий'
}


def test_author_can_edit_comment(
        author_client,
        author, news_item,
        news_edit_url,
        news_detail_url,
        comment
):
    assertRedirects(
        author_client.post(news_edit_url, refresh_comment_data),
        f'{news_detail_url}#comments'
    )
    refresh_comment = Comment.objects.get(pk=comment.pk)
    # comment.refresh_from_db()
    assert refresh_comment.text == refresh_comment_data['text']
    assert refresh_comment.news == news_item
    assert comment.news == news_item
    assert refresh_comment.author == author
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        news_edit_url,
        comment
):
    comments_before = Comment.objects.all()
    reader_client.post(news_edit_url, refresh_comment_data)
    # comment.refresh_from_db()
    refresh_comment = Comment.objects.get(pk=comment.pk)
    comments_after = Comment.objects.all()
    assert set(comments_before) == set(comments_after)
    assert refresh_comment.text == comment.text
    assert refresh_comment.author == comment.author
