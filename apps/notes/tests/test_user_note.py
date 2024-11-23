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
        UserNote.objects.create(user=self.user2, note=self.note)

    def test_listar_notas_usuario(self) -> None:
        """
        Prueba que permite que el usuario liste solo sus notas.
        Se espera un estado de respuesta 200 (OK).
        """

        self.client.login(username='user1', password='user1')
        url = reverse('user-note-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo debería devolver una nota de user1

    def test_listar_notas_de_otro_usuario(self) -> None:
        """
        Prueba que permite que el usuario liste solo sus notas.
        Este debe devolver un estado de respuesta 200 (OK).
        """

        self.client.login(username='user2', password='user2')
        url = reverse('user-note-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_agregar_users_usernote(self) -> None:
        """
        Prueba que permite al usuario agregar a alguien a sus notas.
        Esta debe devolver un estado de respuesta 200 (OK).
        """

        self.client.login(username='user1', password='user1')
        url = reverse("user-note-list")
        data = {
            "user": self.user2.pk,  # Usar el ID del objeto user2
            "note": self.note.pk,    # Usar el ID de la nota
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserNote.objects.count(), 3)  # Debe haber 3 UserNotes ahora

    def test_agregar_users_note_que_no_son_suyas(self) -> None:
        """
        Prueba que no permite al usuario agregar usuarios a otras notas que no sean las suyas.
        Se espera un estado de respuesta 403 (FORBIDDEN).
        """

        self.client.login(username='user2', password='user2')
        url = reverse("user-note-list")

        data = {
            "user": self.user1.pk,
            "note": 2,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_eliminar_usuario_de_nota(self) -> None:

        self.client.login(username='user1', password='user1')
        usernote = UserNote.objects.get(user=self.user1, note=self.note)
        url = reverse('user-note-detail', kwargs={'pk': usernote.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserNote.objects.filter(pk=usernote.pk).exists())

    def test_no_puede_eliminar_usuario_de_nota_que_no_es_suya(self) -> None:

        self.client.login(username='user2', password='user2')
        usernote = UserNote.objects.get(user=self.user1, note=self.note)
        url = reverse('user-note-detail', kwargs={'pk': usernote.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(UserNote.objects.filter(pk=usernote.pk).exists())
