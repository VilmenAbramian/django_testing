from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note
from notes.tests.conf import BaseParameters, Urls, Text

User = get_user_model()


class TestPostCreation(BaseParameters):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes_before = set(Note.objects.all())

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.add_url, data=self.note_form_data)
        notes_count_after = Note.objects.count()
        self.assertEqual(len(self.notes_before), notes_count_after)

    def test_user_can_create_note(self):
        Note.objects.filter(slug=Text.NOTE_SLUG).delete()
        response = self.author_client.post(self.add_url,
                                           data=self.note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        notes_count_after = Note.objects.count()
        self.assertEqual(len(self.notes_before), notes_count_after)
        note = (set(Note.objects.all()) - self.notes_before).pop()
        self.assertEqual(note.title, self.note_form_data['title'])
        self.assertEqual(note.text, self.note_form_data['text'])
        self.assertEqual(note.slug, self.note_form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_uniq_slug(self):
        response_for_similar_note = self.author_client.post(
            self.add_url,
            data=self.note_form_data
        )
        self.assertFormError(
            response_for_similar_note,
            form='form',
            field='slug',
            errors=self.note_form_data['slug'] + WARNING
        )
        notes_count_after = Note.objects.count()
        # 1 заметка из конструктора
        self.assertEqual(len(self.notes_before), notes_count_after)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, len(self.notes_before) - 1)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = set(Note.objects.all())
        self.assertEqual(self.notes_before, notes_after)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url,
                                           data=self.refresh_note_form_data)
        self.assertRedirects(response, Urls.SUCCESS_ADDING_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.refresh_note_form_data['title'])
        self.assertEqual(self.note.text, self.refresh_note_form_data['text'])
        self.assertEqual(self.note.slug, self.refresh_note_form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            self.edit_url,
            data=self.refresh_note_form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.note_form_data['text'])
