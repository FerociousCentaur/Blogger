from django.db import models
from django.contrib.auth.models import User
from Users.models import Profile
import uuid
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=250)
    aid = models.UUIDField(default=uuid.uuid4, editable=False)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='images/')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    rating = models.CharField(max_length=3, default=0)
    raters = models.ManyToManyField('Users.Profile', related_name='raters')
    published = models.BooleanField(default=True)
    category = models.CharField(max_length=50, null=True)
    tags = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title[:10]+ " ["+self.author.first_name+"]"}'

class Comment(models.Model):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cid = models.UUIDField(default=uuid.uuid4, editable=False)
    commentText = models.TextField()
    likes = models.ManyToManyField('Users.Profile', related_name='likes')
    commentOn = models.ForeignKey(Article, related_name='commentOn', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    replyTo = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f'{self.commenter.first_name + "  [" + str(self.likes.count()) + "]"}'

class Notification(models.Model):
    type = models.CharField(max_length=30)
    msg = models.TextField()
    notifiedOn = models.ForeignKey(Article, on_delete=models.CASCADE)
    noti_for = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='noti_for')
    noti_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='noti_by')
    created_at = models.DateTimeField(default=timezone.now)
