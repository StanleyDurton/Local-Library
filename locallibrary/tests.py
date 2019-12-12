from django.test import TestCase
from django.utils import timezone
from django.db.models import Sum, Count

from .models import User, Book, Borrow

# Create your tests here.


class TestBorrow(TestCase):

    u = User.objects.get(user_name="banana")
    query_set = Borrow.objects.filter(user=u,
                                      borrow_time__range=(timezone.now()-timezone.timedelta(days=365), timezone.now()))
    name_list = query_set.order_by('book').values_list('book', flat=True).distinct()

    # 统计
    name_dict = dict()
    for name in name_list:
        name_dict.setdefault(name, query_set.filter(book=name).count())
    print(name_dict)

    # 排序
    rank_list = sorted(name_dict.items(), key=lambda x: x[1], reverse=True)
    print(rank_list)


