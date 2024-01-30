from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class Text:
    NOTE_TITLE = 'Заголовок заметки'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'test228'
    NEW_PREFIX = 'new_'
    NEW_NOTE_TITLE = NEW_PREFIX + NOTE_TITLE
    NEW_NOTE_TEXT = NEW_PREFIX + NOTE_TEXT
    NEW_NOTE_SLUG = NEW_PREFIX + NOTE_SLUG


class Urls():
    HOME = reverse('notes:home')
    ADD_NOTE_URL = reverse('notes:add')
    SUCCESS_ADDING_URL = reverse('notes:success')
    NOTES_LIST = reverse('notes:list')
    USER_LOGIN = reverse('users:login')
    USER_LOGOUT = reverse('users:logout')
    USER_SIGNUP = reverse('users:signup')
    NOTE_EDIT = reverse('notes:edit', args=(Text.NOTE_SLUG,))
    NOTE_DELETE = reverse('notes:delete', args=(Text.NOTE_SLUG,))
    NOTE_DETAIL = reverse('notes:detail', args=(Text.NOTE_SLUG,))


class BaseParameters(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Другой пользователь')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.add_url = Urls.ADD_NOTE_URL
        cls.note_form_data = {
            'title': Text.NOTE_TITLE,
            'text': Text.NOTE_TEXT,
            'slug': Text.NOTE_SLUG,
        }
        cls.refresh_note_form_data = {
            'title': Text.NEW_NOTE_TITLE,
            'text': Text.NEW_NOTE_TEXT,
            'slug': Text.NEW_NOTE_SLUG,
        }
        cls.note = Note.objects.create(
            title=cls.note_form_data['title'],
            text=cls.note_form_data['text'],
            slug=cls.note_form_data['slug'],
            author=cls.author,
        )
        cls.edit_url = Urls.NOTE_EDIT
        cls.delete_url = Urls.NOTE_DELETE
