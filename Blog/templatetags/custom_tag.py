from django import template
from Blog.models import Comment

register = template.Library()

@register.filter(name='get_reply_count')
def get_reply_count(cid):
   num = Comment.objects.filter(replyTo=cid).count()
   return num

@register.filter(name='get_list')
def get_list(value):
   #print(type(value))
   #print(type(eval(value)))# convert string to list
   return eval(value)

@register.filter(name='get_comment_count')
def get_comment_count(value):
   #print(type(value))
   #print(type(eval(value)))# convert string to list
   coun = Comment.objects.filter(commentOn=value, replyTo__isnull=True).count()
   return coun