from http import HTTPStatus

from notes.models import Note
from notes.tests.conf import BaseParameters, Urls


class TestRoutes(BaseParameters):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes_before = set(Note.objects.all())

    def test_pages_availability_for_anon(self):
        urls = (
            Urls.HOME,
            Urls.USER_LOGIN,
            Urls.USER_LOGOUT,
            Urls.USER_SIGNUP,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_auth(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in (Urls.NOTE_DETAIL, Urls.NOTE_EDIT, Urls.NOTE_DELETE):
                with self.subTest(user=user, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = Urls.USER_LOGIN
        for url in (Urls.NOTE_EDIT, Urls.NOTE_DELETE):
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
