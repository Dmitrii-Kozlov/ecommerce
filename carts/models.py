from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def get_or_create(self, request):
        cart_id = request.session.get('cart_id', None)
        cart_id = cart_id if isinstance(cart_id, int) else None
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            is_new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
            is_new_obj = True
        return cart_obj, is_new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def cart_m2m_changed_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        total = sum([x.price for x in instance.products.all()])
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)


def cart_pre_save_reciever(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.1)
    else:
        instance.total = 0

pre_save.connect(cart_pre_save_reciever, sender=Cart)