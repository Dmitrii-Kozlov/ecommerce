from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, post_save

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

    def __str__(self):
        return self.order_id

    def update_total(self):
        shipping_total = self.shipping_total
        cart_total = self.cart.total
        self.total = format(Decimal(cart_total) + Decimal(shipping_total), '.2f')
        self.save()
        return self.total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)
