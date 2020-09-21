from django.contrib import admin
from .models import MembershipPlan, Coupons, Customer


admin.site.register(MembershipPlan)
admin.site.register(Customer)


class CouponAdmin(admin.ModelAdmin):
    class Media:
        js = ("admin/js/jquery.init.js", "/static/memberships/coupon_admin.js",)

admin.site.register(Coupons, CouponAdmin)

