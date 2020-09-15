from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
def PaymentHome(request):
    if request.method == 'GET':
        return render(request, 'payments/payment_home.html')
    else:
        return render(request, 'payments/payment_home.html', {'subscriber': request.POST})

