from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import paypalrestsdk
from paypalrestsdk import WebhookEvent
import json
from collections import OrderedDict
import os

paypal_api = paypalrestsdk.configure({
    'mode': 'sandbox',
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['SANDBOX_SECRET']
})


def verify_webhook_signature_using_sdk(*args):
    return WebhookEvent.verify(*args)


def verify_event(request):
    auth_algo = request.META.get("HTTP_PAYPAL_AUTH_ALGO")
    cert_url = request.META.get("HTTP_CERT_URL")
    transmission_id = request.META.get("HTTP_PAYPAL_TRANSMISSION_ID")
    transmission_sig = request.META.get("HTTP_PAYPAL_TRANSMISSION_SIG")
    transmission_time = request.META.get("HTTP_PAYPAL_TRANSMISSION_TIME")
    webhook_id = settings.WEBHOOK_ID

    ordered_payload = json.loads(request.body, object_pairs_hook=OrderedDict)

    data = dict(auth_algo=auth_algo,
                cert_url=cert_url,
                transmission_id=transmission_id,
                transmission_sig=transmission_sig,
                transmission_time=transmission_time,
                webhook_id=webhook_id,
                webhook_event=ordered_payload)

    return verify_webhook_signature_using_sdk(transmission_id,
                                              transmission_time,
                                              webhook_id,
                                              request.body,
                                              cert_url,
                                              transmission_sig,
                                              auth_algo)


# Create your views here.
def PaymentHome(request):
    if request.method == 'GET':
        return render(request, 'payments/payment_home.html')
    else:
        return render(request, 'payments/payment_home.html', {'subscriber': request.POST})


@csrf_exempt
@require_POST
def Webhook(request):
    verified = verify_event(request)
    return HttpResponse(f'Response: {verified}\n')

