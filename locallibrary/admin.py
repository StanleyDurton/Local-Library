#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : Team
# @FileName: admin.py
# @Software: PyCharm

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Book, User, Borrow


# 图书视图
class BookAdmin(ImportExportModelAdmin):
    # 显示列
    list_display = ('book_id', 'book_name', 'book_author', 'book_press', 'book_isbn', 'book_language',
                    'book_price', 'book_publish_date', 'book_add_time', 'book_number', 'book_category_choice',
                    'book_views', 'book_borrow')
    # 过滤器
    list_filter = ['book_publish_date', 'book_category_choice']
    # 搜索域
    search_fields = ['book_name', 'book_author', 'book_press']


class UserAdmin(ImportExportModelAdmin):
    # 显示列
    list_display = ("user_id", "user_name", "user_phone", "user_email", "user_gender")
    search_fields = ['user_name']


class BorrowAdmin(ImportExportModelAdmin):
    list_display = ('user', 'book', 'borrow_time', 'return_time', 'is_return')
    search_fields = ['user__user_name', 'book__book_name']


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Borrow, BorrowAdmin)
