import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instanse):
    Klass = instanse.__class__
    order_new_id = random_string_generator()
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instanse)
    return order_new_id

def unique_slug_generator(instanse, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instanse.title)

    Klass = instanse.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instanse, new_slug=new_slug)
    return slug