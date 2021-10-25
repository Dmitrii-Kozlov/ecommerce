import os
import random

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from .utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000000000000)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"products/{new_filename}/{final_filename}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

class ProductManager(models.Manager):
    def all(self):
        return self.get_queryset().active()

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def features(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)