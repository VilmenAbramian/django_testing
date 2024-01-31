from pytils.translit import slugify
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
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(Urls.NOTE_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.notes_before, set(Note.objects.all()))

    def test_author_can_edit_note(self):
        response = self.author_client.post(Urls.NOTE_EDIT,
                                           data=self.refresh_note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        refresh_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(
            refresh_note.title,
            self.refresh_note_form_data['title']
        )
        self.assertEqual(
            refresh_note.text,
            self.refresh_note_form_data['text']
        )
        self.assertEqual(
            refresh_note.slug,
            self.refresh_note_form_data['slug']
        )
        self.assertEqual(
            refresh_note.author,
            self.note.author
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            Urls.NOTE_EDIT,
            data=self.refresh_note_form_data)
        refresh_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.note.title, refresh_note.title)
        self.assertEqual(self.note.text, refresh_note.text)
        self.assertEqual(self.note.slug, refresh_note.slug)
        self.assertEqual(
            self.note.author,
            refresh_note.author
        )

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(Urls.ADD_NOTE_URL,
                                           data=self.note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.all()[0]
        self.assertEqual(note.title, self.note_form_data['title'])
        self.assertEqual(note.text, self.note_form_data['text'])
        self.assertEqual(note.slug, self.note_form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_void_slug_creation_note(self):
        Note.objects.all().delete()
        self.author_client.post(
            Urls.ADD_NOTE_URL,
            data={'title': self.note_form_data['title'],
                  'text': self.note_form_data['text']}
        )
        new_note = Note.objects.all()[0]
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(new_note.title, self.note_form_data['title'])
        self.assertEqual(new_note.text, self.note_form_data['text'])
        self.assertEqual(new_note.slug, slugify(new_note.title)[:100])
        self.assertEqual(new_note.author, self.author)
