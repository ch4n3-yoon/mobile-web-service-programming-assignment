from django.urls import path
from django.urls import include
from rest_framework import routers
from blog.views import IntruderImage
from blog.views import post_list
from blog.views import post_detail
from blog.views import post_new
from blog.views import post_edit
from blog.views import test

router = routers.DefaultRouter()
router.register('Post', IntruderImage)

urlpatterns = [
    path('', post_list, name='post_list'),
    path('api_root/', include(router.urls)),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_new, name='post_new'),
    path('post/<int:pk>/edit', post_edit, name='post_edit'),
    path('test/', test, name='test'),
]
