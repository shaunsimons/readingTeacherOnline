from django.db import models
from django.contrib.auth.models import User


class MembershipPlan(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    premium = models.BooleanField(default=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=True)
    membership = models.BooleanField(default=False)

class Coupons(models.Model):
    code = models.CharField(max_length=10)
    percent_off = models.IntegerField()
    durations = (
        (0, 'once'),
        (1, 'repeating'),
        (2, 'forever')
    )
    duration = models.IntegerField(choices=durations, default=0)
    duration_months = models.IntegerField(default=0, blank=True, null=True)
