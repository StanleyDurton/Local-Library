"""LibrarySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from locallibrary import views as view

urlpatterns = [
    path('', view.index),
    path('admin/', admin.site.urls),
    path('query/', view.query),
    path('login/', view.login),
    path('register/', view.register),
    path('user/', view.account),
    path('return/<book_isbn>', view.return_book_view),
    path('book/<isbn>', view.book),
    path('borrow/<book_isbn>', view.borrow_view),
    path('logout/', view.logout),
    path('modify/', view.modify),
    path('filter/', view.filter)
]
