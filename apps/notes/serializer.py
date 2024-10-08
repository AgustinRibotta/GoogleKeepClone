from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Note, UserNote, Attachment, ListItems
from django.contrib.auth.models import User


"""
Serializadores para Notas
"""


class UserForNoteSerializer(serializers.ModelSerializer):
    """ Serializador User para Note """
    class Meta:
        model = User
        fields = ['id', 'username']


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


class UserNoteSerializer(serializers.ModelSerializer):
    """ Serializer para el listado de las Notas relacionadas un Usuario """
    user = UserForNoteUserSerializer(read_only=True)
    note = NoteForNoteUserSerialzier(read_only=True)
    update_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    retrieve_url = serializers.SerializerMethodField()

    class Meta:
        model = UserNote
        fields = ['user', 'note', 'update_url', 'delete_url', 'retrieve_url']

    def get_update_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_delete_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)

    def get_retrieve_url(self, obj):
        request = self.context.get('request')
        return reverse(
                'note-detail',
                kwargs={'pk': obj.note.id},
                request=request)
