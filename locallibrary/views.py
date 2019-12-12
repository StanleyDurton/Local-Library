from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
import json

from .models import Book, User, Borrow


# 主界面视图
def index(request):
    # 选取最近上架的六本书来展示
    book_list = Book.objects.all()[:6]
    return render(request, 'index.html', {'book_list': book_list})


# 登录视图
def login(request):
    if request.method == 'GET':
        # 链接跳转过来的登录页面，采用GET方法 <a href="">
        return render(request, 'login.html')
    elif request.method == 'POST':
        # 登录页面form提交事件，采用post方法
        name = request.POST.get('user_name')
        password = request.POST.get('user_password')
        try:
            q = User.objects.get(user_name=name)
        except:
            messages.error(request, "账号不存在，请重新输入")
        else:
            if q.user_password == password:
                request.session['user_name'] = name
                messages.success(request,  "登录成功")
            else:
                messages.error(request, "输入的密码有误，请重新登陆")
        # 将登录结果返回登录界面
        return render(request, 'login.html')


# 注册视图
def register(request):
    if request.method == 'GET':
        # 链接跳转过来的注册页面，采用GET方法 <a href="">
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
        record = User.objects.filter(user_name=user_name)
        if record.exists():
            messages.error(request, '账号已被注册，请换一个账号')
        else:
            if user_password.strip() == user_confirm_password.strip():
                u = User.objects.create(user_name=user_name,
                                        user_password=user_password,
                                        user_phone=user_phone,
                                        user_birthday=user_birthday,
                                        user_gender=user_gender,
                                        user_email=user_email
                                        )
                u.save()
                request.session['user_name'] = user_name
                messages.success(request, "注册成功！您可以选择")
            else:
                messages.error(request, '密码确认不通过')
        # 将注册结果返回注册界面
        return render(request, 'register.html')


# 注销视图
def logout(request):
    request.session.flush()
    # 回到首页
    return redirect('/')


# 查询视图
def query(request):
    if request.method == 'POST':
        # 主页form提交搜索事件，采用post方法
        search_string = request.POST.get('search')
        if search_string.strip():
            # 若搜索字段不为空
            # 对book_name, book_author, book_isbn 分别进行匹配，最后得出并集
            # query_string 向下传递给filter本次查询的条件
            book_name_list = Book.objects.filter(book_name__contains=search_string)
            book_author_list = Book.objects.filter(book_author__contains=search_string)
            book_isbn_list = Book.objects.filter(book_isbn__contains=search_string)
            book_list = book_name_list | book_author_list | book_isbn_list
            query_string = search_string
        else:
            # 若搜索字段不为空
            book_list = Book.objects.all()
            query_string = ""

    else:
        # 链接跳转过来的高级查询页面，采用GET方法 <a href="">
        book_list = Book.objects.all()
        query_string = ""

    # arr_length: 查询结果的条目数；flag: 防止嵌套的高级查询（因为没有意义）
    arr_length = len(book_list)
    flag = True
    if arr_length > 0:
        # 返回可供二次筛选的主题类别和出版社
        subject_list = book_list.order_by('book_category_choice').values_list('book_category_choice', flat=True).distinct()
        press_list = book_list.order_by('book_press').values_list('book_press', flat=True).distinct()
        messages.success(request, "为您找到 %s 本书" % arr_length)
    else:
        messages.error(request, "没有检索到您的输入信息")

    return render(request, 'query.html', locals())


# 高级查询视图
def advance_query(request):
    if request.method == "POST":
        # form表单提交搜索事件，采用post方法
        title = request.POST.get("title")
        author = request.POST.get("author")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        subject = request.POST.get("subject")
        press = request.POST.get("press")
        query_string = request.POST.get("query_string")
        # print("query_String:", query_string)
        # 判断是直接进行高级查询还是首次查询后的过滤器
        if query_string == "":
            record = Book.objects.all()
        else:
            # print("yes")
            record = Book.objects.filter(book_name__contains=query_string)
        # print("record:", record)
        # 查询是否有需要高级检索的项目并执行条件查询
        if title.strip():
            print("title: ", title)
            record = record.filter(book_name__contains=title.strip())
        if author.strip():
            print("author:", author)
            record = record.filter(book_author=author.strip())
        if start_date and end_date:
            print("date:", start_date, end_date)
            record = record.filter(book_publish_date__range=(start_date, end_date))
        if subject:
            print("subect:", subject)
            record = record.filter(book_category_choice=subject)
        if press:
            print("press:", press)
            record = record.filter(book_press=press)
        book_list = record
        # arr_length: 查询结果的条目数；flag: 防止嵌套的高级查询（因为没有意义）
        arr_length = len(book_list)
        flag = True
        if arr_length > 0:
            # 返回可供二次筛选的主题类别和出版社
            subject_list = book_list.order_by('book_category_choice').values_list('book_category_choice',
                                                                                  flat=True).distinct()
            press_list = book_list.order_by('book_press').values_list('book_press', flat=True).distinct()
            messages.success(request, "为您找到 %s 本书" % arr_length)
        else:
            messages.error(request, "没有检索到您的输入信息")

        return render(request, 'query.html', locals())


# 书目详情视图
def book(request, isbn):
    book = Book.objects.get(book_isbn=isbn)
    book.book_views += 1
    book.save()
    return render(request, 'book.html', locals())


# 读者账号页面视图
def account(request):
    name = request.session.get('user_name')
    request.session['record'] = True
    request.session['report'] = False
    # print(name)
    # 获取用户信息和借还书记录
    q = User.objects.get(user_name=name)
    records = Borrow.objects.filter(user=q)
    record_number = len(records)
    return render(request, 'interface.html', locals())


