from django.contrib import admin
from.models import *
from .models import Book

# Register your models here.
admin.site.register(Reader)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'genre', 'price_5_days', 'daily_rate', 'available')  # Add fields to list display
    search_fields = ('title', 'author', 'isbn')
    
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')