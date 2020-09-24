from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    current_period_end = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.user.email


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

    class Meta:
        verbose_name_plural = 'coupons'

    def __str__(self):
        return self.code


class Subscriptions(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    current = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'subscriptions'

    def __str__(self):
        return self.customer.user.email



