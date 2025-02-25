from django.contrib import admin
from.models import *
from .models import Book
from .models import BorrowRecord

for model in [Reader, Book, BorrowRecord]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# Register your models here.
admin.site.register(Reader)
admin.site.register(Book)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'borrowed_date', 'return_date', 'is_returned')
    # list_filter = ('is_returned', 'borrowed_date', 'return_date')
    # search_fields = ('book__title', 'user__username')

admin.site.register(BorrowRecord, BorrowRecordAdmin)




