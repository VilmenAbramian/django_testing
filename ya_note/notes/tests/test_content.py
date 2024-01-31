from notes.forms import NoteForm
from notes.tests.conf import TestBaseParameters, Urls
from notes.models import Note


class TestContent(TestBaseParameters):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_one_note_in_context(self):
        self.assertIsInstance(
            self.author_client.get(
                Urls.NOTES_LIST
            ).context['object_list'][0], Note
        )

    def test_author_has_only_his_notes(self):
        self.assertNotIn(
            self.note,
            self.reader_client.get(Urls.NOTES_LIST).context['object_list']
        )

    def test_add_edit_pages_have_form(self):
        add_response = self.author_client.get(Urls.ADD_NOTE_URL)
        self.assertIn('form', add_response.context)
        self.assertIsInstance(add_response.context['form'], NoteForm)
        edit_response = self.author_client.get(Urls.NOTE_EDIT)
        self.assertIn('form', edit_response.context)
        self.assertIsInstance(edit_response.context['form'], NoteForm)
