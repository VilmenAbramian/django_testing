from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note
from notes.tests.conf import TestBaseParameters, Urls

User = get_user_model()


class TestPostCreation(TestBaseParameters):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes_before = set(Note.objects.all())

    def test_anonymous_user_cant_create_note(self):
        self.client.post(Urls.ADD_NOTE_URL, data=self.note_form_data)
        self.assertEqual(self.notes_before, set(Note.objects.all()))

    def test_uniq_slug(self):
        response_for_similar_note = self.author_client.post(
            Urls.ADD_NOTE_URL,
            data=self.note_form_data
        )
        self.assertFormError(
            response_for_similar_note,
            form='form',
            field='slug',
            errors=self.note_form_data['slug'] + WARNING
        )
        # 1 заметка из конструктора
        self.assertEqual(self.notes_before, set(Note.objects.all()))

    def test_author_can_delete_note(self):
        response = self.author_client.delete(Urls.NOTE_DELETE)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        self.assertEqual(Note.objects.count(), len(self.notes_before) - 1)
        self.assertFalse(Note.objects.filter(slug=self.note.slug).exists())

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(Urls.NOTE_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.notes_before, set(Note.objects.all()))

    def test_author_can_edit_note(self):
        response = self.author_client.post(Urls.NOTE_EDIT,
                                           data=self.refresh_note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.refresh_note_form_data['title'])
        self.assertEqual(self.note.text, self.refresh_note_form_data['text'])
        self.assertEqual(self.note.slug, self.refresh_note_form_data['slug'])
        self.assertEqual(
            self.note.author,
            self.refresh_note_form_data['author']
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            Urls.NOTE_EDIT,
            data=self.refresh_note_form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.note.title, self.note_form_data['title'])
        self.assertEqual(self.note.text, self.note_form_data['text'])
        self.assertEqual(self.note.slug, self.note_form_data['slug'])
        self.assertEqual(
            self.note.author,
            Note.objects.get(slug=self.note.slug).author
        )

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(Urls.ADD_NOTE_URL,
                                           data=self.note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        note = (set(Note.objects.all()) - self.notes_before).pop()
        self.assertEqual(note.title, self.note_form_data['title'])
        self.assertEqual(note.text, self.note_form_data['text'])
        self.assertEqual(note.slug, self.note_form_data['slug'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(1, Note.objects.count())

    def test_void_slug_creation_note(self):
        Note.objects.all().delete()
        self.author_client.post(
            Urls.ADD_NOTE_URL,
            data={'title': self.note_form_data['title'],
                  'text': self.note_form_data['text']}
        )
        self.assertEqual(Note.objects.all()[0].slug, 'test-note-title')
