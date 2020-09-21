from django.shortcuts import render,get_object_or_404, redirect
from .models import MembershipPlan, Coupons, Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

endpoint_secret = 'whsec_AQPXlprXr7Hhv4UqfActwgFA7EnuY4d0'


@csrf_exempt
def my_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # if event['type'] == 'checkout.session.completed':
    #     session = event['data']['object']
    #     print(session)

    print(event)

    return HttpResponse(status=200)


def selected_membership(request, pk):
    membership = get_object_or_404(MembershipPlan, pk=pk)
    if membership.premium:
        return redirect('join')
    else:
        return render(request, 'memberships/join.html', {'membership': membership})


def join(request):
    return render(request, 'memberships/join.html')


@login_required(login_url='login/')
@ require_GET
def checkout(request):
    coupons = Coupons.objects.all()
    coupons_dict = {coupon.code: coupon.percent_off for coupon in coupons}

    coupon = 'none'
    price = 3000
    og_dollar = 30
    coupon_dollar = 0
    final_dollar = 30
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


        coupon_price = int((percentage / 100) * price)
        price = price - coupon_price
        coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
        final_dollar = str(price)[:-2] + "." + str(price)[-2:]
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1HRv3sGlBCx2ENx5MpRRA3Ov',
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/checkout/',
            customer_email=request.user.email,
            metadata={'user_id': request.user.id},
            subscription_data={
                'coupon': stripe.Coupon.retrieve(coupon)['id'],
            }
        )
    else:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1HRv3sGlBCx2ENx5MpRRA3Ov',
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/checkout/',
            customer_email=request.user.email,
            metadata={'user_id': request.user.id}
        )
    return render(request, 'memberships/checkout.html',
                  {'coupon': coupon,
                   'price': price,
                   'og_dollar': og_dollar,
                   'coupon_dollar': coupon_dollar,
                   'final_dollar': final_dollar,
                   'session': session})


def settings(request):
    return render(request, 'memberships/settings.html')


@login_required(login_url='login/')
def payment_success(request):
    return render(request, 'memberships/payment_success.html')


@login_required(login_url='login/')
def payment_cancel(request):
    return render(request, 'memberships/payment_cancel.html')
