from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Note
from django.urls import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User


class NoteViewSetTests(APITestCase):

    def setUp(self) -> None:
        """Crea un usuario y una instancia de Note para las pruebas."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_create_note_with_valid_data(self) -> None:
        """Prueba crear una nueva nota con datos válidos."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': 'This is a new note.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.last().title, 'New Note')

    def test_create_note_with_empty_content(self) -> None:
        """Prueba crear una nueva nota con contenido vacío."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_note_with_empty_title(self) -> None:
        """Prueba crear una nueva nota con título vacío."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-list')
        data = {
            'title': '',
            'content': 'This is a new note.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_get_notes(self) -> None:
        """Prueba recuperar la lista de notas."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_update_note_with_valid_data(self) -> None:
        """Prueba actualizar una nota existente con datos válidos."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-detail', args=[self.note.id])
        data = {
            'title': 'Updated Note',
            'content': 'This note has been updated.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')

    def test_update_note_with_empty_title(self) -> None:
        """Prueba actualizar una nota existente con un título vacío."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-detail', args=[self.note.id])
        data = {
            'title': '',  # Título vacío
            'content': 'This note has been updated.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_update_nonexistent_note(self) -> None:
        """Prueba actualizar una nota que no existe."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-detail', args=[999])  # ID de nota no existente
        data = {
            'title': 'Updated Note',
            'content': 'This note has been updated.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_delete_note(self) -> None:
        """Prueba eliminar una nota existente."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_nonexistent_note(self) -> None:
        """Prueba eliminar una nota que no existe."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('note-detail', args=[999])  # ID de nota no existente
        response: Response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_create_note_without_authentication(self) -> None:
        """Prueba crear una nueva nota sin autenticación."""
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': 'This note should not be created.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
