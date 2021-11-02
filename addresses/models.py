from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)

class Address(models.Model):
    class Meta:
        verbose_name_plural = 'Addresses'
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(choices=ADDRESS_TYPE, max_length=20)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, default='Russia')
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line_1}\n{line_2}\n{city}\n{postal}, \n{state}\n{country}".format(
            line_1 = self.address_line_1,
            line_2 = self.address_line_2 or "",
            city = self.city,
            postal = self.postal_code,
            state = self.state,
            country = self.country
        )