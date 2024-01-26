from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects

from .consts import Urls, UserClient

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, param_client, status_code',
    [
        (Urls.NEWS_HOME, UserClient.ANONIMUS, HTTPStatus.OK),
        (Urls.NEWS_DETAIL, UserClient.ANONIMUS, HTTPStatus.OK),
        (Urls.LOGIN, UserClient.ANONIMUS, HTTPStatus.OK),
        (Urls.LOGOUT, UserClient.ANONIMUS, HTTPStatus.OK),
        (Urls.SIGNUP, UserClient.ANONIMUS, HTTPStatus.OK),
        (Urls.NEWS_EDIT, UserClient.AUTHOR, HTTPStatus.OK),
        (Urls.NEWS_DELETE, UserClient.AUTHOR, HTTPStatus.OK),
        (Urls.NEWS_EDIT, UserClient.READER, HTTPStatus.NOT_FOUND),
        (Urls.NEWS_DELETE, UserClient.READER, HTTPStatus.NOT_FOUND),
    ]
)
def test_pages_availability(url, param_client, status_code):
    assert param_client.get(url).status_code == status_code


@pytest.mark.parametrize(
    'url, expected_url',
    [(Urls.NEWS_EDIT, Urls.REDIRECT_EDIT),
     (Urls.NEWS_DELETE, Urls.REDIRECT_DELETE)]
)
def test_redirect(client, url, expected_url):
    assertRedirects(client.get(url), expected_url)
