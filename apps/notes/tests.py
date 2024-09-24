from rest_framework import status
from rest_framework.test import APITestCase
from .models import Note
from django.urls import reverse
from rest_framework.response import Response

class NoteViewSetTests(APITestCase):

    def setUp(self) -> None:
        """ Create an instance of Note for testing """
        self.note = Note.objects.create(  # type: ignore
            title="Test Note",
            content="This is a test note."
        )

    def test_create_note_with_valid_data(self) -> None:
        """ Test creating a new note with valid data """
        url = reverse('note-list')
        data = {'title': 'New Note', 'content': 'This is a new note.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)  # type: ignore
        self.assertEqual(Note.objects.last().title, 'New Note')  # type: ignore

    def test_create_note_with_empty_content(self) -> None:
        """ Test creating a new note with empty content """
        url = reverse('note-list')
        data = {'title': 'New Note', 'content': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_notes(self) -> None:
        """ Test retrieving the list of notes """
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_note_with_valid_data(self) -> None:
        """ Test updating an existing note with valid data """
        url = reverse('note-detail', args=[self.note.id])
        data = {
            'title': 'Updated Note',
            'content': 'This note has been updated.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')

    def test_update_note_with_invalid_data(self) -> None:
        """ Test updating an existing note with invalid data """
        url = reverse('note-detail', args=[self.note.id])
        data = {
            'title': '',  # Invalid empty title
            'content': 'This note has been updated.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_note(self) -> None:
        """ Test deleting an existing note """
        url = reverse('note-detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)  # type: ignore

    def test_delete_nonexistent_note(self) -> None:
        """ Test deleting a note that does not exist """
        url = reverse('note-detail', args=[999])
        response: Response  = self.client.delete(url)
        self.assertEqual(
                response.status_code,  # Correct attribute
                status.HTTP_404_NOT_FOUND
                )
