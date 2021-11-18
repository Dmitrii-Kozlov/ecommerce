from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from .signals import object_viewed_signal
from .utils import get_client_ip
# Create your models here.

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object} viewed on {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Object Viewed"
        verbose_name_plural = "Objects Viewed"


def object_viewed_reciever(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_object_viewed = ObjectViewed.objects.create(
        user=request.user,
        ip_address=get_client_ip(request),
        content_type=c_type,
        object_id=instance.id
    )
    # print(sender)
    # print(instance)
    # print(request.user)


object_viewed_signal.connect(object_viewed_reciever)
