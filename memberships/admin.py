from django.contrib import admin
from .models import Coupons, Customer, Subscriptions


class InlineSubscriptions(admin.TabularInline):
    model = Subscriptions
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    inlines = [InlineSubscriptions]
    fields = ('user', 'stripe_id', 'cancel_at_period_end', 'current_period_end')


admin.site.register(Customer, CustomerAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off')

    class Media:
        js = ("admin/js/jquery.init.js", "/static/memberships/coupon_admin.js",)

admin.site.register(Coupons, CouponAdmin)

# admin.site.register(Subscriptions)
