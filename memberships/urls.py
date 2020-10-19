from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('settings/', views.settings, name='settings'),
    path('success/', views.payment_success, name='payment_success'),
    path('updatesuccess', views.update_success, name='update_success'),
    path('webhook/', views.my_webhook, name='my_webhook'),
    path('join/', views.join, name='join'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),

]



