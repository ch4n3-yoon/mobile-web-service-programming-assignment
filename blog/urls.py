from django.urls import path
from blog.views import post_list
from blog.views import post_detail
from blog.views import post_new
from blog.views import post_edit
from blog.views import test

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_new, name='post_new'),
    path('post/<int:pk>/edit', post_edit, name='post_edit'),
    path('test/', test, name='test'),
]
