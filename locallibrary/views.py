from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from .models import Book, User, Borrow


# 主界面视图
def index(request):
    # 选取最近上架的三本书来展示
    book_list = Book.objects.all()[:6]
    return render(request, 'index.html', {'book_list': book_list})


# 登录视图
def login(request):
    if request.method == 'GET':
        # 链接跳转过来的登录页面，采用GET方法 <a href
        return render(request, 'login.html')

    elif request.method == 'POST':
        # 登录页面form提交事件，采用post方法
        name = request.POST.get('user_name')
        password = request.POST.get('user_password')
        try:
            q = User.objects.get(user_name=name)
        except:
            messages.error(request, "Nonexistent account")
        else:
            if q.user_password == password:
                request.session['is_login'] = True
                request.session['user_name'] = name
                messages.success(request,  "Login Successfully")
            else:
                messages.error(request, "Wrong password")
        return render(request, 'login.html')


# 注册视图
def register(request):
    if request.method == 'GET':
        # 链接跳转过来的注册页面，采用GET方法 <a href
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 注册页面form提交事件，采用post方法
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        user_confirm_password = request.POST.get('user_confirm_password')
        user_phone = request.POST.get('user_phone')
        user_birthday = request.POST.get('user_birthday')
        user_gender = request.POST.get('user_gender')
        user_email = request.POST.get('user_email')
        # 需要进一步验证注册信息
        # 注册成功后返回用户账号界面或者之前的页面
        if user_password.strip() == user_confirm_password.strip():
            u = User.objects.create(user_name=user_name, user_password=user_password, user_phone=user_phone,
                                    user_birthday=user_birthday, user_gender=user_gender, user_email=user_email)
            u.save()
            messages.success(request, "register Successfully")
            request.session['is_login'] = True
            request.session['user_name'] = user_name
        else:
            messages.error(request, 'Password confirmed incorrectly')
        return render(request, 'register.html')


# 注销视图
def logout(request):
    request.session.flush()
    return redirect('/')


# 查询视图
def query(request):
    if request.method == 'POST':
        book_name = request.POST.get('search')
        if book_name.strip():
            books = Book.objects.filter(book_name__contains=book_name)
            return render(request, 'query.html', {'book_list': books, 'arr_length': len(books)})


# 书目详情视图
def book(request, isbn):
    book = Book.objects.get(book_isbn=isbn)
    return render(request, 'book.html', locals())


# 读者账号页面视图
def account(request):
    name = request.session.get('user_name')
    # print(name)
    q = User.objects.get(user_name=name)
    records = Borrow.objects.filter(user=q)
    return render(request, 'interface.html', locals())


# 还书
def return_book_view(request, book_isbn):
    name = request.session.get('user_name')
    q = User.objects.get(user_name=name)
    b = Book.objects.get(book_isbn=book_isbn)
    return_book = Borrow.objects.get(user=q, book=b)
    return_book.is_return = "True"
    return_book.return_time = timezone.now()
    b.book_number += 1
    b.save()
    return_book.save()
    records = Borrow.objects.filter(user=q)
    return render(request, 'interface.html', locals())


# 借书
def borrow_view(request, book_isbn):
    if request.method == 'GET':
        # 链接跳转过来的登录页面，采用GET方法 <a href
        user = User.objects.get(user_name=request.session.get('user_name'))
        book = Book.objects.get(book_isbn=book_isbn)
        print(user, book)
        duplicate = Borrow.objects.filter(user=user, book=book)
        if duplicate:
            messages.error(request, "Already borrow one, don't be greedy!")
            # messages.error(request, "Something wrong with the information")
        elif book.book_number >= 1:
            try:
                # print(timezone.now().strftime("%Y-%m-%d %H:%M"))
                new_record = Borrow.objects.create(user=user, book=book, borrow_time=timezone.now(), is_return="False")
            except Exception as e:
                messages.error(request, "Error while creating a borrow record")
            else:
                new_record.save()
                book.book_number = book.book_number - 1
                book.save()
                messages.success(request, "Borrow Successful!")
        else:
            messages.error(request, "Not Enough Book for User")
        return render(request, 'book.html', {'book': book})


def modify(request):
    if request.method == "GET":
        user = User.objects.get(user_name=request.session.get('user_name'))
        return render(request, 'modify.html', locals())
    else:
        # 修改账号信息
        # 不可以修改用户名和生日
        user_name = request.session.get('user_name')
        user_password = request.POST.get('user_password')
        # user_birthday = request.POST.get('user_birthday')
        user_phone = request.POST.get('user_phone')
        user_email = request.POST.get('user_email')
        user = User.objects.get(user_name=user_name)
        flag_modify = False
        if user_password.strip() and user_password != user.user_password:
            user.user_password = user_password
            flag_modify = True
        if user_phone.strip() and user.user_phone != user_phone:
            user.user_phone = user_phone
            flag_modify = True
        if user_email.strip() and user.user_email != user_email:
            user.user_email = user_email
            flag_modify = True
        if flag_modify:
            user.save()
            messages.success(request, "修改成功")
        else:
            messages.info(request, "您没有修改任何信息")
        return render(request, 'modify.html')