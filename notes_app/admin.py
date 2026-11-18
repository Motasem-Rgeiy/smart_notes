from django.contrib import admin
from notes_app.models import Note , Category , User
# Register your models here.


@admin.register(Category)

@admin.register(User)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_per_page = 10