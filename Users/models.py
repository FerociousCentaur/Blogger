from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import uuid

User._meta.get_field('email')._unique = True

def localtime():
    return timezone.localtime(timezone.now())

def default_local():
    return timezone.localtime(timezone.now()+timedelta(days=365))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    valid_till = models.DateTimeField(default=default_local)
    pfp = models.ImageField(upload_to='images/')
    is_creator = models.BooleanField(default=False)
    rating = models.CharField(max_length=3, blank=True)
    saved = models.ManyToManyField('Blog.Article')
    blog_subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=Profile)
def check_smail(sender, instance, created, **kwargs):
    if created:
        if instance.email[-10:]== 'iitm.ac.in':
            instance.is_creator = True
            instance.save()





