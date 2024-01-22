# test_routes.py
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

import pytest

@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup', 'news:detail')
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, news_item):
    if name == 'news:detail':
        url = reverse(name, args=(news_item.id,))
    else:
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('id_for_args')),
        ('news:delete', pytest.lazy_fixture('id_for_args')),
    ),
)
@pytest.mark.django_db
def test_redirect_for_anonymous_client(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url) 