# 读者读书报告
def calculate_subject(book_list):
    # 去重书名
    id_list = book_list.order_by('book_id').values_list('book_id', flat=True).distinct()

    # 统计不同主题的书目数量
    subject_dict = dict()
    for book_id in id_list:
        subject = Book.objects.get(book_id=book_id).book_category_choice
        if subject not in subject_dict:
            subject_dict.setdefault(subject, 1)
        else:
            # book_list.filter(book_category_choice=subject).count()
            subject_dict[subject] += 1
    print("subject dict:", subject_dict)
    return subject_dict


def calculate_book(book_list):
    # 去重书名
    name_list = book_list.order_by('book_id').values_list('book_id', flat=True).distinct()

    # 统计借阅次数最多的图书
    name_dict = dict()
    for name in name_list:
        name_dict.setdefault(name, book_list.filter(book=name).count())
    # print(name_dict)

    # 排序
    rank_list = sorted(name_dict.items(), key=lambda x: x[1], reverse=True)
    title_list = []
    for rank in rank_list:
        name = Book.objects.get(book_id=rank[0]).book_name
        title_list.append((name, rank[1]))

    print("rank_list:", title_list)
    return title_list


def report(request):
    name = request.session.get('user_name')
    request.session['record'] = False
    request.session['report'] = True
    # print(name)
    # 获取用户信息和借还书记录
    q = User.objects.get(user_name=name)
    records = Borrow.objects.filter(user=q)

    # 计算月度和年度的读书报告，注意1月的报告
    cur_year = timezone.now().year
    cur_month = timezone.now().month
    # 上个月的报告
    # 本年度报告
    if cur_month < 2:
        last_month = 12
        last_year = cur_year - 1
        start = "%s-%s-%s" % (last_year, last_month, 1)
        end = "%s-%s-%s" % (cur_year, cur_month, 1)
    else:
        last_month = cur_month - 1
        start = "%s-%s-%s" % (cur_year, last_month, 1)
        end = "%s-%s-%s" % (cur_year, cur_month, 1)

    start_time = timezone.datetime.strptime(start, '%Y-%m-%d')
    end_time = timezone.datetime.strptime(end, '%Y-%m-%d')

    start_date_string = "%s-%s-%s" % (cur_year, 1, 1)
    start_date = timezone.datetime.strptime(start_date_string, '%Y-%m-%d')

    # 筛选记录
    month_records = Borrow.objects.filter(user=q, borrow_time__range=(start_time, end_time))
    year_records = Borrow.objects.filter(user=q, borrow_time__range=(start_date, timezone.now()))

    # 统计书目数量
    month_number = calculate_book(month_records)
    year_number = calculate_book(year_records)[:3]
    print(type(year_number))
    print(year_number)

    # 统计主题种类
    month_subject_dict = calculate_subject(month_records)
    year_subject_dict = calculate_subject(year_records)
    # messages.info(request, "Show report")
    # print((year_number))

    data_month = json.dumps(month_subject_dict)
    data_year = json.dumps(year_subject_dict)

    return render(request, 'interface.html', locals())


# 还书操作处理
def return_book(request, book_isbn):
    name = request.session.get('user_name')
    # 获取账号信息，书目信息和借还书记录
    q = User.objects.get(user_name=name)
    b = Book.objects.get(book_isbn=book_isbn)
    record = Borrow.objects.get(user=q, book=b, is_return="False")
    # 将还书标志记为已还状态，并记录还书时间
    record.is_return = "True"
    record.return_time = timezone.now()
    # 图书数量加一
    b.book_number += 1
    b.save()
    record.save()
    records = Borrow.objects.filter(user=q)
    return render(request, 'interface.html', locals())


# 借书操作处理
def borrow_book(request, book_isbn):
    if request.method == 'GET':
        # 按钮链接跳转过来，采用GET方法 <a href="">
        # 获取账号信息，书目信息和借还书记录
        user = User.objects.get(user_name=request.session.get('user_name'))
        book = Book.objects.get(book_isbn=book_isbn)
        # print(user, book)
        # 查看读者是否重复借书
        duplicate = Borrow.objects.filter(user=user, book=book, is_return="False")
        if duplicate:
            messages.error(request, "您已经借过此书了，不要太贪心哦!")
        # 判断库存书是否有余
        elif book.book_number >= 1:
            try:
                # 创建借书记录
                new_record = Borrow.objects.create(user=user, book=book, borrow_time=timezone.now(), is_return="False")
            except:
                messages.error(request, "数据库出现了一些错误，请您刷新试试")
            else:
                book.book_number -= 1
                book.book_borrow += 1
                book.save()
                new_record.save()
                messages.success(request, "借阅成功！")
        else:
            messages.error(request, "库存书目不足，已经通知管理员啦~")
        return render(request, 'book.html', {'book': book})


def modify(request):
    if request.method == "GET":
        user = User.objects.get(user_name=request.session.get('user_name'))
        return render(request, 'modify.html', locals())
    else:
        # 修改账号信息，但是不可以修改用户名
        user_name = request.session.get('user_name')
        user_password = request.POST.get('user_password')
        user_birthday = request.POST.get('user_birthday')
        user_phone = request.POST.get('user_phone')
        user_email = request.POST.get('user_email')
        user = User.objects.get(user_name=user_name)
        flag_modify = False
        if user_password.strip() and user_password != user.user_password:
            user.user_password = user_password
            flag_modify = True
        if user_birthday.strip() and user_birthday != user.user_birthday:
            user.user_birthday = user_birthday
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