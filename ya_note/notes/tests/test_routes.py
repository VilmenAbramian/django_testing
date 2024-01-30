from http import HTTPStatus

from notes.models import Note
from notes.tests.conf import TestBaseParameters, Urls


class TestRoutes(TestBaseParameters):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes_before = set(Note.objects.all())

    def test_urls_status_code(self):
        testing_pages = (
            (Urls.HOME, self.anonymous_client, HTTPStatus.OK),
            (Urls.USER_LOGIN, self.anonymous_client, HTTPStatus.OK),
            (Urls.USER_LOGOUT, self.anonymous_client, HTTPStatus.OK),
            (Urls.USER_SIGNUP, self.anonymous_client, HTTPStatus.OK),
            (Urls.ADD_NOTE_URL, self.reader_client, HTTPStatus.OK),
            (Urls.NOTES_LIST, self.reader_client, HTTPStatus.OK),
            (Urls.SUCCESS_ADDING_URL, self.reader_client, HTTPStatus.OK),
            (Urls.NOTE_EDIT, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_DETAIL, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_DELETE, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (Urls.NOTE_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (Urls.NOTE_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for address, client, status in testing_pages:
            with self.subTest(address=address, client=client, status=status):
                self.assertEqual(client.get(address).status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (Urls.NOTE_EDIT, Urls.REDIRECT_TO_NOTE_EDIT),
            (Urls.NOTE_DELETE, Urls.REDIRECT_TO_NOTE_DELETE)
        )
        for url, redirect_url in urls:
            with self.subTest(url=url, redirect_url=redirect_url):
                self.assertRedirects(self.client.get(url), redirect_url)
