from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import Note, UserNote


class NoteViewSetTests(APITestCase):
    """
    Pruebas para el conjunto de vistas de notas.
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

    def test_create_note_with_valid_data(self) -> None:
        """
        Prueba para verificar la creación de una nota con datos válidos.
        Se espera un estado de respuesta 201 (CREATED) y que la nota se
        guarde en la base de datos.
        """
        self.client.login(username='user1', password='user1')
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': 'This is a new note %$@@ 1234.'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.last().title, 'New Note')
        self.assertTrue(
            UserNote.objects.filter(
                user=self.user1, note=Note.objects.last()
            ).exists()
        )

    def test_crear_nota_sin_titulo(self) -> None:
        """
        Prueba para verificar que se rechaza la creación de una nota sin
        título. Se espera un estado de respuesta 400 (BAD REQUEST).
        """
        self.client.login(username='user2', password='user2')
        url = reverse('note-list')
        data = {
            'title': '',
            'content': 'Esto es un test',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_nota_con_titulo_solo(self) -> None:
        """
        Prueba para verificar que se puede crear una nota solo con título.
        Se espera un estado de respuesta 201 (CREATED).
        """
        self.client.login(username='user1', password='user1')
        url = reverse('note-list')
        data = {
            'title': 'Nota Solo Titulo',
            'content': ''  # Contenido vacío
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)  # Debe haber dos notas
        self.assertEqual(Note.objects.last().title, 'Nota Solo Titulo')

    def test_listar_notas(self) -> None:
        """
        Prueba para listar las notas del usuario.
        Se espera un estado de respuesta 405 .
        """
        self.client.login(username='user2', password='user2')
        url = reverse('note-list')
        response = self.client.get(url)

        self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_ver_detalles_de_nota(self) -> None:
        """
        Prueba para verificar la visualización de los detalles de una
        nota. Se espera un estado de respuesta 200 (OK).
        """
        self.client.login(username='user1', password='user1')
        url = reverse('note-detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.note.title)

    def test_ver_detalles_de_nota_no_autorizado(self) -> None:
        """
        Prueba para verificar que un usuario no autorizado no puede
        acceder a los detalles de una nota. Se espera un estado de
        respuesta 403 (FORBIDDEN).
        """
        self.client.login(username='user2', password='user2')
        url = reverse('note-detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
