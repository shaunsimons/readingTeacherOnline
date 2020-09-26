from django.contrib import admin
from .models import Coupons, Customer




class CustomerAdmin(admin.ModelAdmin):
    fields = ('user', 'stripe_id', 'cancel_at_period_end', 'current_period_end', 'subscription_id')


admin.site.register(Customer, CustomerAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off')

    class Media:
        js = ("admin/js/jquery.init.js", "/static/memberships/coupon_admin.js",)

admin.site.register(Coupons, CouponAdmin)

# admin.site.register(Subscriptions)
