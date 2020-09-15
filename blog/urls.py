from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.allBlogs, name='allBlogs'),
    path('<int:blog_id>', views.detail, name='detail'),
]

