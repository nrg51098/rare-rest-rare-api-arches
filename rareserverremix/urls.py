"""rareserverremix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rareserverapi.views import register_user, login_user, PostsViewSet, CommentViewSet, CategoriesViewSet, PostTagViewSet, TagViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostsViewSet, 'posts')
router.register(r'comments', CommentViewSet, 'comments')
router.register(r'categories', CategoriesViewSet, 'categories')
router.register(r'posttags', PostTagViewSet, 'posttags')
router.register(r'tags', TagViewSet, 'tags')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls)
]
