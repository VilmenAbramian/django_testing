from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


NOTE_SLUG = 'test228'
NEW_PREFIX = 'new_'


class Urls():
    HOME = reverse('notes:home')
    ADD_NOTE_URL = reverse('notes:add')
    SUCCESS_ADDING_URL = reverse('notes:success')
    NOTES_LIST = reverse('notes:list')
    USER_LOGIN = reverse('users:login')
    USER_LOGOUT = reverse('users:logout')
    USER_SIGNUP = reverse('users:signup')
    NOTE_EDIT = reverse('notes:edit', args=(NOTE_SLUG,))
    NOTE_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
    NOTE_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
    REDIRECT_TO_NOTE_EDIT = f'{USER_LOGIN}?next={NOTE_EDIT}'
    REDIRECT_TO_NOTE_DELETE = f'{USER_LOGIN}?next={NOTE_DELETE}'


class TestBaseParameters(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create(username='Другой пользователь')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.anonymous_client = Client()
        cls.anonymous_client.username = 'Anonymous client'

        cls.note_form_data = {
            'title': 'Test note title',
            'text': 'Текст заметки',
            'slug': NOTE_SLUG,
        }
        cls.refresh_note_form_data = {
            'title': NEW_PREFIX + cls.note_form_data['title'],
            'text': NEW_PREFIX + cls.note_form_data['text'],
            'slug': NEW_PREFIX + cls.note_form_data['slug'],
            'author': cls.author
        }
        cls.note = Note.objects.create(
            title=cls.note_form_data['title'],
            text=cls.note_form_data['text'],
            slug=cls.note_form_data['slug'],
            author=cls.author,
        )
