from django.db import models
from django.utils import timezone


# 图书模型：Book
class Book(models.Model):
    book_catergary = (
        ('technology', '科技'),
        ('literature', '文学'),
        ('culture', '文化'),
        ('language', '语言'),
        ('history', '历史'),
        ('philosophy', '哲学'),
        ('medicine', '医学'),
        ('society', '社会'),
    )
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField('书名', max_length=100)
    book_author = models.CharField('作者', max_length=100, default="")
    book_press = models.CharField('出版社', max_length=100, default="")
    book_isbn = models.CharField('ISBN', max_length=100, default="")
    book_language = models.CharField('语言', max_length=100, default="中文")
    book_price = models.FloatField('价格', default=0.0)
    book_publish_date = models.DateField('出版日期', default="1999-12-31")
    book_number = models.PositiveSmallIntegerField('数量', default=1)
    book_category_choice = models.CharField('主题', max_length=100, choices=book_catergary, default='literature')
    book_summary = models.TextField('内容简介', default="")

    def __str__(self):
        return self.book_name

    class Meta:
        ordering = ['book_id']
        verbose_name = "图书"
        verbose_name_plural = "图书"


# 用户模型：User
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField('用户名', max_length=100, unique=True)
    user_password = models.CharField('密码', max_length=100)
    user_phone = models.CharField('手机号', max_length=100)
    user_birthday = models.DateField('生日', default=timezone.now())
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    user_gender = models.CharField('性别', max_length=100, choices=gender)
    user_email = models.CharField('邮件地址', max_length=100)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['-user_id']
        verbose_name = '用户'
        verbose_name_plural = "用户"


# 借还书模型Borrow
class Borrow(models.Model):
    user = models.ForeignKey('User', to_field="user_id", on_delete=models.CASCADE)
    book = models.ForeignKey('Book', to_field="book_id", on_delete=models.CASCADE)
    borrow_time = models.DateTimeField(default=timezone.now())
    return_time = models.DateTimeField(null=True)
    is_return = models.CharField(max_length=10, default="True")

    def __str__(self):
        return self.is_return

    class Meta:
        ordering = ['-return_time']
        verbose_name = '借还书管理'
        verbose_name_plural = "借还书管理"
