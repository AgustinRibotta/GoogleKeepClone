from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import Note, UserNote


class NoteViewSetTests(APITestCase):
    """
    Pruebas para el conjunto de vistas de user notas.
    """

    def setUp(self) -> None:
        """
        Configuración inicial para las pruebas.
        Crea dos usuarios y una instancia de nota para realizar las pruebas.
        También establece la relación entre el usuario y la nota en UserNote.
        """
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='user2'
        )

        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )
        UserNote.objects.create(user=self.user1, note=self.note)

    def test_agregar_users_usernote(self) -> None:
        """
        Prueba que permite al usuario agregar a alguien a sus notas.
        Esta deve devover un estado de respuesta 200 (OK).
        """

        self.client.login(
                username='user1',
                password='user1',
                )
        url = reverse("user-note")
        data = {
                "user": 2,
                "note": 1,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserNote.objects.count(), 2)
