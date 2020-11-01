"""readingTeacherOnline URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from courses_site import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('blog/', include('blog.urls')),
    path('courses/', views.all_courses, name='all_courses'),
    path('courses/<str:slug>/', views.course_detail, name='course_detail'),
    path('courses/<str:slug>/<int:order_number>', views.course_video, name='course_video'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('memberships/', include('memberships.urls')),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html", email_template_name='password_reset_email.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_done.html'),
         name="password_reset_complete"),
    path('change_password/',
         auth_views.PasswordChangeView.as_view(template_name='auth/change_password.html'),
         name='change_password'),
    path('activation_email_sent', views.activation_email_sent, name='activation_email_sent'),
    path('account_activated', views.account_activated, name='account_activation_complete'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



