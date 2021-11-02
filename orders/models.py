from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, post_save

from ecommerce.utils import unique_order_id_generator
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address

ORDER_STATUS_CHOISES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refused', 'Refused')
)


class OrderManager(models.Manager):
    def get_or_new(self, billing_profile, cart_obj):
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
            created = False
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name='billing_address', null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOISES, default='created')
    shipping_total = models.DecimalField(default=5.99, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        shipping_total = self.shipping_total
        cart_total = self.cart.total
        self.total = format(Decimal(cart_total) + Decimal(shipping_total), '.2f')
        self.save()
        return self.total

    def check_done(self):
        if self.billing_profile and self.billing_address and self.shipping_address and self.total > 0:
            return True
        else:
            return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
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
