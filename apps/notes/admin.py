from django.contrib import admin
from .models import Note, UserNote, Attachment, ListItems
# Register your models here.

admin.site.register(Note)
admin.site.register(UserNote)
admin.site.register(Attachment)
admin.site.register(ListItems)
