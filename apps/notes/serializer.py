from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Note, UserNote
from django.contrib.auth.models import User


"""
Serializadores para Notas
"""


class UserForNoteSerializer(serializers.ModelSerializer):
    """ Serializador User para Note """
    delete_user_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'delete_user_url']

    def get_delete_user_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'usernote-detail',
                kwargs={'pk': obj.id},
                request=request)


class UserNoteForNoteSerializerNote(serializers.ModelSerializer):
    """ Serializador para User Note para Note Serialzier"""
    user = UserForNoteSerializer()

    class Meta:
        model = UserNote
        fields = ['user']


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Serializer para detalles de Note """
    users = UserNoteForNoteSerializerNote(many=True, source='note_user')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'users']


class NoteSerializer(serializers.ModelSerializer):
    """ Serializar para Note """
    class Meta:
        model = Note
        fields = '__all__'


"""
Serializadores para User Nota
"""


class UserForNoteUserSerializer(serializers.ModelSerializer):
    """ Serializador User para User Note """
    class Meta:
        model = User
        fields = ['id', 'username']


class NoteForNoteUserSerialzier(serializers.ModelSerializer):
    """ Serializor Note para User Note """
    class Meta:
        model = Note
        fields = ['id', 'title', 'content']


class UserNoteListSerializer(serializers.ModelSerializer):
    """ Serializer para el listado de las Notas relacionadas un Usuario """
    user = UserForNoteUserSerializer(read_only=True)
    note = NoteForNoteUserSerialzier(read_only=True)
    update_note_url = serializers.SerializerMethodField()
    delete_note_url = serializers.SerializerMethodField()
    retrieve_note_url = serializers.SerializerMethodField()

    class Meta:
        model = UserNote
        fields = [
                'user',
                'note',
                'update_note_url',
                'delete_note_url',
                'retrieve_note_url'
                ]

    def get_update_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_delete_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_retrieve_note_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)


class UserNoteSerializer(serializers.ModelSerializer):
    """ Serialzador par Metodo Create - Delete - Update - Retrive"""
    class Meta:
        model = UserNote
        fields = '__all__'
