from django.urls import path

from . import views


urlpatterns = [
    path('', views.PaymentHome, name='payment_home'),
    path('webhook/', views.Webhook, name='webhook')
]