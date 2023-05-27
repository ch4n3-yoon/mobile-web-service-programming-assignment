from django.urls import path
from blog.views import post_list
from blog.views import test

urlpatterns = [
    path('', post_list, name='post_list'),
    path('test/', test, name='test'),
]
