from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Book, User, Borrow


class BookAdmin(ImportExportModelAdmin):
    list_display = ('book_id', 'book_name', 'book_author', 'book_press', 'book_isbn', 'book_language',
                    'book_price', 'book_publish_date', 'book_number', 'book_category_choice')
    list_filter = ['book_publish_date', 'book_category_choice']
    search_fields = ['book_name', 'book_author', 'book_press']


class UserAdmin(ImportExportModelAdmin):
    list_display = ("user_name", "user_phone", "user_email", "user_gender")


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_time', 'return_time', 'is_return')


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Borrow, BorrowAdmin)
