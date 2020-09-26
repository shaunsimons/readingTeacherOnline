from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, default='')
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


class CancelSurvey(models.Model):
    satisfaction_choices = (
        (0, 'Very Satisfied'),
        (1, 'Satisfied'),
        (2, 'Neutral'),
        (3, 'Unsatisfied'),
        (4, 'Very Unsatisfied'),
    )
    satisfaction = models.IntegerField(choices=satisfaction_choices)

    reasons = (
        (0, "No longer needed it"),
        (1, "It didn't meet my needs"),
        (2, "Found an alternative"),
        (3, "Quality was less than expected"),
        (4, "Ease of use was less than expected"),
        (5, "Access to the service was less than expected"),
        (4, "Customer service was less than expected"),
        (5, "Other")
    )
    primary_reason = models.IntegerField()
    other = models.TextField(null=True)
    suggestion = models.TextField(null=True)




