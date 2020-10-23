from django.urls import path
from . import views

app_name = 'blog'

# urlpatterns = [
#     path('', views.allBlogs, name='allBlogs'),
#     path('<str:slug>/', views.detail, name='blog_detail'),
# ]

urlpatterns = [
    path('', views.redirect_to_home, name='home_redirect'),
]

