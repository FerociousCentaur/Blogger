from django import template
from Blog.models import Comment

register = template.Library()

@register.filter(name='get_reply_count')
def get_reply_count(cid):
   num = Comment.objects.filter(replyTo=cid).count()
   return num