from django.db import models
from django.db.models.signals import pre_save

from ecommerce.utils import unique_order_id_generator
from carts.models import Cart

ORDER_STATUS_CHOISES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refused', 'Refused')
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    # billing_profile
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOISES)
    shipping_total = models.DecimalField(default=5.99, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

