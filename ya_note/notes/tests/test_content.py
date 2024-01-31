from notes.forms import NoteForm
from notes.tests.conf import TestBaseParameters, Urls


class TestContent(TestBaseParameters):
    def test_one_note_in_context(self):
        notes = self.author_client.get(
            Urls.NOTES_LIST
        ).context['object_list']
        self.assertEqual(len(notes), 1)
        note = notes[0]
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_has_only_his_notes(self):
        self.assertNotIn(
            self.note,
            self.reader_client.get(Urls.NOTES_LIST).context['object_list']
        )

    def test_add_edit_pages_have_form(self):
        test_cases = (Urls.ADD_NOTE_URL, Urls.NOTE_EDIT)
        for url in test_cases:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
