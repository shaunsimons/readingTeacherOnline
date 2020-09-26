from django.shortcuts import render, redirect
from .models import Coupons, Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta
from django.utils import timezone


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

endpoint_secret = 'whsec_AQPXlprXr7Hhv4UqfActwgFA7EnuY4d0'

DOMAIN = 'http://localhost:8000/'  # change to real domain for production

SUCCESS_URL = DOMAIN + 'memberships/success'
CANCEL_URL = DOMAIN + 'memberships/checkout'

@csrf_exempt
def my_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session['mode'] == 'setup':
            setup_intent = session['setup_intent']
            intent = stripe.SetupIntent.retrieve(setup_intent)
            customer = intent['customer']
            payment_method = intent['payment_method']

            # update customer's payment method
            stripe.Customer.modify(
                customer,
                invoice_settings={'default_payment_method': payment_method}
            )
            return HttpResponse(status=200)

        elif session['mode'] == 'subscription':
            # try to retrieve a customer object for user or create a new one
            try:
                customer = Customer.objects.get(user=session['client_reference_id'])
            except Customer.DoesNotExist:
                customer = Customer()
                customer.user_id = session['client_reference_id']
            customer.stripe_id = session['customer']
            subscription_id = session['subscription']
            subscription_response = stripe.Subscription.retrieve(subscription_id)
            customer.cancel_at_period_end = True if subscription_response['cancel_at_period_end'] == 'true' else False
            current_period_end_datetime = datetime.fromtimestamp(subscription_response['current_period_end']) + timedelta(days=7)  # add 7 days grace after potential failed payment
            customer.current_period_end = current_period_end_datetime
            customer.subscription_id = subscription_id
            customer.save()






    # if payment is successful, update current_period_end for customer
    elif event['type'] == 'payment_intent.succeeded':
        event_object = event['data']['object']
        try:
            customer = Customer.objects.get(stripe_id=event_object['customer'])
            subscription_id = customer.subscription_id
            subscription_response = stripe.Subscription.retrieve(subscription_id)
            customer.current_period_end = datetime.fromtimestamp(subscription_response['current_period_end']) + timedelta(days=7)  # add 7 days grace after potential failed payment
            customer.save()
        except Customer.DoesNotExist:
            print('No Customer')
            return HttpResponse(status=200)

    elif event['type'] == 'payment_intent.payment_failed':
        event_object = event['data']['object']
        try:
            # get customer object
            customer = Customer.objects.get(stripe_id=event_object['customer'])
        except Customer.DoesNotExist:
            # not a current customer so no action required yet (probably failed at checkout)
            return HttpResponse(status=200)

        print(f'Customer: {customer.user}\nPayment Failed\nLetting Support know.....')

    # elif event['type'] == 'customer.subscription.deleted':
    #     print(event)
    #     event_object = event['data']['object']
    #     subscription_id = event_object['id']
    #     subscription = Subscriptions.objects.get(stripe_subscription_id=subscription_id)
    #     subscription.current = False

    return HttpResponse(status=200)


def join(request):
    return render(request, 'memberships/join.html')




@login_required(login_url='/login/')
@ require_GET
def checkout(request):
    try:
        if request.user.customer.current_period_end > timezone.now():
            return redirect('settings')

    except Customer.DoesNotExist:
        pass


    # get all coupons stored in db
    coupons = Coupons.objects.all()
    coupons_dict = {coupon.code: coupon.percent_off for coupon in coupons}

    # set initial prices and totals
    coupon = 'none'
    price = 3000
    og_dollar = 30
    coupon_dollar = 0
    final_dollar = 30

    # initial session parameters
    payment_method_types = ['card']
    line_items = [{
        'price': 'price_1HRv3sGlBCx2ENx5MpRRA3Ov',
        'quantity': 1,
    }]
    mode = 'subscription'
    client_reference_id = request.user.id
    customer_email = request.user.email
    customer = None
    subscription_data = None

    # check if user has a stripe customer id already and add that to the session
    try:
        stripe_customer_id = Customer.objects.get(user=request.user.id).stripe_id
        customer = stripe_customer_id
        customer_email = None
    except Customer.DoesNotExist:
        pass

    # check if coupon was added
    if 'coupon' in request.GET and request.GET['coupon'].upper() in coupons_dict:
        coupon = request.GET['coupon'].upper()
        percentage = coupons_dict[coupon]

        # create coupon or skip if it already exists
        try:
            stripe.Coupon.create(
                percent_off=percentage,
                duration='once',
                id=coupon,
            )
        except:
            pass

        # add coupon to session
        subscription_data = {
            'coupon': coupon
        }

        # set new prices and totals
        coupon_price = int((percentage / 100) * price)
        price = price - coupon_price
        coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
        final_dollar = str(price)[:-2] + "." + str(price)[-2:]



    # create session
    session = stripe.checkout.Session.create(
        payment_method_types=payment_method_types,
        line_items=line_items,
        mode=mode,
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
        client_reference_id=client_reference_id,
        customer_email=customer_email,
        customer=customer,
        subscription_data=subscription_data

    )

    return render(request, 'memberships/checkout.html',
                  {'coupon': coupon,
                   'price': price,
                   'og_dollar': og_dollar,
                   'coupon_dollar': coupon_dollar,
                   'final_dollar': final_dollar,
                   'session': session})


@login_required(login_url='/login/')
def settings(request):
    cancel_at_period_end = False
    try:
        customer = request.user.customer.stripe_id
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='setup',
            customer=customer,
            success_url=DOMAIN + 'memberships/updatesuccess/',
            cancel_url=DOMAIN + 'memberships/settings/',
        )
        member_until = request.user.customer.current_period_end
        cancel_at_period_end = True if request.user.customer.cancel_at_period_end else False
    except Customer.DoesNotExist:
        session = None
        member_until = False
    date_joined = request.user.date_joined
    return render(request, 'memberships/settings.html',
                  {'session': session,
                   'date_joined': date_joined,
                   'member_until': member_until,
                   'cancel_at_end_period': cancel_at_period_end})


@login_required(login_url='/login/')
def payment_success(request):
    return render(request, 'memberships/payment_success.html')


@login_required(login_url='/login/')
def payment_cancel(request):
    return render(request, 'memberships/payment_cancel.html')


def update_success(request):
    return render(request, 'memberships/update_success.html')


@login_required(login_url='/login/')
def cancel_subscription(request):
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
        return redirect('settings')
    else:
        satisfaction_choices = [
            'Very Satisfied',
            'Satisfied',
            'Neutral',
            'Unsatisfied',
            'Very Unsatisfied'
        ]

        reasons = [
            "No longer needed it",
            "It didn't meet my needs",
            "Found an alternative",
            "Quality was less than expected",
            "Ease of use was less than expected",
            "Access to the service was less than expected",
            "Customer service was less than expected",
            "Other"
        ]

        return render(request, 'memberships/cancel_survey.html',
                      {'satisfaction_choices': satisfaction_choices,
                       'reasons': reasons})
